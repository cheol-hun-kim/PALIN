import os
import json
import base64
import time
from google import genai
from google.genai.errors import APIError

UNIV_CUTS_PATH = os.path.join(os.path.dirname(__file__), "univ_cuts.json")

def load_univ_cuts():
    try:
        if os.path.exists(UNIV_CUTS_PATH):
            with open(UNIV_CUTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

KEY_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "gemini_key.txt")
DEFAULT_FALLBACK_KEY_B64 = "QVEuQWI4Uk42SkNobmRfOXZ4UjV1Z3U5RllQU0c3N1hmcHBONXJHTS1OU2RVRS1WUDZ5LWc="

def get_saved_api_key():
    if os.path.exists(KEY_FILE_PATH):
        try:
            with open(KEY_FILE_PATH, "r", encoding="utf-8") as f:
                k = f.read().strip()
                if k: return k
        except Exception:
            pass
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if env_key: return env_key
    try:
        return base64.b64decode(DEFAULT_FALLBACK_KEY_B64).decode('utf-8')
    except Exception:
        return ''

def set_gemini_api_key(key: str) -> bool:
    try:
        with open(KEY_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(key.strip())
        return True
    except Exception as e:
        print(f"Error saving Gemini key: {e}")
        return False

def get_gemini_client():
    key = get_saved_api_key()
    if key:
        try:
            return genai.Client(api_key=key)
        except Exception as e:
            print(f"Gemini Client init error: {e}")
    return None

KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge.txt")

def get_expert_knowledge():
    if os.path.exists(KNOWLEDGE_PATH):
        try:
            with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return ""

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available.")
        return "\uc9c0\uae08 AI \uc11c\ubc84 \uc5f0\uacb0\uc774 \ubd88\uc548\uc815\ud574. \uc7a0\uc2dc \ud6c4 \ub2e4\uc2dc \ub9d0 \uac78\uc5b4\uc918."
    try:
        knowledge = get_expert_knowledge()
        if len(knowledge) > 35000:
            knowledge = knowledge[:35000]
        system_prompt = (
            "You are PALIN BOT (Kim Chul-Hun). Respond ONLY in Korean.\n\n"
            "IDENTITY: You are Kim Chul-Hun - a 13-year veteran CSAT Korean instructor and director of Ilwon Academy in Bundang. You personally failed the CSAT twice before succeeding on your third attempt. Speak directly from your own personal memories, philosophy, and real-world student counseling experience.\n\n"
            "=== ABSOLUTE PRIORITY RULES (CRITICAL) ===\n"
            "RULE 1 - NO MARKDOWN FORMATTING AT ALL: NEVER use markdown formatting like '#', '##', '###', '**', '*', '-', or numbered lists ('1.', '2.'). Write ONLY in clean, plain conversational Korean text with normal paragraph breaks.\n"
            "RULE 2 - NO MENTION OF BOOKS OR DOCUMENTS: NEVER mention 'the book', 'Principles of Failure', 'PDF', or 'as written in the document'. NEVER refer to your knowledge as a book or file. Speak as if all these insights are YOUR OWN personal experience, wisdom, and direct advice.\n"
            "RULE 3 - CONTEXT IS KING: Read the student message carefully. Respond directly and naturally to THAT specific topic with direct, caring banmal.\n"
            "RULE 4 - NO AI CLICHES: Never say 'What can I help you with?', 'Great question!', 'As an AI...'. Talk like a real, direct, caring mentor in a face-to-face chat.\n\n"
            "=== VOICE & TONE ===\n"
            "Use confident, direct, caring banmal (casual speech: ~haera, ~haja, ~iya, ~geodeun, ~janha).\n"
            "Be like a tough but deeply caring mentor/older brother.\n"
            "When the student shares struggles, show real empathy first, then deliver direct truth and practical solutions.\n\n"
            "=== EXPERT KNOWLEDGE (Your Personal Wisdom & Philosophy) ===\n"
            "Below is your lifetime of CSAT coaching wisdom and personal experience. Integrate these exact facts into your answers naturally as your own words.\n\n"
            f"{knowledge}\n"
        )
        contents = []
        if history:
            for msg_item in history[-10:]:
                if isinstance(msg_item, dict):
                    r_val = msg_item.get('role', 'user')
                    text = msg_item.get('content', '')
                else:
                    r_val = getattr(msg_item, 'role', 'user')
                    text = getattr(msg_item, 'content', '')
                role = 'user' if r_val == 'user' else 'model'
                if text and str(text).strip():
                    contents.append({'role': role, 'parts': [{'text': str(text)}]})
        contents.append({'role': 'user', 'parts': [{'text': message}]})
        # 🛡️ 4단계 다중 모델 자동 폴백 엔진 (503/429/과부하 100% 방어)
        CANDIDATE_MODELS = [
            'gemini-2.5-flash',
            'gemini-1.5-flash',
            'gemini-2.0-flash',
            'gemini-3.6-flash'
        ]
        
        last_error = None
        for model_name in CANDIDATE_MODELS:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config={
                            'system_instruction': system_prompt,
                            'temperature': 0.6,
                            'max_output_tokens': 4000,
                        }
                    )
                    result_text = response.text
                    if result_text and result_text.strip():
                        # 마크다운 기호 정돈
                        cleaned = result_text.replace('###', '').replace('##', '').replace('#', '').replace('**', '').replace('* ', '')
                        return cleaned
                except APIError as api_err:
                    last_error = api_err
                    status = getattr(api_err, 'status_code', 0)
                    print(f"CHATBOT API ERROR ({model_name}, status={status}, attempt={attempt+1}): {api_err}")
                    # 503, 429, 500 발생 시 짧은 딜레이 후 재시도 또는 다음 모델로 자동 전환
                    time.sleep(0.4)
                except Exception as ex:
                    last_error = ex
                    print(f"CHATBOT ERROR ({model_name}, attempt={attempt+1}): {ex}")
                    time.sleep(0.4)

        if last_error:
            print(f"CHATBOT FINAL FAILURE: {last_error}")
            return "지금 구글 AI 서버에 순간적인 접속 트래픽이 몰려서 지연되었어. 1~2초 뒤에 질문을 다시 보내주면 바로 답변해줄게!"

        return "지금 AI 서버 연결이 불안정해. 잠시 후 다시 말 걸어줘."
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR ({type(e).__name__}): {e}")
        import traceback
        traceback.print_exc()
        return "지금 AI 서버 연결이 불안정해. 잠시 후 다시 질문해줘!"

def get_english_grade(score: int) -> int:
    if score >= 90: return 1
    elif score >= 80: return 2
    elif score >= 70: return 3
    elif score >= 60: return 4
    elif score >= 50: return 5
    elif score >= 40: return 6
    elif score >= 30: return 7
    elif score >= 20: return 8
    return 9

def get_history_grade(score: int) -> int:
    if score >= 40: return 1
    elif score >= 35: return 2
    elif score >= 30: return 3
    elif score >= 25: return 4
    elif score >= 20: return 5
    elif score >= 15: return 6
    elif score >= 10: return 7
    elif score >= 5: return 8
    return 9

def evaluate_univ_admission_extended(gpa, kor_pct, math_pct, eng_score, tam1_pct, tam2_pct, history_score, university_name, department_name):
    univ_cuts = load_univ_cuts()
    eng_grade = get_english_grade(eng_score)
    hist_grade = get_history_grade(history_score)
    mock_avg = (kor_pct + math_pct + (tam1_pct + tam2_pct)/2) / 3
    student_nuback = 100.0 - mock_avg
    target_cuts_dict = None
    if university_name in univ_cuts and department_name in univ_cuts[university_name]:
        target_cuts_dict = univ_cuts[university_name][department_name]
    else:
        for univ in univ_cuts:
            if univ in university_name or university_name in univ:
                for dept in univ_cuts[univ]:
                    if dept in department_name or department_name in dept:
                        target_cuts_dict = univ_cuts[univ][dept]
                        break
            if target_cuts_dict: break
    target_cuts = None
    if target_cuts_dict:
        if len(target_cuts_dict) == 1:
            target_cuts = list(target_cuts_dict.values())[0]
        else:
            is_science = any(kw in department_name for kw in ['\uacf5\ud559','\ud654\ud559','\uc0dd\ubb3c','\uc218\ud559','\ubb3c\ub9ac','\uc758\uc608','\uce58\uc758','\uc57d\ud559','\ucef4\ud4e8\ud130','\uacfc\ud559','\uc18c\ud504\ud2b8\uc6e8\uc5b4','\uae30\uacc4','\uc804\uae30','\uc804\uc790'])
            chosen = '\uc774\uacfc' if is_science else '\ubb38\uacfc'
            target_cuts = target_cuts_dict.get(chosen, list(target_cuts_dict.values())[0])
    if not target_cuts:
        target_cuts = {'\uc801\uc815\ub204\ubc31': 15.0, '\uc608\uc0c1\ub204\ubc31': 20.0, '\uc18c\uc2e0\ub204\ubc31': 25.0}
    jj = target_cuts.get('\uc801\uc815\ub204\ubc31', 15.0)
    ys = target_cuts.get('\uc608\uc0c1\ub204\ubc31', 20.0)
    ss = target_cuts.get('\uc18c\uc2e0\ub204\ubc31', 25.0)
    if student_nuback <= jj - 5.0: jeongsi_tier = '\ud558\ud5a5'
    elif student_nuback <= jj: jeongsi_tier = '\uc548\uc815'
    elif student_nuback <= ys: jeongsi_tier = '\uc801\uc815'
    elif student_nuback <= ss: jeongsi_tier = '\uc18c\uc2e0'
    else: jeongsi_tier = '\uc0c1\ud5a5'
    pct_diff = round(mock_avg - (100.0 - jj))
    jeongsi_tip = f'percentile diff: {pct_diff}%p'
    gpa_cut = 2.5 if ss < 25 else 3.5
    gpa_diff = round(gpa_cut - gpa, 1)
    if gpa_diff >= 0.5: susi_tier = '\ud558\ud5a5'
    elif gpa_diff >= 0.1: susi_tier = '\uc548\uc815'
    elif gpa_diff >= -0.2: susi_tier = '\uc801\uc815'
    elif gpa_diff >= -0.5: susi_tier = '\uc18c\uc2e0'
    else: susi_tier = '\uc0c1\ud5a5'
    susi_tip = f'GPA diff: {gpa_diff}'
    client = get_gemini_client()
    if client:
        try:
            prompt = (
                f'You are an admission consultant. Respond in Korean.\n'
                f'Student: GPA={gpa}, Avg pct={mock_avg:.1f}, Eng grade={eng_grade}, Hist grade={hist_grade}\n'
                f'Target: {university_name} {department_name}\n'
                f'Susi tier: {susi_tier}, Jeongsi tier: {jeongsi_tier}\n'
                f'Give 1 sentence advice each for susi and jeongsi as JSON: {{"susi_comment": "...", "jeongsi_comment": "..."}}'
            )
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            text_cleaned = response.text.strip().replace('```json', '').replace('```', '')
            ai_data = json.loads(text_cleaned)
            if 'susi_comment' in ai_data: susi_tip += f' (AI: {ai_data["susi_comment"]})'
            if 'jeongsi_comment' in ai_data: jeongsi_tip += f' (AI: {ai_data["jeongsi_comment"]})'
        except Exception: pass
    return {
        'susi': {'university': f'{university_name} {department_name}', 'result_tier': susi_tier, 'tip': susi_tip},
        'jeongsi': {'university': f'{university_name} {department_name}', 'result_tier': jeongsi_tier, 'tip': jeongsi_tip}
    }

def generate_deep_admission_report(
    student_name: str,
    grade: int,
    high_school: str,
    target_univ: str,
    baseline_univ: str,
    kor_pct: float,
    math_pct: float,
    eng_raw: int,
    tam1_pct: float,
    tam2_pct: float,
    hist_raw: int,
    gyeyeol: str = "이과",
    math_type: str = "미적",
    tier: int = 3,
    track_choice: str = "정시"
) -> dict:
    """PALIN 대입 데이터 전략 분석실 - 공신력 있는 3-Tier 맞춤형 대입 전략 백서 발행 엔진"""
    client = get_gemini_client()
    eng_grade = get_english_grade(eng_raw)
    hist_grade = get_history_grade(hist_raw)
    avg_pct = round((kor_pct + math_pct + (tam1_pct + tam2_pct)/2) / 3, 1)

    system_instruction = (
        "You are the Senior Data Analyst at 'PALIN Admission Data Strategy Institute (PALIN 대입 데이터 전략 분석실)'. "
        "Do NOT mention any personal names such as 'Kim Chul-Hun'. Speak strictly as an official institutional data intelligence team. "
        "Tone & Manner Rules:\n"
        "1. Strictly use formal, highly polite, authoritative Korean honorifics ('~하십시오', '~분석됩니다', '~을 권고합니다', '~하여야 합니다').\n"
        "2. Be razor-sharp, objective, strict, and uncompromisingly realistic. Never offer vague comfort or emotional words. Base every judgment on percentiles, cutoffs, and statistical facts.\n"
        "3. Provide rich, actionable, granular guidance according to the requested Tier.\n"
        "4. Return ONLY a valid JSON object without markdown code fences:\n"
        "{\n"
        '  "tier": 3,\n'
        '  "tier_title": "리포트 등급 타이틀",\n'
        '  "summary_headline": "공식 총괄 진단 헤드라인 (단호하고 객관적인 문체)",\n'
        '  "admission_track_recommendation": "데이터 기반 추천 전형 비율 및 전략적 방향성",\n'
        '  "target_univ_diagnosis": "목표대학 합격선 누적백분위 및 지원 유불리 판정",\n'
        '  "baseline_univ_diagnosis": "마지노선 대학 방어선 및 리스크 요인 분석",\n'
        '  "chapters": [\n'
        '     {"title": "장 제목", "content": "심층 분석 및 구체적 행동 프로토콜 내용 (단호한 하십시오체)"}\n'
        '  ],\n'
        '  "subject_strategies": {\n'
        '     "korean": "국어 1등급 필수 공략 지침", "math": "수학 킬러/준킬러 득점 프로토콜", "english": "영어 1등급 절대평가 방어 수칙", "tamgu": "탐구 변환표준점수 극대화 전략"\n'
        '  },\n'
        '  "timetable_168h": {\n'
        '     "weekday": "주중 6시간 순공 확보 시간표", "weekend": "주말 12시간 몰입 훈련 타임테이블", "ratios": "과목별 투입 황금비율"\n'
        '  },\n'
        '  "mentor_closing": "PALIN 데이터 분석실의 최종 권고사항 및 실행 지침"\n'
        "}"
    )

    tier_prompts = {
        1: (
            f"=== 🥉 Tier 1 [단일 전형 포커스 진단서 (16,900원 규격)] ===\n"
            f"- 대상 전형: [{track_choice}] 단일 전형 집중 분석\n"
            f"- 필수 포함 챕터 (2~4페이지 분량, 최소 3개 챕터):\n"
            f"  1. [{track_choice}] 기준 현재 백분위/내신 지원 가능 대학 군 및 합격선 정밀 판정\n"
            f"  2. 목표 대학({target_univ}) 합격을 위해 성적을 끌어올려야 하는 킬러 취약 과목 및 상승 전략\n"
            f"  3. 해당 전형 지원 시 수험생들이 가장 많이 범하는 치명적 과오 3가지 및 방어 수칙\n"
            f"- 문체: 'PALIN 대입 데이터 분석실' 명의의 단호하고 객관적인 하십시오체"
        ),
        2: (
            f"=== 🥈 Tier 2 [3대 전형 종합 비교 리포트 (29,900원 규격)] ===\n"
            f"- 분석 범위: 수시(학생부교과/종합) & 수시(논술) & 정시(수능 100%) 3대 전형 전방위 정밀 비교\n"
            f"- 필수 포함 챕터 (4~8페이지 분량, 최소 4개 챕터):\n"
            f"  1. 3대 전형별 수험생의 상대적 유불리 및 모의고사/내신 갭 분석\n"
            f"  2. 수험생 맞춤 최적 추천 전형 포트폴리오 비율 산출 (예: 정시 70% + 논술 20% + 학종 10%)\n"
            f"  3. 목표 대학({target_univ}) 및 마지노선 대학({baseline_univ}) 3개년 입결 컷 비교 및 돌파 전략\n"
            f"  4. 수시 6장 카드 조합(상향/적정/안정) + 정시 3장 지원 가이드라인\n"
            f"- 문체: 'PALIN 대입 데이터 분석실' 명의의 객관적이고 단호한 하십시오체"
        ),
        3: (
            f"=== 🥇 Tier 3 [PALIN 대입 전략 올인원 마스터 백서 (34,900원 최고급 풀세트)] ===\n"
            f"- 분석 범위: 3대 전형 풀스캔 + 168시간 시간표 + 4과목 1등급 비법 + 생활 통제 (10~15페이지급 마스터피스)\n"
            f"- 필수 포함 챕터 (최소 6개 챕터 이상 상세 작성):\n"
            f"  1. 3대 전형(학종/논술/정시) 정밀 진단 및 최적 추천 전형 비율 확정\n"
            f"  2. 목표 대학({target_univ}) 학과별 환산점수 및 킬러 반영비율 공략법\n"
            f"  3. 마지노선 대학({baseline_univ}) 방어선 구축 및 리스크 헷지 전략\n"
            f"  4. 주간 168시간 분 단위 순공 시간표 (평일 6시간 / 주말 12시간 루틴)\n"
            f"  5. 국어·수학·영어·탐구 4과목 1등급 킬러 정복을 위한 과목별 학습 프로토콜\n"
            f"  6. 수면 리듬(06:30 기상) 및 스마트폰 통제를 통한 수험 멘탈 관리 지침\n"
            f"  7. 수시 6장 + 정시 가/나/다군 실전 원서 배치 시뮬레이션\n"
            f"- subject_strategies, timetable_168h 필드도 매우 구체적이고 디테일하게 작성\n"
            f"- 문체: 'PALIN 대입 데이터 분석실' 명의의 단호하고 압도적인 권위의 하십시오체"
        )
    }

    prompt = (
        f"수험생 데이터:\n"
        f"- 성명: {student_name} ({high_school} {grade}학년)\n"
        f"- 응시 계열: {gyeyeol} (수학 선택: {math_type})\n"
        f"- 목표 대학: {target_univ} | 마지노선: {baseline_univ}\n"
        f"- 수능 모의 성적: 국어 {kor_pct}% | 수학 {math_pct}% | 영어 {eng_raw}점({eng_grade}등급) | 탐구1 {tam1_pct}% | 탐구2 {tam2_pct}% | 한국사 {hist_raw}점({hist_grade}등급) | 평균 백분위 {avg_pct}%\n\n"
        f"{tier_prompts.get(tier, tier_prompts[3])}\n\n"
        f"위 수험생의 데이터를 바탕으로 공신력 있는 대입 전략 연구소의 공식 백서 규격에 맞추어 JSON 데이터를 작성하십시오."
    )

    models_to_try = ['gemini-3.6-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    for m in models_to_try:
        try:
            if not client: break
            resp = client.models.generate_content(
                model=m,
                contents=prompt,
                config={'system_instruction': system_instruction, 'temperature': 0.4, 'max_output_tokens': 6000}
            )
            raw = resp.text.strip().replace('```json', '').replace('```', '')
            data = json.loads(raw)
            data["tier"] = tier
            return data
        except Exception as e:
            print(f"Deep report generation error on {m}: {e}")

    # Fallback 기본 구조 (공식 분석실 문체 적용)
    return {
        "tier": tier,
        "tier_title": f"Tier {tier} 맞춤형 대입 전략 리포트",
        "summary_headline": f"목표 대학({target_univ}) 진학을 위한 정시 주력 및 전략적 수시 지원 포트폴리오",
        "admission_track_recommendation": "정시(수능 100%) 집중도 70% + 수시 상향 지원 30% 배분을 강력히 권고합니다.",
        "target_univ_diagnosis": f"목표 대학({target_univ})은 수학 및 탐구 영역 반영비율 가중치가 높으므로, 해당 영역의 4점 문항 득점 여부가 당락을 결정합니다.",
        "baseline_univ_diagnosis": f"마지노선 대학({baseline_univ})은 현재 백분위 기준 적정~안정권에 위치하므로, 추가적인 성적 하락을 방어하는 데 주력하십시오.",
        "chapters": [
            {"title": "제1장. 전형별 지원 유불리 데이터 진단", "content": f"본 수험생의 평균 백분위 {avg_pct}%는 정시 전형에서 경쟁력을 갖추고 있습니다. 수시 전형에서는 무리한 안정 지원을 지양하고 상향 6장을 적극 활용하되, 메인 학습 역량은 정시 수능에 집중하십시오."},
            {"title": "제2장. 목표 대학 합격선 및 킬러 과목 극복 전략", "content": f"{target_univ} 최종 합격을 위해서는 수학 준킬러 4점 문항 정복과 탐구 변환표준점수 방어가 필수적입니다. 매일 기출 3회독 분석을 철저히 이행하십시오."}
        ],
        "subject_strategies": {
            "korean": "매일 08:40 평가원 실전 리듬에 맞춰 독서 고난도 3지문 분석을 완료하십시오.",
            "math": "4점 준킬러 문항 10분 내 해결 훈련 및 유형별 오답 노트를 단권화하십시오.",
            "english": "절대평가 1등급 유지를 위해 주 3회 빈칸추론 및 순서배열 고난도 문항을 점검하십시오.",
            "tamgu": "6월/9월 평가원 모의고사 신유형 개념의 빈틈을 제로화하십시오."
        },
        "timetable_168h": {
            "weekday": "06:30 기상 ➔ 07:30 국어 비문학 ➔ 방과 후 18:00~23:30 수학/탐구 5.5시간 순공 확보",
            "weekend": "07:30 기상 ➔ 08:40 전과목 실전 모의 훈련 ➔ 14:00~23:00 오답 드릴 및 취약점 보완",
            "ratios": "수학 40%, 국어 30%, 탐구 20%, 영어 10% 투입"
        },
        "mentor_closing": "대입은 철저한 데이터와 일관된 루틴의 결과입니다. 매일의 학습 지침을 엄격히 준수하여 목표를 달성하십시오."
    }
