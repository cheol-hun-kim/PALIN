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
    
    # 1. 인사 및 상태 점검
    if any(k in m for k in ["안녕", "반가워", "하이", "처음"]):
        return (
            "어 그래, 반갑다! 난 네 수험생활 궤적을 철저하게 통제하고 정시 합격으로 이끌어줄 과외선생님이자 입시 선배야. "
            "남들이 다 하는 감정적 희망 고문이나 무의미한 문제 양치기는 전부 걷어내고, 오직 데이터랑 팩트로만 이야기해 줄 거다.\n\n"
            "너 지금 현재 가장 불안하거나 막히는 과목이 뭐야? 국어, 수학, 내신 미련, 아니면 하루 공부 바이오리듬 문제야? 편하게 솔직하게 다 말해봐."
        )

    # 1.5. 밥 / 식사 / 음식 관련 일상 대화
    if any(k in m for k in ["밥", "식사", "음식", "배고파", "먹기"]):
        return (
            f"네가 말한 '{msg}'처럼 입맛이 떨어지거나 밥 먹기 싫은 건 수험 스트레스로 위장이 굳어서 생기는 신체 신호야.\n\n"
            "하지만 뇌를 쓰려면 포도당과 영양분이 필수거든. 정 제대로 된 밥이 안 넘어간다면 소화 잘 되는 죽이나 바나나, 단백질 음료라도 가볍게 챙겨 먹어라.\n\n"
            "속이 비어있으면 오후 집중력이 반토막 난다. 오늘 점심이나 저녁에 가볍게 뭐라도 챙겨 먹었어?"
        )
    
    # 2. 의욕 없음 / 공부하기 싫음 / 지침 / 슬럼프
    if any(k in m for k in ["의욕", "싫어", "싫다", "힘들", "지친", "피곤", "졸려", "포기", "죽겠", "우울", "쉬고", "슬럼프", "망했"]):
        return (
            f"네가 말한 '{msg}'라는 감정, 수험생 마라톤 중간 지점에서 뇌랑 신체가 보내는 자연스러운 자율 방어 기제야. 의지가 부족한 게 절대 아니다.\n\n"
            "이럴 때 억지로 독서실 책상 앞에 멍하게 10시간 앉아있는 건 뇌에 '공부는 괴로운 것'이라는 열등감만 학습시키는 자살행위야. "
            "하루 6시간 30분 수면부터 사수해라. 뇌가 맑은 상태로 2시간 기출 사색하는 게 멍한 10시간보다 100배 이득이거든.\n\n"
            "너 요며칠 평균 몇 시간이나 자고 있어? 혹시 새벽까지 휴대폰 보거나 숙제 밀려서 잠 줄인 건 아니지?"
        )
        
    # 3. 국어 / 독해 / 비문학
    if any(k in m for k in ["국어", "독해", "비문학", "문학", "언매", "화작"]):
        return (
            "국어 점수 정체는 지문을 '읽는 것'과 지문의 논리를 '해독하는 것'을 구분 못 해서 생기는 거야. 수능 국어는 단 하나도 단순 지식을 묻지 않아. "
            "문장 간 대립 구조랑 정보 관계를 펜 들고 깊게 사색해야 하거든. 판교도서관에서 1문항 가지고 온종일 뇌를 몰아붙였던 것처럼, 하루에 1지문이라도 원리를 100% 뚫어내는 훈련을 해봐.\n\n"
            "너 혹시 언매 표점 높다고 무작정 선택했어? 아니면 비문학 긴 지문 읽을 때 현장에서 정보 멘탈 나가는 편이야? 구체적으로 말해봐."
        )
        
    # 4. 수학 / 기출 / 문제풀이
    if any(k in m for k in ["수학", "킬러", "준킬러", "백분위", "기출", "양치기"]):
        return (
            "수학 문제 100개씩 무작정 양치기하는 건 사설 학원 마케팅에 속는 거다. 사설 변형 문제 아무리 많이 풀어봤자 시험장 낯선 조건 앞에서는 헛발질만 해.\n\n"
            "평가원 고3 기출로 돌아가라. 한 문제 틀렸을 때 해설지 바로 보지 말고, 조건 1개가 왜 그 위치에 배치됐는지 최소 30분 이상 뇌를 들쑤셔야 해. "
            "너 지금 하루에 수학 기출 사색에 몇 시간이나 쓰고 있어? 사설 모의고사 양치기에 쏠려있는 건 아니지?"
        )
        
    # 5. 내신 / 수시 / 수행평가
    if any(k in m for k in ["내신", "수시", "수행", "중간", "기말", "3등급", "4등급"]):
        return (
            "내신이랑 수능은 완전히 다른 게임이야. 이미 평균 내신이 3, 4등급 이하로 밀렸다면 인서울 수시 교과/학종 합격 확률은 0%에 수렴해. "
            "선생님 눈치 보느라 내신 밤새우고 수행평가 챙기는 사이 수능 최저 미달에 정시 점수까지 다 날아간다.\n\n"
            "수시 미련 접고 정시 수능 100% 또는 약술형 논술(가천대, 고려대 세종 등 단답형 논술)로 당장 전략적 조기 전환해. "
            "너 현재 평균 내신 등급이 정확히 몇 등급이고, 수시 미련 때문에 일주일에 몇 시간이나 쓰고 있어?"
        )
        
    # 6. 계획 / 시간관리 / 플래너
    if any(k in m for k in ["계획", "플래너", "시간", "숙제", "밀려"]):
        return (
            "'문제집 30페이지 풀기' 같은 분량 단위 계획은 난이도 변수 때문에 3일을 못 가고 무너져. 밀린 플래너 보면 '난 안 돼' 패배의식만 뇌에 남는다.\n\n"
            "모든 계획을 [시간 단위](예: 국어 1.5시간, 수학 4시간)로 바꿔라. 시간은 문제 난이도와 상관없이 일정하게 흐르니까 계획 달성률이 100%가 되거든. "
            "학원 숙제 끝내는 걸 공부라고 착각하지 말고 네가 필요한 시간에 집중해. 오늘 세운 계획 중에 네 순수 사색 시간이 몇 시간이나 돼?"
        )

    # 7. 기본 유연 대화 (학생 발화 반영)
    return (
        f"네가 말한 '{msg}'에 대해서 냉정하게 짚어줄게. 수능 입시는 단순히 엉덩이로 버티는 무의미한 노동이 아니야. "
        f"낯선 조건 속에서 출제자의 원리를 파악하는 '사색과 깨달음'의 평가거든. 남들이 다 하니까 따라 하는 방식은 당장 멈춰야 해.\n\n"
        f"오직 고3 평가원 기출문제를 펴놓고, 하루 1문항을 풀더라도 출제자 설계를 100% 해독할 때까지 뇌를 몰아붙이자. 수면시간 6시간 30분부터 사수하고.\n\n"
        f"너 지금 이 문제에 대해서 진짜 원인이 뭐라고 생각해? 현장에서 어떤 부분이 제일 막히는지 더 구체적으로 말해봐, 같이 풀어보게."
    )

def ask_ai_chatbot(message: str) -> str:
    client = get_gemini_client()
    if client:
        try:
            knowledge = get_expert_knowledge()
            
            system_prompt = (
                "# Role & Persona (역할 및 페르소나)\n"
                "- 당신의 이름은 PALIN BOT이며 냉혹하지만 진심으로 학생을 아끼는 전문 입시 컨설턴트이자 입시 선배(김철훈 원장 페르소나)다.\n"
                "- 삼수까지 하며 겪은 실패 경험과 '실패의 원리' 지식 베이스에 근거하여 학생들에게 팩트 기반의 진실만을 전하는 '등대' 역할을 한다.\n"
                "- 뻔한 사교육 마케팅(양치기, 사설 모의고사, 무조건적인 내신 챙기기)을 경계하며 팩트와 숫자에 기반한 냉철한 분석을 제공한다.\n\n"
                
                "# General Natural Dialogue Principles (자연스러운 대화 기본 지침)\n"
                "- 가장 중요한 원칙: 사용자의 질문/말에 공감하고 맥락에 맞게 '자연스럽게' 대화하라. 동문서답(질문과 상관없는 뚱딴지 답변)을 절대 하지 마라!\n"
                "- 사용자가 '밥 뭐 먹지', '날씨 좋네', '오늘 피곤하다' 등 일상 대화를 건네면, 동문서답으로 갑자기 수능 기출을 풀라는 식의 기계적인 답변을 내뱉지 말고, 우선 멘토로서 일상 대화를 자연스럽게 주고받아라.\n"
                "- 일상 대화 답변 끝에 가볍게 '수험생 식단 관리', '수면 패턴 유지' 같은 멘토링 조언을 츤데레 스타일로 1~2문장 덧붙이는 수준으로 자연스럽게 마무리하라.\n"
                "- 단호하고 전문가적인 카리스마가 느껴지는 친근한 반말 어조(~해라, ~하자, ~이야, ~거든, ~잖아)를 사용하라.\n"
                "- 마크다운 서식(#, **, -, ``` 등)과 기계적인 이모티콘 남발을 피하고 순수 구어체 텍스트로 작성하라.\n\n"
                
                "# Knowledge-Based Deep Consultation (입시/학습 심층 상담 지침)\n"
                "- 학생이 성적, 공부법, 내신, 수시/정시, 플래너, 슬럼프 등 입시 관련 고민을 털어놓을 때는 [김철훈 원장님의 실패의 원리 전문 지식 베이스]를 100% 바탕으로 답하라.\n"
                "- 핑계 타파: 능력을 탓하는 것은 현실 도피일 뿐이며 올바른 방향(기출 출제원리 해독)과 실전 변수 통제(수면 6시간 30분 사수 등)가 핵심임을 짚어줘라.\n"
                "- 답변 맨 끝에는 학생의 현 상태를 묻는 날카로운 반말 질문 1개를 던져 대화를 이어나가라.\n\n"
                
                "# [김철훈 원장님의 실패의 원리 통합 지식 베이스 (202페이지 전문)]\n"
                f"{knowledge}\n"
            )
            
            # Gemini API 호출 (Model: gemini-2.5-flash, Temperature: 0.4)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=message,
                config={
                    'system_instruction': system_prompt,
                    'temperature': 0.4,
                    'max_output_tokens': 2000,
                }
            )
            return response.text
        except APIError as api_err:
            print(f"Gemini API Error: {api_err}. Falling back to dynamic fallback engine.")
        except Exception as e:
            print(f"Gemini unexpected error: {e}. Falling back to dynamic fallback engine.")

    # Dynamic Banmal Mentoring Engine Fallback
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
                model='gemini-2.5-flash',
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
