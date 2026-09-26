# -*- coding: utf-8 -*-
import os, sys
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\1286o\.gemini\antigravity\brain\c1de3934-5a87-4ee0-87ca-1ab3de4dc4df"
STATIC_DIR = r"C:\Users\1286o\.gemini\antigravity\scratch\pass-mate\static\downloads\card_news"

os.makedirs(ARTIFACT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_REG = r"C:\Windows\Fonts\malgun.ttf"

slides_data = [
    {
        "num": "01",
        "tag": "수능 국어의 본질",
        "title": "수능 국어,\n정말 '독해력'이\n부족해서 틀릴까요?",
        "body": "수학, 영어, 탐구도 한글을 독해해서 공부합니다.\n근데 국어 성적만 낮은 학생들은 차고 넘칩니다.\n국어시험 볼 때만 독해력이 부족해진다니\n앞뒤가 맞지 않죠.",
        "accent": "#38bdf8"
    },
    {
        "num": "02",
        "tag": "독해력의 착시",
        "title": "이해해야 문제가 풀린다면,\n이해 못 할 글이 나오면\n틀려야 한다는 뜻입니다.",
        "body": "아무리 많은 문제를 풀고 지식을 습득해도\n결국 수능 때는 이해할 수 없는 글과 새로운 작품이 나옵니다.\n즉 이해력을 길러서 수능 국어를 대비한다는 것은\n애초에 불가능한 일입니다.",
        "accent": "#f59e0b"
    },
    {
        "num": "03",
        "tag": "만점의 비밀",
        "title": "수능 국어는\n국어가 아니었습니다.",
        "body": "출제자의 진짜 의도가 있을 것이라 생각해 모든 기출을 연구했고,\n그 결과 이해력, 독해력 등을 완벽히 배제해야\n항상 만점이 나온다는 사실을 깨달았습니다.",
        "accent": "#a855f7"
    },
    {
        "num": "04",
        "tag": "사교육의 현실",
        "title": "매달 쏟아지는\n고가의 사설 모의고사,\n끝없는 EBS 특강.",
        "body": "그 많은 비용과 시간을 쏟아붓고도\n왜 아이의 국어 성적은\n오르지 않는 것일까요?",
        "accent": "#f87171"
    },
    {
        "num": "05",
        "tag": "평가원의 진실",
        "title": "수능 국어는\n주관적 이해력을\n묻는 시험이 아닙니다.",
        "body": "수십만 명의 수험생들이 동시에 치르는 시험에서\n'이견 없는 단 하나의 정답'을 만들기 위해\n출제자는 '객관적인 규칙' 하나만을 출제의 원리로 정해두었습니다.\n그리고 그것은 오직 기출문제를 통해서만 발견할 수 있습니다.",
        "accent": "#34d399"
    },
    {
        "num": "06",
        "tag": "일원학원의 원칙",
        "title": "사설 문제를 늘리면\n학원 매출은\n쉽게 올라갑니다.",
        "body": "그럼에도 일원학원이\n오직 '기출문제' 하나만을 고집하는 이유",
        "accent": "#fbbf24"
    },
    {
        "num": "07",
        "tag": "절대적 해답",
        "title": "평가원의 출제의도를\n완벽히 담은 시험지는\n'기출문제' 뿐입니다.",
        "body": "거품을 걷어내고 본질만을 봐야 합니다.\n그래야 비용 낭비 없이, 그리고 시간 낭비 없이\n입시를 한 번에 끝낼 수 있게 됩니다.",
        "accent": "#818cf8"
    },
    {
        "num": "08",
        "tag": "입학 안내 및 철학",
        "title": "일원학원은\n수능을 관통하는\n단 하나의 원리만 가르칩니다.\n그것이 수능의 전부입니다.",
        "body": "학원에 오래 다니게 만들기 위한\n학년별 수준별 반편성도, 컨텐츠 장사도 없습니다.\n편견에서 벗어나 진짜 수능의 본질을 마주할 학생을 기다립니다.\n\n블로그 입학안내 : blog.naver.com/12yonsei21 공지참고",
        "accent": "#10b981"
    }
]

W, H = 1080, 1080
TOTAL_SLIDES = len(slides_data)

for idx, s in enumerate(slides_data, 1):
    img = Image.new("RGB", (W, H), color="#0a0b0e")
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle Outer Border / Laser Hairline
    draw.rectangle([(40, 40), (W-40, H-40)], outline="#1e293b", width=2)
    draw.rectangle([(48, 48), (W-48, H-48)], outline="#111827", width=1)
    
    # Accent top-left corner marker
    draw.line([(40, 40), (130, 40)], fill=s["accent"], width=4)
    draw.line([(40, 40), (40, 130)], fill=s["accent"], width=4)
    
    # 2. Header Brand (Left: ONLY ILWON ACADEMY) & Slide Number (Right Pill)
    font_brand = ImageFont.truetype(FONT_BOLD, 32)
    font_num = ImageFont.truetype(FONT_BOLD, 28)
    font_tag = ImageFont.truetype(FONT_BOLD, 22)
    
    # Left Header: Strictly "ILWON ACADEMY" only
    draw.text((80, 75), "ILWON ACADEMY", font=font_brand, fill="#f1f5f9")
    
    # Slide Pill (Right Header: e.g. 01 / 08)
    pill_text = f"{s['num']} / {TOTAL_SLIDES:02d}"
    pill_bbox = font_num.getbbox(pill_text)
    pill_text_w = pill_bbox[2] - pill_bbox[0]
    pill_text_h = pill_bbox[3] - pill_bbox[1]
    
    pill_pad_x = 24
    pill_pad_y = 12
    pill_w = pill_text_w + pill_pad_x * 2
    pill_h = pill_text_h + pill_pad_y * 2
    
    pill_x2 = W - 80
    pill_x1 = pill_x2 - pill_w
    pill_y1 = 70
    pill_y2 = pill_y1 + pill_h
    
    draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=12, fill="#111827", outline=s["accent"], width=2)
    draw.text((pill_x1 + pill_pad_x - pill_bbox[0], pill_y1 + pill_pad_y - pill_bbox[1]), pill_text, font=font_num, fill="#ffffff")
    
    # Category Tag Badge (Dynamic width with proper padding)
    tag_text = f"◆ {s['tag']}"
    tag_bbox = font_tag.getbbox(tag_text)
    tag_text_w = tag_bbox[2] - tag_bbox[0]
    tag_text_h = tag_bbox[3] - tag_bbox[1]
    
    tag_pad_x = 20
    tag_pad_y = 10
    tag_box_w = tag_text_w + tag_pad_x * 2
    tag_box_h = tag_text_h + tag_pad_y * 2
    tag_x1 = 80
    tag_y1 = 195
    
    draw.rounded_rectangle([(tag_x1, tag_y1), (tag_x1 + tag_box_w, tag_y1 + tag_box_h)], radius=8, fill="#111827", outline="#334155", width=1)
    draw.text((tag_x1 + tag_pad_x - tag_bbox[0], tag_y1 + tag_pad_y - tag_bbox[1]), tag_text, font=font_tag, fill=s["accent"])
    
    # 3. Main Title (Large Bold Typography)
    font_title = ImageFont.truetype(FONT_BOLD, 56)
    title_lines = s["title"].split("\n")
    y_text = 280
    for line in title_lines:
        draw.text((80, y_text), line, font=font_title, fill="#ffffff")
        y_text += 78
        
    # Divider line
    y_text += 18
    draw.line([(80, y_text), (W-80, y_text)], fill="#1e293b", width=2)
    draw.line([(80, y_text), (240, y_text)], fill=s["accent"], width=4)
    
    # 4. Body Description (High Readability)
    y_text += 38
    font_body = ImageFont.truetype(FONT_REG, 31)
    body_lines = s["body"].split("\n")
    for line in body_lines:
        if line.startswith("블로그"):
            draw.text((80, y_text), line, font=ImageFont.truetype(FONT_BOLD, 30), fill=s["accent"])
        elif line.strip() == "":
            y_text += 10
            continue
        else:
            draw.text((80, y_text), line, font=font_body, fill="#cbd5e1")
        y_text += 52
        
    # 5. Bottom Footer (Right-aligned: "수능을 관통하는 단 하나의 원리 일원학원")
    font_footer = ImageFont.truetype(FONT_REG, 22)
    footer_text = "수능을 관통하는 단 하나의 원리 · 일원학원"
    
    # Measure text width roughly for right align
    # font_footer.getlength available in Pillow >= 9.2
    try:
        footer_w = draw.textlength(footer_text, font=font_footer)
    except Exception:
        footer_w = len(footer_text) * 20
        
    draw.text((W - 80 - footer_w, H - 85), footer_text, font=font_footer, fill="#94a3b8")
    
    # Save to both Artifact & Static directories
    artifact_path = os.path.join(ARTIFACT_DIR, f"card_slide_{idx}.png")
    static_path = os.path.join(STATIC_DIR, f"card_slide_{idx}.png")
    
    img.save(artifact_path, "PNG")
    img.save(static_path, "PNG")
    print(f"[OK] Slide {idx}/{TOTAL_SLIDES} generated successfully -> {artifact_path}")

print(f"[COMPLETE] All {TOTAL_SLIDES} High-Resolution 1080x1080 Card News Images generated with 100% precision!")
