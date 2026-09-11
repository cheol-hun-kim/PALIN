import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Tuple

EMAIL_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "email_settings.json")
EMAIL_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "email_log.txt")

def load_email_settings() -> Dict[str, Any]:
    """
    Loads SMTP email configuration from JSON file or environment variables.
    """
    if os.path.exists(EMAIL_SETTINGS_FILE):
        try:
            with open(EMAIL_SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "smtp_user": data.get("smtp_user", "").strip(),
                    "smtp_password": data.get("smtp_password", "").strip(),
                    "smtp_host": data.get("smtp_host", "smtp.gmail.com").strip(),
                    "smtp_port": int(data.get("smtp_port", 587)),
                    "from_name": data.get("from_name", "PASS MATE (PALIN)").strip()
                }
        except Exception as e:
            print(f"[EMAIL SETTINGS] Error reading {EMAIL_SETTINGS_FILE}: {e}")

    return {
        "smtp_user": os.environ.get("SMTP_USER", "").strip(),
        "smtp_password": os.environ.get("SMTP_PASSWORD", "").strip(),
        "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com").strip(),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "from_name": os.environ.get("SMTP_FROM_NAME", "PASS MATE (PALIN)").strip()
    }

def save_email_settings(smtp_user: str, smtp_password: str, smtp_host: str = "smtp.gmail.com", smtp_port: int = 587, from_name: str = "PASS MATE (PALIN)") -> bool:
    """
    Saves SMTP settings to email_settings.json.
    """
    try:
        data = {
            "smtp_user": smtp_user.strip(),
            "smtp_password": smtp_password.strip(),
            "smtp_host": smtp_host.strip() if smtp_host else "smtp.gmail.com",
            "smtp_port": int(smtp_port) if smtp_port else 587,
            "from_name": from_name.strip() if from_name else "PASS MATE (PALIN)"
        }
        with open(EMAIL_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[EMAIL SETTINGS] Successfully saved SMTP settings for user: {smtp_user}")
        return True
    except Exception as e:
        print(f"[EMAIL SETTINGS] Error saving SMTP settings: {e}")
        return False

def test_smtp_connection(to_email: str) -> Tuple[bool, str]:
    """
    Tests SMTP connection by sending a diagnostic verification email.
    """
    cfg = load_email_settings()
    smtp_user = cfg.get("smtp_user", "")
    smtp_password = cfg.get("smtp_password", "")
    smtp_host = cfg.get("smtp_host", "smtp.gmail.com")
    smtp_port = cfg.get("smtp_port", 587)
    from_name = cfg.get("from_name", "PASS MATE (PALIN)")

    if not smtp_user or not smtp_password:
        return False, "SMTP 사용자 계정(이메일) 또는 앱 비밀번호가 설정되지 않았습니다."

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "[PASS MATE] SMTP 메일 발송 서버 연동 테스트 성공"
        msg["From"] = f"{from_name} <{smtp_user}>"
        msg["To"] = to_email

        html = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; background: #0f172a; color: #ffffff; border-radius: 12px;">
            <h2 style="color: #38bdf8; margin-top: 0;">PASS MATE SMTP 연동 테스트</h2>
            <p>이 메일이 정상 수신되었다면 PASS MATE의 실시간 이메일 발송 서버(SMTP)가 완벽하게 연동된 것입니다.</p>
            <p style="font-size: 12px; color: #94a3b8;">발송 계정: {smtp_user} | 호스트: {smtp_host}:{smtp_port}</p>
        </div>
        """
        msg.attach(MIMEText(html, "html", "utf-8"))

        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()

        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        return True, "테스트 메일이 성공적으로 발송되었습니다."
    except Exception as e:
        return False, f"SMTP 연결 실패: {str(e)}"

def send_real_email_otp(to_email: str, otp_code: str) -> Tuple[bool, str]:
    """
    Sends authentic 6-digit OTP email using configured SMTP.
    Returns (True, "OK") or (False, "Error description").
    """
    cfg = load_email_settings()
    smtp_user = cfg.get("smtp_user", "")
    smtp_password = cfg.get("smtp_password", "")
    smtp_host = cfg.get("smtp_host", "smtp.gmail.com")
    smtp_port = cfg.get("smtp_port", 587)
    from_name = cfg.get("from_name", "PASS MATE (PALIN)")

    if not smtp_user or not smtp_password:
        err_msg = "SMTP 메일 발송 계정이 설정되지 않았습니다. 관리자 콘솔에서 SMTP 계정(Gmail 앱 비밀번호 등)을 설정해 주세요."
        print(f"⚠️ [EMAIL OTP FAILED] {err_msg}")
        return False, err_msg

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>PASS MATE 본인인증 번호</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0f172a; padding: 30px 15px;">
            <tr>
                <td align="center">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 520px; background-color: #1e1b4b; border: 1.5px solid #6366f1; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                        <tr>
                            <td style="padding: 28px 24px; text-align: center;">
                                <div style="font-size: 24px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 4px;">
                                    PASS MATE <span style="font-size: 13px; color: #818cf8; font-weight: 800;">by PALIN</span>
                                </div>
                                <div style="font-size: 13px; color: #94a3b8;">
                                    수험생 입시 관제 플랫폼 본인인증
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 24px 28px 24px;">
                                <div style="background-color: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 24px 16px; text-align: center;">
                                    <div style="font-size: 14px; color: #c7d2fe; margin-bottom: 12px; font-weight: 600;">
                                        아래의 6자리 인증번호를 회원가입 화면에 입력해 주세요.
                                    </div>
                                    <div style="font-size: 34px; font-weight: 900; letter-spacing: 10px; color: #38bdf8; background-color: rgba(15, 23, 42, 0.7); border: 1px dashed #38bdf8; border-radius: 10px; padding: 14px 0; margin-bottom: 12px;">
                                        {otp_code}
                                    </div>
                                    <div style="font-size: 12px; color: #f43f5e; font-weight: 700;">
                                        유효시간: 5분 (300초 이내 입력)
                                    </div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 24px 24px 24px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 18px;">
                                <div style="font-size: 11px; color: #64748b; line-height: 1.5;">
                                    본인이 요청하지 않은 경우 이 메일을 즉시 무시해 주세요.<br>
                                    © PALIN Corp. All rights reserved.
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[PASS MATE] 회원가입 본인인증 번호 [{otp_code}]"
        msg["From"] = f"{from_name} <{smtp_user}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=8)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=8)
            server.starttls()

        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()

        print(f"📧 [REAL SMTP SUCCESS] Sent OTP [{otp_code}] to [{to_email}]")
        return True, "OK"
    except Exception as e:
        err_str = f"SMTP 전송 오류 ({str(e)})"
        print(f"⚠️ [REAL SMTP ERROR] Failed to send email to {to_email}: {err_str}")
        return False, err_str
