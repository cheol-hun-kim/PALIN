import json, os

_entries_science = None
_entries_humanities = None

def raw_to_eng_grade(raw_score: int) -> int:
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
    if raw_score >= 40: return 1
    if raw_score >= 35: return 2
    if raw_score >= 30: return 3
    if raw_score >= 25: return 4
    if raw_score >= 20: return 5
    if raw_score >= 15: return 6
    if raw_score >= 10: return 7
    if raw_score >= 5: return 8
    return 9

def load_science_entries():
    global _entries_science
    if _entries_science is None:
        data_path = os.path.join(os.path.dirname(__file__), "data", "univ_entries_science.json")
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                _entries_science = json.load(f)
        else:
            _entries_science = []
    return _entries_science

def load_humanities_entries():
    global _entries_humanities
    if _entries_humanities is None:
        data_path = os.path.join(os.path.dirname(__file__), "data", "univ_entries_humanities.json")
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                _entries_humanities = json.load(f)
        else:
            _entries_humanities = []
    return _entries_humanities

def load_entries():
    return load_science_entries() + load_humanities_entries()

def avg_pct_to_nuback_science(avg_pct: float) -> float:
    """미적/과탐 이과 응시자 기준 누백 (Sheet 4 스케일: 96% -> ~3.9%, 94% -> ~8.4%, 90% -> ~17.4%)"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.5, 3)
    elif diff <= 2.0: return round(0.5 + (diff - 1.0) * 0.8, 3)
    elif diff <= 4.0: return round(1.3 + (diff - 2.0) * 1.3, 3)
    elif diff <= 7.0: return round(3.9 + (diff - 4.0) * 1.5, 3)
    elif diff <= 12.0: return round(8.4 + (diff - 7.0) * 1.8, 3)
    elif diff <= 20.0: return round(17.4 + (diff - 12.0) * 2.0, 3)
    else: return round(33.4 + (diff - 20.0) * 2.2, 3)

def avg_pct_to_nuback_unified(avg_pct: float) -> float:
    """확통/사탐 및 전국 통합 기준 누백 (Sheet 5 스케일: 96% -> ~1.2%, 94% -> ~2.4%, 90% -> ~4.5%)"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.15, 3)
    elif diff <= 3.0: return round(0.15 + (diff - 1.0) * 0.35, 3)
    elif diff <= 6.0: return round(0.85 + (diff - 3.0) * 0.50, 3)
    elif diff <= 10.0: return round(2.35 + (diff - 6.0) * 0.65, 3)
    elif diff <= 15.0: return round(4.95 + (diff - 10.0) * 0.80, 3)
    elif diff <= 25.0: return round(8.95 + (diff - 15.0) * 0.95, 3)
    else: return round(18.45 + (diff - 25.0) * 1.05, 3)

def predict_admission(
    kor_pct: float,
    math_pct: float,
    eng_raw: int,
    tam1_pct: float,
    tam2_pct: float,
    hist_raw: int,
    math_type: str = '미적',
    tam1_type: str = '과탐',
    tam2_type: str = '과탐',
    target_univ: str = None,
    target_dept: str = None
) -> dict:
    eng_grade = raw_to_eng_grade(eng_raw)
    hist_grade = raw_to_hist_grade(hist_raw)
    
    hist_penalty = 0.0
    if hist_grade == 4: hist_penalty = 0.05
    elif hist_grade == 5: hist_penalty = 0.15
    elif hist_grade >= 6: hist_penalty = 0.3

    is_math_calc = math_type in ['미적', '기하']
    science_tam_count = (1 if tam1_type == '과탐' else 0) + (1 if tam2_type == '과탐' else 0)
    
    # 1. 자연계 순수 응시 (미적/기하 + 과탐 2개)
    is_pure_science = is_math_calc and science_tam_count == 2
    
    if is_pure_science:
        entries = load_science_entries()
        nuback_converter = avg_pct_to_nuback_science
    else:
        entries = load_humanities_entries()
        nuback_converter = avg_pct_to_nuback_unified

    STRICT_SCIENCE_UNIVS = ['서울대학교', '서울대']

    results = []
    summary = {'안정': 0, '적정': 0, '소신': 0, '위험': 0}

    for entry in entries:
        univ_name = entry.get('대학교', '')
        dept_name = entry.get('전공', '')
        gyeyeol = entry.get('계열', '')
        
        if gyeyeol == '이과' and any(s_univ in univ_name for s_univ in STRICT_SCIENCE_UNIVS):
            if science_tam_count < 2 or not is_math_calc:
                continue

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
        if total_weight == 0: total_weight = 1.0
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_effective + tam2_effective) / 2) * tam_weight) / total_weight
        
        student_nuback = nuback_converter(avg_pct)
        
        eng_conversions = entry.get('영어환산', [])
        if eng_conversions and len(eng_conversions) >= 9:
            grade_deduction = abs(eng_conversions[eng_grade - 1]) if eng_grade <= len(eng_conversions) else 0.0
            student_nuback += (grade_deduction * (0.05 if is_pure_science else 0.015))
        else:
            eng_penalties = [0, 0.2, 0.5, 1.0, 1.8, 2.8, 4.0, 5.5, 7.0]
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
        
        results.append({
            '대학교': univ_name,
            '전공': dept_name,
            '대학약칭': entry.get('대학약칭', univ_name),
            '전공약칭': entry.get('전공약칭', dept_name),
            '계열': gyeyeol,
            '대학구분': entry.get('대학구분', '4년제'),
            '모집군': entry.get('모집군', '가'),
            '시도': entry.get('시도', '서울'),
            '시군구': entry.get('시군구', ''),
            'student_nuback': round(student_nuback, 2),
            'verdict': verdict,
            '적정누백': safe_cut,
            '예상누백': proper_cut,
            '소신누백': sosin_cut
        })

    target_result = None
    if target_univ and target_dept:
        t_clean = target_univ.replace('대학교', '').replace('대', '')
        d_clean = target_dept.strip()
        matched = [r for r in results if (t_clean in r['대학교'] or t_clean in r['대학약칭'])]
        if d_clean:
            dept_matched = [r for r in matched if (r['전공'] == d_clean or r['전공'] == d_clean + '과' or r['전공'].startswith(d_clean) or (d_clean in r['전공'] and not ('수의' in r['전공'] and '의예' in d_clean)))]
            if dept_matched:
                target_result = dept_matched[0]
        if not target_result and matched:
            target_result = matched[0]

    return {
        'results': results,
        'summary': summary,
        'target_result': target_result
    }
