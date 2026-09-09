"""
PALIN OS Kakao BizMessage (Alimtalk) Engine with SMS Fallback
Kakao Official Approved Templates & 73% Cost Optimization (8 KRW/msg)
"""

import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any

ALIGO_API_KEY = os.getenv("ALIGO_API_KEY", "palin_kakao_live_key_2026")
ALIGO_USER_ID = os.getenv("ALIGO_USER_ID", "palinos_corp")
ALIGO_SENDER = os.getenv("ALIGO_SENDER", "02-1588-1286")
KAKAO_SENDER_KEY = os.getenv("KAKAO_SENDER_KEY", "palin_sender_key_auth")

TEMPLATES = {
    "EXAM_REPORT": {
        "code": "TEMPL_EXAM_01",
        "title": "[PALIN OS] 주차별 실전 모의고사 채점 & 원장 진단서",
        "format": "[PALIN OS 모의고사 채점 결과]\n{student_name} 학생의 {exam_week}주차 {subject} 채점 결과입니다.\n• 획득 원점수: {raw_score}점 ({grade}등급)\n• 오답 문항수: {wrong_count}개\n\n[원장 1:1 맞춤 진단]\n{director_diagnosis}\n\n상세 오답 분석 리포트 확인:\n{report_url}"
    },
    "ATTENDANCE_CARE": {
        "code": "TEMPL_ATTEND_01",
        "title": "[PALIN OS] 재원생 등하원 안심 알림",
        "format": "[PALIN OS 등하원 안심 알림]\n{student_name} 학생이 {time_str}에 {academy_name}에 {status_text}하였습니다.\n오늘도 168시간 자기주도 몰입 학습을 응원합니다!"
    },
    "DISTRACTION_ALERT": {
        "code": "TEMPL_DISTRACT_01",
        "title": "[PALIN OS] 순공 타이머 몰입 케어 알림",
        "format": "[PALIN OS 몰입 케어]\n{student_name} 학생이 순공 타이머 실행 중 타 앱 전환이 감지되었습니다.\n열정 페이스메이커 약정보증금 1,000원이 차감되어 장학금 풀로 이관되었습니다."
    }
}


def send_kakao_alimtalk(
    to_phone: str,
    template_type: str,
    params: Dict[str, Any],
    button_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    카카오 알림톡 공식 발송 (실패 시 SMS 자동 Fallback)
    """
    tmpl = TEMPLATES.get(template_type)
    if not tmpl:
        # Fallback to general SMS
        from app.sms import send_sms
        msg_text = params.get("message", "PALIN OS 알림입니다.")
        return send_sms(to_phone=to_phone, message=msg_text, title="[PALIN OS 알림]")

    clean_phone = to_phone.replace("-", "").strip()
    formatted_msg = tmpl["format"].format(**params)

    # 시뮬레이션 / 실제 API 호출 분기
    # 실환경: Aligo/BizM Kakao API endpoint
    try:
        # Aligo Kakao Alimtalk API
        url = "https://kakaoapi.aligo.in/akv10/alimtalk/send/"
        data = {
            "apikey": ALIGO_API_KEY,
            "userid": ALIGO_USER_ID,
            "senderkey": KAKAO_SENDER_KEY,
            "tpl_code": tmpl["code"],
            "sender": ALIGO_SENDER,
            "receiver_1": clean_phone,
            "subject_1": tmpl["title"],
            "message_1": formatted_msg,
            "failover": "Y", # 실패 시 자동 SMS 대체 발송
            "fsubject_1": tmpl["title"],
            "fmessage_1": formatted_msg
        }
        if button_url:
            data["button_1"] = f'{{"name":"결과 리포트 보기","linkType":"WL","linkTypeName":"웹링크","linkMo":"{button_url}","linkPc":"{button_url}"}}'

        # Live vs Mock test
        if ALIGO_API_KEY == "palin_kakao_live_key_2026":
            # Simulation mode
            return {
                "status": "SUCCESS",
                "mode": "SIMULATION",
                "template_code": tmpl["code"],
                "recipient": clean_phone,
                "cost_krw": 8.0,
                "kakao_mid": f"MOCK_KID_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "message": formatted_msg
            }
        
        resp = requests.post(url, data=data, timeout=5)
        res_json = resp.json()
        if res_json.get("code") == 0:
            return {
                "status": "SUCCESS",
                "mode": "LIVE_KAKAO",
                "template_code": tmpl["code"],
                "recipient": clean_phone,
                "cost_krw": 8.0,
                "kakao_mid": str(res_json.get("info", {}).get("mid", "")),
                "message": formatted_msg
            }
        else:
            # Fallback to SMS
            from app.sms import send_sms
            send_sms(to_phone=to_phone, message=formatted_msg, title=tmpl["title"])
            return {
                "status": "FALLBACK_SMS",
                "mode": "FALLBACK_SMS",
                "template_code": tmpl["code"],
                "recipient": clean_phone,
                "cost_krw": 30.0,
                "error": res_json.get("message"),
                "message": formatted_msg
            }
    except Exception as e:
        # Fallback to SMS
        from app.sms import send_sms
        send_sms(to_phone=to_phone, message=formatted_msg, title=tmpl["title"])
        return {
            "status": "FALLBACK_SMS",
            "mode": "FALLBACK_SMS",
            "template_code": tmpl["code"],
            "recipient": clean_phone,
            "cost_krw": 30.0,
            "error": str(e),
            "message": formatted_msg
        }
