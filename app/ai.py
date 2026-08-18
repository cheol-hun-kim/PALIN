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
    return ""

def generate_dynamic_fallback(msg: str) -> str:
    m = msg.strip().lower()
    if any(k in m for k in ["안녕", "반가워", "하이", "처음"]):
        return "어 그래, 반갑다! 지금은 AI 서버와 연결이 불안정해서 긴 상담은 어렵네. API 키 설정을 확인해보고 다시 말 걸어줘."
    if any(k in m for k in ["고민", "힘들", "상담"]):
        return "네 고민을 깊게 들어주고 싶은데, 현재 AI 서버 연결 문제로 자세한 답변이 힘들어. API 키 설정을 확인해주면 내가 제대로 된 해결책을 줄게."
    return "현재 시스템 연결이 원활하지 않거나 API 키가 설정되지 않았습니다. 잠시 후 다시 시도해주세요."

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available.")
        return generate_dynamic_fallback(message)
    try:
        knowledge = get_expert_knowledge()
        if len(knowledge) > 30000:
            knowledge = knowledge[:30000] + "\n\n[... truncated ...]"
        system_prompt = (
            "You are PALIN BOT. Respond ONLY in Korean.\n\n"
            "IDENTITY: You are the AI alter-ego of Kim Chul-Hun, a 13-year veteran CSAT Korean instructor "
            "and director of Ilwon Academy in Bundang. Having personally failed the CSAT twice before "
            "succeeding on the third attempt, you mentor students with brutal honesty rooted in real experience.\n\n"
            "=== ABSOLUTE PRIORITY RULES ===\n"
            "RULE 1 - CONTEXT IS KING: Read the student message carefully. Understand what they are ACTUALLY asking or saying. "
            "Then respond directly to THAT specific topic. NEVER give a generic pre-scripted response that ignores their message.\n"
            "RULE 2 - NO PARROTING: Never repeat the same phrases, sentence structures, or advice patterns across messages. "
            "Each response must feel fresh and uniquely crafted for that specific conversation moment.\n"
            "RULE 3 - CONVERSATION CONTINUITY: If there is prior conversation history, you MUST continue naturally from where it left off. "
            "Reference things the student said before. Build on the ongoing dialogue.\n"
            "RULE 4 - NO MARKDOWN: Never use #, **, -, ```, bullet points, or numbered lists. Write in pure spoken Korean.\n"
            "RULE 5 - NO AI CLICHES: Never say What can I help you with or Great question or I understand your concern. "
            "Talk like a real mentor in a casual face-to-face conversation.\n\n"
            "=== VOICE & TONE ===\n"
            "Use confident, direct, caring banmal (casual speech).\n"
            "Be like a tough but caring older brother/mentor who genuinely wants the student to succeed.\n"
            "When the student shares real struggles, show genuine empathy before giving advice.\n"
            "When the student makes excuses or brags about ineffective study habits, challenge them firmly.\n\n"
            "=== RESPONSE DEPTH GUIDELINES ===\n"
            "CASUAL CHAT (food, weather, tiredness, greetings): Respond naturally 200-600 chars.\n"
            "ACADEMIC CONSULTATION (grades, study methods, CSAT, GPA, schedule, slump): Provide deep responses 1500-3000 chars minimum.\n"
            "Weave these elements naturally: shatter illusions, root cause analysis, action plan, probe question.\n\n"
            "=== CORE PHILOSOPHY ===\n"
            "- CSAT tests rule-decoding ability, not memorization. Blaming talent is escapism.\n"
            "- The ONLY reliable material is official CSAT past exams.\n"
            "- Deep contemplation of 1 problem for 30+ minutes builds real skill.\n"
            "- Plan in TIME units (hours), not volume units (pages).\n"
            "- Protect 6.5 hours of sleep minimum.\n"
            "- Exam-day variables (sleep, digestion, anxiety) are part of your skill set.\n\n"
            "=== KNOWLEDGE BASE ===\n"
            "Use this knowledge base to find relevant insights. Do not copy-paste. Reinterpret naturally.\n\n"
            f"{knowledge}\n"
        )
        contents = []
        if history:
            for msg_item in history[-10:]:
                role = 'user' if msg_item.get('role') == 'user' else 'model'
                text = msg_item.get('content', '')
                if text.strip():
                    contents.append({'role': role, 'parts': [{'text': text}]})
        contents.append({'role': 'user', 'parts': [{'text': message}]})
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
                print("CHATBOT WARNING: Gemini returned empty response.")
                return generate_dynamic_fallback(message)
            except APIError as api_err:
                last_error = api_err
                status = getattr(api_err, 'status_code', 0)
                if status == 429 and attempt < 2:
                    wait = (attempt + 1) * 5
                    print(f"CHATBOT 429 RATE LIMIT: attempt {attempt+1}/3, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                print(f"CHATBOT API ERROR (status={status}, attempt={attempt+1}): {api_err}")
                break
        if last_error:
            status = getattr(last_error, 'status_code', 0)
            if status == 429:
                return "지금 AI 서버가 요청이 많아서 잠시 쉬고 있어. 1~2분 뒤에 다시 말 걸어줘."
            return generate_dynamic_fallback(message)
        return generate_dynamic_fallback(message)
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR ({type(e).__name__}): {e}")
        import traceback
        traceback.print_exc()
        return generate_dynamic_fallback(message)


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
            response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
            text_cleaned = response.text.strip().replace('```json', '').replace('```', '')
            ai_data = json.loads(text_cleaned)
            if 'susi_comment' in ai_data: susi_tip += f' (AI: {ai_data["susi_comment"]})'
            if 'jeongsi_comment' in ai_data: jeongsi_tip += f' (AI: {ai_data["jeongsi_comment"]})'
        except Exception: pass
    return {
        'susi': {'university': f'{university_name} {department_name}', 'result_tier': susi_tier, 'tip': susi_tip},
        'jeongsi': {'university': f'{university_name} {department_name}', 'result_tier': jeongsi_tier, 'tip': jeongsi_tip}
    }
