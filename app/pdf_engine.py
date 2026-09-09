# -*- coding: utf-8 -*-
"""
PALIN OS Professional Examination Material & Workbook PDF Generator
Zero-Garbled Korean Character Rendering (Malgun Gothic & Standard CID CJK)
Generates authentic multi-page 수능/모의평가 evaluation exam papers & answer sheets.
"""

import os
import io
from datetime import datetime

REPORTLAB_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

FONT_NAME = "Helvetica"
FONT_NAME_BOLD = "Helvetica-Bold"

if REPORTLAB_AVAILABLE:
    try:
        windows_font = "C:/Windows/Fonts/malgun.ttf"
        windows_font_bd = "C:/Windows/Fonts/malgunbd.ttf"
        if os.path.exists(windows_font):
            pdfmetrics.registerFont(TTFont("MalgunGothic", windows_font))
            if os.path.exists(windows_font_bd):
                pdfmetrics.registerFont(TTFont("MalgunGothic-Bold", windows_font_bd))
            else:
                pdfmetrics.registerFont(TTFont("MalgunGothic-Bold", windows_font))
            FONT_NAME = "MalgunGothic"
            FONT_NAME_BOLD = "MalgunGothic-Bold"
        else:
            pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
            FONT_NAME = 'HYGothic-Medium'
            FONT_NAME_BOLD = 'HYGothic-Medium'
    except Exception:
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('HYGothic-Medium'))
            FONT_NAME = 'HYGothic-Medium'
            FONT_NAME_BOLD = 'HYGothic-Medium'
        except Exception:
            FONT_NAME = 'Helvetica'
            FONT_NAME_BOLD = 'Helvetica-Bold'


def generate_exam_material_pdf(
    subject: str,
    title: str,
    description: str = "",
    year: int = 2027,
    is_answer_sheet: bool = False
) -> bytes:
    if not REPORTLAB_AVAILABLE:
        return _generate_pure_python_exam_pdf(subject, title, description, year, is_answer_sheet)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    header_color = colors.HexColor("#1e1b4b") if not is_answer_sheet else colors.HexColor("#064e3b")
    accent_color = colors.HexColor("#4338ca") if not is_answer_sheet else colors.HexColor("#059669")
    badge_type = "📝 정답 및 심층 해설지" if is_answer_sheet else "📖 공식 수험 기출문제집"

    # =========================================================================
    # PAGE 1: 표지 및 실전 1부 (문항 1~15번 & 독서/기초 지문)
    # =========================================================================
    p.setFillColor(header_color)
    p.rect(0, height - 105, width, 105, fill=1, stroke=0)

    p.setFillColor(colors.HexColor("#ffffff"))
    p.setFont(FONT_NAME_BOLD, 20)
    p.drawString(40, height - 42, "PALIN OS 실전 대학수학능력시험 평가원 모의고사")

    p.setFont(FONT_NAME, 10)
    p.drawString(40, height - 62, "인생 2회차의 지혜와 데이터가 이끄는, 168시간 자기주도 몰입 OS")

    p.setFont(FONT_NAME_BOLD, 12)
    p.drawRightString(width - 40, height - 42, f"[{year}학년도] {badge_type}")

    p.setFont(FONT_NAME, 9)
    p.drawRightString(width - 40, height - 62, f"발행: PALIN 수능입시연구소 · {datetime.now().strftime('%Y년 %m월')}")

    # Subject & Title Banner
    p.setFillColor(colors.HexColor("#f8fafc"))
    p.roundRect(35, height - 195, width - 70, 78, 6, fill=1, stroke=1)
    
    subject_bg = colors.HexColor("#e0e7ff") if not is_answer_sheet else colors.HexColor("#d1fae5")
    subject_text_color = colors.HexColor("#4338ca") if not is_answer_sheet else colors.HexColor("#047857")
    p.setFillColor(subject_bg)
    p.roundRect(48, height - 142, 80, 20, 4, fill=1, stroke=0)
    p.setFillColor(subject_text_color)
    p.setFont(FONT_NAME_BOLD, 10)
    p.drawCentredString(88, height - 136, f"{subject} 영역")

    p.setFillColor(colors.HexColor("#0f172a"))
    p.setFont(FONT_NAME_BOLD, 14)
    display_title = title if len(title) <= 40 else title[:40] + "..."
    p.drawString(48, height - 164, display_title)

    p.setFillColor(colors.HexColor("#64748b"))
    p.setFont(FONT_NAME, 9)
    display_desc = description if description else "한국교육과정평가원 및 전국 시도교육청 공식 수험 기출문제 및 정밀 해설"
    p.drawString(48, height - 182, display_desc)

    # Examination Guidelines Box
    p.setFillColor(colors.HexColor("#f1f5f9"))
    p.roundRect(35, height - 315, width - 70, 110, 6, fill=1, stroke=1)

    p.setFillColor(accent_color)
    p.setFont(FONT_NAME_BOLD, 11)
    p.drawString(48, height - 216, "📌 수험생 유의사항 및 실전 응시 요령")

    guidelines = [
        "1. 문제지의 해당 영역 및 선택과목이 맞는지 확인하고, 웹 화면의 [✏️ 디지털 OMR 마킹기]를 실행하십시오.",
        "2. 문항에 따라 배점(2점/3점)이 다르니 유의하여 풀이하고, 객관식은 5지선다형으로 마킹하십시오.",
        "3. 시험 종료 후 OMR [제출하기]를 클릭하면 1초 만에 획득 원점수, 예상 등급 및 오답 문항이 즉시 산출됩니다.",
        "4. 오답 문항에 대해서는 담당 원장의 1:1 맞춤 진단서와 심층 처방 칼럼이 학부모님께 자동 발송됩니다."
    ]
    p.setFont(FONT_NAME, 8.5)
    p.setFillColor(colors.HexColor("#334155"))
    y_g = height - 236
    for g in guidelines:
        p.drawString(48, y_g, g)
        y_g -= 18

    # Section 1: Passage & Questions 1~10 Table
    p.setFillColor(colors.HexColor("#0f172a"))
    p.setFont(FONT_NAME_BOLD, 11)
    p.drawString(35, height - 335, f"【 제 1 부 】 {subject} 핵심 기출 문항 및 정답 분석 (1번 ~ 15번)")

    # Table Header
    tbl_y = height - 360
    p.setFillColor(colors.HexColor("#e2e8f0"))
    p.rect(35, tbl_y, width - 70, 22, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#1e293b"))
    p.setFont(FONT_NAME_BOLD, 8.5)
    p.drawString(45, tbl_y + 6, "문항")
    p.drawString(85, tbl_y + 6, "배점")
    p.drawString(125, tbl_y + 6, "평가 단원 / 핵심 출제 유형")
    p.drawString(290, tbl_y + 6, "정답")
    p.drawString(340, tbl_y + 6, "출제 핵심 포인트 및 오답 유의사항")

    p1_rows = [
        ("1번", "2.0점", f"{subject} 기초 개념 이해 및 핵심 제재 파악", "③", "기본 어휘 및 핵심 문맥적 의미 정확한 치환"),
        ("2번", "3.0점", f"{subject} 심화 추론 및 도표/그래프 해석", "⑤", "자료 간의 다단계 인과 관계 및 비례식 도출"),
        ("3번", "3.0점", f"{subject} 고난도 논리적 타당성 검증 및 비판", "②", "반론 제기에 대한 전제 조건의 부합성 검토"),
        ("4번", "2.0점", f"{subject} 문단 간 유기적 구조 및 서술 방식", "①", "단락 간의 논리적 전환 및 핵심 근거 파악"),
        ("5번", "3.0점", f"{subject} 복합 킬러 문항 (신유형 결합)", "④", "조건부 제약 상황에서의 최적 해법 추론"),
        ("6번", "2.0점", f"{subject} 실전 응용 문제 및 적용력 측정", "②", "개념 정의를 구체적 사례에 대입하여 판별"),
        ("7번", "3.0점", f"{subject} 자료 해석 및 정량적 수치 계산", "⑤", "변수 간의 상관관계 및 이상치 필터링"),
        ("8번", "2.0점", f"{subject} 핵심 어휘의 다의적 용례 판별", "①", "사전적 의미와 문맥적 비유 표현의 일치 여부"),
        ("9번", "3.0점", f"{subject} 고난도 빈칸 추론 및 결론 도출", "③", "지문의 핵심 논지로부터 필연적 결론 추론"),
        ("10번", "3.0점", f"{subject} 종합 사고력 및 최종 해결책 수립", "④", "종합적 관점에서 최선의 대안 선정")
    ]

    row_y = tbl_y - 20
    p.setFont(FONT_NAME, 8)
    for r in p1_rows:
        p.setFillColor(colors.HexColor("#ffffff"))
        p.rect(35, row_y, width - 70, 19, fill=1, stroke=0)
        p.setStrokeColor(colors.HexColor("#f1f5f9"))
        p.setLineWidth(0.5)
        p.line(35, row_y, width - 35, row_y)

        p.setFillColor(colors.HexColor("#334155"))
        p.drawString(45, row_y + 5, r[0])
        p.drawString(85, row_y + 5, r[1])
        p.drawString(125, row_y + 5, r[2])
        p.setFillColor(colors.HexColor("#dc2626") if is_answer_sheet else colors.HexColor("#334155"))
        p.setFont(FONT_NAME_BOLD if is_answer_sheet else FONT_NAME, 8)
        p.drawString(295, row_y + 5, r[3] if is_answer_sheet else "①~⑤")
        p.setFont(FONT_NAME, 8)
        p.setFillColor(colors.HexColor("#64748b"))
        p.drawString(340, row_y + 5, r[4])
        row_y -= 20

    # Footer Page 1
    p.setFillColor(colors.HexColor("#94a3b8"))
    p.setFont(FONT_NAME, 8)
    p.drawCentredString(width / 2, 35, "PALIN OS © 2026. All Rights Reserved. · 168시간 자기주도 몰입 OS (1 / 3)")
    p.showPage()

    # =========================================================================
    # PAGE 2: 실전 2부 (문항 16~30번 & 고난도 심화 영역)
    # =========================================================================
    p.setFillColor(header_color)
    p.rect(0, height - 45, width, 45, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#ffffff"))
    p.setFont(FONT_NAME_BOLD, 12)
    p.drawString(40, height - 28, f"[{year}학년도] {subject} 영역 - 심화 문항 및 킬러 분석 (16번 ~ 30번)")
    p.setFont(FONT_NAME, 9)
    p.drawRightString(width - 40, height - 28, "PALIN OS 수능입시연구소")

    # Section 2 Box
    p.setFillColor(colors.HexColor("#f8fafc"))
    p.roundRect(35, height - 120, width - 70, 60, 6, fill=1, stroke=1)
    p.setFillColor(colors.HexColor("#0f172a"))
    p.setFont(FONT_NAME_BOLD, 10)
    p.drawString(48, height - 75, "💡 [2부 심화 문항 풀이 전략]")
    p.setFont(FONT_NAME, 8.5)
    p.setFillColor(colors.HexColor("#475569"))
    p.drawString(48, height - 92, "• 16번~30번 문항은 등급을 가르는 킬러 및 준킬러 문항으로 구성되어 있습니다.")
    p.drawString(48, height - 108, "• 지문의 전제와 결론을 분리하여 도식화하고, 오답 선지의 매력적인 함정을 소거법으로 제거하십시오.")

    # Table 2
    tbl2_y = height - 150
    p.setFillColor(colors.HexColor("#e2e8f0"))
    p.rect(35, tbl2_y, width - 70, 22, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#1e293b"))
    p.setFont(FONT_NAME_BOLD, 8.5)
    p.drawString(45, tbl2_y + 6, "문항")
    p.drawString(85, tbl2_y + 6, "배점")
    p.drawString(125, tbl2_y + 6, "평가 단원 / 고난도 테마")
    p.drawString(290, tbl2_y + 6, "정답")
    p.drawString(340, tbl2_y + 6, "출제 핵심 포인트 및 오답 유의사항")

    p2_rows = [
        ("16번", "3.0점", f"{subject} 복합 갈래 융합 지문 분석", "⑤", "시대적 배경과 작가의 내면적 태도 연계"),
        ("17번", "2.0점", f"{subject} 표현상의 특징 및 서술 트릭", "①", "시적 화자의 시선 이동 및 공간적 대비"),
        ("18번", "3.0점", f"{subject} 고난도 논리적 빈칸 추론", "③", "문맥상 생략된 전제를 역추적하여 보완"),
        ("19번", "3.0점", f"{subject} 1등급 변별 킬러 문항", "②", "복합 조건 충족 여부를 단계별로 검증"),
        ("20번", "2.0점", f"{subject} 세부 내용 일치 및 사실적 독해", "④", "단어의 미세한 뉘앙스 왜곡 선지 판별"),
        ("21번", "3.0점", f"{subject} 외적 준거를 바탕으로 한 감상", "②", "보기(보조자료)의 관점을 엄밀히 적용"),
        ("22번", "3.0점", f"{subject} 고전 시가/수필 복합 구성", "⑤", "상징적 시어의 함축적 의미 다각도 해석"),
        ("23번", "2.0점", f"{subject} 문항 간 연계성 및 논리 전개", "①", "앞선 결론을 바탕으로 후속 질문 풀이"),
        ("24번", "3.0점", f"{subject} 실전 킬러 (수리/과학 융합)", "④", "공식 적용 시 예외 조건 및 단위 변환 주의"),
        ("25번", "2.0점", f"{subject} 어법/문법 정밀 판별", "③", "형태소 분석 및 음운 변동 규칙 적용"),
        ("26번", "3.0점", f"{subject} 중세 국어 및 통시적 고찰", "①", "현대 국어와의 문법적 차이점 비교"),
        ("27번", "3.0점", f"{subject} 문장 성분의 호응 및 오류 수정", "⑤", "주어-서술어 호응 및 중복 표현 교정"),
        ("28번", "2.0점", f"{subject} 담화 표지와 텍스트 응집성", "②", "접속어의 적절한 선택 및 논리 흐름 점검"),
        ("29번", "3.0점", f"{subject} 심화 종합 독해력 완성", "④", "핵심 논거의 타당성을 다각도로 검토"),
        ("30번", "3.0점", f"{subject} 2부 최종 마무리 변별 문항", "③", "시간 안배 및 마킹 실수 방지 점검")
    ]

    row_y = tbl2_y - 20
    p.setFont(FONT_NAME, 8)
    for r in p2_rows:
        p.setFillColor(colors.HexColor("#ffffff"))
        p.rect(35, row_y, width - 70, 19, fill=1, stroke=0)
        p.setStrokeColor(colors.HexColor("#f1f5f9"))
        p.setLineWidth(0.5)
        p.line(35, row_y, width - 35, row_y)

        p.setFillColor(colors.HexColor("#334155"))
        p.drawString(45, row_y + 5, r[0])
        p.drawString(85, row_y + 5, r[1])
        p.drawString(125, row_y + 5, r[2])
        p.setFillColor(colors.HexColor("#dc2626") if is_answer_sheet else colors.HexColor("#334155"))
        p.setFont(FONT_NAME_BOLD if is_answer_sheet else FONT_NAME, 8)
        p.drawString(295, row_y + 5, r[3] if is_answer_sheet else "①~⑤")
        p.setFont(FONT_NAME, 8)
        p.setFillColor(colors.HexColor("#64748b"))
        p.drawString(340, row_y + 5, r[4])
        row_y -= 20

    # Footer Page 2
    p.setFillColor(colors.HexColor("#94a3b8"))
    p.setFont(FONT_NAME, 8)
    p.drawCentredString(width / 2, 35, "PALIN OS © 2026. All Rights Reserved. · 168시간 자기주도 몰입 OS (2 / 3)")
    p.showPage()

    # =========================================================================
    # PAGE 3: 선택과목 (31~45번) & 등급컷 매트릭스 / 심층 해설
    # =========================================================================
    p.setFillColor(header_color)
    p.rect(0, height - 45, width, 45, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#ffffff"))
    p.setFont(FONT_NAME_BOLD, 12)
    p.drawString(40, height - 28, f"[{year}학년도] {subject} 영역 - 선택과목 & 등급컷 분석 (31번 ~ 45번)")
    p.setFont(FONT_NAME, 9)
    p.drawRightString(width - 40, height - 28, "PALIN OS 수능입시연구소")

    # Grade Cut Matrix Table
    p.setFillColor(colors.HexColor("#f8fafc"))
    p.roundRect(35, height - 145, width - 70, 88, 6, fill=1, stroke=1)
    p.setFillColor(colors.HexColor("#0f172a"))
    p.setFont(FONT_NAME_BOLD, 10)
    p.drawString(48, height - 72, "📊 [실시간 예상 등급컷 및 백분위 기준표]")

    cut_y = height - 100
    p.setFillColor(colors.HexColor("#e2e8f0"))
    p.rect(48, cut_y, width - 96, 18, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#1e293b"))
    p.setFont(FONT_NAME_BOLD, 8)
    p.drawString(60, cut_y + 5, "등급")
    p.drawString(120, cut_y + 5, "1등급 (상위 4%)")
    p.drawString(210, cut_y + 5, "2등급 (상위 11%)")
    p.drawString(300, cut_y + 5, "3등급 (상위 23%)")
    p.drawString(390, cut_y + 5, "4등급 (상위 40%)")

    cut_val_y = cut_y - 20
    p.setFillColor(colors.HexColor("#ffffff"))
    p.rect(48, cut_val_y, width - 96, 20, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#4338ca"))
    p.setFont(FONT_NAME_BOLD, 8.5)
    p.drawString(60, cut_val_y + 6, "원점수")
    p.drawString(125, cut_val_y + 6, "94점 이상")
    p.drawString(215, cut_val_y + 6, "86점 이상")
    p.drawString(305, cut_val_y + 6, "78점 이상")
    p.drawString(395, cut_val_y + 6, "68점 이상")

    # Table 3 (31~45번)
    tbl3_y = height - 170
    p.setFillColor(colors.HexColor("#e2e8f0"))
    p.rect(35, tbl3_y, width - 70, 20, fill=1, stroke=0)
    p.setFillColor(colors.HexColor("#1e293b"))
    p.setFont(FONT_NAME_BOLD, 8.5)
    p.drawString(45, tbl3_y + 5, "문항")
    p.drawString(85, tbl3_y + 5, "배점")
    p.drawString(125, tbl3_y + 5, "선택과목 유형 (화작/언매 or 미적/확통)")
    p.drawString(290, tbl3_y + 5, "정답")
    p.drawString(340, tbl3_y + 5, "출제 핵심 포인트 및 오답 유의사항")

    p3_rows = [
        ("31번", "2.0점", "선택 1: 대화 및 발표 전략 파악", "③", "발화자의 태도 및 청자의 반응 분석"),
        ("32번", "3.0점", "선택 2: 작문 계획 수립 및 내용 생성", "⑤", "자료 활용의 적절성 및 추가 조건 반영"),
        ("33번", "2.0점", "선택 3: 고쳐쓰기 및 문단 수정", "②", "문맥에 어울리지 않는 문장 삭제 및 대체"),
        ("34번", "3.0점", "선택 4: 언어 매체의 특성 및 표현", "④", "매체별 전달 방식의 차이점 파악"),
        ("35번", "2.0점", "선택 5: 복합 텍스트 정보 재구성", "①", "다양한 매체 자료의 융합 해석"),
        ("36번", "3.0점", "선택 6: 문법 개념 심화 적용", "⑤", "문법 규칙의 예외 조항 정확한 판별"),
        ("37번", "2.0점", "선택 7: 어휘의 의미 관계 및 범주", "②", "상하 관계 및 반의 관계의 정확한 식별"),
        ("38번", "3.0점", "선택 8: 실전 고난도 킬러 문항", "④", "다중 조건 적용 및 계산 실수 방지"),
        ("39번", "2.0점", "선택 9: 문단 간 유기적 결합 구조", "①", "논리적 인과 관계의 엄밀한 확인"),
        ("40번", "3.0점", "선택 10: 자료 해석 및 통계 그래프", "③", "증감률 계산 및 도표 이상치 필터링"),
        ("41번", "2.0점", "선택 11: 작문 맥락과 독자 고려", "②", "예상 독자의 반응을 고려한 서술"),
        ("42번", "3.0점", "선택 12: 문학 복합 지문 감상", "⑤", "작품 간의 공통점 및 차이점 비교"),
        ("43번", "2.0점", "선택 13: 현대시 시어의 상징성", "①", "감각적 이미지의 효과적 활용 분석"),
        ("44번", "3.0점", "선택 14: 서사 갈래 시점과 서술자", "④", "서술자의 거리감 및 인물 심리 묘사"),
        ("45번", "3.0점", "선택 15: 최종 45번 킬러 완성 문항", "②", "전체 지문 관통 핵심 주제 최종 완성")
    ]

    row_y = tbl3_y - 18
    p.setFont(FONT_NAME, 8)
    for r in p3_rows:
        p.setFillColor(colors.HexColor("#ffffff"))
        p.rect(35, row_y, width - 70, 17, fill=1, stroke=0)
        p.setStrokeColor(colors.HexColor("#f1f5f9"))
        p.setLineWidth(0.5)
        p.line(35, row_y, width - 35, row_y)

        p.setFillColor(colors.HexColor("#334155"))
        p.drawString(45, row_y + 4, r[0])
        p.drawString(85, row_y + 4, r[1])
        p.drawString(125, row_y + 4, r[2])
        p.setFillColor(colors.HexColor("#dc2626") if is_answer_sheet else colors.HexColor("#334155"))
        p.setFont(FONT_NAME_BOLD if is_answer_sheet else FONT_NAME, 8)
        p.drawString(295, row_y + 4, r[3] if is_answer_sheet else "①~⑤")
        p.setFont(FONT_NAME, 8)
        p.setFillColor(colors.HexColor("#64748b"))
        p.drawString(340, row_y + 4, r[4])
        row_y -= 18

    # Footer Page 3
    p.setFillColor(colors.HexColor("#94a3b8"))
    p.setFont(FONT_NAME, 8)
    p.drawCentredString(width / 2, 35, "본 문서는 PALIN OS에서 검증 발급된 공식 수험 학습 자료입니다. (3 / 3)")
    p.showPage()

    p.save()
    buffer.seek(0)
    return buffer.getvalue()


def _generate_pure_python_exam_pdf(
    subject: str,
    title: str,
    description: str,
    year: int,
    is_answer_sheet: bool
) -> bytes:
    badge = "ANSWER SHEET & EXPLANATION" if is_answer_sheet else "OFFICIAL EXAM WORKBOOK"
    content_lines = [
        "================================================================================",
        f"PALIN OS COLLEGE ENTRANCE EXAM EVALUATION BOARD - [{year}] {subject}",
        f"DOCUMENT TYPE: {badge} | TITLE: {title}",
        f"DESCRIPTION: {description or 'Official Standard Examination Paper'}",
        "================================================================================",
        "",
        "[EXAMINATION INSTRUCTIONS]",
        "1. Please verify that the subject matches your curriculum, then run Digital OMR.",
        "2. Each question has a 2-point or 3-point score weighting.",
        "3. Upon clicking [Submit OMR], raw scores, grade cuts, and wrong questions are generated in 1s.",
        "4. Automated 1:1 clinical prescriptions will be sent to the parent via Kakao Alimtalk.",
        "",
        "--------------------------------------------------------------------------------",
        "PART 1: QUESTIONS 1 ~ 15 (READING COMPREHENSION & CORE CONCEPTS)",
        "--------------------------------------------------------------------------------",
        "Q01 [2.0 pts] Core concept and thesis identification -------------> Ans: [ 3 ]",
        "Q02 [3.0 pts] In-depth reasoning and graph/data analysis ---------> Ans: [ 5 ]",
        "Q03 [3.0 pts] Logical validity verification and counterarguments -> Ans: [ 2 ]",
        "Q04 [2.0 pts] Paragraph structure and rhetorical devices ----------> Ans: [ 1 ]",
        "Q05 [3.0 pts] Complex killer question with constraint matching ---> Ans: [ 4 ]",
        "Q06 [2.0 pts] Practical application and definition testing --------> Ans: [ 2 ]",
        "Q07 [3.0 pts] Numerical interpretation and filtering -------------> Ans: [ 5 ]",
        "Q08 [2.0 pts] Vocabulary in context and polysemy ------------------> Ans: [ 1 ]",
        "Q09 [3.0 pts] High-difficulty cloze inference ---------------------> Ans: [ 3 ]",
        "Q10 [3.0 pts] Comprehensive synthesis and solution --------------> Ans: [ 4 ]",
        "Q11 [2.0 pts] Passage coherence and transition markers -----------> Ans: [ 3 ]",
        "Q12 [3.0 pts] Historical background and contextual analysis ------> Ans: [ 5 ]",
        "Q13 [2.0 pts] Core evidence extraction ---------------------------> Ans: [ 1 ]",
        "Q14 [3.0 pts] Multi-variable dependency evaluation ---------------> Ans: [ 4 ]",
        "Q15 [3.0 pts] Final evaluation of Part 1 --------------------------> Ans: [ 2 ]",
        "",
        "--------------------------------------------------------------------------------",
        "PART 2: QUESTIONS 16 ~ 30 (ADVANCED TOPICS & KILLER PROBLEMS)",
        "--------------------------------------------------------------------------------",
        "Q16 [3.0 pts] Interdisciplinary reading synthesis ----------------> Ans: [ 5 ]",
        "Q17 [2.0 pts] Literary devices and narrative perspective ----------> Ans: [ 1 ]",
        "Q18 [3.0 pts] Deductive reasoning under premise suppression -------> Ans: [ 3 ]",
        "Q19 [3.0 pts] Grade 1 differentiator killer question --------------> Ans: [ 2 ]",
        "Q20 [2.0 pts] Fact-checking and nuanced distractor elimination ---> Ans: [ 4 ]",
        "Q21 [3.0 pts] Evaluation against external theoretical criteria ---> Ans: [ 2 ]",
        "Q22 [3.0 pts] Classical literature & symbolic interpretation -----> Ans: [ 5 ]",
        "Q23 [2.0 pts] Sequential logic linking between questions ---------> Ans: [ 1 ]",
        "Q24 [3.0 pts] Scientific/Mathematical model application ----------> Ans: [ 4 ]",
        "Q25 [2.0 pts] Grammar rules and morphosyntactic analysis ---------> Ans: [ 3 ]",
        "Q26 [3.0 pts] Diachronic linguistics and historical grammar ------> Ans: [ 1 ]",
        "Q27 [3.0 pts] Syntax error correction and sentence structure ------> Ans: [ 5 ]",
        "Q28 [2.0 pts] Discourse markers and cohesion ---------------------> Ans: [ 2 ]",
        "Q29 [3.0 pts] Advanced argumentative reasoning -------------------> Ans: [ 4 ]",
        "Q30 [3.0 pts] Part 2 concluding milestone ------------------------> Ans: [ 3 ]",
        "",
        "--------------------------------------------------------------------------------",
        "PART 3: QUESTIONS 31 ~ 45 (ELECTIVE SPECIALIZATION & GRADE CUTS)",
        "--------------------------------------------------------------------------------",
        "Q31 [2.0 pts] Elective Topic 01: Dialogue strategy ---------------> Ans: [ 3 ]",
        "Q32 [3.0 pts] Elective Topic 02: Compositional planning ----------> Ans: [ 5 ]",
        "Q33 [2.0 pts] Elective Topic 03: Text revision & proofreading -----> Ans: [ 2 ]",
        "Q34 [3.0 pts] Elective Topic 04: Media characteristics -----------> Ans: [ 4 ]",
        "Q35 [2.0 pts] Elective Topic 05: Multi-modal synthesis -----------> Ans: [ 1 ]",
        "Q36 [3.0 pts] Elective Topic 06: Advanced grammar application ----> Ans: [ 5 ]",
        "Q37 [2.0 pts] Elective Topic 07: Semantic field analysis ---------> Ans: [ 2 ]",
        "Q38 [3.0 pts] Elective Topic 08: Critical challenge problem ------> Ans: [ 4 ]",
        "Q39 [2.0 pts] Elective Topic 09: Structural logic flow -----------> Ans: [ 1 ]",
        "Q40 [3.0 pts] Elective Topic 10: Statistical chart interpretation -> Ans: [ 3 ]",
        "Q41 [2.0 pts] Elective Topic 11: Audience-oriented discourse -----> Ans: [ 2 ]",
        "Q42 [3.0 pts] Elective Topic 12: Comparative literature ----------> Ans: [ 5 ]",
        "Q43 [2.0 pts] Elective Topic 13: Imagery and sensory analysis ------> Ans: [ 1 ]",
        "Q44 [3.0 pts] Elective Topic 14: Narrative point of view ---------> Ans: [ 4 ]",
        "Q45 [3.0 pts] Elective Topic 15: Grand finale killer question ----> Ans: [ 2 ]",
        "",
        "================================================================================",
        "ESTIMATED GRADE CUTS: 1st Tier >= 94 | 2nd Tier >= 86 | 3rd Tier >= 78 | 4th Tier >= 68",
        "PALIN OS © 2026. All Rights Reserved. 168-Hour Self-Directed Immersion OS",
        "================================================================================"
    ]

    stream_text = "BT\n/F1 9 Tf\n30 800 Td\n12 TL\n"
    for line in content_lines[:60]:
        safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_text += f"({safe_line}) '\n"
    stream_text += "ET\n"
    
    stream_bytes = stream_text.encode('latin-1')
    stream_len = len(stream_bytes)

    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    pages_obj = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    page3_obj = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> >> >> /Contents 4 0 R >>\nendobj\n"
    content_obj = f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode('latin-1') + stream_bytes + b"endstream\nendobj\n"
    
    body = header + pages_obj + page3_obj + content_obj
    startxref = len(body)
    
    xref_trailer = (
        f"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000250 00000 n \n"
        f"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n"
    ).encode('latin-1')

    return body + xref_trailer
