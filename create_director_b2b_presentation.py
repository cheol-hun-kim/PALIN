# -*- coding: utf-8 -*-
"""
PALIN OS Minimalist Luxury B2B Director Presentation (20 High-Impact Slides)
Design Philosophy:
- Minimalist, Heavy, Prestigious Executive Aesthetic (Deep Matte Charcoal Black + Champagne Gold + Crisp White)
- Zero rainbow noise / Zero clutter
- Large, bold, readable typography (28~32pt headers, 15~16pt body, 56~64pt key metrics)
- Spacious layouts with breathing room
- Complete speaker scripts on every slide
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Minimalist Luxury Color Palette
    BG_BLACK = RGBColor(9, 11, 16)         # #090B10 (Deep Matte Slate Black)
    CARD_BG = RGBColor(17, 20, 28)         # #11141C (Refined Dark Slate)
    CARD_BORDER = RGBColor(38, 43, 58)     # #262B3A (Subtle Elegant Border)
    GOLD_ACCENT = RGBColor(212, 175, 55)   # #D4AF37 (Champagne Luxury Gold)
    WHITE = RGBColor(255, 255, 255)        # Pure Crisp White
    SILVER_GRAY = RGBColor(160, 174, 192)  # #A0AEC0 (High-Contrast Slate Silver)
    MUTED_GRAY = RGBColor(113, 128, 150)   # #718096 (Subtle Muted)

    blank_layout = prs.slide_layouts[6]

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_BLACK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, kicker="PALIN OS EXECUTIVE B2B PROPOSAL"):
        # Kicker tag
        tb_kicker = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.35))
        p_k = tb_kicker.text_frame.paragraphs[0]
        p_k.text = kicker.upper()
        p_k.font.size = Pt(11)
        p_k.font.bold = True
        p_k.font.color.rgb = GOLD_ACCENT
        p_k.font.name = "Malgun Gothic"

        # Main Title (Large, Bold, High Impact)
        tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(0.8), Inches(11.5), Inches(0.8))
        p_t = tb_title.text_frame.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.font.name = "Malgun Gothic"

    def add_card(slide, left, top, width, height, title, content_items, border_color=CARD_BORDER, bg_color=CARD_BG, title_color=WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.28)
        tf.margin_bottom = Inches(0.28)

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(18)
            p_title.font.bold = True
            p_title.font.color.rgb = title_color
            p_title.font.name = "Malgun Gothic"
            p_title.space_after = Pt(14)
            first = False
        else:
            first = True

        for item in content_items:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            if isinstance(item, tuple):
                h_text, b_text = item
                run_h = p.add_run()
                run_h.text = f"• {h_text}\n"
                run_h.font.bold = True
                run_h.font.size = Pt(14)
                run_h.font.color.rgb = WHITE
                run_h.font.name = "Malgun Gothic"

                run_b = p.add_run()
                run_b.text = f"  {b_text}"
                run_b.font.size = Pt(13)
                run_b.font.color.rgb = SILVER_GRAY
                run_b.font.name = "Malgun Gothic"
            else:
                p.text = f"• {item}"
                p.font.size = Pt(13.5)
                p.font.color.rgb = SILVER_GRAY
                p.font.name = "Malgun Gothic"
            p.space_after = Pt(12)

    def add_speaker_note(slide, note_text):
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = f"🎙️ [발표자 스크립트]\n{note_text}"

    # ==========================================
    # SLIDE 1: Cover Title (Minimal Luxury)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4.5))
    tf1 = tb1.text_frame
    
    p1_kicker = tf1.paragraphs[0]
    p1_kicker.text = "THE ULTIMATE ACADEMY AUTOPILOT"
    p1_kicker.font.size = Pt(13)
    p1_kicker.font.bold = True
    p1_kicker.font.color.rgb = GOLD_ACCENT
    p1_kicker.font.name = "Malgun Gothic"

    p1_title = tf1.add_paragraph()
    p1_title.text = "PALIN OS"
    p1_title.font.size = Pt(54)
    p1_title.font.bold = True
    p1_title.font.color.rgb = WHITE
    p1_title.font.name = "Malgun Gothic"
    p1_title.space_before = Pt(8)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "교육의 한계 비용을 '0'으로 만들다.\n1인 원장을 위한 궁극의 입시 관제 오토파일럿."
    p1_sub.font.size = Pt(24)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = GOLD_ACCENT
    p1_sub.font.name = "Malgun Gothic"
    p1_sub.space_before = Pt(12)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "강사의 노동력을 파는 시대는 끝났습니다. 이제 '압도적인 통제 시스템'을 파십시오."
    p1_desc.font.size = Pt(15)
    p1_desc.font.color.rgb = SILVER_GRAY
    p1_desc.font.name = "Malgun Gothic"
    p1_desc.space_before = Pt(14)

    p1_foot = tf1.add_paragraph()
    p1_foot.text = "CONFIDENTIAL & PROPRIETARY  |  공식 문의: 1286orbital21@gmail.com"
    p1_foot.font.size = Pt(11)
    p1_foot.font.color.rgb = MUTED_GRAY
    p1_foot.font.name = "Malgun Gothic"
    p1_foot.space_before = Pt(36)

    add_speaker_note(s1, "원장님, 하루에 상담과 행정에 몇 시간을 쓰십니까? 조교 인건비로는 매월 얼마가 나갑니까? 오늘 저는 원장님의 학원을 노동 집약적 가내수공업에서, 한계 비용이 제로에 수렴하는 하이테크 IT 비즈니스로 바꿔드릴 시스템을 소개합니다.")

    # ==========================================
    # SLIDE 2: The Problem - 1인 원장의 딜레마
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "The Problem: 우리는 왜 원생이 늘어날수록 더 불행해지는가?")

    add_card(s2, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "01. 인건비의 늪", [
        ("조교 의존도 심화", "원생 통제를 위해 비싼 조교를 계속 고용하지만 잦은 퇴사와 관리 부실 반복"),
        ("수익성 악화", "원생이 늘어도 인건비가 정비례로 증가하여 실제 남는 순이익은 정체")
    ], title_color=GOLD_ACCENT)

    add_card(s2, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "02. 감정 노동의 한계", [
        ("상담 전화 과부하", "학부모의 끝없는 성적 불안과 심야 상담 요구로 원장의 에너지 완전 고갈"),
        ("수납 독촉의 스트레스", "수강료 결제일마다 반복되는 민망하고 어색한 수납 통화 스트레스")
    ], title_color=GOLD_ACCENT)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "03. 스케일업 불가", [
        ("물리적 시간의 한계", "원장의 24시간은 한정되어 있어 50~100명 이상 원생 확장 불가능"),
        ("학원에 갇힌 삶", "원장이 하루라도 자리를 비우면 학원 전체 운영이 마비되는 구조적 덫")
    ], title_color=GOLD_ACCENT)

    add_speaker_note(s2, "학생이 늘면 돈은 벌지만, 원장님의 삶은 사라집니다. 조교를 뽑자니 인건비가 수익을 갉아먹고, 퀄리티는 떨어집니다. 이 딜레마를 해결하지 못하면 영원히 학원에 갇혀 일해야 합니다.")

    # ==========================================
    # SLIDE 3: The Paradigm Shift - 본질의 전환
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "The Paradigm Shift: '더 가르치는 것'이 아니라 '완벽하게 통제하는 것'")

    add_card(s3, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "기존의 학원 모델", [
        ("핵심 가치", "강사의 강의력과 노동 시간에 의존"),
        ("학부모 보고", "원장이 직접 수동 전화 상담 및 감정 소모"),
        ("학생 관리", "조교가 복도를 순찰하며 수동 감시"),
        ("원장의 위치", "모든 잡무를 도맡아 하는 '플레이어 (Player)'")
    ], title_color=SILVER_GRAY)

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "PALIN OS 도입 학원", [
        ("핵심 가치", "시스템의 압도적인 24시간 통제력과 데이터"),
        ("학부모 보고", "AI가 매주 화요일 밤 10시 정밀 리포트 자동 발송"),
        ("학생 관리", "WiFi 감지 + 타이머 + 마이크로 랭킹전으로 자발적 몰입"),
        ("원장의 위치", "손가락 하나로 수백 명을 통제하는 '제국 설계자 (God Mode)'")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s3, "어차피 강의는 1타 강사들의 인강이 가장 훌륭합니다. 학부모가 동네 학원에 기대하는 진짜 본질은 '내 아이를 책상에 묶어두고 관리해 주는 것'입니다. 우리는 이 관리를 100% 자동화했습니다.")

    # ==========================================
    # SLIDE 4: The Core Solution - PALIN OS 3대 기둥
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "The Solution: 원장님의 '뇌'를 복제하여 24시간 돌아가는 SaaS 제국")

    add_card(s4, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "01. 완전 무인 행정", [
        ("무설치 0.1초 출결", "학원 네트워크 감지 즉시 자동 출결 및 학부모 안심 통보"),
        ("1-Click 미납 관리", "미납자 원클릭 필터링 및 카톡 정중 안내 자동화"),
        ("조교 인건비 0원화", "출결, 수납, OMR 채점, 과제 검사의 100% 무인화")
    ], title_color=GOLD_ACCENT)

    add_card(s4, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "02. AI 커스텀 뇌 이식", [
        ("원장 입시 철학 주입", "원장님의 교재와 상담 대본을 벡터 DB로 100% 학습"),
        ("24시간 1:1 상담 대행", "새벽 2시에도 원장님의 어투로 팩트폭격 및 멘탈 케어"),
        ("상담 리소스 90% 절감", "원장님은 오직 VIP 심층 상담에만 집중")
    ], title_color=GOLD_ACCENT)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "03. 심리적 락인 (Lock-in)", [
        ("마이크로 랭킹전", "내 동네/고교 친구들과의 실시간 자습 순위 경쟁"),
        ("Beeminder 보증금", "기상/취침 미션 실패 시 1,000원~5,000원 벌금 차감"),
        ("퇴원율 0% 수렴", "한 번 들어오면 수능 날까지 나갈 수 없는 강력한 몰입")
    ], title_color=GOLD_ACCENT)

    add_speaker_note(s4, "PALIN OS는 단순한 프로그램이 아닙니다. 원장님의 행정, 상담, 통제를 완벽히 대신해 주는 3대 모듈로 구성된 종합 운영체제입니다.")

    # ==========================================
    # SLIDE 5: Architecture - 3자 완벽 권한 격리 (RBAC)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Architecture: 철저한 3자 역할 기반 권한 격리 (RBAC)")

    add_card(s5, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "🧑‍🎓 수험생 모드 (몰입)", [
        ("통제 UI만 독점 노출", "자습 타이머, 동네/학교 랭킹, 주간 미션, D-Day 학생증만 사용 가능"),
        ("관리자 영역 원천 차단", "학부모의 감시 설정이나 관리자 기능에는 일절 접근 불가"),
        ("게임 같은 몰입감", "경쟁심과 성취감을 자극하여 공부를 게임처럼 플레이")
    ], title_color=WHITE)

    add_card(s5, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "👨‍👩‍👧 학부모 모드 (안심)", [
        ("실시간 조회 (Read-only)", "자녀의 자습시간, 출결 현황, 일일 미션 달성률을 실시간 모니터링"),
        ("간섭 불가 & 안심 극대화", "자녀의 학습 흐름을 방해하지 않고 묵묵히 응원"),
        ("원클릭 금융 지원", "교재비, 모의고사 리포트, 학원비 결제 창구 일원화")
    ], title_color=WHITE)

    add_card(s5, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "🏫 학원장 모드 (관제실)", [
        ("B2B 전용 중앙 ERP", "전체 원생의 실시간 위치, 타이머, 이탈 상태 실시간 전지적 조망"),
        ("원클릭 절대 통제권", "원장 직통 레드카드 발부, 보증금 차감, 긴급 SMS 발송"),
        ("독점 폐쇄망 운영", "학원 전용 로고 및 가맹 코드 기반 독립 생태계 운영")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s5, "학생이 학부모의 감시 UI를 보게 되면 거부감을 느끼고 이탈합니다. PALIN OS는 철저한 권한 분리를 통해 학생에겐 게임 같은 경쟁을, 학부모에겐 안심과 결제 창구를, 원장에겐 절대 권력을 줍니다.")

    # ==========================================
    # SLIDE 6: Feature 1 - 마스터 관제실 (원장 전용 ERP)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Feature 01: 손가락 하나로 수백 명을 통제하는 '마스터 관제실'")

    add_card(s6, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "무설치 0.1초 네트워크 출결 & 미납 관리", [
        ("하드웨어 설치 비용 0원", "비싼 지문인식기나 비콘 없이 학원 WiFi/네트워크 대역 감지로 0.1초 자동 등원 체크"),
        ("지각/결석 자동 격발", "수업 시작 시간까지 미등원 시 학부모 안심 SMS 즉시 자동 발송"),
        ("1-Click 미납금 관리", "수강료/교재비 미납자 목록 원클릭 색출 및 정중한 카카오톡 수납 안내 자동 발송")
    ], title_color=GOLD_ACCENT)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "원장 직통 원클릭 레드카드 발송기", [
        ("자습 태도 불량 즉시 제재", "졸음, 잡담, 스마트폰 몰래 사용 적발 시 관제실 버튼 하나로 즉각 경고 발부"),
        ("성실 보증금 벌금 차감", "학생 에스크로 보증금에서 1,000원~5,000원 즉시 삭감"),
        ("학부모 통보 동시 실행", "부모님께 징계 사유와 타임스탬프가 자동 문자로 전송되어 학원 내 기강 100% 확립")
    ], title_color=WHITE)

    add_speaker_note(s6, "더 이상 조교가 문 앞에서 출석 체크를 할 필요가 없습니다. 미납자에게 전화해서 아쉬운 소리 할 필요도 없습니다. 버튼 한 번이면 끝납니다.")

    # ==========================================
    # SLIDE 7: Feature 2 - AI 커스텀 뇌 이식 (복제된 원장님)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "Feature 02: 내가 자는 동안에도 내 분신이 1:1 상담을 진행하는 AI 뇌 이식")

    add_card(s7, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "원장님 입시 철학 & 수험생활백서 RAG 주입", [
        ("학원 자체 데이터 무제한 학습", "원장님의 강의 교재, 커리큘럼, 입시 노하우, 상담 대본을 시스템에 텍스트/PDF로 업로드"),
        ("원장 전용 AI 뇌 동적 병합", "Gemini AI가 원장님의 지식을 학습하여 '우리 학원만의 방침과 커리큘럼'으로만 완벽 응답"),
        ("지식의 영구 자산화", "강사가 퇴사해도 학원의 핵심 입시 노하우와 상담 퀄리티는 시스템에 영구 보존")
    ], title_color=GOLD_ACCENT)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "24시간 1:1 원장 페르소나 팩트폭격", [
        ("심야 1:1 밀착 멘토링", "새벽 2시에 학생이 슬럼프 고민을 토로해도 원장님의 어투로 즉각 처방전 제시"),
        ("냉혹한 팩트폭격", "달콤한 위로 대신 목표 대학 갭 분석을 바탕으로 한 현실적 행동 강령 제시"),
        ("무한 스케일업", "원생이 500명으로 늘어나도 상담 퀄리티의 타협 없이 24시간 완벽 커버")
    ], title_color=WHITE)

    add_speaker_note(s7, "수백 명의 학생이 새벽 2시에 우울하다며 질문을 던져도, 원장님의 철학이 담긴 AI가 1:1로 밀착 멘토링을 해줍니다. 퀄리티의 타협 없이 무한대로 스케일업이 가능해집니다.")

    # ==========================================
    # SLIDE 8: Feature 3 - 학부모용 자율 AI 페르소나
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "Feature 03: 원장님의 영업 철학에 맞춘 100% 자율 학부모 AI 페르소나")

    add_card(s8, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "모드 A: 신뢰형 멘토 (Anti-Marketing)", [
        ("결제를 만류하는 역설적 진정성", "불안해하는 학부모가 추가 특강/결제를 문의할 때, '지금은 돈을 쓸 때가 아니라 기본 복습 밀도를 높일 때입니다' 단호히 만류"),
        ("학부모의 절대적 신뢰 획득", "상업적이지 않고 아이를 진심으로 위한다는 확신을 주어 재등록률 100% 달성"),
        ("원장의 품격 상승", "학원과 원장님의 브랜드를 지역 최고 수준의 교육 전문가로 각인")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "모드 B: 전략적 제안형 (Active-Sales)", [
        ("취약점 진단 기반 자연스러운 제안", "모의고사 성적 하락 시 해당 단원 클리닉 및 방학 특강을 논리적으로 추천"),
        ("학원 매출 극대화", "학부모의 니즈가 가장 높은 시점에 최적의 맞춤형 커리큘럼 안내"),
        ("관제실에서 1초 원클릭 스위칭", "본사의 강요 없이 원장님의 사업 방식에 따라 AI 성향을 100% 자유롭게 세팅")
    ], title_color=WHITE)

    add_speaker_note(s8, "우리는 본사의 영업 방식을 원장님께 강요하지 않습니다. 신뢰형 멘토 모드로 학부모를 완벽히 록인할지, 적극적인 특강 제안으로 매출을 올릴지는 오직 원장님의 자유의사에 달려 있습니다.")

    # ==========================================
    # SLIDE 9: Feature 4 - 게이미피케이션 (학생 통제 매커니즘)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "Feature 04: 강압적 감시가 아닌, 자발적 중독을 설계하는 게이미피케이션")

    add_card(s9, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "01. 동네/학교 랭킹전", [
        ("국지적 자존심 경쟁", "'분당구 1위', '낙생고 2위' 등 실시간 동네/학교 순위 노출"),
        ("실시간 띠배너 공지", "1위 탈환 시 전교생 화면 상단에 골드 띠배너 즉시 브로드캐스트"),
        ("자발적 자습 폭증", "친구를 이기기 위해 밤늦게까지 타이머를 켜두는 선의의 경쟁")
    ], title_color=GOLD_ACCENT)

    add_card(s9, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "02. 주간 초기화 룰", [
        ("매주 일요일 자정 리셋", "모든 랭킹 점수가 일요일 자정에 0으로 초기화"),
        ("새로운 희망 부여", "이번 주에 뒤처진 학생도 다음 주 월요일 0시부터 다시 1등 도전 가능"),
        ("이탈 방지", "포기하지 않고 매주 월요일 아침 앱에 재접속하도록 유도")
    ], title_color=WHITE)

    add_card(s9, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "03. 1% VIP 라운지 강등제", [
        ("가차 없는 권한 박탈", "주간 자습 상위 1% 미달 시 즉시 VIP 라운지에서 강제 퇴장(Kick-out)"),
        ("상실의 공포 (FOMO)", "VIP 자격을 유지하기 위해 자습량을 극한으로 유지"),
        ("의치한약수 멘토링", "상위 1% 학생에게만 주어지는 명예와 특권 부여")
    ], title_color=GOLD_ACCENT)

    add_speaker_note(s9, "감시 카메라로 감시하면 반발하지만, 랭킹과 게임으로 만들면 학생들은 스스로 밤을 새워 공부합니다.")

    # ==========================================
    # SLIDE 10: Feature 5 - 빈틈없는 오토파일럿 행정
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "Feature 05: 핑계를 원천 봉쇄하는 기계적인 엄격함의 오토파일럿")

    add_card(s10, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "01. 주간 OMR 자정 마감", [
        ("타협 없는 자동 마감", "일요일 23:59까지 OMR 미제출 시 예외 없이 자동 차단"),
        ("보증금 벌금 즉시 차감", "과제 미제출에 따른 성실 보증금 벌금 에스크로 자동 삭감"),
        ("학부모 자동 통보", "과제 미제출 사실이 부모님께 즉시 알림톡으로 발송")
    ], title_color=WHITE)

    add_card(s10, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "02. VOD 168시간 락", [
        ("7일 후 시청 원천 차단", "강의 권한 부여 후 168시간(7일) 경과 시 영상 자동 락(Lock)"),
        ("배속 롤백 안티치트", "2배속 이상 날림 수강 시 시청 시간 미인정 및 경고"),
        ("초단위 완강률 추적", "학생이 진짜로 집중해서 들었는지 초단위 타임라인 분석")
    ], title_color=WHITE)

    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "03. 화요일 22:00 AI 리포트", [
        ("Gemini AI 종합 진단", "한 주간의 자습시간, 출결, 미션 성공률을 분석해 300자 카톡 대본 생성"),
        ("전교생 일괄 발송", "화요일 밤 학부모 스마트폰으로 고품격 리포트 자동 발송"),
        ("수납 링크 연동", "미납자의 경우 리포트 하단에 결제 안내 정중히 포함")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s10, "학생의 핑계와 타협하지 않습니다. 정해진 룰대로 시스템이 기계처럼 엄격하게 작동하여 학원의 기강을 완성합니다.")

    # ==========================================
    # SLIDE 11: Business Model - 선배-후배 클리닉 선순환
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "Business Model 01: 제자를 잘 키울수록 학원의 영구적 부가 수익이 되는 생태계")

    add_card(s11, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "🎓 학원 출신 선배 ➔ 후배 1:1 클리닉 (8:1:1)", [
        ("원장이 키운 제자가 학원의 자산", "학원 출신 의대/SKY 합격생을 학원 전용 튜터로 등록"),
        ("후배 재원생의 압도적 신뢰", "우리 학원에서 공부해 명문대 간 검증된 선배에게 1:1 킬러문항 질의응답"),
        ("수익 분배 구조", "선배 튜터 80% : 학원장 10% (브랜드 보증료) : 본사 10% (플랫폼 운영)")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "💰 구독료를 상쇄하고 남는 확실한 Profit Center", [
        ("월 순수익 시뮬레이션", "재원생 100명 중 30명이 주 1회 선배 클리닉(회당 5만 원) 이용 시\n➔ 월 결제 총액: 600만 원\n➔ 학원장 수수료(10%): 월 60만 원 추가 순수익 발생"),
        ("구독료 전액 회수", "학원 월 구독료(59.9만 원)를 내면서도, 선배 클리닉 수수료로 구독료 전액을 회수하고 순이익 창출")
    ], title_color=WHITE)

    add_speaker_note(s11, "원장님이 정성껏 가르쳐 명문대에 보낸 제자가 다시 후배를 가르치고, 그 수익의 일부가 학원 통장에 매달 꽂힙니다. 학생을 잘 키울수록 학원의 수익이 영구적으로 늘어나는 생태계입니다.")

    # ==========================================
    # SLIDE 12: Business Model - 마이크로 과금 & 부가 수익
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "Business Model 02: 학원비 외에 '불안감'과 '서비스'를 현금화하는 파이프라인")

    add_card(s12, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "📊 AI 입시 심층 리포트 (16,900원~34,900원)", [
        ("불안감의 현금화", "모의고사 직후 학부모의 불안감이 극에 달했을 때, 버튼 클릭 한 번으로 발급되는 정밀 AI 진단서"),
        ("11,688개 대학 정시 컷 연동", "목표 대학 합격 가능성 및 역전 전략 로드맵 0.1초 제공"),
        ("학부모 자발적 결제", "학원에 추가 비용을 내지 않고도 학부모 스스로 결제하는 고부가가치 아이템")
    ], title_color=GOLD_ACCENT)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "💬 AI 대화 토큰 충전 & 캐시 지갑", [
        ("추가 질문 토큰 과금", "학생이 기본 무료 챗봇 횟수 소진 시, 50회 충전(4,900원)을 통한 부가 수익"),
        ("PALIN 캐시 지갑 연동", "학생/학부모 충전 포인트를 통한 학원 내 유료 콘텐츠 결제 활성화"),
        ("완벽한 Profit Center", "소프트웨어 사용료를 내는 구조에서, 소프트웨어가 매달 돈을 벌어다 주는 구조로 전환")
    ], title_color=WHITE)

    add_speaker_note(s12, "학원비 외에도 입시 리포트와 토큰 충전을 통해 학부모와 학생이 자발적으로 결제하는 다양한 부가 수익 파이프라인이 열립니다.")

    # ==========================================
    # SLIDE 13: Case Study - 일원학원 Beta 실측 데이터
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "Case Study: 이미 증명된 일원학원 Beta의 압도적인 실측 운영 데이터")

    add_card(s13, Inches(0.9), Inches(1.8), Inches(2.7), Inches(5.0), "-100%", [
        ("조교 인건비 절감", "월 150만~200만 원 나가던 조교 인건비 전액 0원화"),
        ("원장 1인 통제", "100명 이상의 재원생을 원장 1인이 완벽 관리")
    ], title_color=GOLD_ACCENT)

    add_card(s13, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0), "+34.2%", [
        ("평균 순공 자습시간", "마이크로 랭킹전과 보증금 에스크로 도입 후 자습량 급증"),
        ("주말 자습실 만석", "자발적 면학 분위기 형성")
    ], title_color=WHITE)

    add_card(s13, Inches(6.7), Inches(1.8), Inches(2.7), Inches(5.0), "-90%", [
        ("학부모 전화 클레임", "매일 밤 22:00 알림톡으로 불안감 100% 해소"),
        ("상담 스트레스 소멸", "수납/성적 문의 전화 90% 이상 급감")
    ], title_color=WHITE)

    add_card(s13, Inches(9.6), Inches(1.8), Inches(2.7), Inches(5.0), "0%", [
        ("재원생 중도 퇴원율", "D-Day 합격예측과 선배 클리닉 락인 효과"),
        ("재등록률 99.4%", "경쟁 학원으로의 이탈 원천 차단")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s13, "이것은 기획서가 아닙니다. 현재 일원학원에서 실제로 구동되며 완벽한 성과를 내고 있는 실시간 라이브 데이터입니다.")

    # ==========================================
    # SLIDE 14: The Vision - 교육의 무한 스케일업
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "The Vision: 원장님의 공간(Space)을 제국(Empire)으로 확장하십시오")

    add_card(s14, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "01. 공간과 시간의 한계를 돌파", [
        ("강의실 평수의 한계 극복", "오프라인 좌석 수에 얽매이지 않고 온라인 관리형 원생 무한 확장"),
        ("원장 노동 시간의 탈피", "원생 수가 50명에서 500명으로 늘어나도 원장님의 행정 시간은 '0분' 증가"),
        ("분점 및 프랜차이즈화", "동일한 시스템과 AI 뇌를 그대로 복제하여 2호점, 3호점 즉시 개설")
    ], title_color=WHITE)

    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "02. 제국 설계자로의 완벽한 전환", [
        ("잡무에서 완전 해방", "출결 체크, 성적표 입력, 수납 독촉 등 3D 행정 업무 100% 소멸"),
        ("고부가가치 영역 집중", "오직 VIP 심층 입시 상담과 학원 사업 확장에만 원장의 에너지 투입"),
        ("지역 1위 절대 권력", "경쟁 학원이 따라올 수 없는 최첨단 AI 시스템으로 지역 패권 장악")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s14, "강의실 평수와 강사의 시간에 얽매이는 비즈니스는 한계가 명확합니다. PALIN OS를 통해 관리 원생 수를 50명에서 500명으로 늘려도, 원장님의 행정 시간은 0분 증가합니다.")

    # ==========================================
    # SLIDE 15: Pricing - 타협 없는 엔터프라이즈 정가제
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_header(s15, "Pricing: 타협 없는 최고급 정가 정책 (구독료 할인 없음)")

    add_card(s15, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "Tier 1: 베이직 (단과)", [
        ("월 구독료", "월 299,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 50명 한정"),
        ("초기 세팅비", "1,000,000원 (최초 1회)"),
        ("기능", "실시간 관제실 + 기본 출결/수납/OMR ERP + 안심 알림톡 기본 충전")
    ], title_color=SILVER_GRAY)

    add_card(s15, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "Tier 2: 프로 (성장형)", [
        ("월 구독료", "월 599,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 100명 한정"),
        ("초기 세팅비", "1,000,000원 (최초 1회)"),
        ("기능", "원장 전용 AI 뇌 이식(RAG) + 화요일 AI 주간 리포트 + 레드카드 에스크로")
    ], title_color=WHITE)

    add_card(s15, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Tier 3: 엔터프라이즈", [
        ("월 구독료", "월 999,000원 (VAT 별도)"),
        ("수용 정원", "재원생 무제한 (Unlimited)"),
        ("초기 세팅비", "1,000,000원 (화이트라벨링 포함)"),
        ("기능", "100% 화이트라벨링 + 전용 AI 봇 + 선배 클리닉 수수료 쉐어 (Profit Center)")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s15, "할인으로 유혹하지 않습니다. PALIN OS는 단 1원도 깎아주지 않는 최고급 엔터프라이즈 정가를 고수합니다. 대신 선배 클리닉 매칭을 통해 구독료 이상의 수익을 돌려받는 자산이 되어 드립니다.")

    # ==========================================
    # SLIDE 16: Territory Exclusivity - 상권 독점권
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16)
    add_header(s16, "Exclusivity: 반경 2km 권역 내 선착순 1개 학원 독점 가맹 원칙")

    add_card(s16, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "상권 독점권 (Territory Protection)", [
        ("동일 상권 내 중복 가맹 원천 차단", "반경 2km 이내 동일 교습 과목 학원의 가맹을 일절 불허"),
        ("지역 1위 학원의 독점 무기", "주변 경쟁 학원이 도입하고 싶어도 가맹할 수 없는 배타적 경쟁력 부여"),
        ("선착순 계약 원칙", "해당 지역의 첫 번째 원장님께 독점 권한 우선 부여")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "놓치면 경쟁 학원의 무기가 됩니다", [
        ("인근 학원 도입 시 리스크", "옆 학원이 PALIN OS를 먼저 도입할 경우, 학부모와 학생의 이탈 방어 불가"),
        ("즉각적인 도입 결정의 중요성", "원장님의 학원이 지역 내 유일무이한 AI 관제 학원으로 우뚝 설 수 있는 유일한 기회")
    ], title_color=WHITE)

    add_speaker_note(s16, "우리는 무분별하게 가맹점을 늘리지 않습니다. 반경 2km 내 선착순 딱 1개 학원만 독점 가맹을 맺습니다. 원장님이 먼저 잡지 않으시면 옆 경쟁 학원의 무기가 됩니다.")

    # ==========================================
    # SLIDE 17: Live Demo - 1-Click 실시간 역할 체험
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17)
    add_header(s17, "Live Demo: 백문이 불여일견, 스마트폰으로 지금 직접 체험하십시오")

    add_card(s17, Inches(0.9), Inches(1.8), Inches(5.6), Inches(5.0), "3-Way 실시간 롤 시뮬레이터", [
        ("QR 코드 원클릭 접속", "별도 앱 설치 없이 스마트폰 카메라로 QR 코드를 스캔하여 즉시 체험"),
        ("원장 모드 (God Mode)", "관제실에서 실시간 출결 현황을 보고 원클릭 레드카드 발부"),
        ("학생 모드 (수감자)", "레드카드가 발부되는 순간 학생 화면에 경고창이 뜨고 타이머가 정지되는 통제력 체감"),
        ("학부모 모드 (스폰서)", "자녀의 자습 데이터와 AI 주간 리포트가 어떻게 보이는지 실시간 검증")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_card(s17, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "체험 포인트", [
        ("속도와 반응성", "웹 기반임에도 네이티브 앱보다 빠른 0.001초 인터랙션"),
        ("완벽한 권한 분리", "학생이 학부모나 원장의 화면을 절대로 훔쳐볼 수 없는 완벽한 보안 격리")
    ], title_color=WHITE)

    add_speaker_note(s17, "백문이 불여일견입니다. 지금 스마트폰을 꺼내 QR 코드를 찍고, 원장 모드와 학생 모드를 오가며 이 시스템의 압도적인 통제력을 직접 경험해 보십시오.")

    # ==========================================
    # SLIDE 18: FAQ - 원장님 주요 의문점 해소
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s18)
    add_header(s18, "FAQ: 원장님들께서 가장 자주 묻는 질문 3가지")

    add_card(s18, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "Q1. 기존 시스템과 호환되나요?", [
        ("1초 엑셀 일괄 업로드", "기존에 사용하시던 엑셀 명단을 끌어다 놓으면 1초 만에 전산 반영"),
        ("병행 사용 가능", "기존 관리 프로그램과 충돌 없이 독립적인 관제 인프라로 즉시 가동")
    ], title_color=WHITE)

    add_card(s18, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "Q2. 세팅에 얼마나 걸리나요?", [
        ("단 3일 완성", "신청 즉시 학원 전용 코드 발급 및 로고/브랜딩 화이트라벨링 적용"),
        ("AI 뇌 이식 즉시 완료", "원장님 자료 업로드 후 24시간 내 RAG 임베딩 완료")
    ], title_color=GOLD_ACCENT)

    add_card(s18, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Q3. 강사들이 반발하지 않나요?", [
        ("강사 만족도 100%", "출결 체크, 과제 검사, 성적표 입력 등 허드렛일이 90% 사라짐"),
        ("강의에만 전념", "강사들이 행정 스트레스 없이 수업 연구에만 집중 가능")
    ], title_color=WHITE)

    add_speaker_note(s18, "복잡한 이전 작업이나 기계 설치가 필요 없습니다. 단 3일이면 기존 원생 명단 그대로 원장님의 학원에 완벽히 안착합니다.")

    # ==========================================
    # SLIDE 19: Implementation - 3일 완성 온보딩 로드맵
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s19)
    add_header(s19, "Roadmap: 단 3일 만에 완성되는 학원 전산 혁신 온보딩 프로세스")

    add_card(s19, Inches(0.9), Inches(1.8), Inches(3.6), Inches(5.0), "Day 1: 가맹 계약 & 세팅", [
        ("가맹 신청 접수", "이메일 또는 직통 전화로 학원 규모 및 요구사항 확정"),
        ("관리자 계정 개설", "원장님 전용 보안 PIN 및 마스터 관제실 즉시 생성"),
        ("화이트라벨링 반영", "학원 로고, 테마 컬러, 가맹 고유코드 세팅")
    ], title_color=WHITE)

    add_card(s19, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0), "Day 2: AI 뇌 이식 & 테스트", [
        ("원장 자료 RAG 업로드", "원장님의 입시 철학 및 상담 대본 벡터 DB 주입"),
        ("가상 테스트 시뮬레이션", "가상 계정으로 랭킹전 및 레드카드/알림톡 사전 점검"),
        ("전교생 엑셀 일괄 등록", "기존 원생 명단 1초 만에 전산 업로드")
    ], title_color=GOLD_ACCENT)

    add_card(s19, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Day 3: 정식 가동 & 오토파일럿", [
        ("초대 카톡 일괄 발송", "학생과 학부모에게 전용 앱 설치 링크 및 코드 안내"),
        ("기상/취침 미션 시작", "06:30 기상 및 자습실 출결 에스크로 본격 가동"),
        ("화요일 AI 주간 리포트", "매주 화요일 밤 학부모 감동 리포팅 자동 개시")
    ], border_color=GOLD_ACCENT, title_color=GOLD_ACCENT)

    add_speaker_note(s19, "단 3일이면 됩니다. 금요일에 신청하시면 다음 주 월요일부터 완전히 새로운 학원으로 재탄생합니다.")

    # ==========================================
    # SLIDE 20: Contact & Closing (Minimal Luxury)
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s20)

    tb20 = s20.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11), Inches(5.2))
    tf20 = tb20.text_frame
    
    p20_1 = tf20.paragraphs[0]
    p20_1.text = "지금 귀 학원의 'AI 관제 제국'을 구축하십시오."
    p20_1.font.size = Pt(30)
    p20_1.font.bold = True
    p20_1.font.color.rgb = GOLD_ACCENT
    p20_1.font.name = "Malgun Gothic"

    p20_2 = tf20.add_paragraph()
    p20_2.text = "학생의 퇴원율을 0%로 막고, 학원의 가치를 압도적으로 끌어올리는 차세대 교육 OS"
    p20_2.font.size = Pt(16)
    p20_2.font.bold = True
    p20_2.font.color.rgb = WHITE
    p20_2.font.name = "Malgun Gothic"
    p20_2.space_before = Pt(14)

    p20_3 = tf20.add_paragraph()
    p20_3.text = "PALIN OS는 단순한 학습 앱이 아닙니다. 원장님의 교육 철학과 입시 노하우를 완벽히 복제하여\n24시간 지치지 않고 일하는 '학원 전용 AI 수석 부원장'을 이식해 드리는 독점 솔루션입니다."
    p20_3.font.size = Pt(13)
    p20_3.font.color.rgb = SILVER_GRAY
    p20_3.font.name = "Malgun Gothic"
    p20_3.space_before = Pt(16)

    # Contact Box
    contact_card = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(10.9), Inches(2.6))
    contact_card.fill.solid()
    contact_card.fill.fore_color.rgb = CARD_BG
    contact_card.line.color.rgb = GOLD_ACCENT
    contact_card.line.width = Pt(1.5)

    tf_c = contact_card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.4)
    tf_c.margin_top = Inches(0.3)

    pc1 = tf_c.paragraphs[0]
    pc1.text = "🏢 PALIN OS 가맹 및 B2B 시스템 도입 1:1 직통 문의"
    pc1.font.size = Pt(17)
    pc1.font.bold = True
    pc1.font.color.rgb = GOLD_ACCENT
    pc1.font.name = "Malgun Gothic"

    pc2 = tf_c.add_paragraph()
    pc2.text = "• 공식 제휴 이메일: 1286orbital21@gmail.com"
    pc2.font.size = Pt(14)
    pc2.font.bold = True
    pc2.font.color.rgb = WHITE
    pc2.font.name = "Malgun Gothic"
    pc2.space_before = Pt(10)

    pc3 = tf_c.add_paragraph()
    pc3.text = "• 문의 양식: [학원명 / 지역 / 원장님 성함 및 연락처 / 재원생 규모]를 기재하여 메일을 보내주시면 24시간 내 1:1 맞춤 제안서를 전달해 드립니다."
    pc3.font.size = Pt(12)
    pc3.font.color.rgb = SILVER_GRAY
    pc3.font.name = "Malgun Gothic"
    pc3.space_before = Pt(6)

    pc4 = tf_c.add_paragraph()
    pc4.text = "• 지역별 독점권 보장: 동일 상권(반경 2km 내) 선착순 1개 학원 독점 가맹 원칙 준수"
    pc4.font.size = Pt(12)
    pc4.font.bold = True
    pc4.font.color.rgb = GOLD_ACCENT
    pc4.font.name = "Malgun Gothic"
    pc4.space_before = Pt(8)

    add_speaker_note(s20, "경쟁 학원이 먼저 도입하기 전에, 지금 원장님의 학원에 독점 AI 관제 인프라를 구축하십시오. 감사합니다.")

    # Save pptx to both pass-mate, PALIN_UPLOAD, and Downloads
    output_filename = "PALIN_OS_B2B_Director_Proposal.pptx"
    
    pass_mate_path = os.path.join(r"C:\Users\1286o\.gemini\antigravity\scratch\pass-mate", output_filename)
    prs.save(pass_mate_path)
    print(f"Saved PPTX to {pass_mate_path}")

    upload_dir = r"C:\Users\1286o\.gemini\antigravity\scratch\PALIN_UPLOAD"
    if os.path.exists(upload_dir):
        upload_path = os.path.join(upload_dir, output_filename)
        prs.save(upload_path)
        print(f"Saved PPTX to {upload_path}")

    downloads_dir = r"C:\Users\1286o\Downloads"
    if os.path.exists(downloads_dir):
        try:
            dl_path = os.path.join(downloads_dir, output_filename)
            prs.save(dl_path)
            print(f"Saved PPTX to {dl_path}")
        except Exception as e:
            print(f"Could not save to downloads: {e}")

if __name__ == "__main__":
    build_presentation()
