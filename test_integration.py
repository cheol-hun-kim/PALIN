import urllib.request
import json
import subprocess
import sys
import time

# Reconfigure stdout for UTF-8 to handle emojis in Windows console
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def run_seed():
    print("Re-running database seed...")
    result = subprocess.run([sys.executable, "seed.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Seed stderr:", result.stderr)

def make_request(url, method="GET", data=None):
    req = urllib.request.Request(url, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        json_data = json.dumps(data).encode("utf-8")
    else:
        json_data = None
    
    try:
        with urllib.request.urlopen(req, data=json_data) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print("Response body:", e.read().decode("utf-8"))
        raise e

def test_flow():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Get student 1 info
    print("\n--- Test 1: Get Student Info ---")
    student = make_request(f"{base_url}/api/student/1")
    print(f"Student: {student['name']}, Points: {student['current_points']}, Tutor Profile: {student['tutor_profile']}")
    assert student['id'] == 1
    assert student['current_points'] == 100
    assert student['tutor_profile'] is None
    
    # 2. Trigger mission failure (triggers SMS)
    print("\n--- Test 2: Mission Failure & SMS check ---")
    payload = {
        "student_id": 1,
        "mission_type": "WAKEUP",
        "img_data": "fail"
    }
    res = make_request(f"{base_url}/api/mission/verify", method="POST", data=payload)
    print("Mission verification result:", res)
    assert res['status'] == "FAIL"
    assert res['earned_points'] == 0
    
    # Check if SMS log is generated and not crashed
    with open("sms_log.txt", "r", encoding="utf-8") as f:
        sms_logs = f.readlines()
        print("Last SMS log entry:", sms_logs[-1].strip())
    
    # 3. Upgrade to Tutor
    print("\n--- Test 3: Upgrade to Tutor ---")
    tutor_payload = {
        "student_id": 1,
        "university": "서울대학교",
        "major": "의예과",
        "admission_year": 25,
        "high_school": "대치고",
        "bio": "의대생 선배의 확실한 수학 과외",
        "contact_link": "open.kakao.com/o/testlink"
    }
    tutor = make_request(f"{base_url}/api/tutor/upgrade", method="POST", data=tutor_payload)
    print("Tutor Profile Created:", tutor)
    assert tutor['student_id'] == 1
    assert tutor['univ_emblem'] == "🦁 서울대 의예과 [합격배지] ⚕️"
    
    # Check student points increased (100 + 500 = 600)
    student = make_request(f"{base_url}/api/student/1")
    print(f"Student Points after upgrade: {student['current_points']}")
    assert student['current_points'] == 600
    assert student['tutor_profile'] is not None
    assert student['tutor_profile']['id'] == tutor['id']

    # 3.5. Admission Predict (Susi/Jeongsi split)
    print("\n--- Test 3.5: Admission Prediction (Susi/Jeongsi) ---")
    predict_payload = {
        "student_id": 1,
        "gpa": 2.1,
        "kor_percentile": 92,
        "math_percentile": 88,
        "eng_score": 85,
        "tam1_percentile": 89,
        "tam2_percentile": 90,
        "history_score": 38,
        "target_univ": "연세대학교 신소재공학과",
        "baseline_univ": "국민대학교 신소재공학과"
    }
    pred_res = make_request(f"{base_url}/api/ai/predict", method="POST", data=predict_payload)
    print("Prediction Result Target Susi:", pred_res['target_susi'])
    print("Prediction Result Target Jeongsi:", pred_res['target_jeongsi'])
    assert pred_res['success'] is True
    assert 'target_susi' in pred_res
    assert 'target_jeongsi' in pred_res
    
    # Points should decrease by 50 (600 - 50 = 550)
    student = make_request(f"{base_url}/api/student/1")
    print(f"Student Points after predict: {student['current_points']}")
    assert student['current_points'] == 550
    
    # 3.6. Test Range validation (English score = 150 should throw HTTP Error 422)
    print("\n--- Test 3.6: Score Range Validation (Out of Bounds) ---")
    invalid_payload = predict_payload.copy()
    invalid_payload["eng_score"] = 150
    try:
        make_request(f"{base_url}/api/ai/predict", method="POST", data=invalid_payload)
        assert False, "Should have raised HTTPError for out of bounds score"
    except urllib.error.HTTPError as e:
        print(f"Correctly caught HTTP Error {e.code} for invalid score range.")
        assert e.code == 422

    # 4. Update Tutor Profile
    print("\n--- Test 4: Update Tutor Profile ---")
    update_payload = {
        "tutor_id": tutor['id'],
        "bio": "의대생 선배의 확실한 수학 과외 (수정본)",
        "contact_link": "open.kakao.com/o/testlink_updated"
    }
    updated_tutor = make_request(f"{base_url}/api/tutor/update-profile", method="POST", data=update_payload)
    print("Updated Tutor Bio:", updated_tutor['bio'])
    assert updated_tutor['bio'] == "의대생 선배의 확실한 수학 과외 (수정본)"
    assert updated_tutor['contact_link'] == "open.kakao.com/o/testlink_updated"

    # 5. Create Tutoring Request from Student
    print("\n--- Test 5: Create Tutoring Request ---")
    request_payload = {
        "student_id": 1,
        "subject": "수학",
        "budget": "월 50만원",
        "details": "수능 1등급 대비 미적분 심화 개념 및 문제 풀이"
    }
    tutoring_req = make_request(f"{base_url}/api/tutoring/request", method="POST", data=request_payload)
    print("Tutoring Request:", tutoring_req)
    assert tutoring_req['student_id'] == 1
    assert tutoring_req['subject'] == "수학"
    
    # 6. Propose Tutoring from Tutor
    print("\n--- Test 6: Propose Tutoring from Tutor ---")
    proposal_payload = {
        "tutor_id": tutor['id'],
        "request_id": tutoring_req['id'],
        "message": "안녕하세요. 서울대 의예과 합격생입니다. 성심껏 지도하겠습니다."
    }
    proposal = make_request(f"{base_url}/api/tutoring/propose", method="POST", data=proposal_payload)
    print("Tutoring Proposal:", proposal)
    assert proposal['tutor_id'] == tutor['id']
    assert proposal['status'] == "PENDING"

    # 7. Accept Proposal from Student (triggers SMS log)
    print("\n--- Test 7: Accept Proposal ---")
    accept_payload = {
        "proposalId": proposal['id'],
        "studentId": 1
    }
    accept_res = make_request(f"{base_url}/api/tutoring/accept", method="POST", data=accept_payload)
    print("Accept Result:", accept_res)
    assert accept_res['success'] is True
    assert accept_res['tutor_contact'] == student['phone'] # tutor phone matches student phone in this test
    
    # Verify SMS was sent to tutor
    with open("sms_log.txt", "r", encoding="utf-8") as f:
        sms_logs = f.readlines()
        print("Last SMS log entry after accept:", sms_logs[-1].strip())
        
    print("\n🎉 ALL FLOW TESTS PASSED SUCCESSFULLY! NO ENCODING ERRORS DETECTED.")

if __name__ == "__main__":
    run_seed()
    test_flow()
