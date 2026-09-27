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

DEFAULT_CATALOG = [
    # 1. A4 및 복사용지
    {
        "id": "item-a4-01",
        "category": "A4_PAPER",
        "category_name": "복사용지 · A4용지",
        "title": "Double A 더블에이 프리미엄 복사용지 A4 80g 2500매 (5권 1박스)",
        "spec": "80g / 백색도 100% / 무결점 고속출력",
        "price": 28900,
        "raw_url": "https://www.coupang.com/vp/products/6890123456",
        "icon": "article",
        "is_essential": True
    },
    {
        "id": "item-a4-02",
        "category": "A4_PAPER",
        "category_name": "복사용지 · A4용지",
        "title": "밀크(MiLK) 프리미엄 고평량 복사용지 A4 80g 2500매",
        "spec": "한국제지 MiLK / 번짐 방지 / 매끄러운 필기감",
        "price": 27500,
        "raw_url": "https://www.coupang.com/vp/products/6890123457",
        "icon": "description",
        "is_essential": True
    },
    {
        "id": "item-a4-03",
        "category": "A4_PAPER",
        "category_name": "복사용지 · A4용지",
        "title": "페이퍼원(PaperOne) 실속형 복사용지 A4 75g 2500매",
        "spec": "75g / 대량 시험지 출력 최적화 / 가성비 1위",
        "price": 24900,
        "raw_url": "https://www.coupang.com/vp/products/6890123458",
        "icon": "feed",
        "is_essential": False
    },

    # 2. 프린터 토너 및 잉크
    {
        "id": "item-ink-01",
        "category": "PRINTER_INK",
        "category_name": "프린터 토너 · 잉크",
        "title": "삼성 레이저 대용량 토너 카트리지 (MLT-D111S/L 호환)",
        "spec": "1500매 출력 / 흑색 / 선명한 시험지 폰트 렌더링",
        "price": 18500,
        "raw_url": "https://www.coupang.com/vp/products/6890123460",
        "icon": "print",
        "is_essential": True
    },
    {
        "id": "item-ink-02",
        "category": "PRINTER_INK",
        "category_name": "프린터 토너 · 잉크",
        "title": "HP 오피스젯 무한잉크 리필용 벌크 잉크 4색 세트 (각 1000ml)",
        "spec": "BK/C/M/Y 대용량 / 노즐 막힘 방지 포뮬러",
        "price": 32000,
        "raw_url": "https://www.coupang.com/vp/products/6890123461",
        "icon": "format_color_fill",
        "is_essential": True
    },

    # 3. 독서실 & 학습 인프라 소모품
    {
        "id": "item-desk-01",
        "category": "STUDY_DESK",
        "category_name": "독서실 · 학습 인프라",
        "title": "필립스 LED 시력보호 눈부심방지 독서실 스탠드 (밝기 4단계 조절)",
        "spec": "EyeComfort 공인 / 플리커 프리 / 독서실 좌석 최적화",
        "price": 34900,
        "raw_url": "https://www.coupang.com/vp/products/6890123470",
        "icon": "lightbulb",
        "is_essential": True
    },
    {
        "id": "item-desk-02",
        "category": "STUDY_DESK",
        "category_name": "독서실 · 학습 인프라",
        "title": "드레텍 무소음 수능 스톱워치 타이머 (D-Day 카운트 기능 탑재)",
        "spec": "무음 점멸 알람 / 독서실 매너 모드 / 백라이트 지원",
        "price": 12800,
        "raw_url": "https://www.coupang.com/vp/products/6890123471",
        "icon": "timer",
        "is_essential": True
    },
    {
        "id": "item-desk-03",
        "category": "STUDY_DESK",
        "category_name": "독서실 · 학습 인프라",
        "title": "3M 1100 폼 소프트 귀마개 벌크 대용량 200쌍 한 박스 (개별포장)",
        "spec": "NRR 29dB 소음차단 / 위생 개별포장 / 원생 자습 배부용",
        "price": 29800,
        "raw_url": "https://www.coupang.com/vp/products/6890123472",
        "icon": "hearing_disabled",
        "is_essential": True
    },
    {
        "id": "item-desk-04",
        "category": "STUDY_DESK",
        "category_name": "독서실 · 학습 인프라",
        "title": "독서실 의자 긁힘방지 펠트 소음방지 캡 16개 세트 (바닥 무소음)",
        "spec": "고탄성 실리콘 + 두꺼운 펠트바닥 / 독서실 소음 원천 차단",
        "price": 9900,
        "raw_url": "https://www.coupang.com/vp/products/6890123473",
        "icon": "chair",
        "is_essential": False
    },

    # 4. 원생 음료 및 간식
    {
        "id": "item-snack-01",
        "category": "SNACKS",
        "category_name": "원생 간식 · 음료 · 커피",
        "title": "카누 다크로스트 아메리카노 미니 100T 스틱 박스",
        "spec": "원두 분쇄 커피 / 독서실 탕비실 비치용 1위",
        "price": 19500,
        "raw_url": "https://www.coupang.com/vp/products/6890123480",
        "icon": "coffee",
        "is_essential": True
    },
    {
        "id": "item-snack-02",
        "category": "SNACKS",
        "category_name": "원생 간식 · 음료 · 커피",
        "title": "맥심 모카골드 마일드 커피믹스 180T 대용량 박스",
        "spec": "학원 탕비실 필수 상비 / 부드럽고 풍부한 맛",
        "price": 24800,
        "raw_url": "https://www.coupang.com/vp/products/6890123481",
        "icon": "local_cafe",
        "is_essential": True
    },
    {
        "id": "item-snack-03",
        "category": "SNACKS",
        "category_name": "원생 간식 · 음료 · 커피",
        "title": "몬스터 에너지 음료 오리지널 355ml x 24캔 1박스 (고등 수험생용)",
        "spec": "고카페인 에너지 드링크 / 야간 심야 자습 몰입용",
        "price": 31900,
        "raw_url": "https://www.coupang.com/vp/products/6890123482",
        "icon": "bolt",
        "is_essential": False
    },
    {
        "id": "item-snack-04",
        "category": "SNACKS",
        "category_name": "원생 간식 · 음료 · 커피",
        "title": "제주 삼다수 무라벨 생수 500ml x 40병 2박스",
        "spec": "무라벨 친환경 / 정수기 비상용 / 모의고사 배부용",
        "price": 18200,
        "raw_url": "https://www.coupang.com/vp/products/6890123483",
        "icon": "water_bottle",
        "is_essential": True
    },
    {
        "id": "item-snack-05",
        "category": "SNACKS",
        "category_name": "원생 간식 · 음료 · 커피",
        "title": "친환경 무표백 종이컵 6.5온스 1000개입 대용량 벌크 박스",
        "spec": "형광물질 무첨가 / 고온수 누수 방지 코팅",
        "price": 14900,
        "raw_url": "https://www.coupang.com/vp/products/6890123484",
        "icon": "local_drink",
        "is_essential": True
    },

    # 5. 청소 및 위생 방역
    {
        "id": "item-clean-01",
        "category": "CLEANING",
        "category_name": "청소 · 소독 · 위생용품",
        "title": "유한락스 살균소독 스프레이 500ml x 3개 세트 (책상/키보드 소독)",
        "spec": "99.9% 유해세균 살균 / 냄새 제거 / 책상 표면 클리닝",
        "price": 13900,
        "raw_url": "https://www.coupang.com/vp/products/6890123490",
        "icon": "sanitizer",
        "is_essential": True
    },
    {
        "id": "item-clean-02",
        "category": "CLEANING",
        "category_name": "청소 · 소독 · 위생용품",
        "title": "베베숲 시그니처 엠보싱 물티슈 캡형 80매 x 10팩 대용량",
        "spec": "두툼한 평량 / 무자극 안심 성분 / 열람실 상시 비치용",
        "price": 17800,
        "raw_url": "https://www.coupang.com/vp/products/6890123491",
        "icon": "cleaning_services",
        "is_essential": True
    },
    {
        "id": "item-clean-03",
        "category": "CLEANING",
        "category_name": "청소 · 소독 · 위생용품",
        "title": "고밀도 대용량 분리수거 비닐봉투 100L x 50매",
        "spec": "찢어짐 없는 고강도 HDPE / 독서실 폐지 및 쓰레기 수거용",
        "price": 12500,
        "raw_url": "https://www.coupang.com/vp/products/6890123492",
        "icon": "delete",
        "is_essential": True
    },

    # 6. 학원 행정 & 문구 사무용품
    {
        "id": "item-stationery-01",
        "category": "STATIONERY",
        "category_name": "학원 행정 · 사무 문구",
        "title": "3M 포스트잇 큐브 팝업 점착메모지 노랑 400매 x 4개입",
        "spec": "강력 점착 / 원장 상담 메모 및 학생 오답노트 코칭용",
        "price": 11900,
        "raw_url": "https://www.coupang.com/vp/products/6890123500",
        "icon": "note_stack",
        "is_essential": True
    },
    {
        "id": "item-stationery-02",
        "category": "STATIONERY",
        "category_name": "학원 행정 · 사무 문구",
        "title": "미쓰비시 유니 제트스트림 볼펜 0.5mm 흑색 12자루 1다스",
        "spec": "초저점도 유성잉크 / 채점 및 교재 첨삭 최적화",
        "price": 15800,
        "raw_url": "https://www.coupang.com/vp/products/6890123501",
        "icon": "edit",
        "is_essential": True
    },
    {
        "id": "item-stationery-03",
        "category": "STATIONERY",
        "category_name": "학원 행정 · 사무 문구",
        "title": "모나미 생잉크 보드마카 흑/적/청 12자루 세트 (칠판 판서용)",
        "spec": "선명하고 진한 발색 / 캡오프 지속성 / 분진 없는 지움",
        "price": 9900,
        "raw_url": "https://www.coupang.com/vp/products/6890123502",
        "icon": "draw",
        "is_essential": True
    },
    {
        "id": "item-stationery-04",
        "category": "STATIONERY",
        "category_name": "학원 행정 · 사무 문구",
        "title": "피스 평화 대용량 33호 스테이플러 + 침 5박스 세트",
        "spec": "시험지 30장 일괄철 가능 / 고내구성 메탈 바디",
        "price": 8900,
        "raw_url": "https://www.coupang.com/vp/products/6890123503",
        "icon": "attach_file",
        "is_essential": True
    }
]

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
