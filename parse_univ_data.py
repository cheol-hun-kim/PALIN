import os
import json
from pyxlsb import open_workbook

def run_parsing():
    excel_path = "univ_data.xlsx.xlsb"
    app_dir = "app"
    
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found.")
        return
        
    print(f"Parsing {excel_path}...")
    
    univ_departments = {}
    univ_cuts = {}
    
    with open_workbook(excel_path) as wb:
        for sheet_name in ["이과계열분석결과", "문과계열분석결과"]:
            print(f"Processing sheet: {sheet_name}...")
            with wb.get_sheet(sheet_name) as sheet:
                for i, row in enumerate(sheet.rows()):
                    # Skip the first 5 rows (headers)
                    if i < 5:
                        continue
                    
                    row_vals = [cell.v for cell in row]
                    if len(row_vals) < 15:
                        continue
                        
                    계열 = row_vals[0]
                    university = row_vals[1]
                    department = row_vals[2]
                    
                    if not university or not department:
                        continue
                        
                    university = str(university).strip()
                    department = str(department).strip()
                    
                    # Read cuts
                    def clean_cut(val):
                        if val is None:
                            return None
                        if isinstance(val, str):
                            val_clean = val.strip()
                            if val_clean == "-" or val_clean == "":
                                return None
                            try:
                                return float(val_clean)
                            except ValueError:
                                return None
                        try:
                            return float(val)
                        except (ValueError, TypeError):
                            return None

                    적정누백 = clean_cut(row_vals[12])
                    예상누백 = clean_cut(row_vals[13])
                    소신누백 = clean_cut(row_vals[14])
                    
                    # Fill dynamic selectors map
                    if university not in univ_departments:
                        univ_departments[university] = []
                    if department not in univ_departments[university]:
                        univ_departments[university].append(department)
                        
                    # Fill cuts database
                    if university not in univ_cuts:
                        univ_cuts[university] = {}
                        
                    if department not in univ_cuts[university]:
                        univ_cuts[university][department] = {}
                        
                    univ_cuts[university][department][str(계열).strip()] = {
                        "적정누백": 적정누백,
                        "예상누백": 예상누백,
                        "소신누백": 소신누백
                    }
                    
    # Sort university names and their department lists
    sorted_univ_departments = {}
    for univ in sorted(univ_departments.keys()):
        sorted_univ_departments[univ] = sorted(univ_departments[univ])
        
    sorted_univ_cuts = {}
    for univ in sorted(univ_cuts.keys()):
        sorted_univ_cuts[univ] = univ_cuts[univ]
        
    # Write to files
    deps_json_path = os.path.join(app_dir, "univ_departments.json")
    cuts_json_path = os.path.join(app_dir, "univ_cuts.json")
    
    with open(deps_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_univ_departments, f, ensure_ascii=False, indent=2)
        
    with open(cuts_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_univ_cuts, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated {deps_json_path} and {cuts_json_path}")
    print(f"Parsed {len(univ_departments)} universities.")

if __name__ == "__main__":
    run_parsing()
