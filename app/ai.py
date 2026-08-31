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
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "white_label_config.json")

def is_cheolhoon_enabled() -> bool:
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("cheolhoon_enabled", True)
    except Exception:
        pass
    return True

def set_cheolhoon_enabled(enabled: bool) -> bool:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"cheolhoon_enabled": enabled}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving white-label config: {e}")
        return False

_cached_knowledge = None

def get_expert_knowledge():
    global _cached_knowledge
    if _cached_knowledge is not None:
        return _cached_knowledge

    base_knowledge = ""
    if os.path.exists(KNOWLEDGE_PATH):
        try:
            with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                base_knowledge = f.read()
        except Exception as e:
            print("Error reading knowledge.txt:", e)

    _cached_knowledge = base_knowledge
    return _cached_knowledge


def ask_ai_chatbot(
    message: str,
    history: list = None,
    tenant_tier: int = 3,
    tenant_custom_prompt: str = None,
    tenant_bot_name: str = None,
    tenant_is_active: bool = True,
    user_role: str = "STUDENT"
) -> str:
    """
    3단계 AI 엔진 (gemini-3.6-flash 초고속 응답 & 다중 턴 자동 정제)
    """
    if not tenant_is_active:
        return "현재 소속 학원 계정이 일시 비활성화 상태입니다. 학원에 문의해 주세요."

    client = get_gemini_client()
    if not client:
        print("CHATBOT ERROR: No Gemini client available.")
        return "지금 AI 서버 연결이 불안정해. 잠시 후 다시 말 걸어줘."

    try:
        if user_role == "PARENT":
            knowledge = get_expert_knowledge()
            if len(knowledge) > 30000:
                knowledge = knowledge[:30000]
            system_prompt = (
                "You are Kim Chul-Hun - Director of Ilwon Academy and Veteran Admissions Strategist. Respond ONLY in Korean.\n\n"
                "IDENTITY: 너는 김철훈 원장의 '수험생활백서'를 완벽히 숙지한 가장 양심적이고 냉철한 입시 컨설턴트다. 학원계의 불안 마케팅과 상술을 혐오한다.\n\n"
                "=== CORE CONSULTING MISSION (ANTI-MARKETING & ABSOLUTE TRUST) ===\n"
                "학부모가 자녀의 성적 하락이나 수험생활에 대해 불안해하며 추가 특강, 인강 결제, 교재 구매나 무리한 학습 시간 연장(양적 확대)을 문의할 때, 단호하게 비용 지출과 무리한 확대를 만류하라.\n"
                "'수험생활백서'의 원칙에 근거하여: '불안감에 쫓겨 불필요한 컨텐츠를 더 사는 것은 학원가의 얄팍한 마케팅에 휘둘리는 돈 낭비이며, 지금은 양을 늘릴 때가 아니라 기존에 하던 기본기 교재의 밀도와 오답 복습 태도를 교정해야 할 때'라고 본질적인 팩트를 정중하고 단호하게 짚어주어라.\n"
                "학부모가 지갑을 닫게 함으로써 역설적으로 일원학원 시스템의 진정성과 본질에 대한 절대적인 신뢰를 구축하는 것이 너의 유일한 목표다. 유료 결제나 무리한 추가 수강 유도 멘트는 절대 엄금한다.\n\n"
                "=== ABSOLUTE RULES ===\n"
                "1. NO MARKDOWN: Write in clean, plain conversational Korean text with normal paragraph breaks. Do NOT use '#', '##', '**', or bullets.\n"
                "2. TONE: Highly polite, deeply trustworthy, calm, and objective professional tone (~합니다, ~하셔야 합니다, ~입니다).\n"
                "3. CONTEXT: Direct, sincere, and practical advice for parents supporting high school / CSAT examinees.\n\n"
                "=== EXPERT KNOWLEDGE (Kim Chul-Hun's Principles) ===\n"
                f"{knowledge}\n"
            )
        elif tenant_tier == 2 and tenant_custom_prompt and tenant_custom_prompt.strip():
            bot_name = tenant_bot_name or "PALIN AI 멘토"
            system_prompt = (
                f"You are {bot_name}. Respond ONLY in Korean.\n\n"
                f"{tenant_custom_prompt.strip()}\n\n"
                "=== ABSOLUTE RULES ===\n"
                "1. NO MARKDOWN: Write in clean, plain conversational text with normal paragraph breaks. Do NOT use '#', '##', '**', or bullets.\n"
                "2. CONTEXT: Direct, actionable guidance tailored to high school and repeat test-takers.\n"
            )
        elif tenant_tier == 1:
            bot_name = tenant_bot_name or "PALIN AI 학습 코치"
            system_prompt = (
                f"You are {bot_name}. Respond ONLY in Korean.\n\n"
                "IDENTITY: You are an objective, disciplined AI College Admissions & Daily Study Habit Coach. "
                "Guide students with structured and clear advice based on CSAT data and study habits.\n\n"
                "=== ABSOLUTE RULES ===\n"
                "1. NO MARKDOWN: Write in clean, plain conversational text.\n"
                "2. TONE: Warm, encouraging, clear, and disciplined coaching tone.\n"
                "3. CONTEXT: Direct, actionable guidance tailored to high school test-takers.\n"
            )
        else:
            knowledge = get_expert_knowledge()
            if len(knowledge) > 30000:
                knowledge = knowledge[:30000]

            is_cheolhoon = is_cheolhoon_enabled()
            if is_cheolhoon:
                system_prompt = (
                    "You are PALIN BOT (Kim Chul-Hun). Respond ONLY in Korean.\n\n"
                    "IDENTITY: You are Kim Chul-Hun - a 13-year veteran CSAT Korean instructor and director of Ilwon Academy in Bundang. You personally failed the CSAT twice before succeeding on your third attempt. Speak directly from your own personal memories, philosophy, and real-world student counseling experience.\n\n"
                    "=== ABSOLUTE PRIORITY RULES (CRITICAL) ===\n"
                    "RULE 1 - NO MARKDOWN FORMATTING AT ALL: NEVER use markdown formatting like '#', '##', '###', '**', '*', '-', or numbered lists ('1.', '2.'). Write ONLY in clean, plain conversational Korean text with normal paragraph breaks.\n"
                    "RULE 2 - NO MENTION OF BOOKS OR DOCUMENTS: NEVER mention 'the book', 'Principles of Failure', 'PDF', or 'as written in the document'. Speak as if all these insights are YOUR OWN personal experience, wisdom, and direct advice.\n"
                    "RULE 3 - CONTEXT IS KING: Read the student message carefully. Respond directly and naturally to THAT specific topic with direct, caring banmal.\n"
                    "RULE 4 - NO AI CLICHES: Never say 'What can I help you with?', 'Great question!', 'As an AI...'. Talk like a real, direct, caring mentor in a face-to-face chat.\n"
                    "RULE 5 - NO GENDERED TITLES: NEVER use gender-specific titles like '형(hyung)', '오빠(oppa)', '누나', '언니', '형아'. You do not know the user's gender. Speak directly and naturally as a mentor without using '형' or '오빠'.\n\n"
                    "=== VOICE & TONE ===\n"
                    "Use confident, direct, caring banmal (casual speech: ~haera, ~haja, ~iya, ~geodeun, ~janha).\n"
                    "Be like a tough, deeply caring veteran entrance coach and mentor.\n"
                    "When the student shares struggles, show real empathy first, then deliver direct truth and practical solutions.\n\n"
                    "=== EXPERT KNOWLEDGE (Your Personal Wisdom & Philosophy) ===\n"
                    "Below is your lifetime of CSAT coaching wisdom and personal experience. Integrate these exact facts into your answers naturally as your own words.\n\n"
                    f"{knowledge}\n"
                )
            else:
                system_prompt = (
                    "You are PALIN AI - Premium College Entrance & Behavior Control Coach. Respond ONLY in Korean.\n\n"
                    "IDENTITY: You are an elite AI College Admissions & Daily Study Habit Coach. Guide students with highly objective, structured, and empathetic advice based on CSAT data and study science.\n\n"
                    "=== ABSOLUTE RULES ===\n"
                    "1. NO MARKDOWN: Write in clean, plain conversational text.\n"
                    "2. TONE: Warm, encouraging, clear, and disciplined coaching tone.\n"
                    "3. CONTEXT: Direct, actionable guidance tailored to high school and repeat test-takers.\n"
                )

        # Build & sanitize contents for Gemini API (Must alternate user/model and start with user)
        raw_turns = []
        if history:
            for item in history[-6:]:
                if isinstance(item, dict):
                    r = item.get('role', 'user')
                    t = item.get('content', '')
                else:
                    r = getattr(item, 'role', 'user')
                    t = getattr(item, 'content', '')
                role = 'user' if r in ('user', 'human') else 'model'
                text_str = str(t).strip() if t else ''
                if text_str:
                    raw_turns.append({'role': role, 'text': text_str})

        raw_turns.append({'role': 'user', 'text': str(message).strip()})

        # Skip leading model turns so conversation starts with user
        while raw_turns and raw_turns[0]['role'] != 'user':
            raw_turns.pop(0)

        # Merge consecutive same-role turns to strictly enforce alternation
        contents = []
        for turn in raw_turns:
            if not contents:
                contents.append({'role': turn['role'], 'parts': [{'text': turn['text']}]})
            else:
                last_turn = contents[-1]
                if last_turn['role'] == turn['role']:
                    last_turn['parts'][0]['text'] += "\n" + turn['text']
                else:
                    contents.append({'role': turn['role'], 'parts': [{'text': turn['text']}]})

        # Ensure last turn is user
        if not contents:
            contents = [{'role': 'user', 'parts': [{'text': message}]}]

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=contents,
                config={
                    'system_instruction': system_prompt,
                    'temperature': 0.6,
                    'max_output_tokens': 2500,
                }
            )
            if response.text and response.text.strip():
                cleaned = response.text.replace('###', '').replace('##', '').replace('#', '').replace('**', '').replace('* ', '')
                return cleaned
        except Exception as ex:
            print(f"CHATBOT ERROR (gemini-3.6-flash): {ex}")
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-pro',
                    contents=contents,
                    config={
                        'system_instruction': system_prompt,
                        'temperature': 0.6,
                        'max_output_tokens': 2500,
                    }
                )
                if response.text and response.text.strip():
                    cleaned = response.text.replace('###', '').replace('##', '').replace('#', '').replace('**', '').replace('* ', '')
                    return cleaned
            except Exception as ex2:
                print(f"CHATBOT PRO ERROR: {ex2}")

        return "지금 구글 AI 서버에 순간적인 접속 트래픽이 몰려서 지연되었어. 1~2초 뒤에 질문을 다시 보내주면 바로 답변해줄게!"
    except Exception as e:
        print(f"CHATBOT UNEXPECTED ERROR: {e}")
        return "지금 AI 서버 연결이 불안정해. 잠시 후 다시 말 걸어줘."


def test_sandbox_prompt(system_prompt: str, user_message: str) -> str:
    client = get_gemini_client()
    if not client:
        return "Gemini 클라이언트 연결 실패"

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[{'role': 'user', 'parts': [{'text': user_message}]}],
            config={
                'system_instruction': system_prompt,
                'temperature': 0.6,
                'max_output_tokens': 1500,
            }
        )
        if response.text and response.text.strip():
            return response.text.replace('###', '').replace('##', '').replace('#', '').replace('**', '')
    except Exception as e:
        print(f"Sandbox test error: {e}")
        return f"샌드박스 테스트 실행 오류: {e}"

    return "샌드박스 테스트 실행 중 오류가 발생했습니다."
