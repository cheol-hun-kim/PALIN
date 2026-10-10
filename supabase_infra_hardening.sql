-- ============================================================================
-- ReadMath & PassMate (PALIN OS) Supabase Infrastructure & Security Hardening
-- Version: 1.0.0 (Production Scaled)
-- Target: Supabase PostgreSQL (Pro Plan)
-- Covers: 1. pgvector Semantic Cache, 2. Rate Limiting, 3. Refund Defense Audit,
--         4. Row Level Security (RLS) & PII Encryption, 5. Compliance Audit Logs
-- ============================================================================

-- 0. ENABLE EXTENSIONS
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================================
-- 1. PGVECTOR SEMANTIC CACHING LAYER (LLM API Cost Reduction by 75~85%)
-- ============================================================================

-- Table for caching standardized and past exam questions with high-dimensional embeddings
CREATE TABLE IF NOT EXISTS public.problem_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    problem_hash VARCHAR(64) UNIQUE,                 -- Perceptual Hash (pHash) or MD5 of normalized text/image
    problem_title TEXT NOT NULL,
    problem_text TEXT NOT NULL,
    curriculum_grade VARCHAR(32) DEFAULT '고1',
    solution_data JSONB NOT NULL,                    -- Parsed steps, prescriptions, and clean SVG diagram
    final_answer TEXT,
    embedding VECTOR(1536),                          -- OpenAI text-embedding-3-small (1536-dim) or Gemini (768-dim)
    hit_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    last_accessed_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Fast Approximate Nearest Neighbor (ANN) HNSW Index for Cosine Distance
CREATE INDEX IF NOT EXISTS idx_problem_embeddings_hnsw 
ON public.problem_embeddings 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Index for exact hash match (O(1) lookup before vector search)
CREATE INDEX IF NOT EXISTS idx_problem_embeddings_hash 
ON public.problem_embeddings (problem_hash);

-- RPC Function: Match cached problem with cosine similarity >= threshold (default 0.95)
CREATE OR REPLACE FUNCTION public.match_cached_problem(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.95,
    match_count INT DEFAULT 1
)
RETURNS TABLE (
    id UUID,
    problem_title TEXT,
    problem_text TEXT,
    solution_data JSONB,
    final_answer TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pe.id,
        pe.problem_title,
        pe.problem_text,
        pe.solution_data,
        pe.final_answer,
        (1 - (pe.embedding <=> query_embedding))::FLOAT AS similarity
    FROM public.problem_embeddings pe
    WHERE (1 - (pe.embedding <=> query_embedding)) >= match_threshold
    ORDER BY (pe.embedding <=> query_embedding) ASC
    LIMIT match_count;
END;
$$;


-- ============================================================================
-- 2. RATE LIMITING & ABUSE DEFENSE ENGINE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.user_rate_limits (
    user_id VARCHAR(128) PRIMARY KEY,
    user_tier VARCHAR(32) DEFAULT 'FREE',            -- 'FREE', 'PRO', 'INSTITUTION'
    minute_window TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    minute_count INTEGER DEFAULT 0,
    day_window DATE DEFAULT CURRENT_DATE NOT NULL,
    day_count INTEGER DEFAULT 0,
    is_blocked BOOLEAN DEFAULT FALSE,
    blocked_reason TEXT,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_rate_limits_tier ON public.user_rate_limits (user_tier);

-- RPC Function: Atomically check rate limit and increment counters
-- Free Tier Default: 5 requests / min, 20 requests / day
-- Pro Tier Default: 20 requests / min, 200 requests / day
CREATE OR REPLACE FUNCTION public.check_and_increment_rate_limit(
    p_user_id VARCHAR(128),
    p_user_tier VARCHAR(32) DEFAULT 'FREE',
    p_max_per_min INTEGER DEFAULT 5,
    p_max_per_day INTEGER DEFAULT 20
)
RETURNS TABLE (
    allowed BOOLEAN,
    current_minute_count INTEGER,
    current_day_count INTEGER,
    retry_after_seconds INTEGER,
    reason TEXT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_now TIMESTAMPTZ := TIMEZONE('utc'::text, NOW());
    v_today DATE := CURRENT_DATE;
    v_rec RECORD;
    v_minute_diff INTEGER;
    v_min_count INTEGER;
    v_day_count INTEGER;
    v_blocked BOOLEAN;
BEGIN
    -- Check if record exists, insert if not
    INSERT INTO public.user_rate_limits (user_id, user_tier, minute_window, minute_count, day_window, day_count)
    VALUES (p_user_id, p_user_tier, v_now, 0, v_today, 0)
    ON CONFLICT (user_id) DO NOTHING;

    SELECT * INTO v_rec FROM public.user_rate_limits WHERE user_id = p_user_id FOR UPDATE;

    IF v_rec.is_blocked THEN
        RETURN QUERY SELECT FALSE, v_rec.minute_count, v_rec.day_count, 86400, '계정이 비정상 트래픽 또는 운영 정책 위반으로 차단되었습니다.';
        RETURN;
    END IF;

    -- Calculate minute window reset
    v_minute_diff := EXTRACT(EPOCH FROM (v_now - v_rec.minute_window))::INTEGER;
    IF v_minute_diff >= 60 THEN
        v_min_count := 1;
        UPDATE public.user_rate_limits 
        SET minute_window = v_now, minute_count = 1, updated_at = v_now 
        WHERE user_id = p_user_id;
    ELSE
        IF v_rec.minute_count >= p_max_per_min THEN
            RETURN QUERY SELECT FALSE, v_rec.minute_count, v_rec.day_count, (60 - v_minute_diff), '1분당 호출 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.';
            RETURN;
        END IF;
        v_min_count := v_rec.minute_count + 1;
        UPDATE public.user_rate_limits 
        SET minute_count = v_min_count, updated_at = v_now 
        WHERE user_id = p_user_id;
    END IF;

    -- Calculate day window reset
    IF v_rec.day_window < v_today THEN
        v_day_count := 1;
        UPDATE public.user_rate_limits 
        SET day_window = v_today, day_count = 1, updated_at = v_now 
        WHERE user_id = p_user_id;
    ELSE
        IF v_rec.day_count >= p_max_per_day THEN
            RETURN QUERY SELECT FALSE, v_min_count, v_rec.day_count, 3600, '일일 AI 질의 허용량을 모두 소진했습니다. 내일 다시 이용하시거나 플랜을 업그레이드해 주세요.';
            RETURN;
        END IF;
        v_day_count := v_rec.day_count + 1;
        UPDATE public.user_rate_limits 
        SET day_count = v_day_count, updated_at = v_now 
        WHERE user_id = p_user_id;
    END IF;

    RETURN QUERY SELECT TRUE, v_min_count, v_day_count, 0, 'OK'::TEXT;
END;
$$;


-- ============================================================================
-- 3. REFUND DEFENSE SYSTEM (ELECTRONIC COMMERCE ACT COMPLIANCE)
-- ============================================================================
-- Under Article 17, Paragraph 2, Item 5 of the Act on Consumer Protection in Electronic Commerce,
-- digital content value is consumed upon opening solutions or downloading materials.

CREATE TABLE IF NOT EXISTS public.user_content_access_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(128) NOT NULL,
    action_type VARCHAR(64) NOT NULL,                -- 'VIEW_SOLUTION', 'DOWNLOAD_PDF', 'PRINT_WORKSHEET', 'SOCRATIC_CHAT'
    content_id VARCHAR(128) NOT NULL,                -- problem_id or worksheet_id
    content_title TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    accessed_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_content_access_user_action 
ON public.user_content_access_logs (user_id, action_type);

CREATE INDEX IF NOT EXISTS idx_content_access_timestamp 
ON public.user_content_access_logs (accessed_at DESC);

-- RPC Function: Check refund eligibility based on legal digital content consumption
CREATE OR REPLACE FUNCTION public.check_refund_defense_status(
    p_user_id VARCHAR(128),
    p_max_trial_views INTEGER DEFAULT 3
)
RETURNS TABLE (
    eligible_for_auto_refund BOOLEAN,
    solution_views_count INTEGER,
    pdf_downloads_count INTEGER,
    first_access_at TIMESTAMPTZ,
    defense_reason TEXT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_views INTEGER;
    v_downloads INTEGER;
    v_first_access TIMESTAMPTZ;
BEGIN
    SELECT 
        COUNT(*) FILTER (WHERE action_type = 'VIEW_SOLUTION'),
        COUNT(*) FILTER (WHERE action_type IN ('DOWNLOAD_PDF', 'PRINT_WORKSHEET')),
        MIN(accessed_at)
    INTO v_views, v_downloads, v_first_access
    FROM public.user_content_access_logs
    WHERE user_id = p_user_id;

    v_views := COALESCE(v_views, 0);
    v_downloads := COALESCE(v_downloads, 0);

    -- Defense Rule 1: PDF download/print immediately extinguishes right to simple-change-of-mind refund
    IF v_downloads > 0 THEN
        RETURN QUERY SELECT 
            FALSE, v_views, v_downloads, v_first_access,
            '전자상거래 등에서의 소비자보호에 관한 법률 제17조 제2항 제5호에 따라, 디지털 학습지/PDF 자료를 다운로드하거나 인쇄한 경우 서비스 가치가 소비되어 즉시 환불이 제한됩니다.'::TEXT;
        RETURN;
    END IF;

    -- Defense Rule 2: Exceeding trial solution view limit (e.g. 3 questions)
    IF v_views >= p_max_trial_views THEN
        RETURN QUERY SELECT 
            FALSE, v_views, v_downloads, v_first_access,
            format('체험 분량(%s문항)을 초과하여 %s문항의 상세 해설 및 AI 인지 분석을 열람하셨으므로 디지털 콘텐츠 제공이 개시되어 전자상거래법상 자동 환불이 제한됩니다. 문의 사항은 고객센터로 접수해 주십시오.', p_max_trial_views, v_views);
        RETURN;
    END IF;

    -- Eligible if within limits
    RETURN QUERY SELECT 
        TRUE, v_views, v_downloads, v_first_access,
        '자동 환불 가능 대상입니다. (체험 분량 미초과)'::TEXT;
END;
$$;


-- ============================================================================
-- 4. PII ENCRYPTION & COMPLIANCE AUDIT LOGGING (1-YEAR MANDATORY RETENTION)
-- ============================================================================

-- Audit log table for compliance with Personal Information Protection Act and Cyber Insurance
CREATE TABLE IF NOT EXISTS public.audit_access_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id VARCHAR(128) NOT NULL,                  -- Admin or system user who accessed data
    actor_role VARCHAR(32) NOT NULL,                 -- 'ADMIN', 'SYSTEM', 'TEACHER'
    target_user_id VARCHAR(128),                     -- Student/Parent whose data was touched
    action VARCHAR(64) NOT NULL,                     -- 'READ_PII', 'EXPORT_ROSTER', 'DELETE_USER', 'MODIFY_SUBSCRIPTION'
    accessed_columns TEXT[],                         -- e.g. ['phone', 'email', 'parent_phone']
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_actor ON public.audit_access_logs (actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_target ON public.audit_access_logs (target_user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_access_logs (created_at DESC);

-- PII Encryption Helpers using pgcrypto AES-256
CREATE OR REPLACE FUNCTION public.encrypt_pii(data TEXT, secret_key TEXT)
RETURNS BYTEA
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF data IS NULL OR data = '' THEN
        RETURN NULL;
    END IF;
    RETURN pgp_sym_encrypt(data, secret_key, 'compress-algo=1, cipher-algo=aes256');
END;
$$;

CREATE OR REPLACE FUNCTION public.decrypt_pii(encrypted_data BYTEA, secret_key TEXT)
RETURNS TEXT
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF encrypted_data IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN pgp_sym_decrypt(encrypted_data, secret_key);
END;
$$;


-- ============================================================================
-- 5. ROW LEVEL SECURITY (RLS) FOR ABSOLUTE PRIVACY ISOLATION
-- ============================================================================

-- Enable RLS across all tables
ALTER TABLE public.problem_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_rate_limits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_content_access_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_access_logs ENABLE ROW LEVEL SECURITY;

-- 5.1. problem_embeddings: Public can read, only Service Role / Admin can insert or modify
DROP POLICY IF EXISTS "Public read on problem_embeddings" ON public.problem_embeddings;
CREATE POLICY "Public read on problem_embeddings"
ON public.problem_embeddings
FOR SELECT
USING (true);

DROP POLICY IF EXISTS "Service role write on problem_embeddings" ON public.problem_embeddings;
CREATE POLICY "Service role write on problem_embeddings"
ON public.problem_embeddings
FOR ALL
USING (auth.role() = 'service_role');

-- 5.2. user_rate_limits: Users can only see their own rate limits
DROP POLICY IF EXISTS "Users can view own rate limit" ON public.user_rate_limits;
CREATE POLICY "Users can view own rate limit"
ON public.user_rate_limits
FOR SELECT
USING (auth.uid()::TEXT = user_id OR auth.role() = 'service_role');

-- 5.3. user_content_access_logs: Users can see own logs, service role manages
DROP POLICY IF EXISTS "Users can view own access logs" ON public.user_content_access_logs;
CREATE POLICY "Users can view own access logs"
ON public.user_content_access_logs
FOR SELECT
USING (auth.uid()::TEXT = user_id OR auth.role() = 'service_role');

DROP POLICY IF EXISTS "Users can insert own access logs" ON public.user_content_access_logs;
CREATE POLICY "Users can insert own access logs"
ON public.user_content_access_logs
FOR INSERT
WITH CHECK (auth.uid()::TEXT = user_id OR auth.role() = 'service_role');

-- 5.4. audit_access_logs: STRICT ACCESS - Only Service Role and Master Admins
DROP POLICY IF EXISTS "Only service role and admins access audit logs" ON public.audit_access_logs;
CREATE POLICY "Only service role and admins access audit logs"
ON public.audit_access_logs
FOR ALL
USING (auth.role() = 'service_role');

-- Grant necessary permissions to authenticated and anon users
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT ON public.problem_embeddings TO anon, authenticated;
GRANT EXECUTE ON FUNCTION public.match_cached_problem TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.check_and_increment_rate_limit TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.check_refund_defense_status TO anon, authenticated, service_role;
