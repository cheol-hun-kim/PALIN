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
    kor_pct: float,      # 국어 백분위 0-100
    math_pct: float,     # 수학 백분위 0-100
    eng_raw: int,        # 영어 원점수 0-100
    tam1_pct: float,     # 탐구1 백분위 0-100
    tam2_pct: float,     # 탐구2 백분위 0-100
    hist_raw: int,       # 한국사 원점수 0-50
    math_type: str = '미적',  # 미적/기하/확통
    gyeyeol: str = '이과',    # 이과/문과
    target_univ: str = None,
    target_dept: str = None
) -> dict:
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

    results = []
    target_result = None
    summary = {'안정': 0, '적정': 0, '소신': 0, '위험': 0}

    for entry in entries:
        if entry.get('계열') != gyeyeol:
            continue
            
        kor_weight = entry.get('국어구성비', 0)
        math_weight = entry.get('수학구성비', 0)
        tam_weight = entry.get('탐구구성비', 0)
        
        total_weight = kor_weight + math_weight + tam_weight
        if total_weight == 0:
            continue
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_pct + tam2_pct) / 2) * tam_weight) / total_weight
        student_nuback = 100.0 - avg_pct
        
        # Add eng grade penalty (0-indexed array)
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
            '대학교': entry.get('대학교'),
            '전공': entry.get('전공'),
            '대학구분': entry.get('대학구분', ''),
            '모집군': entry.get('모집군', ''),
            '시도': entry.get('시도', ''),
            '정원': entry.get('정원', 0),
            '대학약칭': entry.get('대학약칭', ''),
            '전공약칭': entry.get('전공약칭', ''),
            'student_nuback': round(student_nuback, 4),
            'verdict': verdict,
            '적정누백': entry.get('적정누백'),
            '예상누백': entry.get('예상누백'),
            '소신누백': entry.get('소신누백'),
        }
        results.append(res)
        
        # 목표 대학 매칭 (대학명만으로도 첫 매칭 가능)
        if target_univ and target_result is None:
            univ_match = target_univ in res['대학교'] or target_univ in entry.get('대학약칭', '')
            dept_match = (not target_dept) or (target_dept in res['전공'])
            if univ_match and dept_match:
                target_result = res
                
    # Sort results (안정 -> 위험 순, 누백이 낮을수록 좋음)
    verdict_order = {'안정': 0, '적정': 1, '소신': 2, '위험': 3}
    results.sort(key=lambda x: (verdict_order[x['verdict']], x['student_nuback']))

    return {
        'target_result': target_result,
        'results': results,
        'summary': summary
    }
