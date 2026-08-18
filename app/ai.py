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
    return ""

def generate_dynamic_fallback(msg: str) -> str:
    m = msg.strip().lower()
    if any(k in m for k in ["\uc548\ub155", "\ubc18\uac00\uc6cc", "\ud558\uc774", "\ucc98\uc74c"]):
        return "\uc5b4 \uadf8\ub798, \ubc18\uac11\ub2e4! \uc9c0\uae08\uc740 AI \uc11c\ubc84\uc640 \uc5f0\uacb0\uc774 \ubd88\uc548\uc815\ud574\uc11c \uae34 \uc0c1\ub2f4\uc740 \uc5b4\ub835\ub124. API \ud0a4 \uc124\uc815\uc774 \uc81c\ub300\ub85c \ub418\uc5b4 \uc788\ub294\uc9c0 \ud655\uc778\ud574\ubcf4\uace0 \ub2e4\uc2dc \ub9d0 \uac78\uc5b4\uc918."
    if any(k in m for k in ["\uace0\ubbfc", "\ud798\ub4e4", "\uc0c1\ub2f4"]):
        return "\ub124 \uace0\ubbfc\uc744 \uae4a\uac8c \ub4e4\uc5b4\uc8fc\uace0 \uc2f6\uc740\ub370, \ud604\uc7ac AI \uc11c\ubc84 \uc5f0\uacb0 \ubb38\uc81c\ub85c \uc790\uc138\ud55c \ub2f5\ubcc0\uc774 \ud798\ub4e4\uc5b4. API \ud0a4 \uc124\uc815\uc744 \ud655\uc778\ud574\uc8fc\uba74 \ub0b4\uac00 \uc81c\ub300\ub85c \ub41c \ud574\uacb0\ucc45\uc744 \uc904\uac8c."
    return "\ud604\uc7ac \uc2dc\uc2a4\ud15c \uc5f0\uacb0\uc774 \uc6d0\ud65c\ud558\uc9c0 \uc54a\uac70\ub098 API \ud0a4\uac00 \uc124\uc815\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4. API \ud0a4 \uc124\uc815\uc744 \ud655\uc778\ud558\uac70\ub098 \uc7a0\uc2dc \ud6c4 \ub2e4\uc2dc \uc2dc\ub3c4\ud574\uc8fc\uc138\uc694."

def ask_ai_chatbot(message: str, history: list = None) -> str:
    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available. API key may be missing.")
        return generate_dynamic_fallback(message)
    
    try:
        knowledge = get_expert_knowledge()
        if len(knowledge) > 30000:
            knowledge = knowledge[:30000] + "\n\n[... knowledge base truncated for token savings ...]"
        
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
            "=== KNOWLEDGE BASE ===\n"
            "Use this knowledge base to find relevant insights for the student's specific situation. "
            "Do not copy-paste from it. Reinterpret and adapt the content naturally.\n\n"
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
                return "\uc9c0\uae08 AI \uc11c\ubc84\uac00 \uc694\uccad\uc774 \ub9ce\uc544\uc11c \uc7a0\uc2dc \uc26c\uace0 \uc788\uc5b4. 1~2\ubd84 \ub4a4\uc5d0 \ub2e4\uc2dc \ub9d0 \uac78\uc5b4\uc918. \uadf8\ub3d9\uc548 \uc624\ub298 \uae30\ucd9c 1\ubb38\uc81c\ub77c\ub3c4 \ud3b4\ub193\uace0 \uc0ac\uc0c9\ud574\ubd10."
            return generate_dynamic_fallback(message)
        return generate_dynamic_fallback(message)
        
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR ({type(e).__name__}): {e}")
        import traceback
        traceback.print_exc()
        return generate_dynamic_fallback(message)


# --- English / History grade conversion ---

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


# --- Admission prediction ---

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
            target_cuts["\uacc4\uc5f4"] = list(target_cuts_dict.keys())[0]
        else:
            is_science = False
            science_keywords = ["\uacf5\ud559", "\ud654\ud559", "\uc0dd\ubb3c", "\uc218\ud559", "\ubb3c\ub9ac", "\uc758\uc608", "\uce58\uc758", "\uc57d\ud559", "\ud55c\uc758", "\uac04\ud638", "\ucef4\ud4e8\ud130", "IT", "\uacfc\ud559", "\uc18c\ud504\ud2b8\uc6e8\uc5b4", "\uae30\uacc4", "\uc804\uae30", "\uc804\uc790", "\uc2e0\uc18c\uc7ac", "\ud56d\uacf5", "\uc790\uc5f0", "\ubc14\uc774\uc624", "\uc2dc\uc2a4\ud15c", "\uc735\ud569"]
            for kw in science_keywords:
                if kw in department_name:
                    is_science = True
                    break
            chosen_key = "\uc774\uacfc" if is_science else "\ubb38\uacfc"
            if chosen_key in target_cuts_dict:
                target_cuts = target_cuts_dict[chosen_key]
                target_cuts["\uacc4\uc5f4"] = chosen_key
            else:
                target_cuts = list(target_cuts_dict.values())[0]
                target_cuts["\uacc4\uc5f4"] = list(target_cuts_dict.keys())[0]
                
    if not target_cuts:
        target_cuts = {"\uc801\uc815\ub204\ubc31": 15.0, "\uc608\uc0c1\ub204\ubc31": 20.0, "\uc18c\uc2e0\ub204\ubc31": 25.0, "\uacc4\uc5f4": "\uc774\uacfc"}
        
    jeokjeong = target_cuts.get("\uc801\uc815\ub204\ubc31", 15.0)
    yesang = target_cuts.get("\uc608\uc0c1\ub204\ubc31", 20.0)
    sosin = target_cuts.get("\uc18c\uc2e0\ub204\ubc31", 25.0)
    
    target_cutoff_pct = round(100.0 - jeokjeong)
    pct_diff = round(mock_avg - target_cutoff_pct)
    
    if student_nuback <= jeokjeong - 5.0:
        jeongsi_tier = "\ud558\ud5a5"
    elif student_nuback <= jeokjeong:
        jeongsi_tier = "\uc548\uc815"
    elif student_nuback <= yesang:
        jeongsi_tier = "\uc801\uc815"
    elif student_nuback <= sosin:
        jeongsi_tier = "\uc18c\uc2e0"
    else:
        jeongsi_tier = "\uc0c1\ud5a5"

    if pct_diff >= 0:
        jeongsi_tip = f"\ubaa9\ud45c \ub300\ud559 \ud569\uaca9\uc120 \ub300\ube44 \ubc31\ubd84\uc704 +{pct_diff}%p \uc5ec\uc720 (\uc548\uc815/\uc801\uc815 \uc9c0\uc6d0\uad8c)"
    else:
        jeongsi_tip = f"\ubaa9\ud45c \ub300\ud559 \ud569\uaca9\uc120 \ub300\ube44 \ubc31\ubd84\uc704 {pct_diff}%p \ubbf8\ub2ec (\uc0c1\ud5a5 \uc9c0\uc6d0\uad8c)"

    if eng_grade >= 3 or hist_grade >= 4:
        tier_downgrade = {"\ud558\ud5a5": "\uc548\uc815", "\uc548\uc815": "\uc801\uc815", "\uc801\uc815": "\uc18c\uc2e0", "\uc18c\uc2e0": "\uc0c1\ud5a5", "\uc0c1\ud5a5": "\uc0c1\ud5a5"}
        old_tier = jeongsi_tier
        jeongsi_tier = tier_downgrade.get(jeongsi_tier, "\uc0c1\ud5a5")
        jeongsi_tip += f" [\uc601\uc5b4/\ud55c\uad6d\uc0ac \uac10\uc810 \ubc18\uc601: {old_tier} -> {jeongsi_tier}]"

    gpa_cut = 2.0
    if sosin < 2.0: gpa_cut = 1.3
    elif sosin < 10.0: gpa_cut = 1.8
    elif sosin < 25.0: gpa_cut = 2.5
    else: gpa_cut = 3.5
        
    gpa_diff = round(gpa_cut - gpa, 1)
    if gpa_diff >= 0.5: susi_tier = "\ud558\ud5a5"
    elif gpa_diff >= 0.1: susi_tier = "\uc548\uc815"
    elif gpa_diff >= -0.2: susi_tier = "\uc801\uc815"
    elif gpa_diff >= -0.5: susi_tier = "\uc18c\uc2e0"
    else: susi_tier = "\uc0c1\ud5a5"

    if gpa_diff >= 0:
        susi_tip = f"\ubaa9\ud45c \ud569\uaca9 \ub0b4\uc2e0({gpa_cut}\ub4f1\uae09) \ub300\ube44 +{gpa_diff}\ub4f1\uae09 \uc6b0\uc218 (\uc548\uc815 \uc9c0\uc6d0\uad8c)"
    else:
        susi_tip = f"\ubaa9\ud45c \ud569\uaca9 \ub0b4\uc2e0({gpa_cut}\ub4f1\uae09) \ub300\ube44 {abs(gpa_diff):.1f}\ub4f1\uae09 \ubbf8\ub2ec (\uc0c1\ud5a5 \uc9c0\uc6d0\uad8c)"

    if mock_avg < (100.0 - sosin) - 8:
        tier_downgrade2 = {"\ud558\ud5a5": "\uc548\uc815", "\uc548\uc815": "\uc801\uc815", "\uc801\uc815": "\uc18c\uc2e0", "\uc18c\uc2e0": "\uc0c1\ud5a5", "\uc0c1\ud5a5": "\uc0c1\ud5a5"}
        old_susi = susi_tier
        susi_tier = tier_downgrade2.get(susi_tier, "\uc0c1\ud5a5")
        susi_tip += f" [\uc218\ub2a5 \ucd5c\uc800 \ubbf8\ub2ec \uac00\ub2a5\uc131 \uc8fc\uc758: {old_susi} -> {susi_tier}]"

    client = get_gemini_client()
    if client:
        try:
            prompt = (
                f"You are an admission consultant. Respond in Korean.\n"
                f"Student scores - GPA: {gpa}, Avg percentile: {mock_avg:.1f} (Kor:{kor_pct}, Math:{math_pct}, Eng grade:{eng_grade}, Tam1:{tam1_pct}, Tam2:{tam2_pct}, History grade:{hist_grade})\n"
                f"Target: {university_name} {department_name}\n"
                f"Susi tier: {susi_tier}, Jeongsi tier: {jeongsi_tier}\n"
                f'Give 1 sentence advice each for susi and jeongsi in JSON: {{"susi_comment": "...", "jeongsi_comment": "..."}}'
            )
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            text_cleaned = response.text.strip().replace("```json", "").replace("```", "")
            ai_data = json.loads(text_cleaned)
            if "susi_comment" in ai_data:
                susi_tip += f" (AI: {ai_data['susi_comment']})"
            if "jeongsi_comment" in ai_data:
                jeongsi_tip += f" (AI: {ai_data['jeongsi_comment']})"
        except Exception:
            pass

    return {
        "susi": {
            "university": f"{university_name} {department_name} (susi)",
            "result_tier": susi_tier,
            "tip": susi_tip
        },
        "jeongsi": {
            "university": f"{university_name} {department_name} (jeongsi)",
            "result_tier": jeongsi_tier,
            "tip": jeongsi_tip
        }
    }
