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
            with open(data_path, "r", encoding="utf-8") as f:
                _entries_science = json.load(f)
        else:
            _entries_science = []
    return _entries_science

def load_humanities_entries():
    global _entries_humanities
    if _entries_humanities is None:
        data_path = os.path.join(os.path.dirname(__file__), "data", "univ_entries_humanities.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                _entries_humanities = json.load(f)
        else:
            _entries_humanities = []
    return _entries_humanities

# 서버 기동 시 미리 로드
try:
    load_science_entries()
    load_humanities_entries()
except: pass

def avg_pct_to_nuback_science(avg_pct: float) -> float:
    """8개 샘플 실측 이과 누백 곡선 (Sample 5, 6, 7 실측 캘리브레이션)"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.15, 3)
    elif diff <= 2.0: return round(0.15 + (diff - 1.0) * 0.25, 3)
    elif diff <= 4.0: return round(0.40 + (diff - 2.0) * 0.325, 3) # 96% -> 1.05% (연세대 화공 적정/안정권)
    elif diff <= 7.0: return round(1.05 + (diff - 4.0) * 0.45, 3)  # 93% -> 2.40% (서성한/중경시)
    elif diff <= 12.0: return round(2.40 + (diff - 7.0) * 0.60, 3) # 88% -> 5.40% (건동홍)
    elif diff <= 20.0: return round(5.40 + (diff - 12.0) * 0.85, 3)
    else: return round(12.20 + (diff - 20.0) * 1.10, 3)

def avg_pct_to_nuback_unified(avg_pct: float) -> float:
    """8개 샘플 실측 문과/통합 누백 곡선 (Sample 2, 3, 4 실측 캘리브레이션)"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.12, 3)
    elif diff <= 3.2: return round(0.12 + (diff - 1.0) * 0.33, 3) # 96.8% -> 0.85% (서울대 인문/경영)
    elif diff <= 6.5: return round(0.85 + (diff - 3.2) * 0.60, 3) # 93.5% -> 2.83% (연고대/서강대 경영)
    elif diff <= 10.0: return round(2.83 + (diff - 6.5) * 0.75, 3)
    elif diff <= 15.0: return round(5.45 + (diff - 10.0) * 0.90, 3)
    elif diff <= 25.0: return round(9.95 + (diff - 15.0) * 1.00, 3)
    else: return round(19.95 + (diff - 25.0) * 1.10, 3)

def predict_admission(
    kor_pct: float,
    math_pct: float,
    eng_raw: int,
    tam1_pct: float,
    tam2_pct: float,
    hist_raw: int,
    math_type: str = "\ubbf8\uc801",
    tam1_type: str = "\uacfc\ud0d0",
    tam2_type: str = "\uacfc\ud0d0",
    target_univ: str = None,
    target_dept: str = None,
    *args,
    **kwargs
) -> dict:
    eng_grade = raw_to_eng_grade(eng_raw)
    hist_grade = raw_to_hist_grade(hist_raw)
    
    hist_penalty = 0.0
    if hist_grade == 4: hist_penalty = 0.05
    elif hist_grade == 5: hist_penalty = 0.15
    elif hist_grade >= 6: hist_penalty = 0.3

    is_math_calc = math_type in ["\ubbf8\uc801", "\uae30\ud558"]
    science_tam_count = (1 if tam1_type == "\uacfc\ud0d0" else 0) + (1 if tam2_type == "\uacfc\ud0d0" else 0)
    
    is_pure_science = is_math_calc and science_tam_count == 2
    
    if is_pure_science:
        entries = load_science_entries()
        nuback_converter = avg_pct_to_nuback_science
    else:
        entries = load_humanities_entries()
        nuback_converter = avg_pct_to_nuback_unified

    STRICT_SCIENCE_UNIVS = ["\uc11c\uc6b8\ub300\ud559\uad50", "\uc11c\uc6b8\ub300"]

    results = []
    summary = {
        "\uc548\uc815": 0,
        "\uc801\uc815": 0,
        "\uc18c\uc2e0": 0,
        "\uc704\ud5d8": 0
    }

    for entry in entries:
        univ_name = entry.get("\ub300\ud559\uad50", "")
        dept_name = entry.get("\uc804\uacf5", "")
        gyeyeol = entry.get("\uacc4\uc5f4", "")
        
        if gyeyeol == "\uc774\uacfc" and any(s_univ in univ_name for s_univ in STRICT_SCIENCE_UNIVS):
            if science_tam_count < 2 or not is_math_calc:
                continue

        tam1_effective = tam1_pct
        tam2_effective = tam2_pct
        if gyeyeol == "\uc774\uacfc":
            if tam1_type == "\uacfc\ud0d0":
                tam1_effective = min(100.0, tam1_pct * 1.03)
            if tam2_type == "\uacfc\ud0d0":
                tam2_effective = min(100.0, tam2_pct * 1.03)

        kor_weight = entry.get("\uad6d\uc5b4\uad6c\uc131\ube44", 0.3)
        math_weight = entry.get("\uc218\ud559\uad6c\uc131\ube44", 0.35)
        tam_weight = entry.get("\ud0d0\uad6c\uad6c\uc131\ube44", 0.35)
        
        total_weight = kor_weight + math_weight + tam_weight
        if total_weight == 0: total_weight = 1.0
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_effective + tam2_effective) / 2) * tam_weight) / total_weight
        
        student_nuback = nuback_converter(avg_pct)
        
        # 영어 감점 (Sample 5 vs Sample 8 캘리브레이션)
        eng_conversions = entry.get("\uc601\uc5b4\ud658\uc0b0", [])
        if eng_conversions and len(eng_conversions) >= 9:
            grade_deduction = abs(eng_conversions[eng_grade - 1]) if eng_grade <= len(eng_conversions) else 0.0
            student_nuback += (grade_deduction * (0.04 if is_pure_science else 0.012))
        else:
            eng_penalties = [0, 0.25, 0.6, 1.2, 2.0, 3.2, 4.5, 6.0, 8.0]
            if 1 <= eng_grade <= 9:
                student_nuback += eng_penalties[eng_grade - 1]
            
        student_nuback += hist_penalty

        verdict = "\uc704\ud5d8"
        safe_cut = entry.get("\uc801\uc815\ub204\ubc31", 0)
        proper_cut = entry.get("\uc608\uc141\ub204\ubc31", 0)
        sosin_cut = entry.get("\uc18c\uc2e0\ub204\ubc31", 0)

        if student_nuback <= safe_cut:
            verdict = "\uc548\uc815"
        elif student_nuback <= proper_cut:
            verdict = "\uc801\uc815"
        elif student_nuback <= sosin_cut:
            verdict = "\uc18c\uc2e0"
            
        summary[verdict] += 1
        
        results.append({
            "\ub300\ud559\uad50": univ_name,
            "\uc804\uacf5": dept_name,
            "\ub300\ud559\uc57d\uce6d": entry.get("\ub300\ud559\uc57d\uce6d", univ_name),
            "\uc804\uacf5\uc57d\uce6d": entry.get("\uc804\uacf5\uc57d\uce6d", dept_name),
            "\uacc4\uc5f4": gyeyeol,
            "\ub300\ud559\uad6c\ubd84": entry.get("\ub300\ud559\uad6c\ubd84", "4\ub144\uc81c"),
            "\ubaa8\uc9d1\uad70": entry.get("\ubaa8\uc9d1\uad70", "\uac00"),
            "\uc2dc\ub3c4": entry.get("\uc2dc\ub3c4", "\uc11c\uc6b8"),
            "\uc2dc\uad70\uad6c": entry.get("\uc2dc\uad70\uad6c", ""),
            "student_nuback": round(student_nuback, 2),
            "verdict": verdict,
            "\uc801\uc815\ub204\ubc31": safe_cut,
            "\uc608\uc141\ub204\ubc31": proper_cut,
            "\uc18c\uc2e0\ub204\ubc31": sosin_cut
        })

    return {
        "results": results,
        "summary": summary
    }
