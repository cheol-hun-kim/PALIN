import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')
cuts_path = os.path.join("app", "univ_cuts.json")
if os.path.exists(cuts_path):
    with open(cuts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("--- Total Universities:", len(data.keys()))
    matched = [k for k in data.keys() if any(x in k for x in ["연세", "서울", "가천", "고려"])]
    for m in matched:
        print("KEY:", repr(m))
