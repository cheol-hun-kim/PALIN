# -*- coding: utf-8 -*-
"""
PALIN OS Enterprise B2B Director Proposal Generator (16 Slides)
Generates the finalized, 16-slide PowerPoint presentation with complete speaker notes
and enhanced business model (Alumni Clinic 8:1:1 Revenue Share, Strict Full-Price SaaS,
Anti-Marketing vs Active-Sales AI Persona Switcher, 0.1s Zero-Hardware Attendance).
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

    # Color Palette (Dark Tech Luxury)
    BG_DARK = RGBColor(10, 14, 26)       # #0A0E1A
    CARD_BG = RGBColor(18, 24, 38)       # #121826
    INDIGO = RGBColor(99, 102, 241)      # #6366F1
    GOLD = RGBColor(245, 158, 11)        # #F59E0B
    EMERALD = RGBColor(16, 185, 129)     # #10B981
    ROSE = RGBColor(244, 63, 94)         # #F43F5E
    CYAN = RGBColor(6, 182, 212)         # #06B6D4
    WHITE = RGBColor(248, 250, 252)      # #F8FAFC
    GRAY = RGBColor(148, 163, 184)       # #94A3B8

    blank_layout = prs.slide_layouts[6]

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="PALIN OS ENTERPRISE B2B PROPOSAL"):
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(10), Inches(0.32))
        p_cat = tb_cat.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GOLD
        p_cat.font.name = "Malgun Gothic"

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.65))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(19)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Malgun Gothic"

    def add_card(slide, left, top, width, height, title, content_items, accent_color=INDIGO, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.font.name = "Malgun Gothic"
        p_title.space_after = Pt(7)

        for item in content_items:
            p = tf.add_paragraph()
            if isinstance(item, tuple):
                h_text, b_text = item
                run_h = p.add_run()
                run_h.text = f"• {h_text}: "
                run_h.font.bold = True
                run_h.font.size = Pt(9.5)
                run_h.font.color.rgb = WHITE
                run_h.font.name = "Malgun Gothic"

                run_b = p.add_run()
                run_b.text = b_text
                run_b.font.size = Pt(9.5)
                run_b.font.color.rgb = GRAY
                run_b.font.name = "Malgun Gothic"
            else:
                p.text = f"• {item}"
                p.font.size = Pt(9.5)
                p.font.color.rgb = GRAY
                p.font.name = "Malgun Gothic"
            p.space_after = Pt(3.5)

    def add_speaker_note(slide, note_text):
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = f"🎙️ [발표자 스크립트]\n{note_text}"

    # ==========================================
    # SLIDE 1: Title
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11), Inches(4.5))
    tf1 = tb1.text_frame
    p1_1 = tf1.paragraphs[0]
    p1_1.text = "PALIN OS"
    p1_1.font.size = Pt(48)
    p1_1.font.bold = True
    p1_1.font.color.rgb = GOLD
    p1_1.font.name = "Malgun Gothic"

    p1_2 = tf1.add_paragraph()
    p1_2.text = "교육의 한계 비용을 '0'으로 만들다.\n1인 원장을 위한 궁극의 오토파일럿, PALIN OS."
    p1_2.font.size = Pt(22)
    p1_2.font.bold = True
    p1_2.font.color.rgb = WHITE
    p1_2.font.name = "Malgun Gothic"
    p1_2.space_before = Pt(8)

    p1_3 = tf1.add_paragraph()
    p1_3.text = "강사의 노동력을 파는 시대는 끝났습니다. 이제 '압도적인 통제 시스템'을 파십시오."
    p1_3.font.size = Pt(14)
    p1_3.font.color.rgb = GRAY
    p1_3.font.name = "Malgun Gothic"
    p1_3.space_before = Pt(12)

    p1_4 = tf1.add_paragraph()
    p1_4.text = "🔒 B2B ENTERPRISE CONFIDENTIAL | 공식 도입 문의: 1286orbital21@gmail.com"
    p1_4.font.size = Pt(11)
    p1_4.font.color.rgb = EMERALD
    p1_4.font.name = "Malgun Gothic"
    p1_4.space_before = Pt(28)

    add_speaker_note(s1, "원장님, 하루에 상담과 행정에 몇 시간을 쓰십니까? 조교 인건비로는 매월 얼마가 나갑니까? 오늘 저는 원장님의 학원을 노동 집약적 가내수공업에서, 한계 비용이 제로에 수렴하는 하이테크 IT 비즈니스로 바꿔드릴 시스템을 소개합니다.")

    # ==========================================
    # SLIDE 2: The Problem - 1인 원장의 딜레마
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "Slide 02. The Problem: 우리는 왜 원생이 늘어날수록 더 불행해지는가?")

    add_card(s2, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 인건비의 늪 (Labor Trap)", [
        ("조교 의존도 심화", "원생 통제를 위해 비싼 조교를 계속 채용해야 하는 고정비 부담"),
        ("잦은 퇴사와 관리 부실", "조교의 불성실한 출결/과제 검사로 인해 원장이 다시 검토하는 악순환"),
        ("수익성 악화", "원생이 늘어도 인건비와 임대료가 정비례로 증가하여 실제 남는 순이익 정체")
    ], ROSE)

    add_card(s2, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 감정 노동의 한계 (Burnout)", [
        ("끝없는 성적 불안", "매주 반복되는 학부모의 불안감 해소를 위한 심야 전화 상담 폭탄"),
        ("수납 독촉의 굴욕", "수업료 결제일마다 반복되는 민망하고 어색한 수납 독촉 통화"),
        ("원장의 에너지 고갈", "학생을 가르치고 연구해야 할 원장의 멘탈이 행정/상담에 완전히 소진")
    ], GOLD)

    add_card(s2, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 스케일업 불가 (Hard Cap)", [
        ("물리적 시간 한계", "원장 1인의 24시간은 한정되어 있어 50~100명 이상 원생 확장 불가"),
        ("시스템 부재", "원장의 입시 노하우와 관리가 매뉴얼화되지 않아 분점/확장 불가능"),
        ("학원에 갇힌 삶", "원장이 하루라도 아프거나 자리를 비우면 학원 전체 운영이 마비")
    ], EMERALD)

    add_speaker_note(s2, "학생이 늘면 돈은 벌지만, 원장님의 삶은 사라집니다. 조교를 뽑자니 인건비가 수익을 갉아먹고, 퀄리티는 떨어집니다. 이 딜레마를 해결하지 못하면 영원히 학원에 갇혀 일해야 합니다.")

    # ==========================================
    # SLIDE 3: The Paradigm Shift - 본질의 전환
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Slide 03. The Paradigm Shift: 해답은 '더 가르치는 것'이 아니라 '완벽하게 통제하는 것'")

    add_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🏛️ 기존 학원 모델의 한계", [
        ("핵심 가치", "강사의 강의력과 시간에 전적으로 의존"),
        ("학부모 보고", "원장이 직접 매주 수동으로 전화 상담 및 불만 응대"),
        ("학생 관리", "조교가 복도를 순찰하며 스마트폰 압수 및 수동 감시"),
        ("원장의 역할", "강의, 상담, 수납, 청소를 도맡아 하는 '플레이어(Player)'"),
        ("수익 구조", "원장의 노동 시간에 비례하는 선형적(Linear) 한계")
    ], ROSE)

    add_card(s3, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🚀 PALIN OS 도입 학원의 혁신", [
        ("핵심 가치", "시스템의 압도적인 24시간 통제력과 실시간 데이터"),
        ("학부모 보고", "AI가 매주 화요일 밤 10시 정밀 심층 리포트 자동 발송"),
        ("학생 관리", "WiFi 감지 + 타이머 + 마이크로 랭킹전으로 자발적 몰입 강제"),
        ("원장의 역할", "손가락 하나로 수백 명을 통제하는 '제국 설계자(God Mode)'"),
        ("수익 구조", "한계 비용이 제로에 수렴하는 지수적(Exponential) 확장")
    ], EMERALD)

    add_speaker_note(s3, "어차피 강의는 1타 강사들의 인강이 가장 훌륭합니다. 학부모가 동네 학원에 기대하는 진짜 본질은 '내 아이를 책상에 묶어두고 관리해 주는 것'입니다. 우리는 이 관리를 100% 자동화했습니다.")

    # ==========================================
    # SLIDE 4: The Core Solution - PALIN OS 소개
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Slide 04. The Core Solution: 원장님의 '뇌'를 복제하여 24시간 돌아가는 SaaS 제국")

    add_card(s4, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚙️ 1. 완전 무인 행정 (Auto-Admin)", [
        ("무인 출결 & 즉시 알림", "학원 네트워크 감지 즉시 자동 출결 기록 및 부모님 통보"),
        ("수납/미납 자동화", "미납자 원클릭 필터링 및 정중한 납부 알림 문자 자동 발송"),
        ("주간 OMR 자동 마감", "일요일 자정 OMR 미제출 시 보증금 벌금 즉시 에스크로 삭감"),
        ("조교 인건비 0원화", "학원의 모든 행정 프로세스가 기계처럼 24시간 자동 실행")
    ], CYAN)

    add_card(s4, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "🧠 2. AI 맞춤형 뇌 (AI Brain)", [
        ("원장 입시 철학 RAG 주입", "원장님의 수험생활백서와 상담 대본을 벡터 DB로 동적 병합"),
        ("24시간 1:1 상담 대행", "새벽 2시에도 원장님의 어투와 팩트폭격으로 학생 멘탈 케어"),
        ("학부모 페르소나 스위칭", "신뢰형 멘토 모드 vs 전략적 특강 제안 모드 자유 선택"),
        ("상담 리소스 90% 절감", "원장님은 특급 심층 상담에만 집중")
    ], GOLD)

    add_card(s4, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🔒 3. 심리적 락인 (Psychological Lock-in)", [
        ("Strava식 랭킹전", "내 동네/고교 친구들과의 실시간 자습 순위 경쟁"),
        ("Beeminder 보증금", "기상/취침 미션 실패 시 1,000원~5,000원 벌금 에스크로 차감"),
        ("철저한 권한 격리 (RBAC)", "학생/학부모/원장이 각자 최적화된 화면만 열람"),
        ("퇴원율 0% 수렴", "한 번 들어오면 수능 날까지 빠져나갈 수 없는 강력한 몰입")
    ], INDIGO)

    add_speaker_note(s4, "PALIN OS는 단순한 프로그램이 아닙니다. 원장님의 행정, 상담, 통제를 완벽히 대신해 주는 3대 모듈로 구성된 종합 운영체제입니다.")

    # ==========================================
    # SLIDE 5: Architecture - 3자 완벽 권한 격리 (RBAC)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Slide 05. Architecture: 철저한 3자 역할 기반 권한 격리 (RBAC)")

    add_card(s5, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "🧑‍🎓 수험생 모드 (몰입/수감자)", [
        ("통제 UI만 노출", "자습 타이머, 동네/학교 랭킹, 주간 미션, D-Day 학생증만 사용 가능"),
        ("관리자 영역 원천 차단", "학부모의 감시 설정이나 관리자 기능에는 일절 접근 불가"),
        ("게임 같은 몰입감", "경쟁심과 성취감을 자극하여 공부를 게임처럼 플레이")
    ], INDIGO)

    add_card(s5, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "👨‍👩‍👧 학부모 모드 (안심/스폰서)", [
        ("실시간 조회 (Read-only)", "자녀의 자습시간, 출결 현황, 일일 미션 달성률을 실시간 모니터링"),
        ("간섭 불가 & 안심 극대화", "자녀의 학습 흐름을 방해하지 않고 묵묵히 응원"),
        ("원클릭 금융 지원", "교재비, 모의고사 리포트, 학원비 결제 창구 일원화")
    ], EMERALD)

    add_card(s5, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🏫 학원장 모드 (갓 모드 관제실)", [
        ("B2B 전용 중앙 ERP", "전체 원생의 실시간 위치, 타이머, 이탈 상태 실시간 전지적 조망"),
        ("원클릭 절대 통제권", "원장 직통 레드카드 발부, 보증금 차감, 긴급 SMS 발송"),
        ("전산 마스터 연동", "학원 전용 로고 및 가맹 코드 기반 독립 폐쇄망 운영")
    ], GOLD)

    add_speaker_note(s5, "학생이 학부모의 감시 UI를 보게 되면 거부감을 느끼고 이탈합니다. PALIN OS는 철저한 권한 분리를 통해 학생에겐 게임 같은 경쟁을, 학부모에겐 안심과 결제 창구를, 원장에겐 절대 권력을 줍니다.")

    # ==========================================
    # SLIDE 6: Feature 1 - 마스터 관제실 (원장 전용 ERP)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Slide 06. Feature 1: 손가락 하나로 수백 명을 통제하는 마스터 관제실")

    add_card(s6, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "📡 무설치 0.1초 네트워크 출결", [
        ("하드웨어 설치 제로", "비싼 비콘이나 지문인식기 없이 학원 WiFi/네트워크 대역 감지"),
        ("0.1초 즉시 체크인", "학원 문을 열고 들어오는 순간 관제실에 등원 기록 자동 반영"),
        ("지각/결석 자동 격발", "수업 시작 시간까지 미등원 시 학부모 안심 SMS 즉시 발송")
    ], CYAN)

    add_card(s6, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "💳 1-Click 미납금 관리", [
        ("미납 원생 실시간 필터링", "수강료/교재비 미납자 목록을 1초 만에 색출"),
        ("원클릭 카톡 안내 발송", "원장이 직접 아쉬운 소리 할 필요 없이 정중한 수납 안내 자동 발송"),
        ("미납 상태 자동 동기화", "결제 완료 즉시 관제실 및 학부모 앱에서 정상 처리")
    ], GOLD)

    add_card(s6, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🟥 원클릭 레드카드 발송기", [
        ("자습 태도 불량 즉시 제재", "졸음, 잡담, 스마트폰 몰래 사용 적발 시 버튼 하나로 경고"),
        ("성실 보증금 벌금 차감", "학생 에스크로 보증금에서 1,000원~5,000원 즉시 삭감"),
        ("학부모 통보 동시 실행", "부모님께 징계 사유와 타임스탬프가 자동 문자로 전송")
    ], ROSE)

    add_speaker_note(s6, "더 이상 조교가 문 앞에서 출석 체크를 할 필요가 없습니다. 미납자에게 전화해서 아쉬운 소리 할 필요도 없습니다. 버튼 한 번이면 끝납니다.")

    # ==========================================
    # SLIDE 7: Feature 2 - AI 커스텀 뇌 이식 (복제된 원장님)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "Slide 07. Feature 2: 내가 자는 동안에도 내 분신이 1:1 상담을 진행하는 AI 뇌 이식")

    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📚 1. 원장님 입시 철학 & 수험생활백서 RAG", [
        ("학원 자체 데이터 무제한 주입", "원장님의 강의 교재, 커리큘럼, 입시 노하우, 상담 대본 PDF/TXT 업로드"),
        ("실시간 동적 임베딩", "Gemini AI가 원장님의 지식을 학습하여 학원 전용 AI 뇌로 완벽 동기화"),
        ("단순 챗봇과의 차별화", "일반 범용 AI와 달리 '우리 학원만의 커리큘럼과 원장님 방침'으로만 완벽하게 응답"),
        ("지식의 자산화", "강사가 퇴사해도 학원의 핵심 입시 노하우와 상담 퀄리티는 영구 보존")
    ], GOLD)

    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "💬 2. 원장 페르소나 팩트폭격 & 멘탈 케어", [
        ("24시간 1:1 밀착 코칭", "새벽 2시에 학생이 슬럼프 고민을 토로해도 원장님의 어투로 즉각 처방전 제시"),
        ("냉혹한 팩트폭격", "달콤한 위로 대신 목표 대학 갭 분석을 바탕으로 한 현실적 행동 강령 제시"),
        ("시스템 프롬프트 커스텀", "스파르타식 엄격한 원장, 따뜻한 멘토형 원장 등 학원 성향에 맞춰 성격 자유 세팅"),
        ("무한 스케일업", "원생이 500명으로 늘어나도 1:1 상담 퀄리티의 타협 없이 24시간 완벽 커버")
    ], INDIGO)

    add_speaker_note(s7, "수백 명의 학생이 새벽 2시에 우울하다며 질문을 던져도, 원장님의 철학이 담긴 AI가 1:1로 밀착 멘토링을 해줍니다. 퀄리티의 타협 없이 무한대로 스케일업이 가능해집니다.")

    # ==========================================
    # SLIDE 8: Feature 3 - 학부모용 자율 AI 페르소나
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "Slide 08. Feature 3: 원장님의 영업 철학에 맞춘 100% 자율 학부모 AI 페르소나")

    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🛡️ 모드 A: 신뢰형 멘토 (Anti-Marketing)", [
        ("결제를 만류하는 역설적 진정성", "불안해하는 학부모가 추가 결제를 문의할 때, '지금은 돈을 쓸 때가 아니라 기본 복습 밀도를 높일 때입니다' 단호히 권고"),
        ("학부모의 절대적 신뢰 획득", "상업적이지 않고 아이를 진심으로 위한다는 확신을 주어 재등록률 100% 달성"),
        ("원장의 품격 상승", "학원과 원장님의 브랜드를 지역 최고 수준의 교육 전문가로 각인")
    ], EMERALD)

    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "📈 모드 B: 전략적 제안형 (Active-Sales)", [
        ("취약점 진단 기반 자연스러운 제안", "모의고사 성적 하락 시 해당 단원 클리닉 및 방학 특강을 논리적으로 추천"),
        ("학원 매출 극대화", "학부모의 니즈가 가장 높은 시점에 최적의 맞춤형 커리큘럼 안내"),
        ("관제실에서 1초 원클릭 스위칭", "본사의 강요 없이 원장님의 사업 방식에 따라 AI 성향을 100% 자유롭게 세팅")
    ], GOLD)

    add_speaker_note(s8, "우리는 본사의 영업 방식을 원장님께 강요하지 않습니다. 신뢰형 멘토 모드로 학부모를 완벽히 록인할지, 적극적인 특강 제안으로 매출을 올릴지는 오직 원장님의 자유의사에 달려 있습니다.")

    # ==========================================
    # SLIDE 9: Feature 4 - 게이미피케이션 (학생 통제 매커니즘)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "Slide 09. Feature 4: 강압적 감시가 아닌, 자발적 중독을 설계하는 게이미피케이션")

    add_card(s9, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "🏆 지역/고교 마이크로 랭킹", [
        ("국지적 자존심 경쟁", "'분당구 1위', '낙생고 2위' 등 실시간 동네/학교 순위 노출"),
        ("실시간 띠배너 브로드캐스트", "1위 탈환 시 전교생 화면 상단에 골드 띠배너 즉시 공지"),
        ("자발적 자습 시간 폭증", "친구를 이기기 위해 밤늦게까지 타이머를 켜두는 선의의 경쟁")
    ], GOLD)

    add_card(s9, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "🔄 주간 초기화 룰 (Reset)", [
        ("매주 일요일 자정 리셋", "모든 랭킹 점수가 일요일 자정에 0으로 초기화"),
        ("새로운 희망 부여", "이번 주에 뒤처진 학생도 다음 주 월요일 0시부터 다시 1등 도전 가능"),
        ("이탈 방지", "포기하지 않고 매주 월요일 아침 앱에 재접속하도록 유도")
    ], CYAN)

    add_card(s9, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "👑 상위 1% VIP 라운지 강등제", [
        ("가차 없는 권한 박탈", "주간 자습 상위 1% 미달 시 즉시 VIP 블랙 라운지에서 강제 퇴장(Kick-out)"),
        ("상실의 공포 (FOMO)", "VIP 자격을 유지하기 위해 자습량을 극한으로 유지"),
        ("의치한약수 멘토링", "상위 1% 학생에게만 주어지는 특권으로 도전 의식 고취")
    ], ROSE)

    add_speaker_note(s9, "감시 카메라로 감시하면 반발하지만, 랭킹과 게임으로 만들면 학생들은 스스로 밤을 새워 공부합니다.")

    # ==========================================
    # SLIDE 10: Feature 5 - 빈틈없는 오토파일럿 행정
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "Slide 10. Feature 5: 핑계를 원천 봉쇄하는 기계적인 엄격함의 오토파일럿")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "📝 주간 OMR 일요일 자정 마감", [
        ("타협 없는 자동 마감", "일요일 23:59까지 OMR 미제출 시 예외 없이 자동 차단"),
        ("보증금 패널티 즉시 차감", "과제 미제출에 따른 성실 보증금 벌금 에스크로 자동 삭감"),
        ("학부모 자동 통보", "과제 미제출 사실이 부모님께 즉시 알림톡으로 발송")
    ], ROSE)

    add_card(s10, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "⏱️ VOD 168시간 락 & 안티치트", [
        ("7일 후 시청 원천 차단", "강의 권한 부여 후 168시간(7일) 경과 시 영상 자동 락(Lock)"),
        ("배속 롤백 안티치트", "2배속 이상 날림 수강 시 시청 시간 미인정 및 경고"),
        ("초단위 완강률 추적", "학생이 진짜로 집중해서 들었는지 초단위 타임라인 분석")
    ], CYAN)

    add_card(s10, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "📊 매주 화요일 22:00 AI 리포트", [
        ("Gemini AI 종합 진단", "한 주간의 자습시간, 출결, 미션 성공률을 분석해 300자 카톡 대본 생성"),
        ("전교생 일괄 발송", "화요일 밤 학부모 스마트폰으로 고품격 리포트 자동 발송"),
        ("수납 촉구 링크 연동", "미납자의 경우 리포트 하단에 결제 안내 정중히 포함")
    ], EMERALD)

    add_speaker_note(s10, "학생의 핑계와 타협하지 않습니다. 정해진 룰대로 시스템이 기계처럼 엄격하게 작동하여 학원의 기강을 완성합니다.")

    # ==========================================
    # SLIDE 11: Business Model - 학원-졸업생 선순환 클리닉
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "Slide 11. Business Model: 제자를 잘 키울수록 학원의 영구적 부가 수익이 되는 선순환 생태계")

    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🎓 1. 학원 출신 선배 ➔ 후배 1:1 클리닉 (8:1:1)", [
        ("원장이 키운 제자가 학원의 자산", "학원 출신 의대/SKY 합격생을 학원 전용 튜터로 등록"),
        ("후배 재원생의 압도적 신뢰", "우리 학원에서 공부해 명문대 간 검증된 선배에게 1:1 킬러문항 질의응답"),
        ("수익 분배 구조", "선배 튜터 80% : 학원장 10% (브랜드 보증료) : 본사 10% (플랫폼 운영)"),
        ("영구적 Cash Cow", "재원생 100명 중 30명 이용 시 월 60만 원 순수익 창출 (구독료 상쇄)")
    ], GOLD)

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "💎 2. AI 입시 심층 리포트 & 캐시 마이크로 과금", [
        ("AI 심층 리포트 (16,900원~34,900원)", "모의고사 직후 학부모 불안감이 극에 달했을 때 원클릭 정밀 진단서 발급"),
        ("AI 대화 토큰 충전 (4,900원)", "기본 무료 질문 횟수 소진 시 추가 충전을 통한 부가 수익"),
        ("비용에서 수익 센터로 전환", "학원 관리 소프트웨어가 매달 돈을 벌어다 주는 강력한 Profit Center로 탈바꿈")
    ], INDIGO)

    add_speaker_note(s11, "원장님이 정성껏 가르쳐 명문대에 보낸 제자가 다시 후배를 가르치고, 그 수익의 일부가 학원 통장에 매달 꽂힙니다. 학생을 잘 키울수록 학원의 수익이 영구적으로 늘어나는 생태계입니다.")

    # ==========================================
    # SLIDE 12: Case Study - PALIN OS 도입 효과 (일원학원 Beta)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "Slide 12. Case Study: 이미 증명된 일원학원 Beta의 압도적인 운영 데이터")

    add_card(s12, Inches(0.8), Inches(1.5), Inches(2.7), Inches(5.4), "📉 100% 감소", [
        ("조교 인건비 전액 절감", "월 150만~200만 원 나가던 조교 인건비가 0원으로 축소"),
        ("원장 1인 완벽 통제", "100명 이상의 재원생을 원장 1인이 관제실에서 손쉽게 관리")
    ], ROSE)

    add_card(s12, Inches(3.7), Inches(1.5), Inches(2.7), Inches(5.4), "📈 +34.2% 증가", [
        ("평균 순공 자습시간", "마이크로 랭킹전과 보증금 에스크로 도입 후 일일 자습시간 34.2% 급증"),
        ("주말 자습실 만석", "자발적 면학 분위기 형성")
    ], EMERALD)

    add_card(s12, Inches(6.6), Inches(1.5), Inches(2.7), Inches(5.4), "📉 90% 이상 소멸", [
        ("학부모 전화 클레임", "매일 밤 22:00 알림톡과 실시간 대시보드 제공으로 불안감 100% 해소"),
        ("상담 스트레스 해소", "수납 및 성적 문의 전화 90% 이상 급감")
    ], CYAN)

    add_card(s12, Inches(9.5), Inches(1.5), Inches(2.7), Inches(5.4), "🛡️ 0% 수렴", [
        ("재원생 중도 퇴원율", "D-Day 합격예측과 선배 클리닉 락인 효과로 퇴원율 0% 달성"),
        ("재등록률 99.4%", "주변 학원으로의 이탈을 완벽 차단")
    ], GOLD)

    add_speaker_note(s12, "이것은 기획서가 아닙니다. 현재 일원학원에서 실제로 구동되며 완벽한 성과를 내고 있는 실시간 라이브 데이터입니다.")

    # ==========================================
    # SLIDE 13: The Vision - 교육의 무한 스케일업
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "Slide 13. The Vision: 원장님의 공간(Space)을 제국(Empire)으로 확장하십시오")

    add_card(s13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🏢 1. 공간과 시간의 한계를 돌파", [
        ("강의실 평수의 한계 극복", "오프라인 좌석 수에 얽매이지 않고 온라인 관리형 원생 무한 확장"),
        ("원장 노동 시간의 탈피", "원생 수가 50명에서 500명으로 늘어나도 원장님의 행정 시간은 '0분' 증가"),
        ("분점 및 프랜차이즈화", "동일한 시스템과 AI 뇌를 그대로 복제하여 2호점, 3호점 즉시 개설")
    ], CYAN)

    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "👑 2. 제국 설계자로의 완벽한 전환", [
        ("잡무에서 완전 해방", "출결 체크, 성적표 입력, 수납 독촉 등 3D 행정 업무 100% 소멸"),
        ("고부가가치 영역 집중", "오직 VIP 심층 입시 상담과 학원 사업 확장에만 원장의 에너지 투입"),
        ("지역 1위 절대 권력", "경쟁 학원이 따라올 수 없는 최첨단 AI 시스템으로 지역 패권 장악")
    ], GOLD)

    add_speaker_note(s13, "강의실 평수와 강사의 시간에 얽매이는 비즈니스는 한계가 명확합니다. PALIN OS를 통해 관리 원생 수를 50명에서 500명으로 늘려도, 원장님의 행정 시간은 0분 증가합니다.")

    # ==========================================
    # SLIDE 14: Pricing - 타협 없는 정가제 & 상권 독점권
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "Slide 14. Pricing: 타협 없는 최고급 정가 정책 & 반경 2km 권역 독점권")

    add_card(s14, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥉 Tier 1: 베이직 (단과)", [
        ("월 구독료", "월 299,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 50명 한정"),
        ("초기 세팅비", "1,000,000원 (최초 1회 DB 세팅)"),
        ("핵심 기능", "실시간 관제실 + 기본 출결/수납/OMR ERP + 안심 알림톡 기본 충전")
    ], GRAY)

    add_card(s14, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥈 Tier 2: 프로 (성장형)", [
        ("월 구독료", "월 599,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 100명 한정"),
        ("초기 세팅비", "1,000,000원 (최초 1회 DB 세팅)"),
        ("핵심 기능", "원장님 전용 AI 뇌 이식(RAG) + 화요일 AI 주간 리포트 + 레드카드 에스크로")
    ], INDIGO)

    add_card(s14, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥇 Tier 3: 엔터프라이즈 (대형)", [
        ("월 구독료", "월 999,000원 (VAT 별도)"),
        ("수용 정원", "재원생 무제한 (Unlimited)"),
        ("초기 세팅비", "1,000,000원 (화이트라벨링 포함)"),
        ("핵심 기능", "100% 화이트라벨링 + 전용 AI 봇 + 선배 클리닉 수수료 쉐어 (Profit Center)")
    ], GOLD)

    add_speaker_note(s14, "할인으로 유혹하지 않습니다. PALIN OS는 단 1원도 깎아주지 않는 최고급 엔터프라이즈 정가를 고수합니다. 대신 선배 클리닉 매칭을 통해 구독료의 몇 배를 벌어들이는 자산이 되어 드립니다. 반경 2km 내 선착순 1개 학원만 독점 가맹을 체결합니다.")

    # ==========================================
    # SLIDE 15: Q&A 및 1-Click 실시간 역할 체험기
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_header(s15, "Slide 15. Q&A & Live Demo: 백문이 불여일견, 원장님의 스마트폰으로 지금 체험하십시오")

    add_card(s15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📱 1. 실시간 3-Way 롤 시뮬레이터", [
        ("QR 코드 즉시 접속", "별도 앱 설치 없이 스마트폰 카메라로 QR 코드를 스캔하여 즉시 접속"),
        ("원장 모드 (God Mode)", "관제실에서 실시간 출결 현황을 보고 원클릭 레드카드 발부 체험"),
        ("학생 모드 (수감자)", "레드카드가 발부되는 순간 학생 화면에 경고창이 뜨고 타이머가 정지되는 통제력 체감"),
        ("학부모 모드 (스폰서)", "자녀의 자습 데이터와 AI 주간 리포트가 어떻게 보이는지 실시간 검증")
    ], CYAN)

    add_card(s15, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "❓ 2. 현장 질의응답 (FAQ)", [
        ("Q. 기존 학원 프로그램과 병행 가능한가요?", "A. 네, 엑셀 1초 업로드로 기존 데이터와 완벽히 호환됩니다."),
        ("Q. 세팅에 시간이 오래 걸리나요?", "A. 단 3일이면 학원 전용 브랜딩과 AI 뇌 이식 세팅이 완료됩니다."),
        ("Q. 강사들이 반발하지 않나요?", "A. 행정 업무가 90% 사라지므로 강사들이 가장 환호합니다.")
    ], INDIGO)

    add_speaker_note(s15, "백문이 불여일견입니다. 지금 스마트폰을 꺼내 QR 코드를 찍고, 원장 모드와 학생 모드를 오가며 이 시스템의 압도적인 통제력을 직접 경험해 보십시오.")

    # ==========================================
    # SLIDE 16: Partnership & Contact Closing
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16)

    tb16 = s16.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11), Inches(5.2))
    tf16 = tb16.text_frame
    p16_1 = tf16.paragraphs[0]
    p16_1.text = "지금 귀 학원의 'AI 관제 제국'을 구축하십시오."
    p16_1.font.size = Pt(26)
    p16_1.font.bold = True
    p16_1.font.color.rgb = GOLD
    p16_1.font.name = "Malgun Gothic"

    p16_2 = tf16.add_paragraph()
    p16_2.text = "학생의 퇴원율을 0%로 막고, 학원의 가치를 압도적으로 끌어올리는 차세대 교육 OS"
    p16_2.font.size = Pt(15)
    p16_2.font.color.rgb = WHITE
    p16_2.font.name = "Malgun Gothic"
    p16_2.space_before = Pt(14)

    p16_3 = tf16.add_paragraph()
    p16_3.text = "PALIN OS는 단순한 학습 앱이 아닙니다. 원장님의 교육 철학과 입시 노하우를 완벽히 복제하여\n24시간 지치지 않고 일하는 '학원 전용 AI 수석 부원장'을 이식해 드리는 독점 솔루션입니다."
    p16_3.font.size = Pt(12)
    p16_3.font.color.rgb = GRAY
    p16_3.font.name = "Malgun Gothic"
    p16_3.space_before = Pt(16)

    # Contact Box
    contact_card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(10.9), Inches(2.6))
    contact_card.fill.solid()
    contact_card.fill.fore_color.rgb = CARD_BG
    contact_card.line.color.rgb = GOLD
    contact_card.line.width = Pt(2)

    tf_c = contact_card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.4)
    tf_c.margin_top = Inches(0.3)

    pc1 = tf_c.paragraphs[0]
    pc1.text = "🏢 PALIN OS 가맹 및 B2B 시스템 도입 1:1 직통 문의"
    pc1.font.size = Pt(16)
    pc1.font.bold = True
    pc1.font.color.rgb = GOLD
    pc1.font.name = "Malgun Gothic"

    pc2 = tf_c.add_paragraph()
    pc2.text = "• 공식 제휴 이메일: 1286orbital21@gmail.com"
    pc2.font.size = Pt(13)
    pc2.font.bold = True
    pc2.font.color.rgb = WHITE
    pc2.font.name = "Malgun Gothic"
    pc2.space_before = Pt(10)

    pc3 = tf_c.add_paragraph()
    pc3.text = "• 문의 양식: [학원명 / 지역 / 원장님 성함 및 연락처 / 재원생 규모]를 기재하여 메일을 보내주시면 24시간 내 1:1 맞춤 제안서를 전달해 드립니다."
    pc3.font.size = Pt(11)
    pc3.font.color.rgb = GRAY
    pc3.font.name = "Malgun Gothic"
    pc3.space_before = Pt(6)

    pc4 = tf_c.add_paragraph()
    pc4.text = "• 지역별 독점권 보장: 동일 상권(반경 2km 내) 선착순 1개 학원 독점 가맹 원칙 준수"
    pc4.font.size = Pt(11)
    pc4.font.bold = True
    pc4.font.color.rgb = EMERALD
    pc4.font.name = "Malgun Gothic"
    pc4.space_before = Pt(8)

    add_speaker_note(s16, "경쟁 학원이 먼저 도입하기 전에, 지금 원장님의 학원에 독점 AI 관제 인프라를 구축하십시오. 감사합니다.")

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
