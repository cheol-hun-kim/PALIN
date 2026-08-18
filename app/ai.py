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

# --- Context Caching Manager ---
_KNOWLEDGE_CACHE_NAME = None
_KNOWLEDGE_CACHE_EXPIRES = 0

def get_knowledge_cache(client):
    global _KNOWLEDGE_CACHE_NAME, _KNOWLEDGE_CACHE_EXPIRES
    now = time.time()
    if _KNOWLEDGE_CACHE_NAME and now < _KNOWLEDGE_CACHE_EXPIRES:
        return _KNOWLEDGE_CACHE_NAME
    knowledge = get_expert_knowledge()
    if not knowledge or len(knowledge) < 100:
        return None
    system_instruction_with_knowledge = (
        "You are PALIN BOT, the AI mentor based on Kim Chul-Hun. Respond ONLY in Korean.\n\n"
        "IDENTITY: You are Kim Chul-Hun himself - a 13-year veteran CSAT Korean instructor and director of Ilwon Academy in Bundang. You personally failed the CSAT twice before succeeding on your third attempt. Speak directly from your own personal memories, philosophy, and real-world student counseling experience.\n\n"
        "=== ABSOLUTE PRIORITY RULES (CRITICAL) ===\n"
        "RULE 1 - NO MARKDOWN AT ALL: NEVER use markdown formatting syntax like '#', '##', '###', '**', '*', '-', or numbered lists ('1.', '2.'). Write ONLY in clean, plain conversational Korean text with normal paragraph breaks.\n"
        "RULE 2 - NO MENTION OF BOOKS OR EXTERNAL DOCUMENTS: NEVER mention 'the book', 'Principles of Failure', or 'as written in the document'. NEVER refer to your knowledge as a book or file. Speak as if all these insights are YOUR OWN personal experience, wisdom, and direct advice.\n"
        "RULE 3 - CONTEXT IS KING: Read the student message carefully. Respond directly and naturally to THAT specific topic. No pre-scripted avoidance.\n"
        "RULE 4 - NO AI CLICHES: Never say 'What can I help you with?', 'Great question!', 'As an AI...'. Talk like a real, direct, caring mentor in a face-to-face chat.\n\n"
        "=== VOICE & TONE ===\n"
        "Use confident, direct, caring banmal (casual speech: ~haera, ~haja, ~iya, ~geodeun, ~janha).\n"
        "Be like a tough but deeply caring mentor/older brother.\n"
        "When the student shares struggles, show real empathy first, then deliver direct truth and practical solutions.\n\n"
        "=== EXPERT KNOWLEDGE (Your Personal Wisdom & Philosophy) ===\n"
        "Below is your entire lifetime of CSAT coaching wisdom and personal experience. Integrate these exact facts into your answers naturally as your own words.\n\n"
        f"{knowledge}\n"
    )
    try:
        from google.genai import types
        cache = client.caches.create(
            model='gemini-3.6-flash',
            config=types.CreateCachedContentConfig(
                contents=[system_instruction_with_knowledge],
                ttl='86400s',
            )
        )
        _KNOWLEDGE_CACHE_NAME = cache.name
        _KNOWLEDGE_CACHE_EXPIRES = now + 80000
        print(f"CHATBOT CACHE CREATED SUCCESS: {cache.name}")
        return _KNOWLEDGE_CACHE_NAME
    except Exception as e:
        print(f"CHATBOT CACHE CREATE ERROR: {e}")
        return None

def generate_dynamic_fallback(msg: str) -> str:
    m = msg.strip().lower()
    if any(k in m for k in ["\uc548\ub155", "\ubc18\uac00\uc6cc", "\ud558\uc774", "\ucc98\uc74c"]):
        return "\uc5b4 \uadf8\ub798, \ubc18\uac11\ub2e4! \uc9c0\uae08\uc740 AI \uc11c\ubc84\uc640 \uc5f0\uacb0\uc774 \ubd88\uc548\uc815\ud574\uc11c \uae34 \uc0c1\ub2f4\uc740 \uc5b4\ub835\ub124. API \ud0a4 \uc124\uc815\uc744 \ud655\uc778\ud574\ubcf4\uace0 \ub2e4\uc2dc \ub9d0 \uac78\uc5b4\uc918."
    if any(k in m for k in ["\uace0\ubbfc", "\ud798\ub4e4", "\uc0c1\ub2f4"]):
        return "\ub124 \uace0\ubbfc\uc744 \uae4a\uac8c \ub4e4\uc5b4\uc8fc\uace0 \uc2f6\uc740\ub370, \ud604\uc7ac AI \uc11c\ubc84 \uc5f0\uacb0 \ubb38\uc81c\ub85c \uc790\uc138\ud55c \ub2f5\ubcc0\uc774 \ud798\ub4e4\uc5b4. API \ud0a4 \uc124\uc815\uc744 \ud655\uc778\ud574\uc8fc\uba74 \ub0b4\uac00 \uc81c\ub300\ub85c \ub41c \ud574\uacb0\ucc45\uc744 \uc904\uac8c."
    return "\ud604\uc7ac \uc2dc\uc2a4\ud15c \uc5f0\uacb0\uc774 \uc6d0\ud65c\ud558\uc9c0 \uc54a\uac70\ub098 API \ud0a4\uac00 \uc124\uc815\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4. \uc7a0\uc2dc \ud6c4 \ub2e4\uc2dc \uc2dc\ud3c4\ud574\uc8fc\uc138\uc694."

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available.")
        return generate_dynamic_fallback(message)
    try:
        cache_name = get_knowledge_cache(client)
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
        import time
        last_error = None
        for attempt in range(3):
            try:
                if cache_name:
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents,
                        config={
                            'cached_content': cache_name,
                            'temperature': 0.6,
                            'max_output_tokens': 4000,
                        }
                    )
                else:
                    knowledge = get_expert_knowledge()[:20000]
                    system_prompt = 'You are Kim Chul-Hun (PALIN BOT). Do NOT use markdown. Do NOT mention books. Speak as yourself in Korean.\n\n' + knowledge
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
                    # Clean up any leftover markdown formatting if the model slipped
                    cleaned = result_text.replace('###', '').replace('##', '').replace('#', '').replace('**', '').replace('* ', '')
                    return cleaned
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
                return "\uc9c0\uae08 AI \uc11c\ubc84\uac00 \uc694\uccad\uc774 \ub9ce\uc544\uc11c \uc7a0\uc2dc \uc26c\uace0 \uc788\uc5b4. 1~2\ubd84 \ub4a4\uc5d0 \ub2e4\uc2dc \ub9d0 \uac78\uc5b4\uc918."
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
