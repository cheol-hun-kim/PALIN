import os
import json
from google import genai
from google.genai.errors import APIError

UNIV_CUTS_PATH = os.path.join(os.path.dirname(__file__), "univ_cuts.json")

def load_univ_cuts():
    try:
        if os.path.exists(UNIV_CUTS_PATH):
            with open(UNIV_CUTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            try:
                from parse_univ_data import run_parsing
                run_parsing()
                with open(UNIV_CUTS_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
    except Exception:
        return {}

KEY_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "gemini_key.txt")

def get_saved_api_key():
    if os.path.exists(KEY_FILE_PATH):
        try:
            with open(KEY_FILE_PATH, "r", encoding="utf-8") as f:
                k = f.read().strip()
                if k: return k
        except Exception:
            pass
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

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
    return "수능과 내신 공부 균형을 맞추고, 취침/기상 미션을 준수하여 최적의 생체 리듬을 찾으세요."

def generate_dynamic_fallback(msg: str) -> str:
    m = msg.strip().lower()
    
    if any(k in m for k in ["안녕", "반가워", "하이", "처음"]):
        return "어 그래, 반갑다! 지금은 AI 서버와 연결이 불안정해서 긴 상담은 어렵네. API 키 설정이 제대로 되어 있는지 확인해보고 다시 말 걸어줘."
        
    if any(k in m for k in ["고민", "힘들", "상담"]):
        return "네 고민을 깊게 들어주고 싶은데, 현재 AI 서버 연결 문제로 자세한 답변이 힘들어. API 키 설정을 확인해주면 내가 제대로 된 해결책을 줄게."
        
    return "현재 시스템 연결이 원활하지 않거나 API 키가 설정되지 않았습니다. API 키 설정을 확인하거나 잠시 후 다시 시도해주세요."

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available. API key may be missing.")
        return generate_dynamic_fallback(message)
    
    try:
        knowledge = get_expert_knowledge()
        # 토큰 절약: 지식 베이스를 30,000자로 제한 (무료 API 할당량 보호)
        if len(knowledge) > 30000:
            knowledge = knowledge[:30000] + "\n\n[... 지식 베이스 나머지 생략 (토큰 절약) ...]"
        
        system_prompt = (
            "You are 'PALIN BOT'. Respond ONLY in Korean.\n\n"
            
            "IDENTITY: You are the AI alter-ego of Kim Chul-Hun, a 13-year veteran CSAT Korean instructor "
            "and director of Ilwon Academy in Bundang. Having personally failed the CSAT twice before "
            "succeeding on the third attempt, you mentor students with brutal honesty rooted in real experience.\n\n"
            
            "=== ABSOLUTE PRIORITY RULES ===\n"
            "RULE 1 - CONTEXT IS KING: Read the student's message carefully. Understand what they are ACTUALLY asking or saying. "
            "Then respond directly to THAT specific topic. NEVER give a generic pre-scripted response that ignores their message.\n"
            "RULE 2 - NO PARROTING: Never repeat the same phrases, sentence structures, or advice patterns across messages. "
            "Each response must feel fresh and uniquely crafted for that specific conversation moment.\n"
            "RULE 3 - CONVERSATION CONTINUITY: If there is prior conversation history, you MUST continue naturally from where it left off. "
            "Reference things the student said before. Build on the ongoing dialogue.\n"
            "RULE 4 - NO MARKDOWN: Never use #, **, -, ```, bullet points, or numbered lists. Write in pure spoken Korean.\n"
            "RULE 5 - NO AI CLICHES: Never say things like 'What can I help you with?', 'Great question!', 'I understand your concern'. "
            "Talk like a real mentor in a casual face-to-face conversation.\n\n"
            
            "=== VOICE & TONE ===\n"
            "Use confident, direct, caring banmal (casual speech): ~haera, ~haja, ~iya, ~geodeun, ~janha.\n"
            "Be like a tough but caring older brother/mentor who genuinely wants the student to succeed.\n"
            "When the student shares real struggles, show genuine empathy before giving advice.\n"
            "When the student makes excuses or brags about ineffective study habits, challenge them firmly.\n\n"
            
            "=== RESPONSE DEPTH GUIDELINES ===\n"
            "CASUAL CHAT (food, weather, tiredness, greetings, random topics):\n"
            "- Respond naturally and warmly, 200-600 characters.\n"
            "- Connect lightly to student wellness (diet, sleep, exercise) at the end with 1-2 sentences.\n"
            "- Do NOT force exam/study topics into casual conversations.\n\n"
            
            "ACADEMIC/EXAM CONSULTATION (grades, study methods, CSAT, GPA, schedule, slump, subject advice):\n"
            "- Provide deep, substantial responses of 1500-3000 characters minimum.\n"
            "- Weave these elements naturally into a flowing narrative (do NOT label them as steps):\n"
            "  a) Shatter illusions: Identify the student's misconceptions or inefficient habits with data and experience.\n"
            "  b) Root cause: Draw from the knowledge base below to explain WHY their approach isn't working.\n"
            "  c) Action plan: Give 3+ concrete, actionable steps they can implement TODAY.\n"
            "  d) Probe question: End with one sharp question about their current situation to keep the dialogue going.\n\n"
            
            "=== CORE PHILOSOPHY (from the Knowledge Base) ===\n"
            "- CSAT tests rule-decoding ability, not memorization. Blaming talent is escapism.\n"
            "- Private academy worksheets are often written by undergrad part-timers. The ONLY reliable material is official CSAT past exams.\n"
            "- Grinding 100 problems mindlessly is worthless. Deep contemplation of 1 problem for 30+ minutes builds real skill.\n"
            "- If your GPA is below 3rd grade, stop chasing Susi (early admission). Commit fully to Jeongsi (regular admission).\n"
            "- Plan in TIME units (hours), not volume units (pages). Time flows consistently regardless of difficulty.\n"
            "- Protect 6.5 hours of sleep minimum. 2 hours of clear-headed problem analysis beats 10 hours of brain-fog studying.\n"
            "- Exam-day variables (sleep, digestion, anxiety) are part of your skill set. Control them.\n\n"
            
            "=== KNOWLEDGE BASE: Kim Chul-Hun's 'Principles of Failure' ===\n"
            "Use this knowledge base to find relevant insights for the student's specific situation. "
            "Do not copy-paste from it. Reinterpret and adapt the content naturally for the student's context.\n\n"
            f"{knowledge}\n"
        )
        
        # Build multi-turn conversation contents
        contents = []
        if history:
            for msg_item in history[-10:]:  # 최근 10턴으로 줄여 토큰 절약
                role = 'user' if msg_item.get('role') == 'user' else 'model'
                text = msg_item.get('content', '')
                if text.strip():
                    contents.append({'role': role, 'parts': [{'text': text}]})
        contents.append({'role': 'user', 'parts': [{'text': message}]})
        
        # 429 에러 시 재시도 (최대 3회, 지수 백오프)
        import time
        last_error = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=contents,
                    config={
                        'system_instruction': system_prompt,
                        'temperature': 0.6,
                        'max_output_tokens': 4000,
                    }
                )
                
                result_text = response.text
                if result_text and result_text.strip():
                    return result_text
                
                print("CHATBOT WARNING: Gemini returned empty/null response text.")
                return generate_dynamic_fallback(message)
                
            except APIError as api_err:
                last_error = api_err
                status = getattr(api_err, 'status_code', 0)
                if status == 429 and attempt < 2:
                    wait = (attempt + 1) * 5  # 5초, 10초 대기
                    print(f"CHATBOT 429 RATE LIMIT: attempt {attempt+1}/3, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                print(f"CHATBOT API ERROR (status={status}, attempt={attempt+1}): {api_err}")
                break
        
        if last_error:
            status = getattr(last_error, 'status_code', 0)
            if status == 429:
                return "지금 AI 서버가 요청이 많아서 잠시 쉬고 있어. 1~2분 뒤에 다시 말 걸어줘. 그동안 오늘 기출 1문제라도 펴놓고 사색해봐."
            return generate_dynamic_fallback(message)
        return generate_dynamic_fallback(message)
        
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR ({type(e).__name__}): {e}")
        import traceback
        traceback.print_exc()
        return generate_dynamic_fallback(message)


# --- 영어 / 한국사 등급 자동 계산 모듈 ---

def get_english_grade(score: int) -> int:
    """영어 절대평가 등급 변환 (90점 이상 1등급, 80점 이상 2등급...)"""
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
    """한국사 절대평가 등급 변환 (40점 이상 1등급, 35점 이상 2등급...)"""
    if score >= 40: return 1
    elif score >= 35: return 2
    elif score >= 30: return 3
    elif score >= 25: return 4
    elif score >= 20: return 5
    elif score >= 15: return 6
    elif score >= 10: return 7
    elif score >= 5: return 8
    return 9


# --- 합격 예측 알고리즘 (수정) ---

def evaluate_univ_admission_extended(
    gpa: float,
    kor_pct: int,
    math_pct: int,
    eng_score: int,
    tam1_pct: int,
    tam2_pct: int,
    history_score: int,
    university_name: str,
    department_name: str
) -> dict:
    
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
            if target_cuts_dict:
                break
                
    target_cuts = None
    if target_cuts_dict:
        if len(target_cuts_dict) == 1:
            target_cuts = list(target_cuts_dict.values())[0]
            target_cuts["계열"] = list(target_cuts_dict.keys())[0]
        else:
            is_science = False
            science_keywords = ["공학", "화학", "생물", "수학", "물리", "의예", "치의", "약학", "한의", "간호", "컴퓨터", "IT", "과학", "소프트웨어", "기계", "전기", "전자", "신소재", "항공", "자연", "바이오", "시스템", "융합"]
            for kw in science_keywords:
                if kw in department_name:
                    is_science = True
                    break
            
            chosen_key = "이과" if is_science else "문과"
            if chosen_key in target_cuts_dict:
                target_cuts = target_cuts_dict[chosen_key]
                target_cuts["계열"] = chosen_key
            else:
                target_cuts = list(target_cuts_dict.values())[0]
                target_cuts["계열"] = list(target_cuts_dict.keys())[0]
                
    if not target_cuts:
        target_cuts = {
            "적정누백": 15.0,
            "예상누백": 20.0,
            "소신누백": 25.0,
            "계열": "이과"
        }
        
    적정 = target_cuts.get("적정누백")
    예상 = target_cuts.get("예상누백")
    소신 = target_cuts.get("소신누백")
    
    if 적정 is None: 적정 = 15.0
    if 예상 is None: 예상 = 20.0
    if 소신 is None: 소신 = 25.0
    
    # --- 정시 (Jeongsi) 판정 및 미달 % 계산 (소수점 없는 정수) ---
    target_cutoff_pct = round(100.0 - 적정)
    pct_diff = round(mock_avg - target_cutoff_pct)
    
    if student_nuback <= 적정 - 5.0:
        jeongsi_tier = "하향"
    elif student_nuback <= 적정:
        jeongsi_tier = "안정"
    elif student_nuback <= 예상:
        jeongsi_tier = "적정"
    elif student_nuback <= 소신:
        jeongsi_tier = "소신"
    else:
        jeongsi_tier = "상향"

    if pct_diff >= 0:
        jeongsi_tip = f"목표 대학 합격선 대비 백분위 +{pct_diff}%p 여유 (안정/적정 지원권)"
    else:
        jeongsi_tip = f"목표 대학 합격선 대비 백분위 {pct_diff}%p 미달 (상향 지원권)"

    if eng_grade >= 3 or hist_grade >= 4:
        tier_downgrade = {"하향": "안정", "안정": "적정", "적정": "소신", "소신": "상향", "상향": "상향"}
        old_tier = jeongsi_tier
        jeongsi_tier = tier_downgrade.get(jeongsi_tier, "상향")
        jeongsi_tip += f" [영어/한국사 감점 반영: {old_tier} → {jeongsi_tier}]"

    # --- 수시 (Susi) 판정 및 등급 미달 계산 ---
    gpa_cut = 2.0
    if 소신 < 2.0:
        gpa_cut = 1.3
    elif 소신 < 10.0:
        gpa_cut = 1.8
    elif 소신 < 25.0:
        gpa_cut = 2.5
    else:
        gpa_cut = 3.5
        
    gpa_diff = round(gpa_cut - gpa, 1)
    if gpa_diff >= 0.5:
        susi_tier = "하향"
    elif gpa_diff >= 0.1:
        susi_tier = "안정"
    elif gpa_diff >= -0.2:
        susi_tier = "적정"
    elif gpa_diff >= -0.5:
        susi_tier = "소신"
    else:
        susi_tier = "상향"

    if gpa_diff >= 0:
        susi_tip = f"목표 합격 내신({gpa_cut}등급) 대비 +{gpa_diff}등급 우수 (안정 지원권)"
    else:
        susi_tip = f"목표 합격 내신({gpa_cut}등급) 대비 {abs(gpa_diff):.1f}등급 미달 (상향 지원권)"

    if mock_avg < (100.0 - 소신) - 8:
        tier_downgrade = {"하향": "안정", "안정": "적정", "적정": "소신", "소신": "상향", "상향": "상향"}
        old_susi = susi_tier
        susi_tier = tier_downgrade.get(susi_tier, "상향")
        susi_tip += f" [수능 최저 미달 가능성 주의: {old_susi} → {susi_tier}]"

    client = get_gemini_client()
    if client:
        try:
            prompt = (
                f"당신은 입시 컨설턴트입니다. 다음 학생의 개별 성적 진단 결과에 대해 수시전략과 정시전략을 아우르는 피드백 1문장을 각각 작성해주세요.\n"
                f"학생 성적 - 내신: {gpa}등급, 모의고사 평균백분위: {mock_avg:.1f} (국어:{kor_pct}, 수학:{math_pct}, 영어:{eng_grade}등급, 탐구1:{tam1_pct}, 탐구2:{tam2_pct}, 한국사:{hist_grade}등급)\n"
                f"지원대학: {university_name} {department_name} (내신컷대체: {gpa_cut}, 정시백분위컷대체: {100.0-적정})\n"
                f"수시 진단 등급: {susi_tier}, 정시 진단 등급: {jeongsi_tier}\n"
                f"요구사항: 존댓말로 학생에게 조언하듯이 부드럽지만 전문적으로 수시용 조언 1문장, 정시용 조언 1문장을 JSON 형식으로 출력해주세요.\n"
                f"예시 형식: {{\"susi_comment\": \"수시 조언...\", \"jeongsi_comment\": \"정시 조언...\"}}"
            )
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            text_cleaned = response.text.strip().replace("```json", "").replace("```", "")
            ai_data = json.loads(text_cleaned)
            if "susi_comment" in ai_data:
                susi_tip += f" (AI 수시 전략: {ai_data['susi_comment']})"
            if "jeongsi_comment" in ai_data:
                jeongsi_tip += f" (AI 정시 전략: {ai_data['jeongsi_comment']})"
        except Exception:
            pass

    return {
        "susi": {
            "university": f"{university_name} {department_name} (수시)",
            "result_tier": susi_tier,
            "tip": susi_tip
        },
        "jeongsi": {
            "university": f"{university_name} {department_name} (정시)",
            "result_tier": jeongsi_tier,
            "tip": jeongsi_tip
        }
    }
