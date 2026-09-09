"""
PALIN OS Toss Payments Enterprise Integration
B2B Monthly SaaS Billing Key & B2C 1-Click Point Checkout Engine
"""

import os
import base64
import requests
from typing import Dict, Any, Optional

TOSS_CLIENT_KEY = os.getenv("TOSS_CLIENT_KEY", "test_ck_D5GePWvyJnrK0W0k6q8gLzN97Eoq")
TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY", "test_sk_zXLkKEypNArWmo50nX3lmeaxYG5R")
TOSS_API_BASE = "https://api.tosspayments.com/v1"


def get_auth_header() -> Dict[str, str]:
    encoded = base64.b64encode(f"{TOSS_SECRET_KEY}:".encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


def confirm_toss_payment(payment_key: str, order_id: str, amount: int) -> Dict[str, Any]:
    """
    토스페이먼츠 일반 결제 승인 API
    """
    # Test Key / Mock Bypass
    if TOSS_SECRET_KEY.startswith("test_sk_"):
        return {
            "status": "DONE",
            "paymentKey": payment_key,
            "orderId": order_id,
            "totalAmount": amount,
            "method": "카드",
            "receipt": {"url": f"https://dashboard.tosspayments.com/receipt/mock_{order_id}"},
            "approvedAt": "2026-09-07T12:00:00+09:00"
        }

    url = f"{TOSS_API_BASE}/payments/confirm"
    payload = {
        "paymentKey": payment_key,
        "orderId": order_id,
        "amount": amount
    }
    resp = requests.post(url, json=payload, headers=get_auth_header(), timeout=10)
    return resp.json()


def issue_toss_billing_key(auth_key: str, customer_key: str) -> Dict[str, Any]:
    """
    토스페이먼츠 자동 결제(빌링키) 발급 API
    """
    if TOSS_SECRET_KEY.startswith("test_sk_"):
        return {
            "billingKey": f"mock_billing_key_{customer_key}",
            "customerKey": customer_key,
            "card": {
                "issuerCode": "61",
                "acquirerCode": "31",
                "number": "43301234****123*",
                "cardType": "신용",
                "ownerType": "법인/개인사업자"
            },
            "authenticatedAt": "2026-09-07T12:00:00+09:00"
        }

    url = f"{TOSS_API_BASE}/billing/authorizations/issue"
    payload = {
        "authKey": auth_key,
        "customerKey": customer_key
    }
    resp = requests.post(url, json=payload, headers=get_auth_header(), timeout=10)
    return resp.json()


def charge_toss_billing(
    billing_key: str,
    customer_key: str,
    amount: int,
    order_id: str,
    order_name: str
) -> Dict[str, Any]:
    """
    발급된 빌링키로 월간 SaaS 구독료 자동 청구/결제 실행
    """
    if TOSS_SECRET_KEY.startswith("test_sk_"):
        return {
            "status": "DONE",
            "paymentKey": f"mock_paykey_{order_id}",
            "orderId": order_id,
            "orderName": order_name,
            "totalAmount": amount,
            "method": "카드(빌링)",
            "receipt": {"url": f"https://dashboard.tosspayments.com/receipt/billing_{order_id}"},
            "approvedAt": "2026-09-07T12:00:00+09:00"
        }

    url = f"{TOSS_API_BASE}/billing/{billing_key}"
    payload = {
        "customerKey": customer_key,
        "amount": amount,
        "orderId": order_id,
        "orderName": order_name
    }
    resp = requests.post(url, json=payload, headers=get_auth_header(), timeout=10)
    return resp.json()
