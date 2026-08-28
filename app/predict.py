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

def _find_data_file(filename: str):
    candidates = [
        os.path.join(os.path.dirname(__file__), "data", filename),
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join(os.getcwd(), "app", "data", filename),
        os.path.join(os.getcwd(), "data", filename),
        os.path.join(os.getcwd(), filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def load_science_entries():
    global _entries_science
    if _entries_science is None:
        p = _find_data_file("univ_entries_science.json")
        if p and os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                _entries_science = json.load(f)
        else:
            p_uni = _find_data_file("univ_entries.json")
            if p_uni and os.path.exists(p_uni):
                with open(p_uni, "r", encoding="utf-8") as f:
                    all_ent = json.load(f)
                    _entries_science = [e for e in all_ent if e.get("\uacc4\uc5f4") == "\uc774\uacfc"]
            else:
                _entries_science = []
    return _entries_science

def load_humanities_entries():
    global _entries_humanities
    if _entries_humanities is None:
        p = _find_data_file("univ_entries_humanities.json")
        if p and os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                _entries_humanities = json.load(f)
        else:
            p_uni = _find_data_file("univ_entries.json")
            if p_uni and os.path.exists(p_uni):
                with open(p_uni, "r", encoding="utf-8") as f:
                    all_ent = json.load(f)
                    _entries_humanities = [e for e in all_ent if e.get("\uacc4\uc5f4") == "\ub838\uacfc" or e.get("\uacc4\uc5f4") == "\ubb38\uacfc"]
            else:
                _entries_humanities = []
    return _entries_humanities

# 서버 기동 시 사전 로드
try:
    load_science_entries()
    load_humanities_entries()
except: pass

def avg_pct_to_nuback_science(avg_pct: float) -> float:
    """이과 기본 누적백분위 곡선"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.15, 3)
    elif diff <= 2.0: return round(0.15 + (diff - 1.0) * 0.25, 3)
    elif diff <= 4.0: return round(0.40 + (diff - 2.0) * 0.35, 3)
    elif diff <= 7.0: return round(1.10 + (diff - 4.0) * 0.50, 3)
    elif diff <= 12.0: return round(2.60 + (diff - 7.0) * 0.70, 3)
    elif diff <= 20.0: return round(6.10 + (diff - 12.0) * 0.95, 3)
    else: return round(13.70 + (diff - 20.0) * 1.15, 3)

def avg_pct_to_nuback_unified(avg_pct: float) -> float:
    """문과/통합 기본 누적백분위 곡선"""
    if avg_pct >= 100.0: return 0.01
    if avg_pct <= 0.0: return 99.9
    diff = 100.0 - avg_pct
    if diff <= 1.0: return round(diff * 0.12, 3)
    elif diff <= 3.2: return round(0.12 + (diff - 1.0) * 0.33, 3)
    elif diff <= 6.5: return round(0.85 + (diff - 3.2) * 0.60, 3)
    elif diff <= 10.0: return round(2.83 + (diff - 6.5) * 0.75, 3)
    elif diff <= 15.0: return round(5.45 + (diff - 10.0) * 0.90, 3)
    elif diff <= 25.0: return round(9.95 + (diff - 15.0) * 1.00, 3)
    else: return round(19.95 + (diff - 25.0) * 1.10, 3)

def match_target_univ(results, univ_str, dept_str):
    if not univ_str or not results: return None
    u_raw = univ_str.strip()
    u_clean = u_raw.replace("\ub300\ud559\uad50", "").replace("\ub300", "").strip()
    d_clean = (dept_str or "").replace("\ud559\uacfc", "").replace("\ud559\ubd80", "").replace("\uc804\uacf5", "").strip()
    
    univ_matches = [r for r in results if r.get("\ub300\ud559\uad50") == u_raw or r.get("\ub300\ud559\uc57d\uce6d") == u_raw or r.get("\ub300\ud559\uad50") == (u_clean + "\ub300\ud559\uad50") or r.get("\ub300\ud559\uc57d\uce6d") == (u_clean + "\ub300")]
    if not univ_matches:
        univ_matches = [r for r in results if r.get("\ub300\ud559\uad50") and (r.get("\ub300\ud559\uad50").startswith(u_clean) or (r.get("\ub300\ud559\uc57d\uce6d") and r.get("\ub300\ud559\uc57d\uce6d").startswith(u_clean)))]
    if not univ_matches:
        univ_matches = [r for r in results if (r.get("\ub300\ud559\uad50") and u_clean in r.get("\ub300\ud559\uad50")) or (r.get("\ub300\ud559\uc57d\uce6d") and u_clean in r.get("\ub300\ud559\uc57d\uce6d"))]
        
    if not univ_matches: return None
    
    univ_matches.sort(key=lambda x: 1 if ("(" in x.get("\ub300\ud559\uad50", "") or "\ubbf8\ub798" in x.get("\ub300\ud559\uad50", "") or "\uae00\ub85c\uceec" in x.get("\ub300\ud559\uad50", "")) else 0)
    
    if d_clean:
        for r in univ_matches:
            r_clean = r.get("\uc804\uacf5", "").replace("\ud559\uacfc", "").replace("\ud559\ubd80", "").replace("\uc804\uacf5", "").strip()
            if d_clean == "\uc758\uc608" and "\uc218\uc758" in r_clean:
                continue
            if r_clean == d_clean or r_clean.startswith(d_clean) or d_clean.startswith(r_clean):
                return r
        for r in univ_matches:
            r_clean = r.get("\uc804\uacf5", "").replace("\ud559\uacfc", "").replace("\ud559\ubd80", "").replace("\uc804\uacf5", "").strip()
            if d_clean == "\uc758\uc608" and "\uc218\uc758" in r_clean:
                continue
            if d_clean in r_clean or r_clean in d_clean:
                return r
                
    return univ_matches[0]

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
    baseline_univ: str = None,
    baseline_dept: str = None,
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
        
        # 대학별 영어 실질 감점 정밀 모델 (연세대 등 영어 독립반영 대학 치명적 감점)
        eng_conversions = entry.get("\uc601\uc5b4\ud658\uc0b0", [])
        if eng_conversions and len(eng_conversions) >= 9:
            top_score = eng_conversions[0]
            cur_score = eng_conversions[eng_grade - 1] if eng_grade <= len(eng_conversions) else eng_conversions[-1]
            score_diff = abs(top_score - cur_score)
            
            # 연세대학교처럼 영어 감점폭이 극단적인 대학 (2등급 -5점 -> 누백 +3.8% 폭락)
            if "\uc5f0\uc138" in univ_name:
                if eng_grade == 2: student_nuback += 3.8
                elif eng_grade == 3: student_nuback += 8.5
                elif eng_grade >= 4: student_nuback += 15.0
            elif score_diff >= 4.0:
                student_nuback += (score_diff * 0.45)
            elif score_diff >= 2.0:
                student_nuback += (score_diff * 0.25)
            else:
                student_nuback += (score_diff * 0.10)
        else:
            eng_penalties = [0, 0.8, 1.8, 3.2, 5.0, 7.5, 10.5, 14.0, 18.0]
            if 1 <= eng_grade <= 9:
                student_nuback += eng_penalties[eng_grade - 1]
            
        student_nuback += hist_penalty

        verdict = "\uc704\ud5d8"
        safe_cut = entry.get("\uc801\uc815\ub204\ubc31", 0)
        proper_cut = entry.get("\uc608\uc141\ub204\ubc31", 0)
        sosin_cut = entry.get("\uc18c\uc2e0\ub204\ubc31", 0)

        # 판정 비교
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

    target_res = match_target_univ(results, target_univ, target_dept)
    baseline_res = match_target_univ(results, baseline_univ, baseline_dept)

    return {
        "results": results,
        "summary": summary,
        "target_result": target_res,
        "baseline_result": baseline_res
    }
