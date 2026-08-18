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
    return "?�능�??�신 공�? 균형??맞추�? 취침/기상 미션??준?�하??최적???�체 리듬??찾으?�요."

def generate_dynamic_fallback(msg: str) -> str:
    m = msg.strip().lower()
    
    if any(k in m for k in ["?�녕", "반�???, "?�이", "처음"]):
        return "??그래, 반갑?? 지금�? AI ?�버?� ?�결??불안?�해??�??�담?� ?�렵?? API ???�정???��?�??�어 ?�는지 ?�인?�보�??�시 �?걸어�?"
        
    if any(k in m for k in ["고�?", "?�들", "?�담"]):
        return "??고�???깊게 ?�어주고 ?��??? ?�재 AI ?�버 ?�결 문제�??�세???��????�들?? API ???�정???�인?�주�??��? ?��?�????�결책을 줄게."
        
    return "?�재 ?�스???�결???�활?��? ?�거??API ?��? ?�정?��? ?�았?�니?? API ???�정???�인?�거???�시 ???�시 ?�도?�주?�요."

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available. API key may be missing.")
        return generate_dynamic_fallback(message)
    
    try:
        knowledge = get_expert_knowledge()
        # ?�큰 ?�약: 지??베이?��? 30,000?�로 ?�한 (무료 API ?�당??보호)
        if len(knowledge) > 30000:
            knowledge = knowledge[:30000] + "\n\n[... 지??베이???�머지 ?�략 (?�큰 ?�약) ...]"
        
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
            for msg_item in history[-10:]:  # 최근 10?�으�?줄여 ?�큰 ?�약
                role = 'user' if msg_item.get('role') == 'user' else 'model'
                text = msg_item.get('content', '')
                if text.strip():
                    contents.append({'role': role, 'parts': [{'text': text}]})
        contents.append({'role': 'user', 'parts': [{'text': message}]})
        
        # 429 ?�러 ???�시??(최�? 3?? 지??백오??
        import time
        last_error = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
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
                    wait = (attempt + 1) * 5  # 5�? 10�??��?                    print(f"CHATBOT 429 RATE LIMIT: attempt {attempt+1}/3, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                print(f"CHATBOT API ERROR (status={status}, attempt={attempt+1}): {api_err}")
                break
        
        if last_error:
            status = getattr(last_error, 'status_code', 0)
            if status == 429:
                return "지�?AI ?�버가 ?�청??많아???�시 ?�고 ?�어. 1~2�??�에 ?�시 �?걸어�? 그동???�늘 기출 1문제?�도 ?�놓�??�색?�봐."
            return generate_dynamic_fallback(message)
        return generate_dynamic_fallback(message)
        
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR ({type(e).__name__}): {e}")
        import traceback
        traceback.print_exc()
        return generate_dynamic_fallback(message)


# --- ?�어 / ?�국???�급 ?�동 계산 모듈 ---

def get_english_grade(score: int) -> int:
    """?�어 ?��??��? ?�급 변??(90???�상 1?�급, 80???�상 2?�급...)"""
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
    """?�국???��??��? ?�급 변??(40???�상 1?�급, 35???�상 2?�급...)"""
    if score >= 40: return 1
    elif score >= 35: return 2
    elif score >= 30: return 3
    elif score >= 25: return 4
    elif score >= 20: return 5
    elif score >= 15: return 6
    elif score >= 10: return 7
    elif score >= 5: return 8
    return 9


# --- ?�격 ?�측 ?�고리즘 (?�정) ---

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
            science_keywords = ["공학", "?�학", "?�물", "?�학", "물리", "?�예", "치의", "?�학", "?�의", "간호", "컴퓨??, "IT", "과학", "?�프?�웨??, "기계", "?�기", "?�자", "?�소??, "??��", "?�연", "바이??, "?�스??, "?�합"]
            for kw in science_keywords:
                if kw in department_name:
                    is_science = True
                    break
            
            chosen_key = "?�과" if is_science else "문과"
            if chosen_key in target_cuts_dict:
                target_cuts = target_cuts_dict[chosen_key]
                target_cuts["계열"] = chosen_key
            else:
                target_cuts = list(target_cuts_dict.values())[0]
                target_cuts["계열"] = list(target_cuts_dict.keys())[0]
                
    if not target_cuts:
        target_cuts = {
            "?�정?�백": 15.0,
            "?�상?�백": 20.0,
            "?�신?�백": 25.0,
            "계열": "?�과"
        }
        
    ?�정 = target_cuts.get("?�정?�백")
    ?�상 = target_cuts.get("?�상?�백")
    ?�신 = target_cuts.get("?�신?�백")
    
    if ?�정 is None: ?�정 = 15.0
    if ?�상 is None: ?�상 = 20.0
    if ?�신 is None: ?�신 = 25.0
    
    # --- ?�시 (Jeongsi) ?�정 �?미달 % 계산 (?�수???�는 ?�수) ---
    target_cutoff_pct = round(100.0 - ?�정)
    pct_diff = round(mock_avg - target_cutoff_pct)
    
    if student_nuback <= ?�정 - 5.0:
        jeongsi_tier = "?�향"
    elif student_nuback <= ?�정:
        jeongsi_tier = "?�정"
    elif student_nuback <= ?�상:
        jeongsi_tier = "?�정"
    elif student_nuback <= ?�신:
        jeongsi_tier = "?�신"
    else:
        jeongsi_tier = "?�향"

    if pct_diff >= 0:
        jeongsi_tip = f"목표 ?�???�격???��?백분??+{pct_diff}%p ?�유 (?�정/?�정 지?�권)"
    else:
        jeongsi_tip = f"목표 ?�???�격???��?백분??{pct_diff}%p 미달 (?�향 지?�권)"

    if eng_grade >= 3 or hist_grade >= 4:
        tier_downgrade = {"?�향": "?�정", "?�정": "?�정", "?�정": "?�신", "?�신": "?�향", "?�향": "?�향"}
        old_tier = jeongsi_tier
        jeongsi_tier = tier_downgrade.get(jeongsi_tier, "?�향")
        jeongsi_tip += f" [?�어/?�국??감점 반영: {old_tier} ??{jeongsi_tier}]"

    # --- ?�시 (Susi) ?�정 �??�급 미달 계산 ---
    gpa_cut = 2.0
    if ?�신 < 2.0:
        gpa_cut = 1.3
    elif ?�신 < 10.0:
        gpa_cut = 1.8
    elif ?�신 < 25.0:
        gpa_cut = 2.5
    else:
        gpa_cut = 3.5
        
    gpa_diff = round(gpa_cut - gpa, 1)
    if gpa_diff >= 0.5:
        susi_tier = "?�향"
    elif gpa_diff >= 0.1:
        susi_tier = "?�정"
    elif gpa_diff >= -0.2:
        susi_tier = "?�정"
    elif gpa_diff >= -0.5:
        susi_tier = "?�신"
    else:
        susi_tier = "?�향"

    if gpa_diff >= 0:
        susi_tip = f"목표 ?�격 ?�신({gpa_cut}?�급) ?��?+{gpa_diff}?�급 ?�수 (?�정 지?�권)"
    else:
        susi_tip = f"목표 ?�격 ?�신({gpa_cut}?�급) ?��?{abs(gpa_diff):.1f}?�급 미달 (?�향 지?�권)"

    if mock_avg < (100.0 - ?�신) - 8:
        tier_downgrade = {"?�향": "?�정", "?�정": "?�정", "?�정": "?�신", "?�신": "?�향", "?�향": "?�향"}
        old_susi = susi_tier
        susi_tier = tier_downgrade.get(susi_tier, "?�향")
        susi_tip += f" [?�능 최�? 미달 가?�성 주의: {old_susi} ??{susi_tier}]"

    client = get_gemini_client()
    if client:
        try:
            prompt = (
                f"?�신?� ?�시 컨설?�트?�니?? ?�음 ?�생??개별 ?�적 진단 결과???�???�시?�략�??�시?�략???�우르는 ?�드�?1문장??각각 ?�성?�주?�요.\n"
                f"?�생 ?�적 - ?�신: {gpa}?�급, 모의고사 ?�균백분?? {mock_avg:.1f} (�?��:{kor_pct}, ?�학:{math_pct}, ?�어:{eng_grade}?�급, ?�구1:{tam1_pct}, ?�구2:{tam2_pct}, ?�국??{hist_grade}?�급)\n"
                f"지?��??? {university_name} {department_name} (?�신컷�?�? {gpa_cut}, ?�시백분?�컷?��? {100.0-?�정})\n"
                f"?�시 진단 ?�급: {susi_tier}, ?�시 진단 ?�급: {jeongsi_tier}\n"
                f"?�구?�항: 존댓말로 ?�생?�게 조언?�듯??부?�럽지�??�문?�으�??�시??조언 1문장, ?�시??조언 1문장??JSON ?�식?�로 출력?�주?�요.\n"
                f"?�시 ?�식: {{\"susi_comment\": \"?�시 조언...\", \"jeongsi_comment\": \"?�시 조언...\"}}"
            )
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            text_cleaned = response.text.strip().replace("```json", "").replace("```", "")
            ai_data = json.loads(text_cleaned)
            if "susi_comment" in ai_data:
                susi_tip += f" (AI ?�시 ?�략: {ai_data['susi_comment']})"
            if "jeongsi_comment" in ai_data:
                jeongsi_tip += f" (AI ?�시 ?�략: {ai_data['jeongsi_comment']})"
        except Exception:
            pass

    return {
        "susi": {
            "university": f"{university_name} {department_name} (?�시)",
            "result_tier": susi_tier,
            "tip": susi_tip
        },
        "jeongsi": {
            "university": f"{university_name} {department_name} (?�시)",
            "result_tier": jeongsi_tier,
            "tip": jeongsi_tip
        }
    }
