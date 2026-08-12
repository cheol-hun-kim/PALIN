import sys
from pyxlsb import open_workbook

sys.stdout.reconfigure(encoding='utf-8')
file_path = "univ_data.xlsx.xlsb"

try:
    with open_workbook(file_path) as wb:
        for sheet_name in ['이과계열분석결과', '문과계열분석결과']:
            print(f"\n--- Searching for 국민대학교 or 중앙대학교 in '{sheet_name}' ---")
            with wb.get_sheet(sheet_name) as sheet:
                count = 0
                for i, row in enumerate(sheet.rows()):
                    row_vals = [cell.v for cell in row]
                    if len(row_vals) > 2 and row_vals[1] and ('국민대' in str(row_vals[1]) or '중앙대' in str(row_vals[1])):
                        print(f"Row {i}: {row_vals[:10]}")
                        count += 1
                        if count >= 10:
                            break
except Exception as e:
    print(f"Error: {e}")
