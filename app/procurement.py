import json
import os
import re
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any, Optional

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "coupang_partners_config.json")
CUSTOM_ITEMS_FILE = os.path.join(os.path.dirname(__file__), "..", "custom_procurement_items.json")
TEXTBOOK_ORDERS_FILE = os.path.join(os.path.dirname(__file__), "..", "textbook_orders.json")
RENTAL_INQUIRIES_FILE = os.path.join(os.path.dirname(__file__), "..", "rental_inquiries.json")

DEFAULT_PARTNER_ID = "AF5491299"
DEFAULT_SUB_ID = "palin_b2b"

DEFAULT_CATALOG = []

def load_coupang_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if not cfg.get("partner_id"):
                    cfg["partner_id"] = DEFAULT_PARTNER_ID
                if not cfg.get("sub_id"):
                    cfg["sub_id"] = DEFAULT_SUB_ID
                return cfg
        except Exception:
            pass
    
    cfg = {
        "partner_id": DEFAULT_PARTNER_ID,
        "sub_id": DEFAULT_SUB_ID,
        "access_key": "",
        "secret_key": "",
        "auto_rewrite_enabled": True,
        "updated_at": datetime.now().isoformat()
    }
    save_coupang_config(cfg)
    return cfg

def save_coupang_config(cfg: Dict[str, Any]):
    cfg["updated_at"] = datetime.now().isoformat()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def build_affiliate_url(raw_url: str, partner_id: Optional[str] = None, sub_id: Optional[str] = None) -> str:
    cfg = load_coupang_config()
    p_id = partner_id or cfg.get("partner_id") or DEFAULT_PARTNER_ID
    s_id = sub_id or cfg.get("sub_id") or DEFAULT_SUB_ID

    if not raw_url or not raw_url.strip():
        return f"https://www.coupang.com/np/search?component=&q={urllib.parse.quote('학원 비품')}&lptag={p_id}&subid={s_id}"

    raw_url = raw_url.strip()

    # If it's already a short partners link or coupang link, attach/rewrite tracking params
    if "coupang.com" in raw_url:
        parsed = urllib.parse.urlparse(raw_url)
        query_dict = urllib.parse.parse_qs(parsed.query)
        query_dict["lptag"] = [p_id]
        query_dict["subid"] = [s_id]
        new_query = urllib.parse.urlencode(query_dict, doseq=True)
        return urllib.parse.urlunparse((parsed.scheme or "https", parsed.netloc or "www.coupang.com", parsed.path, parsed.params, new_query, parsed.fragment))

    # If keyword is provided instead of url
    return f"https://www.coupang.com/np/search?component=&q={urllib.parse.quote(raw_url)}&lptag={p_id}&subid={s_id}"

def get_procurement_catalog() -> List[Dict[str, Any]]:
    cfg = load_coupang_config()
    partner_id = cfg.get("partner_id", DEFAULT_PARTNER_ID)
    sub_id = cfg.get("sub_id", DEFAULT_SUB_ID)

    items = []
    for item in DEFAULT_CATALOG:
        c_item = dict(item)
        c_item["affiliate_url"] = build_affiliate_url(item["raw_url"], partner_id, sub_id)
        items.append(c_item)

    # Load custom items
    custom_items = load_custom_items()
    for c in custom_items:
        c_item = dict(c)
        c_item["affiliate_url"] = build_affiliate_url(c["raw_url"], partner_id, sub_id)
        items.append(c_item)

    return items

def load_custom_items() -> List[Dict[str, Any]]:
    if os.path.exists(CUSTOM_ITEMS_FILE):
        try:
            with open(CUSTOM_ITEMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def add_custom_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
    items = load_custom_items()
    item_id = f"custom-{int(datetime.now().timestamp() * 1000)}"
    new_item = {
        "id": item_id,
        "category": item_data.get("category", "CUSTOM"),
        "category_name": item_data.get("category_name", "원장 등록 비품"),
        "title": item_data.get("title", "맞춤 비품"),
        "spec": item_data.get("spec", "원장 지정 필수 소모품"),
        "price": int(item_data.get("price", 0)),
        "raw_url": item_data.get("raw_url", ""),
        "icon": item_data.get("icon", "shopping_bag"),
        "is_essential": False,
        "is_custom": True,
        "created_at": datetime.now().isoformat()
    }
    items.insert(0, new_item)
    with open(CUSTOM_ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    return new_item

def delete_custom_item(item_id: str) -> bool:
    items = load_custom_items()
    filtered = [i for i in items if i.get("id") != item_id]
    if len(filtered) != len(items):
        with open(CUSTOM_ITEMS_FILE, "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        return True
    return False

# ==================== 사설 모의고사 & 교재 B2B 발주 ====================

def load_textbook_orders() -> List[Dict[str, Any]]:
    if os.path.exists(TEXTBOOK_ORDERS_FILE):
        try:
            with open(TEXTBOOK_ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def create_textbook_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    orders = load_textbook_orders()
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(orders) + 1:04d}"
    new_order = {
        "id": order_id,
        "tenant_code": order_data.get("tenant_code", "ILWON-2027"),
        "academy_name": order_data.get("academy_name", "일원학원"),
        "publisher": order_data.get("publisher", "대성 마이맥"),
        "textbook_name": order_data.get("textbook_name", ""),
        "quantity": int(order_data.get("quantity", 10)),
        "unit_price": int(order_data.get("unit_price", 15000)),
        "total_amount": int(order_data.get("quantity", 10)) * int(order_data.get("unit_price", 15000)),
        "delivery_address": order_data.get("delivery_address", ""),
        "contact_phone": order_data.get("contact_phone", ""),
        "notes": order_data.get("notes", ""),
        "status": "ORDER_SUBMITTED", # ORDER_SUBMITTED | CONFIRMED | SHIPPING | DELIVERED
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    orders.insert(0, new_order)
    with open(TEXTBOOK_ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    return new_order

# ==================== 아정당형 B2B 렌탈 & 인프라 제휴 ====================

def load_rental_inquiries() -> List[Dict[str, Any]]:
    if os.path.exists(RENTAL_INQUIRIES_FILE):
        try:
            with open(RENTAL_INQUIRIES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def create_rental_inquiry(inquiry_data: Dict[str, Any]) -> Dict[str, Any]:
    inquiries = load_rental_inquiries()
    inquiry_id = f"RNT-{datetime.now().strftime('%Y%m%d')}-{len(inquiries) + 1:04d}"
    new_inquiry = {
        "id": inquiry_id,
        "tenant_code": inquiry_data.get("tenant_code", "ILWON-2027"),
        "academy_name": inquiry_data.get("academy_name", "일원학원"),
        "director_name": inquiry_data.get("director_name", "원장"),
        "phone": inquiry_data.get("phone", ""),
        "items": inquiry_data.get("items", []), # ['복합기', '정수기', '공기청정기', 'CCTV', '기가인터넷']
        "preferred_company": inquiry_data.get("preferred_company", "무관(최저가/최대지원금)"),
        "notes": inquiry_data.get("notes", ""),
        "cashback_estimate": len(inquiry_data.get("items", [])) * 150000, # 대당 평균 지원금 약 15~30만원
        "status": "SUBMITTED", # SUBMITTED | CONSULTING | CONTRACT_COMPLETED
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    inquiries.insert(0, new_inquiry)
    with open(RENTAL_INQUIRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(inquiries, f, ensure_ascii=False, indent=2)
    return new_inquiry
