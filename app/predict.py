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
        os.path.join(os.getcwd(), "static", "data", filename),
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
            _entries_humanities = []
    return _entries_humanities

# 고속성장분석기 엑셀 1:1 이과 누적백분위 변환 공식 (95,501명 이과 표본)
def avg_pct_to_nuback_science(avg_pct: float) -> float:
    sum300 = avg_pct * 3.0
    if sum300 >= 299.5: nb = 0.01
    elif sum300 >= 298.0: nb = 0.01 + (299.5 - sum300) / 1.5 * 0.19
    elif sum300 >= 295.0: nb = 0.20 + (298.0 - sum300) / 3.0 * 0.60
    elif sum300 >= 290.0: nb = 0.80 + (295.0 - sum300) / 5.0 * 1.70
    elif sum300 >= 285.0: nb = 2.50 + (290.0 - sum300) / 5.0 * 2.15
    elif sum300 >= 280.0: nb = 4.65 + (285.0 - sum300) / 5.0 * 2.55
    elif sum300 >= 275.0: nb = 7.20 + (280.0 - sum300) / 5.0 * 2.70
    elif sum300 >= 270.0: nb = 9.90 + (275.0 - sum300) / 5.0 * 2.75
    elif sum300 >= 260.0: nb = 12.65 + (270.0 - sum300) / 10.0 * 6.45
    elif sum300 >= 250.0: nb = 19.10 + (260.0 - sum300) / 10.0 * 6.40
    elif sum300 >= 240.0: nb = 25.50 + (250.0 - sum300) / 10.0 * 6.50
    elif sum300 >= 220.0: nb = 32.00 + (240.0 - sum300) / 20.0 * 14.0
    else: nb = min(99.0, 46.00 + (220.0 - sum300) * 0.70)
    return round(nb, 3)

# 고속성장분석기 엑셀 1:1 문과 누적백분위 변환 공식 (375,873명 문과 표본)
def avg_pct_to_nuback_humanities(avg_pct: float) -> float:
    sum300 = avg_pct * 3.0
    if sum300 >= 298.0: nb = 0.01
    elif sum300 >= 295.0: nb = 0.01 + (298.0 - sum300) / 3.0 * 0.06
    elif sum300 >= 290.0: nb = 0.07 + (295.0 - sum300) / 5.0 * 0.29
    elif sum300 >= 285.0: nb = 0.36 + (290.0 - sum300) / 5.0 * 0.54
    elif sum300 >= 280.0: nb = 0.90 + (285.0 - sum300) / 5.0 * 0.80
    elif sum300 >= 275.0: nb = 1.70 + (280.0 - sum300) / 5.0 * 0.99
    elif sum300 >= 270.0: nb = 2.69 + (275.0 - sum300) / 5.0 * 1.08
    elif sum300 >= 260.0: nb = 3.77 + (270.0 - sum300) / 10.0 * 2.69
    elif sum300 >= 250.0: nb = 6.46 + (260.0 - sum300) / 10.0 * 3.00
    elif sum300 >= 240.0: nb = 9.46 + (250.0 - sum300) / 10.0 * 3.64
    elif sum300 >= 220.0: nb = 13.10 + (240.0 - sum300) / 20.0 * 8.40
    else: nb = min(99.0, 21.50 + (220.0 - sum300) * 0.47)
    return round(nb, 3)

def match_target_univ(results, univ_str, dept_str):
    if not univ_str or not results:
        return None
    u_raw = univ_str.strip()
    u_clean = u_raw.replace("대학교", "").replace("대학", "").replace("대", "").strip()
    
    d_raw = (dept_str or "").strip()
    d_clean = d_raw.replace("학과", "").replace("학부", "").replace("전공", "").replace("과", "").strip()
    
    # 1. 대학 필터링
    univ_matches = [r for r in results if r.get("대학교") == u_raw or r.get("대학약칭") == u_raw or r.get("대학교") == (u_clean + "대학교") or r.get("대학약칭") == (u_clean + "대")]
    if not univ_matches:
        univ_matches = [r for r in results if r.get("대학교") and (r.get("대학교").startswith(u_clean) or (r.get("대학약칭") and r.get("대학약칭").startswith(u_clean)))]
    if not univ_matches:
        univ_matches = [r for r in results if (r.get("대학교") and u_clean in r.get("대학교")) or (r.get("대학약칭") and u_clean in r.get("대학약칭"))]
        
    if not univ_matches:
        return None
        
    # 본교 우선 정렬 (분교/글로컬 뒤로)
    univ_matches.sort(key=lambda x: 1 if ("(" in x.get("대학교", "") or "미래" in x.get("대학교", "") or "글로컬" in x.get("대학교", "") or "세종" in x.get("대학교", "")) else 0)
    
    if not d_raw and not d_clean:
        return univ_matches[0]
        
    # 2. 전공 정밀 스코어링 매처 (Score-based Major Matcher)
    best_match = None
    best_score = -1
    
    for r in univ_matches:
        r_dept = r.get("전공", "").strip()
        r_clean = r_dept.replace("학과", "").replace("학부", "").replace("전공", "").replace("과", "").strip()
        
        # 특수 예외 필터링 (의예 vs 수의예 혼동 방지)
        if d_clean == "의예" and "수의" in r_clean:
            continue
        if "수의" in d_clean and r_clean == "의예":
            continue
            
        score = 0
        
        # 1) 원본 전공명 완전 일치 (1000점)
        if r_dept == d_raw:
            score = 1000
        # 2) 정제 전공명 완전 일치 (900점) (화학생물공학 == 화학생물공학)
        elif r_clean == d_clean:
            score = 900
        # 3) 접두/접미 포함 (길이 차이가 적을수록 고득점)
        elif r_clean.startswith(d_clean) or d_clean.startswith(r_clean):
            len_diff = abs(len(r_clean) - len(d_clean))
            score = 850 - (len_diff * 15)
        # 4) 부분 포함
        elif d_clean in r_clean or r_clean in d_clean:
            len_diff = abs(len(r_clean) - len(d_clean))
            score = 700 - (len_diff * 15)
        # 5) 공통 글자 매칭
        else:
            common_chars = sum(1 for c in d_clean if c in r_clean)
            if common_chars >= 2:
                score = 500 + common_chars * 20 - abs(len(r_clean) - len(d_clean)) * 10
                
        if score > best_score:
            best_score = score
            best_match = r
            
    if best_match and best_score > 0:
        return best_match
        
    return univ_matches[0]

def predict_admission(
    kor_pct: float,
    math_pct: float,
    eng_raw: int,
    tam1_pct: float,
    tam2_pct: float,
    hist_raw: int,
    math_type: str = "미적",
    tam1_type: str = "과탐",
    tam2_type: str = "과탐",
    gyeyeol: str = "이과",
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

    is_math_calc = math_type in ["미적", "기하"]
    science_tam_count = (1 if tam1_type == "과탐" else 0) + (1 if tam2_type == "과탐" else 0)
    is_pure_science = is_math_calc and science_tam_count == 2
    
    # 순수 이과 vs 문과/교차지원 엑셀 시트 선택
    if is_pure_science:
        entries = load_science_entries()
    else:
        entries = load_humanities_entries()

    STRICT_SCIENCE_UNIVS = ["서울대학교", "서울대"]

    results = []
    summary = { "안정": 0, "적정": 0, "소신": 0, "위험": 0 }

    for entry in entries:
        univ_name = entry.get("대학교", "")
        dept_name = entry.get("전공", "")
        entry_gyeyeol = entry.get("계열", "")
        
        # 서울대 등 미적+과탐 필수 대학 필터
        if entry_gyeyeol == "이과" and any(s_univ in univ_name for s_univ in STRICT_SCIENCE_UNIVS):
            if science_tam_count < 2 or not is_math_calc:
                continue

        tam1_effective = tam1_pct
        tam2_effective = tam2_pct
        if entry_gyeyeol == "이과" and is_pure_science:
            if tam1_type == "과탐": tam1_effective = min(100.0, tam1_pct * 1.03)
            if tam2_type == "과탐": tam2_effective = min(100.0, tam2_pct * 1.03)

        kor_weight = entry.get("국어구성비", 0.3)
        math_weight = entry.get("수학구성비", 0.35)
        tam_weight = entry.get("탐구구성비", 0.35)
        
        total_weight = kor_weight + math_weight + tam_weight
        if total_weight == 0: total_weight = 1.0
            
        avg_pct = (kor_pct * kor_weight + math_pct * math_weight + ((tam1_effective + tam2_effective) / 2) * tam_weight) / total_weight
        
        # 계열별 정확한 누백 계산식 매핑 (문과 표본 vs 이과 표본)
        if is_pure_science:
            student_nuback = avg_pct_to_nuback_science(avg_pct)
        else:
            # 확통/사탐 응시자의 경우 문과 시트의 컷과 비교하므로 문과 누백 적용!
            student_nuback = avg_pct_to_nuback_humanities(avg_pct)
        
        # 영어 등급 감점
        eng_conversions = entry.get("영어환산", [])
        if eng_conversions and len(eng_conversions) >= 9:
            top_score = eng_conversions[0]
            cur_score = eng_conversions[eng_grade - 1] if eng_grade <= len(eng_conversions) else eng_conversions[-1]
            score_diff = abs(top_score - cur_score)
            
            if "연세" in univ_name:
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
            eng_penalties = [0, 0.5, 1.2, 2.2, 3.8, 5.5, 8.0, 11.0, 15.0] if not is_pure_science else [0, 0.8, 1.8, 3.2, 5.0, 7.5, 10.5, 14.0, 18.0]
            if 1 <= eng_grade <= 9:
                student_nuback += eng_penalties[eng_grade - 1]
            
        student_nuback += hist_penalty
        student_nuback = round(student_nuback, 2)

        safe_cut = entry.get("적정누백", 0)
        proper_cut = entry.get("예상누백", 0)
        sosin_cut = entry.get("소신누백", 0)

        # 엑셀 실측 기준 대소 판정
        verdict = "위험"
        if student_nuback <= safe_cut:
            verdict = "안정"
        elif student_nuback <= proper_cut:
            verdict = "적정"
        elif student_nuback <= sosin_cut:
            verdict = "소신"
        else:
            verdict = "위험"

        summary[verdict] += 1

        results.append({
            "대학교": univ_name,
            "전공": dept_name,
            "대학약칭": entry.get("대학약칭", univ_name),
            "전공약칭": entry.get("전공약칭", dept_name),
            "계열": entry_gyeyeol,
            "모집군": entry.get("모집군", "가"),
            "대학구분": entry.get("대학구분", "일반"),
            "시도": entry.get("시도", "전국"),
            "student_nuback": student_nuback,
            "verdict": verdict,
            "적정누백": safe_cut,
            "예상누백": proper_cut,
            "소신누백": sosin_cut
        })

    target_res = match_target_univ(results, target_univ, target_dept)
    baseline_res = match_target_univ(results, baseline_univ, baseline_dept)

    return {
        "target_result": target_res,
        "baseline_result": baseline_res,
        "results": results,
        "summary": summary
    }
