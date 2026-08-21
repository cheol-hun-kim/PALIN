import os
import json
import requests
from datetime import datetime

SMS_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "sms_settings.json")
SMS_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "sms_log.txt")

def load_sms_settings():
    if os.path.exists(SMS_SETTINGS_FILE):
        try:
            with open(SMS_SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "aligo_key": os.environ.get("ALIGO_KEY", ""),
        "aligo_user_id": os.environ.get("ALIGO_USER_ID", ""),
        "aligo_sender": os.environ.get("ALIGO_SENDER", "")
    }

def save_sms_settings(key: str, user_id: str, sender: str) -> bool:
    try:
        data = {
            "aligo_key": key.strip(),
            "aligo_user_id": user_id.strip(),
            "aligo_sender": sender.strip()
        }
        with open(SMS_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving SMS settings: {e}")
        return False

def check_aligo_remain():
    settings = load_sms_settings()
    key = settings.get("aligo_key")
    user_id = settings.get("aligo_user_id")
    if not key or not user_id:
        return {"status": "mock", "message": "시뮬레이션 모드 (API 키 미설정)", "SMS_CNT": 9999, "LMS_CNT": 9999}
    try:
        url = "https://apis.aligo.in/remain/"
        res = requests.post(url, data={"key": key, "user_id": user_id}, timeout=5)
        if res.status_code == 200:
            return res.json()
        return {"result_code": -1, "message": f"HTTP {res.status_code}"}
    except Exception as e:
        return {"result_code": -1, "message": str(e)}

def send_sms(to_phone: str, message: str, title: str = "[PALIN OS 알림]") -> dict:
    clean_phone = to_phone.replace("-", "").strip()
    log_line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TO: {clean_phone} | TITLE: {title} | MSG: {message}\n"
    print(log_line.strip())
    try:
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

    settings = load_sms_settings()
    key = settings.get("aligo_key")
    user_id = settings.get("aligo_user_id")
    sender = settings.get("aligo_sender")

    if not key or not user_id or not sender:
        return {"result_code": 1, "message": "Mock SMS logged successfully (시뮬레이션 기록 완료)", "mode": "mock"}

    try:
        url = "https://apis.aligo.in/send/"
        payload = {
            "key": key,
            "user_id": user_id,
            "sender": sender,
            "receiver": clean_phone,
            "msg": message,
            "title": title
        }
        res = requests.post(url, data=payload, timeout=8)
        if res.status_code == 200:
            data = res.json()
            return data
        return {"result_code": -1, "message": f"Aligo HTTP {res.status_code}"}
    except Exception as e:
        print(f"Aligo SMS send error: {e}")
        return {"result_code": -1, "message": str(e)}
