"""
Extract admission data from 입시데이터.xlsb and save as JSON for PALIN OS.
Produces: app/data/univ_entries.json
"""
import json
import os
import bisect
from pyxlsb import open_workbook

WB_PATH = r"C:\Users\1286o\.gemini\antigravity\scratch\pass-mate\입시데이터.xlsb"
OUT_DIR = r"C:\Users\1286o\.gemini\antigravity\scratch\pass-mate\app\data"

def safe_float(v, default=0.0):
    if v is None or v == '' or v == '-':
        return default
    try:
        return float(v)
    except (ValueError, TypeError):
        return default

def safe_int(v, default=0):
    if v is None or v == '' or v == '-':
        return default
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return default

def safe_str(v, default=''):
    if v is None:
        return default
    return str(v).strip()


def extract_entries(wb, sheet_name, gyeyeol):
    """Extract university entries from analysis result sheet."""
    entries = []
    with wb.get_sheet(sheet_name) as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 5:
                continue
            vals = [c.v for c in row]
            if len(vals) < 59:
                continue
            if vals[1] is None or safe_str(vals[1]) == '':
                continue
            
            univ = safe_str(vals[1])
            dept = safe_str(vals[2])
            if not univ or not dept:
                continue

            jeok_nuback = safe_float(vals[12], 999)
            yesang_nuback = safe_float(vals[13], 999)
            sosin_nuback = safe_float(vals[14], 999)
            
            eng_scores = []
            for col in range(50, 59):
                eng_scores.append(safe_float(vals[col] if col < len(vals) else None, 0))
            
            entry = {
                "계열": gyeyeol,
                "대학교": univ,
                "전공": dept,
                "대학구분": safe_str(vals[27]),
                "모집군": safe_str(vals[28]),
                "정원": safe_int(vals[29]),
                "시도": safe_str(vals[30]),
                "시군": safe_str(vals[31]),
                "대학약칭": safe_str(vals[33]),
                "전공약칭": safe_str(vals[34]),
                "선발유형": safe_str(vals[35]),
                "점수환산": safe_str(vals[36]),
                "수탐선택": safe_str(vals[37]),
                "수능조합": safe_str(vals[39]),
                "탐구과목수": safe_int(vals[43], 2),
                "국어구성비": safe_float(vals[47], 0.333),
                "수학구성비": safe_float(vals[48], 0.333),
                "탐구구성비": safe_float(vals[49], 0.333),
                "적정점수": safe_float(vals[9]),
                "예상점수": safe_float(vals[10]),
                "소신점수": safe_float(vals[11]),
                "적정누백": jeok_nuback,
                "예상누백": yesang_nuback,
                "소신누백": sosin_nuback,
                "영어환산": eng_scores,
            }
            entries.append(entry)
    
    return entries


def extract_percentage_table(wb):
    """Extract the PERCENTAGE lookup table."""
    percentiles = []
    headers = []
    table = {}
    
    with wb.get_sheet('PERCENTAGE') as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 3:
                continue
            vals = [c.v for c in row]
            
            if i == 3:
                headers = [safe_str(v) for v in vals]
                for h in headers[1:]:
                    if h:
                        table[h] = []
                continue
            
            pct = safe_float(vals[0], -1)
            if pct < 0:
                continue
            percentiles.append(pct)
            
            for j, h in enumerate(headers[1:], 1):
                if h and h in table:
                    table[h].append(safe_float(vals[j] if j < len(vals) else None, 0))
    
    return percentiles, headers, table


def compute_eng_nuback_adjustments(entries, percentiles, pct_table):
    """Pre-compute how each 영어 grade shifts the 누백 position per university."""
    for entry in entries:
        formula_key = entry['점수환산'] + ' ' + entry['계열']
        if formula_key not in pct_table:
            entry["영어누백조정"] = [0, 0.3, 1.0, 2.5, 4.0, 8.0, 12.0, 16.0, 22.0]
            continue
        
        scores = pct_table[formula_key]
        if not scores or len(scores) < 10:
            entry["영어누백조정"] = [0, 0.3, 1.0, 2.5, 4.0, 8.0, 12.0, 16.0, 22.0]
            continue
        
        ref_nuback = entry["예상누백"]
        if ref_nuback >= 999 or ref_nuback <= 0:
            ref_nuback = 1.0
        
        idx = bisect.bisect_left(percentiles, ref_nuback)
        if idx >= len(scores):
            idx = len(scores) - 1
        if idx < 0:
            idx = 0
        
        base_score = scores[idx]
        
        eng_adjustments = []
        for grade_idx in range(9):
            penalty = entry["영어환산"][grade_idx]
            adjusted_score = base_score + penalty
            
            if grade_idx == 0:
                eng_adjustments.append(0.0)
                continue
            
            new_idx = idx
            for k in range(idx, min(len(scores), idx + 500)):
                if scores[k] <= adjusted_score:
                    new_idx = k
                    break
            else:
                new_idx = min(len(scores) - 1, idx + 200)
            
            if new_idx < len(percentiles):
                new_nuback = percentiles[new_idx]
            else:
                new_nuback = percentiles[-1]
            
            shift = round(new_nuback - percentiles[idx], 3)
            if shift < 0:
                shift = 0.0
            eng_adjustments.append(shift)
        
        entry["영어누백조정"] = eng_adjustments


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("Opening workbook...")
    with open_workbook(WB_PATH) as wb:
        print("Extracting 이과계열분석결과...")
        igwa = extract_entries(wb, '이과계열분석결과', '이과')
        print(f"  -> {len(igwa)} entries")
        
        print("Extracting 문과계열분석결과...")
        mungwa = extract_entries(wb, '문과계열분석결과', '문과')
        print(f"  -> {len(mungwa)} entries")
        
        all_entries = igwa + mungwa
        print(f"Total entries: {len(all_entries)}")
        
        print("Extracting PERCENTAGE table...")
        percentiles, headers, pct_table = extract_percentage_table(wb)
        print(f"  -> {len(percentiles)} rows, {len(pct_table)} formula columns")
        
        print("Computing eng grade adjustments...")
        compute_eng_nuback_adjustments(all_entries, percentiles, pct_table)
        
        for entry in all_entries:
            entry["적정점수"] = round(entry["적정점수"], 2)
            entry["예상점수"] = round(entry["예상점수"], 2)
            entry["소신점수"] = round(entry["소신점수"], 2)
            entry["적정누백"] = round(entry["적정누백"], 4)
            entry["예상누백"] = round(entry["예상누백"], 4)
            entry["소신누백"] = round(entry["소신누백"], 4)
        
        out_path = os.path.join(OUT_DIR, "univ_entries.json")
        print(f"Saving to {out_path}...")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(all_entries, f, ensure_ascii=False, indent=1)
        
        univs = set(e["대학교"] for e in all_entries)
        print(f"\n=== Done ===")
        print(f"Entries: {len(all_entries)}, Universities: {len(univs)}")
        
        for e in all_entries[:3]:
            print(f"  {e['대학교']} {e['전공']} ({e['계열']}) "
                  f"적정누백={e['적정누백']}, 예상누백={e['예상누백']}, "
                  f"영어누백조정={e['영어누백조정']}")
        
        file_size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"Output: {file_size_mb:.1f} MB")


if __name__ == "__main__":
    main()
