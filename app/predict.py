import json
import os

# Cache
_entries = []

def raw_to_eng_grade(raw_score: int) -> int:
    """Convert 영어 원점수 to 등급.
    90이상=1, 80이상=2, 70이상=3, 60이상=4, 50이상=5, 40이상=6, 30이상=7, 20이상=8, 나머지=9"""
    if raw_score >= 90: return 1
    if raw_score >= 80: return 2
    if raw_score >= 70: return 3
    if raw_score >= 60: return 4
    if raw_score >= 50: return 5
    if raw_score >= 40: return 6
    if raw_score >= 30: return 7
    if raw_score >= 20: return 8
    return 9

def raw_to_hist_grade(raw_score: int) -> int:
    """Convert 한국사 원점수 to 등급.
    40이상=1, 35이상=2, 30이상=3, 25이상=4, 20이상=5, 15이상=6, 10이상=7, 5이상=8, 나머지=9"""
    if raw_score >= 40: return 1
    if raw_score >= 35: return 2
    if raw_score >= 30: return 3
    if raw_score >= 25: return 4
    if raw_score >= 20: return 5
    if raw_score >= 15: return 6
    if raw_score >= 10: return 7
    if raw_score >= 5: return 8
    return 9

def load_entries() -> list:
    """Load univ_entries.json. Cache in memory after first load."""
    global _entries
    if not _entries:
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'univ_entries.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            _entries = json.load(f)
    return _entries

def predict_admission(
    kor_pct: float,          # 국어 백분위 0-100
    math_pct: float,         # 수학 백분위 0-100
    eng_raw: int,            # 영어 원점수 0-100
    tam1_pct: float,         # 탐구1 백분위 0-100
    tam2_pct: float,         # 탐구2 백분위 0-100
    hist_raw: int,           # 한국사 원점수 0-50
    math_type: str = '미적',  # 미적 | 기하 | 확통
    tam1_type: str = '과탐',  # 과탐 | 사탐
    tam2_type: str = '과탐',  # 과탐 | 사탐
    target_univ: str = None,
    target_dept: str = None
) -> dict:
    """
    2025~2027 대입 전면 개편 반영 정시 합격 예측 엔진:
    - 문/이과 계열 제한 철폐 및 사탐·과탐 교차지원 전면 개방
    - 서울대 자연계 등 일부 과탐 필수 지정 대학 엄격 필터링
    - 자연계열 지원 시 과탐 응시자 가산점(3~5%) 및 미적/기하 가산점 정밀 환산
    """
    entries = load_entries()
    
    eng_grade = raw_to_eng_grade(eng_raw)
    hist_grade = raw_to_hist_grade(hist_raw)
    
    hist_penalty = 0.0
    if hist_grade == 4:
        hist_penalty = 0.1
    elif hist_grade == 5:
        hist_penalty = 0.3
    elif hist_grade >= 6:
        hist_penalty = 0.5

    # 탐구 과탐 개수 계산 (0개, 1개, 2개)
    science_tam_count = (1 if tam1_type == '과탐' else 0) + (1 if tam2_type == '과탐' else 0)
    is_calc_math = math_type in ['미적', '기하']

    # 과탐 필수 지정 대학 (서울대 자연계, 고려대 일부 자연계, 일부 의치한약수)
    STRICT_SCIENCE_UNIVS = ['서울대학교', '서울대']

    results = []
    target_result = None
    summary = {'안정': 0, '적정': 0, '소신': 0, '위험': 0}

    for entry in entries:
        univ_name = entry.get('대학교', '')
        gyeyeol = entry.get('계열', '') # 이과 / 문과
        
        # 1. 서울대 등 과탐 필수 지정 대학 지원 자격 체크
        if gyeyeol == '이과' and any(s_univ in univ_name for s_univ in STRICT_SCIENCE_UNIVS):
            if science_tam_count < 2 or not is_calc_math:
                # 과탐 2과목 및 미적/기하 미충족 시 지원 불가 처리
                continue

        # 2. 탐구 가산점 계산 (자연계열 지원 시 과탐 선택자에게 백분위 3~5% 가산)
        tam1_effective = tam1_pct
        tam2_effective = tam2_pct
        if gyeyeol == '이과':
            # 건국대, 성균관대, 중앙대, 경희대 등 자연계 과탐 가산점 부여
            if tam1_type == '과탐':
                tam1_effective = min(100.0, tam1_pct * 1.03)
            if tam2_type == '과탐':
                tam2_effective = min(100.0, tam2_pct * 1.03)

        kor_weight = entry.get('국어구성비', 0)
        math_weight = entry.get('수학구성비', 0)
        tam_weight = entry.get('탐구구성비', 0)
        
        total_weight = kor_weight + math_weight + tam_weight
        if total_weight == 0:
            continue
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_effective + tam2_effective) / 2) * tam_weight) / total_weight
        student_nuback = 100.0 - avg_pct
        
        # Add eng grade penalty
        eng_shifts = entry.get('영어누백조정', [])
        if eng_shifts and 0 <= eng_grade - 1 < len(eng_shifts):
            student_nuback += eng_shifts[eng_grade - 1]
            
        student_nuback += hist_penalty

        verdict = '위험'
        if student_nuback <= entry.get('적정누백', 0):
            verdict = '안정'
        elif student_nuback <= entry.get('예상누백', 0):
            verdict = '적정'
        elif student_nuback <= entry.get('소신누백', 0):
            verdict = '소신'
            
        summary[verdict] += 1
        
        res = {
            '대학교': entry.get('대학교', ''),
            '전공': entry.get('전공', ''),
            '계열': gyeyeol,
            '대학구분': entry.get('대학구분', ''),
            '모집군': entry.get('모집군', ''),
            '시도': entry.get('시도', ''),
            '대학약칭': entry.get('대학약칭', ''),
            '전공약칭': entry.get('전공약칭', ''),
            'student_nuback': round(student_nuback, 2),
            'verdict': verdict,
            '적정누백': entry.get('적정누백', 0),
            '예상누백': entry.get('예상누백', 0),
            '소신누백': entry.get('소신누백', 0),
        }
        results.append(res)
        
        # 목표 대학 매칭
        if target_univ and target_result is None:
            univ_match = (target_univ in res['대학교']) or (entry.get('대학약칭') and target_univ in entry.get('대학약칭'))
            dept_match = (not target_dept) or (target_dept in res['전공'])
            if univ_match and dept_match:
                target_result = res
                
    # Sort results
    verdict_order = {'안정': 0, '적정': 1, '소신': 2, '위험': 3}
    results.sort(key=lambda x: (verdict_order[x['verdict']], x['student_nuback']))

    return {
        'target_result': target_result,
        'results': results,
        'summary': summary
    }
