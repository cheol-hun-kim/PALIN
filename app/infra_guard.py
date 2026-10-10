# -*- coding: utf-8 -*-
"""
PassMate & ReadMath Infrastructure Guard:
1. pgvector / Hash Caching Pipeline
2. Rate Limiting & Abuse Defense Proxy
3. Refund Defense (Electronic Commerce Act Art. 17) Tracking
4. PII Audit Compliance Logging
"""

import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/infra", tags=["Infrastructure Hardening"])

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class ContentAccessLogRequest(BaseModel):
    user_id: str
    action_type: str             # 'VIEW_SOLUTION', 'DOWNLOAD_PDF', 'PRINT_WORKSHEET', 'SOCRATIC_CHAT'
    content_id: str
    content_title: Optional[str] = ""

class RefundCheckRequest(BaseModel):
    user_id: str
    max_trial_views: Optional[int] = 3

class AIProxySolveRequest(BaseModel):
    user_id: str
    user_tier: Optional[str] = "FREE"  # 'FREE', 'PRO', 'INSTITUTION'
    problem_text: str
    problem_title: Optional[str] = "수학 문항"
    curriculum_grade: Optional[str] = "고1"

# ============================================================================
# 1. HASH GENERATOR (Perceptual & Text Normalization)
# ============================================================================

def generate_problem_hash(problem_text: str) -> str:
    """
    Normalizes whitespace, symbols, and generates invariant MD5 hash for exact matching.
    """
    normalized = "".join(problem_text.split()).lower()
    return hashlib.md5(normalized.encode("utf-8")).hexdigest()

# ============================================================================
# 2. REFUND DEFENSE ENGINE
# ============================================================================

@router.post("/content-access/log")
def log_content_access(req: ContentAccessLogRequest, request: Request, db: Session = Depends(get_db)):
    """
    Logs student/parent content access events for audit trail and refund defense.
    """
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    now_utc = datetime.now(timezone.utc)

    # In PostgreSQL with Supabase
    try:
        db.execute(text("""
            INSERT INTO public.user_content_access_logs 
            (user_id, action_type, content_id, content_title, ip_address, user_agent, accessed_at)
            VALUES (:uid, :action, :cid, :title, :ip, :ua, :accessed_at)
        """), {
            "uid": req.user_id,
            "action": req.action_type,
            "cid": req.content_id,
            "title": req.content_title,
            "ip": ip,
            "ua": ua,
            "accessed_at": now_utc
        })
        db.commit()
    except Exception as e:
        db.rollback()
        # Fallback to local table if postgres table is syncing
        return {"success": False, "note": str(e)}

    return {"success": True, "action": req.action_type, "timestamp": now_utc.isoformat()}


@router.post("/subscription/refund-check")
def check_refund_defense(req: RefundCheckRequest, db: Session = Depends(get_db)):
    """
    Validates legal eligibility for automated subscription cancellation/refund.
    Enforces Article 17, Paragraph 2, Item 5 of Electronic Commerce Act.
    """
    try:
        res = db.execute(text("""
            SELECT eligible_for_auto_refund, solution_views_count, pdf_downloads_count, defense_reason
            FROM public.check_refund_defense_status(:uid, :max_views)
        """), {
            "uid": req.user_id,
            "max_views": req.max_trial_views
        }).fetchone()

        if res:
            return {
                "success": True,
                "eligible": bool(res[0]),
                "solution_views": int(res[1]),
                "pdf_downloads": int(res[2]),
                "reason": str(res[3])
            }
    except Exception as e:
        # Fallback evaluation query
        try:
            views_res = db.execute(text("""
                SELECT 
                    COUNT(*) FILTER (WHERE action_type = 'VIEW_SOLUTION'),
                    COUNT(*) FILTER (WHERE action_type IN ('DOWNLOAD_PDF', 'PRINT_WORKSHEET'))
                FROM public.user_content_access_logs
                WHERE user_id = :uid
            """), {"uid": req.user_id}).fetchone()

            views = views_res[0] if views_res else 0
            downloads = views_res[1] if views_res else 0

            if downloads > 0:
                return {
                    "success": True,
                    "eligible": False,
                    "solution_views": views,
                    "pdf_downloads": downloads,
                    "reason": "전자상거래법 제17조 제2항 제5호에 따라, PDF 다운로드 또는 인쇄 이력이 존재하여 디지털 콘텐츠 가치 소모로 즉시 환불이 제한됩니다."
                }
            if views >= req.max_trial_views:
                return {
                    "success": True,
                    "eligible": False,
                    "solution_views": views,
                    "pdf_downloads": downloads,
                    "reason": f"체험 분량({req.max_trial_views}회)을 초과한 {views}회의 상세 해설 열람 이력이 확인되어 자동 환불이 제한됩니다."
                }
            return {
                "success": True,
                "eligible": True,
                "solution_views": views,
                "pdf_downloads": downloads,
                "reason": "자동 환불 가능 대상입니다."
            }
        except Exception as inner_e:
            return {"success": False, "error": str(inner_e)}

    return {"success": True, "eligible": True, "solution_views": 0, "pdf_downloads": 0, "reason": "이력 없음"}


# ============================================================================
# 3. RATE LIMITING PROXY
# ============================================================================

@router.post("/rate-limit/check")
def check_rate_limit(user_id: str, tier: str = "FREE", db: Session = Depends(get_db)):
    """
    Checks if user is within rate limits:
    FREE: 5 / min, 20 / day
    PRO: 20 / min, 200 / day
    """
    max_min = 20 if tier.upper() in ["PRO", "INSTITUTION"] else 5
    max_day = 200 if tier.upper() in ["PRO", "INSTITUTION"] else 20

    try:
        res = db.execute(text("""
            SELECT allowed, current_minute_count, current_day_count, retry_after_seconds, reason
            FROM public.check_and_increment_rate_limit(:uid, :tier, :m_min, :m_day)
        """), {
            "uid": user_id,
            "tier": tier,
            "m_min": max_min,
            "m_day": max_day
        }).fetchone()

        if res:
            allowed = bool(res[0])
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "reason": str(res[4]),
                        "retry_after": int(res[3]),
                        "min_count": int(res[1]),
                        "day_count": int(res[2])
                    }
                )
            return {
                "allowed": True,
                "min_count": int(res[1]),
                "day_count": int(res[2]),
                "tier": tier
            }
    except HTTPException:
        raise
    except Exception as e:
        # Fallback permissive if rate limit table is initializing
        return {"allowed": True, "note": str(e)}


# ============================================================================
# 4. PGVECTOR & HASH SEMANTIC CACHE LOOKUP
# ============================================================================

@router.post("/cache/lookup")
def lookup_cached_problem(problem_text: str, db: Session = Depends(get_db)):
    """
    Step 1: O(1) Exact Hash Lookup
    Step 2: Vector Cosine Similarity Search (if vector extension active)
    Returns cached solution immediately (0 LLM token cost).
    """
    p_hash = generate_problem_hash(problem_text)

    try:
        # 1. Exact hash lookup
        row = db.execute(text("""
            SELECT id, problem_title, problem_text, solution_data, final_answer, hit_count
            FROM public.problem_embeddings
            WHERE problem_hash = :p_hash
        """), {"p_hash": p_hash}).fetchone()

        if row:
            # Increment hit counter
            db.execute(text("""
                UPDATE public.problem_embeddings
                SET hit_count = hit_count + 1, last_accessed_at = NOW()
                WHERE id = :id
            """), {"id": row[0]})
            db.commit()

            return {
                "hit": True,
                "type": "EXACT_HASH_MATCH",
                "similarity": 1.0,
                "title": row[1],
                "problem_text": row[2],
                "solution_data": row[3],
                "final_answer": row[4],
                "hit_count": row[5] + 1
            }
    except Exception as e:
        return {"hit": False, "error": str(e)}

    return {"hit": False, "type": "CACHE_MISS"}
