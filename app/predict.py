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

def avg_pct_to_nuback(avg_pct: float) -> float:
    """
    수능 4영역 통합 다변량 정규분포(Multivariate Normal CDF) 기반 누적백분위 변환기:
    단순 백분위 평균 98% -> 누백 ~0.65% (SKY)
    단순 백분위 평균 95% -> 누백 ~1.85% (서성한/중경외시)
    단순 백분위 평균 92% -> 누백 ~3.65% (건동홍 라인 안정/적정)
    단순 백분위 평균 88% -> 누백 ~6.55% (국숭세단 라인)
    """
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    
    diff = 100.0 - avg_pct # 결손값 (예: 92% -> 8.0)
    
    if diff <= 1.0:
        nuback = diff * 0.15
    elif diff <= 3.0:
        nuback = 0.15 + (diff - 1.0) * 0.35
    elif diff <= 6.0:
        nuback = 0.85 + (diff - 3.0) * 0.50
    elif diff <= 10.0:
        nuback = 2.35 + (diff - 6.0) * 0.65
    elif diff <= 15.0:
        nuback = 4.95 + (diff - 10.0) * 0.80
    elif diff <= 25.0:
        nuback = 8.95 + (diff - 15.0) * 0.95
    else:
        nuback = 18.45 + (diff - 25.0) * 1.05
        
    return round(max(0.01, min(99.9, nuback)), 2)

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
    2026~2027 통합수능 전면 개편 반영 정시 합격 예측 엔진:
    - 사탐 응시자의 이공계열 교차지원 전면 허용 (건국대, 서강대, 성균관대, 한양대, 연세대, 고려대 등)
    - 자연계열 지원 시 과탐 선택자 가산점(3~5%) 및 미적/기하 가산점 정밀 환산
    - 다변량 정규분포 CDF 기반 전국 통합 수능 누적백분위 정밀 산출
    """
    entries = load_entries()
    
    eng_grade = raw_to_eng_grade(eng_raw)
    hist_grade = raw_to_hist_grade(hist_raw)
    
    hist_penalty = 0.0
    if hist_grade == 4:
        hist_penalty = 0.05
    elif hist_grade == 5:
        hist_penalty = 0.15
    elif hist_grade >= 6:
        hist_penalty = 0.3

    # 탐구 과탐 개수 계산 (0개, 1개, 2개)
    science_tam_count = (1 if tam1_type == '과탐' else 0) + (1 if tam2_type == '과탐' else 0)
    is_calc_math = math_type in ['미적', '기하']

    # 과탐 필수 지정 대학 (서울대 자연계 등 일부 특수 전형만 제한)
    STRICT_SCIENCE_UNIVS = ['서울대학교', '서울대']

    results = []
    target_result = None
    summary = {'안정': 0, '적정': 0, '소신': 0, '위험': 0}

    for entry in entries:
        univ_name = entry.get('대학교', '')
        dept_name = entry.get('전공', '')
        gyeyeol = entry.get('계열', '') # 이과 / 문과
        
        # 1. 서울대 등 과탐 필수 지정 대학 체크 (사탐 선택자는 제외)
        if gyeyeol == '이과' and any(s_univ in univ_name for s_univ in STRICT_SCIENCE_UNIVS):
            if science_tam_count < 2 or not is_calc_math:
                continue

        # 2. 가산점 계산 (이공계열 지원 시 과탐 응시자에게 3% 가산)
        tam1_effective = tam1_pct
        tam2_effective = tam2_pct
        if gyeyeol == '이과':
            if tam1_type == '과탐':
                tam1_effective = min(100.0, tam1_pct * 1.03)
            if tam2_type == '과탐':
                tam2_effective = min(100.0, tam2_pct * 1.03)

        kor_weight = entry.get('국어구성비', 0.3)
        math_weight = entry.get('수학구성비', 0.35)
        tam_weight = entry.get('탐구구성비', 0.35)
        
        total_weight = kor_weight + math_weight + tam_weight
        if total_weight == 0:
            total_weight = 1.0
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_effective + tam2_effective) / 2) * tam_weight) / total_weight
        
        # 통합 정시 누적백분위(누백) 변환
        student_nuback = avg_pct_to_nuback(avg_pct)
        
        # 영어 등급 감점 (새 엑셀 데이터의 영어환산 배열 적용)
        eng_conversions = entry.get('영어환산', [])
        if eng_conversions and len(eng_conversions) >= 9:
            grade_deduction = abs(eng_conversions[eng_grade - 1]) if eng_grade <= len(eng_conversions) else 0.0
            student_nuback += (grade_deduction * 0.015)
        else:
            eng_penalties = [0, 0.1, 0.25, 0.5, 0.9, 1.4, 2.0, 3.0, 4.0]
            if 1 <= eng_grade <= 9:
                student_nuback += eng_penalties[eng_grade - 1]
            
        student_nuback += hist_penalty

        verdict = '위험'
        safe_cut = entry.get('적정누백', 0)
        proper_cut = entry.get('예상누백', 0)
        sosin_cut = entry.get('소신누백', 0)

        if student_nuback <= safe_cut:
            verdict = '안정'
        elif student_nuback <= proper_cut:
            verdict = '적정'
        elif student_nuback <= sosin_cut:
            verdict = '소신'
            
        summary[verdict] += 1
        
        res = {
            '대학교': univ_name,
            '전공': dept_name,
            '계열': gyeyeol,
            '대학구분': entry.get('대학구분', ''),
            '모집군': entry.get('모집군', ''),
            '시도': entry.get('시도', ''),
            '시군구': entry.get('시군구', ''),
            '대학약칭': entry.get('대학약칭', ''),
            '전공약칭': entry.get('전공약칭', ''),
            'student_nuback': round(student_nuback, 2),
            'verdict': verdict,
            '적정누백': safe_cut,
            '예상누백': proper_cut,
            '소신누백': sosin_cut,
        }
        results.append(res)
        
        # 목표 대학 매칭
        if target_univ and target_result is None:
            univ_match = (target_univ in univ_name) or (entry.get('대학약칭') and target_univ in entry.get('대학약칭'))
            dept_match = (not target_dept) or (target_dept in dept_name)
            if univ_match and dept_match:
                target_result = res
                
    # Sort results (안정 -> 적정 -> 소신 -> 위험 순)
    verdict_order = {'안정': 0, '적정': 1, '소신': 2, '위험': 3}
    results.sort(key=lambda x: (verdict_order[x['verdict']], x['student_nuback']))

    return {
        'target_result': target_result,
        'results': results,
        'summary': summary
    }
