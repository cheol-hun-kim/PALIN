import urllib.request
import json

url = "http://127.0.0.1:8000/api/ai/predict"
data = {
    "student_id": 1,
    "target_univ": "연세대학교 의예과",
    "baseline_univ": "연세대학교 의예과",
    "gpa": 2.1,
    "kor_percentile": 92,
    "math_percentile": 88,
    "eng_score": 85,
    "tam1_percentile": 89,
    "tam2_percentile": 90,
    "history_score": 38
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as resp:
        print("STATUS:", resp.status)
        res_json = json.loads(resp.read().decode("utf-8"))
        print("KEYS:", res_json.keys())
        print("RESPONSE:", json.dumps(res_json, ensure_ascii=False, indent=2))
except Exception as e:
    print("ERROR:", e)
