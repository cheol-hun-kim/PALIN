# -*- coding: utf-8 -*-
"""
PALIN OS Enterprise B2B Director Proposal Generator
Generates a highly detailed, 18-slide PowerPoint presentation (.pptx)
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

    # ==========================================
    # SLIDE 1: Cover Title
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4.5))
    tf1 = tb1.text_frame
    p1_1 = tf1.paragraphs[0]
    p1_1.text = "PALIN OS"
    p1_1.font.size = Pt(46)
    p1_1.font.bold = True
    p1_1.font.color.rgb = GOLD
    p1_1.font.name = "Malgun Gothic"

    p1_2 = tf1.add_paragraph()
    p1_2.text = "학원 가맹 및 엔터프라이즈 중앙 관제 인프라 도입 제안서"
    p1_2.font.size = Pt(23)
    p1_2.font.bold = True
    p1_2.font.color.rgb = WHITE
    p1_2.font.name = "Malgun Gothic"
    p1_2.space_before = Pt(10)

    p1_3 = tf1.add_paragraph()
    p1_3.text = "수험생 · 학부모 · 학원 3자 연동 지능형 입시 관제 & 원장 전용 AI 뇌 이식 솔루션"
    p1_3.font.size = Pt(13.5)
    p1_3.font.color.rgb = GRAY
    p1_3.font.name = "Malgun Gothic"
    p1_3.space_before = Pt(12)

    p1_4 = tf1.add_paragraph()
    p1_4.text = "🔒 B2B CONFIDENTIAL & PROPRIETARY | 공식 도입 문의: 1286orbital21@gmail.com"
    p1_4.font.size = Pt(11)
    p1_4.font.color.rgb = EMERALD
    p1_4.font.name = "Malgun Gothic"
    p1_4.space_before = Pt(30)

    # ==========================================
    # SLIDE 2: Executive Summary
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "01. 도입 배경: 오프라인 학원의 3대 구조적 한계와 PALIN OS의 해법")

    add_card(s2, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 위기 1: 수강생 이탈 & 퇴원율", [
        ("동기부여의 부재", "학원 문을 나서는 순간 집과 독서실에서 스마트폰 중독 및 슬럼프 발생"),
        ("인강/독학 전향", "혼자서 공부하겠다는 학생의 이탈을 막을 객관적 학습 몰입 장치 부재"),
        ("수동적 사후 관리", "퇴원 통보를 받고 나서야 학생의 학습 부진을 인지하는 구조적 악순환"),
        ("PALIN OS 솔루션", "Strava식 동네 랭킹전 + Beeminder 금융 인질 보증금으로 자발적 일일 학습 100% 강제")
    ], ROSE)

    add_card(s2, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 위기 2: 학부모 소통 피로도", [
        ("심야 상담 전화", "매주 반복되는 학부모의 불안감 해소를 위한 감정 소모 및 업무 과부하"),
        ("정량적 증거 부재", "아이의 학습 태도와 자습 시간에 대한 실시간 데이터 증빙 어려움"),
        ("수납/교재비 마찰", "수업료 납부일마다 반복되는 어색하고 번거로운 수납 독촉 커뮤니케이션"),
        ("PALIN OS 솔루션", "매일 밤 22:00 실시간 안심 리포트 자동 발송 + AI 주간 생존 보고서 자동 발간")
    ], GOLD)

    add_card(s2, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "⚠️ 위기 3: 원장/강사 리소스 낭비", [
        ("과도한 행정 업무", "출결 체크, 모의고사 성적표 수기 입력, 상담 일지 기록으로 본업 침해"),
        ("원장 지식의 유실", "원장님만의 독보적 입시/상담 노하우가 강사 퇴사 시 학원 밖으로 유출"),
        ("브랜드 가치 희석", "대형 프랜차이즈 및 일타 강사 플랫폼 대비 차별화된 IT 인프라 부재"),
        ("PALIN OS 솔루션", "원장님 전용 AI 뇌 이식(RAG) + 화이트라벨링 전용 앱 구축으로 지역 1위 방어")
    ], EMERALD)

    # ==========================================
    # SLIDE 3: 3-Way Ecosystem Architecture
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "02. 시스템 아키텍처: 수험생 · 학부모 · 학원 3자 유기적 연동 생태계")

    add_card(s3, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "🧑‍🎓 1. 수험생 모바일 클라이언트", [
        ("Strava식 랭킹전", "우리 동네(분당구, 강남구 등) 및 고등학교별 실시간 자습 순위 리더보드"),
        ("Beeminder 보증금", "06:30 기상/23:30 취침 미션 실패 시 1,000원~5,000원 벌금 에스크로 차감"),
        ("정시 합격예측", "11,688개 대학/학과 백분위 기반 적정/소신 실시간 정밀 진단"),
        ("목표 D-Day 뱃지", "목표 대학 가상 학생증(27학번) 발급 및 인스타그램 합격 부적 공유"),
        ("1% VIP 블랙라운지", "의치한약수 멘토링 및 실시간 비대면 입시 Q&A 질의응답 창구")
    ], INDIGO)

    add_card(s3, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "👨‍👩‍👧 2. 학부모 실시간 안심 포털", [
        ("매일 밤 22:00 리포트", "오늘 총 자습시간, 일일 목표 달성률, 생활 미션 성공 여부 자동 알림톡"),
        ("긴급 결석/이탈 SMS", "정규 자습 시간 이탈 및 지각 발생 시 0.1초 내 부모님 안심 SMS 자동 발송"),
        ("원장 AI 상담 대행", "원장님의 지식이 이식된 24시간 입시 코칭 챗봇으로 1차 질의응답"),
        ("수업료/교재비 조회", "실시간 학원비 수납 현황 및 모의고사 응시 내역 투명 공개"),
        ("자녀 1:1 독립 뷰", "가맹 학원 코드 등록 시 VIP 전액 무료 혜택 자동 부여")
    ], EMERALD)

    add_card(s3, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🏫 3. 학원장 중앙 통합 관제실", [
        ("실시간 재원생 레이더", "전체 원생의 현재 집중 자습 상태, 잔여 시간, 이탈 징후 실시간 모니터링"),
        ("원장 전용 AI 뇌 이식", "원장님의 커리큘럼/상담 대본/입시 철학 RAG 지식 스튜디오 구축"),
        ("원클릭 긴급 징계", "지각/태도 불량 시 원장 직통 레드카드 발부 및 보증금 차감 동시 실행"),
        ("AI 주간 리포트 발간", "매주 화요일 22:00 전 원생 1:1 맞춤형 피드백 카톡 자동 배치 발송"),
        ("VOD 초단위 추적", "강의 녹화본 업로드 및 원생별 초단위 완강률/건너뛰기 감지")
    ], GOLD)

    # ==========================================
    # SLIDE 4: Student App - Micro Rankings
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "03. [수험생 기능 1] Strava 모델 마이크로 지역/고교 랭킹 리더보드")

    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🏆 1. 동네 & 학교별 실시간 랭킹전", [
        ("전국 단위의 절망감 탈피", "전국 50만 수험생과의 무의미한 비교 대신 '대치동', '분당구' 등 내 동네 친구들과의 실시간 순위 경쟁"),
        ("전교 자습 랭킹", "소속 고등학교(예: 낙생고, 대치고) 내 전교 1위~10위 실시간 노출로 강력한 자존심 경쟁 유발"),
        ("실시간 초단위 동기화", "타이머 작동 즉시 순위가 변동되며, 1등 탈환 시 실시간 금메달(🥇) 뱃지 자동 부여"),
        ("0분 학생 무기록 방어", "자습 기록이 없는 학생은 '자습 0분 (집계 대기)'로 처리하여 데이터 왜곡 방지")
    ], GOLD)

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🏫 2. 학교 대항전 (길드전) & Streak 불꽃", [
        ("학교 대항 길드전", "고등학교별 주간 총합 자습시간을 집계하여 지역 내 '가장 공부 많이 하는 고등학교' 리더보드 운영"),
        ("집단 몰입 효과", "같은 학교 친구들을 앱으로 초대하여 함께 순위를 올리는 유기적 바이럴 효과 창출"),
        ("듀오링고 연속 출석 불꽃", "하루라도 미션 실패 시 불꽃이 꺼지는 연속 일수(Streak) 시스템으로 매일 접속 강제"),
        ("성실도 5대 리그 승급", "Bronze(1.0x)부터 Diamond/Master(2.5x)까지 연속 자습에 따른 포인트 배수 보상")
    ], INDIGO)

    # ==========================================
    # SLIDE 5: Student App - Beeminder Financial Escrow
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "04. [수험생 기능 2] Beeminder 금융 인질 성실 보증금 & D-Day 합격 부적")

    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🛡️ 1. 금융 인질 에스크로 (손실 회피 심리)", [
        ("기본 보증금 50,000원 예치", "가입 시 성실 보증금을 예치하고, 일일 생활 미션을 성실히 수행할 의무 부여"),
        ("06:30 기상 / 23:30 취침 미션", "정해진 시간에 성공 인증 버튼을 누르지 못할 경우 1,000원~5,000원 즉시 차감"),
        ("손실 회피(Loss Aversion) 극대화", "보상보다 벌금에 2.5배 민감하게 반응하는 행동경제학 기반 강력한 기상/취침 강제"),
        ("누적 벌금 투명 공개", "마이페이지에서 보증금 잔액 및 누적 벌금을 실시간으로 확인하여 경각심 유지")
    ], ROSE)

    add_card(s5, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🪪 2. 목표 대학 가상 학생증 & 인스타 합격 부적", [
        ("27학번 가상 학생증 캔버스", "목표 대학(서울대, 연세대, 고려대 등)과 학과가 각인된 실물 스타일 디지털 학생증 즉시 발급"),
        ("인스타그램 스토리 공유", "시험 D-Day와 합격 엠블럼이 포함된 합격 부적을 SNS에 공유하여 학원 브랜드 자연 노출"),
        ("D-Day 수동 변경 & 커스텀", "2027 수능, 6월 모평, 9월 모평, 대학별 논술 고사일을 자유롭게 세팅"),
        ("안정 마지노선 백업", "목표 대학 외에 반드시 합격해야 하는 마지노선 대학을 동시에 설정하여 멘탈 관리")
    ], CYAN)

    # ==========================================
    # SLIDE 6: Student App - 11,688 College Prediction Engine
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "05. [수험생 기능 3] 11,688개 전국 대학/학과 정시 실시간 AI 합격예측")

    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📊 1. 정밀 백분위 & 환산점수 계산 엔진", [
        ("11,688개 전체 모집단위 수록", "전국 주요 4년제 대학의 인문/자연/의약학 계열 전 학과 2026/2027 실측 컷 탑재"),
        ("국수탐 반영비율 정밀 적용", "대학별 국어/수학/탐구 반영비율 가중치를 계산하여 대학별 맞춤 누적 백분위 산출"),
        ("영어/한국사 감점표 반영", "대학별 영어 등급간 차등 감점표 및 한국사 가산점 기준을 100% 알고리즘화"),
        ("사탐/과탐 교차지원 시뮬레이션", "문이과 통합 수능에 따른 사탐 가산점 및 과탐 필수 지원 조건 완벽 필터링")
    ], EMERALD)

    add_card(s6, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🎯 2. 4단계 합격 진단 판정 & 역전 전략", [
        ("🟢 안정 (Dark Green)", "적정 누백 이하의 안정 지원군 (합격 확률 90% 이상)"),
        ("🟩 적정 (Light Green)", "예상 누백 범위 내의 소신 합격선 (합격 확률 70%~80%)"),
        ("🟡 소신 (Yellow)", "소신 누백 상단에 걸치는 상향 도전선 (합격 확률 40%~60%)"),
        ("🔴 위험 (Red)", "현재 성적으로 합격이 어려운 불합격 위험선 (목표 격차 제시)"),
        ("0.1초 즉시 검색 & 필터링", "모집군(가/나/다군), 지역(서울/경기/지방), 학과 키워드로 0.1초 내 정렬")
    ], INDIGO)

    # ==========================================
    # SLIDE 7: Student App - VIP Black Lounge & Matching
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "06. [수험생 기능 4] 상위 1% VIP 블랙 라운지 & 메디컬 튜터 매칭")

    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "👑 1. 상위 1% 폐쇄형 VIP 블랙 라운지", [
        ("상위 1% 자습 달성자 독점", "주간 연속 자습 상위 1%를 달성한 최상위권 수험생만 글을 열람하고 작성 가능"),
        ("폐쇄형 심층 Q&A", "의치한약수 및 SKY 재학생 멘토들이 직접 답변하는 고난도 킬러 문항 및 입시 전략 토론"),
        ("VIP 골드 엠블럼 부여", "자습을 열심히 한 학생에게만 열리는 명예의 전당으로 학생들의 강력한 도전 욕구 자극"),
        ("학원 내 스타 플레이어 육성", "우리 학원 소속 학생이 VIP 라운지에 입성할 때마다 학원 전체의 학습 분위기 견인")
    ], GOLD)

    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🧑‍🏫 2. 검증된 명문대 튜터 1:1 과외 매칭", [
        ("수능 만점자/의대생 멘토단", "수능 성적표 및 학생증 인증을 거친 검증된 튜터 프로필 투명 공개"),
        ("과목별 1:1 질의응답", "수학 킬러, 국어 독서, 과탐 등 취약 단원 집중 클리닉 의뢰 가능"),
        ("PALIN 캐시 지갑 연동", "학원 포인트 및 유료 캐시를 활용한 안전 결제 시스템 탑재"),
        ("원장 관리 감독 하에 운영", "학원장 관제실에서 튜터 매칭 현황을 실시간으로 모니터링하여 안전성 확보")
    ], INDIGO)

    # ==========================================
    # SLIDE 8: Parent App - Automated Nightly Report
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "07. [학부모 안심 포털] 매일 밤 22:00 실시간 알림톡 & 긴급 상황 자동 SMS")

    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📱 1. 매일 밤 22:00 안심 리포트 자동 발송", [
        ("당일 총 자습시간 보고", "오늘 학생이 독서실/학원에서 몇 시간 몇 분 집중했는지 정확한 분 단위 수치 제공"),
        ("일일 생활 미션 결과", "06:30 기상 성공 여부, 23:30 수면 모드 진입 여부를 학부모에게 자동 브리핑"),
        ("학습 태도 종합 평점", "AI 집중도 분석에 따른 '오늘의 성실도 지수(100점 만점)' 자동 채점"),
        ("학부모 만족도 98% 달성", "학부모가 학원에 묻지 않아도 매일 밤 정밀 리포트가 도착하여 학원 신뢰도 극대화")
    ], EMERALD)

    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🚨 2. 긴급 이탈/결석 SMS & 투명 수납 관리", [
        ("자습 무단 이탈 즉시 감지", "정해진 자습 시간에 타이머가 중단되거나 자리 이탈 시 0.1초 내 부모님께 안내 문자 발송"),
        ("기상 실패 실시간 통보", "아침 06:30 미션 실패 시 '학생이 아직 기상하지 않았습니다' 자동 통보"),
        ("학원비/교재비 간편 조회", "미납금 및 결제 내역을 투명하게 확인하여 원장님의 수납 독촉 전화 부담 100% 해소"),
        ("학부모 전용 1:1 건의함", "원장님 관제실로 직접 전달되는 프라이빗 소통 창구 제공")
    ], ROSE)

    # ==========================================
    # SLIDE 9: Director Cockpit Deep Dive 1 - Radar
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "08. [원장 관제실 1] 실시간 재원생 레이더 & 출결·좌석 매트릭스")

    add_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📡 1. 실시간 재원생 라이브 레이더", [
        ("전체 원생 상태 한눈에 관제", "학원 자습실, 독서실, 집에서 공부 중인 모든 학생의 타이머가 실시간 초단위로 깜빡이며 표시"),
        ("집중 / 휴식 / 이탈 3단계 감지", "공부 중(초록), 자리비움(노랑), 15분 이상 이탈(빨강) 자동 시각화"),
        ("퇴원 위험군 AI 조기 경보", "최근 3일간 자습 시간이 50% 이상 급감한 슬럼프 학생을 상단에 자동 배치"),
        ("좌석 배치도(Seat Map) 연동", "학원 내 1번~100번 좌석별 착석 현황 및 실시간 이용자 프로필 즉시 조회")
    ], CYAN)

    add_card(s9, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "📋 2. 출결 매트릭스 & 원클릭 SMS 호출", [
        ("자동 등원/하원 체크", "학생이 학원 WiFi 접속 또는 앱 체크인 시 원장 관제실에 등원 시각 자동 기록"),
        ("무단 지각생 원클릭 호출", "수업 시작 10분 전까지 미등원한 학생 전원에게 원클릭으로 '출석 독려 SMS' 일괄 발송"),
        ("출결 엑셀 자동 다운로드", "교육청 보고 및 학원 세무 처리를 위한 월간 출결 대장 1초 만에 엑셀 추출"),
        ("학부모 안심 문자 연동", "등원 시 '학원에 안전하게 도착했습니다', 하원 시 '하원 완료' 부모님 자동 통보")
    ], INDIGO)

    # ==========================================
    # SLIDE 10: Director Cockpit Deep Dive 2 - AI RAG
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "09. [원장 관제실 2] 원장님 전용 AI 뇌 이식 (RAG 지식 스튜디오)")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🧠 1. 원장님의 입시 철학 & 상담 노하우 RAG", [
        ("학원 고유 자료 무제한 업로드", "원장님의 강의 교재, 커리큘럼 소개서, 수시/정시 상담 대본, 학원 규칙 PDF/TXT 업로드"),
        ("실시간 벡터 DB 임베딩", "업로드 즉시 Gemini AI가 원장님의 지식을 학습하여 학원 전용 AI 두뇌로 동적 병합"),
        ("타 학원과의 기술적 격차", "일반 범용 ChatGPT와 달리, '우리 학원만의 커리큘럼과 원장님 방침'으로만 완벽하게 답변"),
        ("강사 퇴사 리스크 제로", "강사가 바뀌어도 학원의 핵심 입시 노하우와 상담 퀄리티는 AI 관제실에 영구 보존")
    ], GOLD)

    add_card(s10, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "💬 2. 24시간 원장 페르소나 상담 챗봇", [
        ("학생 코칭 대행", "새벽 2시에 학생이 질문해도 원장님의 어투와 교육 철학으로 격려 및 학습 가이드 제공"),
        ("학부모 1차 입시 상담 대행", "수시 전형 선택, 모의고사 성적 피드백 등 학부모 질문에 원장님 수준의 정밀한 답변 즉시 생성"),
        ("원장님 직통 질문 필터링", "AI가 해결하기 어려운 특급 상담만 원장님께 연결하여 상담 업무 리소스 90% 절감"),
        ("시스템 프롬프트 커스텀", "엄격한 스파르타식 원장, 따뜻한 멘토형 원장 등 학원 색깔에 맞춰 성격 자유 세팅")
    ], EMERALD)

    # ==========================================
    # SLIDE 11: Director Cockpit Deep Dive 3 - Red Card
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "10. [원장 관제실 3] 원장 직통 원클릭 레드카드 징계 & 보증금 차감")

    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🟥 1. 원클릭 레드카드 발부 시스템", [
        ("학원 내 기강 확립의 핵심", "자습 중 졸음, 스마트폰 몰래 사용, 잡담, 무단 외출 적발 시 관제실에서 즉시 클릭"),
        ("사유별 차등 징계", "경고(Yellow), 자습실 퇴실(Red), 성실 보증금 차감(Penalty) 3단계 제재"),
        ("학생 앱 화면 즉시 차단", "레드카드 발부 즉시 학생 화면에 붉은색 경고 오버레이가 팝업되며 자습 타이머 정지"),
        ("학원 규율 100% 자동화", "원장이 직접 언성을 높이지 않고도 앱 시스템을 통해 깔끔하고 공정한 징계 집행")
    ], ROSE)

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "💸 2. 에스크로 벌금 차감 & 학부모 즉시 통보", [
        ("성실 보증금 즉시 차감", "레드카드 사유에 따라 학생의 보증금에서 1,000원~5,000원 벌금 즉시 에스크로 삭감"),
        ("학부모 긴급 징계 SMS 자동 발송", "'[일원학원] 김철수 학생이 자습 중 스마트폰 사용으로 레드카드가 발부되었습니다' 문자 자동 발송"),
        ("학부모와의 마찰 원천 차단", "시스템 로그와 타임스탬프가 부모님께 투명하게 전송되어 학부모의 이의 제기 제로"),
        ("원생 자정 작용", "벌금과 부모님 통보를 두려워하여 학생 스스로 면학 분위기를 유지하는 놀라운 효과")
    ], GOLD)

    # ==========================================
    # SLIDE 12: Director Cockpit Deep Dive 4 - Weekly AI Report
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "11. [원장 관제실 4] 매주 화요일 22:00 AI 주간 생존 리포트 자동 일괄 발간")

    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📑 1. Gemini AI 1:1 맞춤 주간 종합 분석", [
        ("한 주간의 빅데이터 정밀 진단", "총 자습시간, 일일 목표 달성률, 생활미션 성공률, 주간 모의고사 성적 변동률 통합 분석"),
        ("300자 카카오톡 전용 대본 생성", "딱딱한 그래프가 아닌, 원장님이 직접 작성한 듯한 자연스럽고 따뜻한 300자 줄글 피드백 생성"),
        ("취약점 & 개선 행동 강령 제시", "'이번 주는 수학 자습량이 20% 부족했습니다. 다음 주에는 오답 노트 작성을 늘리겠습니다'"),
        ("원장 검토 및 원클릭 발송", "화요일 저녁 관제실에서 AI가 작성한 리포트를 1초 검토 후 전교생 학부모에게 일괄 전송")
    ], INDIGO)

    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "💰 2. 지능형 수납 촉구 & 퇴원 방어 효과", [
        ("미납 학부모 맞춤 문구 자동 삽입", "수업료 미납 학생의 경우 리포트 하단에 '수강료 결제 안내' 링크가 정중하게 자동 포함"),
        ("학부모 감동 & 재등록률 99%", "매주 화요일 밤마다 도착하는 고품격 AI 리포트로 인해 학부모의 학원 만족도 극대화"),
        ("상담 시간 80% 단축", "이미 모든 학습 데이터가 리포트에 담겨 있어, 전화 상담 시간이 1인당 2분 미만으로 단축"),
        ("완벽한 마케팅 무기", "학부모들이 주변 맘카페와 단톡방에 리포트를 공유하며 신규 원생 문의 폭증")
    ], EMERALD)

    # ==========================================
    # SLIDE 13: Director Cockpit Deep Dive 5 - VOD & Tracking
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "12. [원장 관제실 5] VOD 인강 스토리지 & 초단위 완강률 추적")

    add_card(s13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🎥 1. 학원 전용 VOD 인강 라이브러리", [
        ("원장님 현장 강의 녹화본 탑재", "수업 결석생 보충 및 심화 복습을 위한 고화질 VOD 강의 스토리지 제공 (50GB~무제한)"),
        ("등급별/반별 수강 권한 제어", "S클래스, 의대반, 정규반 등 수강생 권한에 따라 볼 수 있는 VOD 강의 차등 설정"),
        ("모바일 & 태블릿 완벽 스트리밍", "별도의 플레이어 설치 없이 웹 브라우저에서 0.5초 만에 즉시 재생"),
        ("불법 복제 & 캡처 방지", "학생 이름 및 휴대폰 번호가 영상 위에 워터마크로 움직이며 화면 녹화 원천 차단")
    ], CYAN)

    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "⏱️ 2. 초단위 완강률 & 스킵 감지 분석", [
        ("진짜로 강의를 들었는지 검증", "단순히 틀어놓기만 한 것인지, 끝까지 집중해서 시청했는지 초단위 타임라인 추적"),
        ("배속 재생 & 건너뛰기 감지", "2배속 이상 재생하거나 중요한 개념 설명 구간을 스킵한 경우 '날림 수강' 플래그 경고"),
        ("완강 미달 시 보증금 차감 연동", "지정된 날짜까지 VOD를 100% 완강하지 않을 경우 자동으로 과제 미제출 처리"),
        ("부모님 안심 알림톡 연동", "주말 VOD 복습 완료 시 '이번 주 보충 강의 100% 완강 완료' 부모님 알림톡 자동 발송")
    ], INDIGO)

    # ==========================================
    # SLIDE 14: Director Cockpit Deep Dive 6 - Mock Exam Diagnosis
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "13. [원장 관제실 6] 주차별 모의고사 성적 엑셀 일괄 진단 시스템")

    add_card(s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "📈 1. 주차별 모의고사 성적 엑셀 일괄 등록", [
        ("엑셀 파일 드래그 앤 드롭", "학원에서 자체 실시한 주간/월간 모의고사 성적표 엑셀을 끌어다 놓으면 1초 만에 전산 반영"),
        ("국수영탐 원점수/표준점수 자동 계산", "점수 입력 즉시 전국 컷 대비 예상 등급 및 백분위가 자동 변환"),
        ("개인별 성적 누적 궤적 차트", "3월부터 11월까지 국어/수학 점수 변화 그래프가 학생/학부모 앱에 실시간 업데이트"),
        ("취약 문항 유형 자동 분류", "수학 미적분 킬러, 국어 비문학 등 학생별 오답 집중 단원을 AI가 자동 추출")
    ], EMERALD)

    add_card(s14, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🎯 2. 학원 내 등급 컷 & 합격 가능성 재진단", [
        ("학원 내 석차 백분율 산출", "우리 학원 원생 100명 중 상위 10%, 평균 점수, 표준 편차 자동 산출"),
        ("11,688개 대학 정시 컷 실시간 재연산", "모의고사 성적이 등록되는 즉시 학생의 목표 대학 합격 가능성(안정/소신) 재평가"),
        ("학부모 성적표 PDF 원클릭 발급", "학원 로고와 원장님 직인이 찍힌 프리미엄 컬러 성적 분석표를 PDF로 즉시 출력/발송"),
        ("입시 상담 무기 확보", "원장실 방문 상담 시 화면에 성적 궤적과 목표 대학 갭 분석을 띄워 압도적 전문성 과시")
    ], GOLD)

    # ==========================================
    # SLIDE 15: Director Cockpit Deep Dive 7 - White Labeling
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_header(s15, "14. [원장 관제실 7] 100% 화이트라벨링 (학원 단독 브랜딩 구축)")

    add_card(s15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "🏢 1. 학원 브랜드 아이덴티티 완벽 적용", [
        ("학원 상호명 & 로고 전면 배치", "앱 상단과 로그인 화면에 'PALIN OS' 대신 '일원학원 입시 관제 OS' 등 원장님 브랜드 단독 노출"),
        ("학원 고유 테마 컬러 커스텀", "학원 시그니처 색상(네이비, 버건디, 골드 등)에 맞춰 전체 UI 테마 색상 100% 일치화"),
        ("단독 도메인 연결 지원", "academy.ilwon.com 등 학원 자체 서브 도메인으로 수험생/학부모 접속 가능"),
        ("지역 1위 학원의 위상 확립", "자체 AI 시스템을 개발한 초대형 명문 학원으로 학부모들에게 독보적 신뢰감 부여")
    ], GOLD)

    add_card(s15, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4), "🔑 2. 전용 가맹 코드 & 프라이빗 생태계", [
        ("학원 전용 고유 코드 발급", "예: ILWON-2027, DAECHI-SKY 등 학원만의 독점 가맹 초대 코드 부여"),
        ("재원생 독점 혜택 배정", "해당 코드를 입력한 학생은 월 99,000원 상당의 마스터 AI 혜택을 '원장님 전액 지원'으로 무료 이용"),
        ("외부 유출 차단 폐쇄망", "우리 학원 학생들끼리만 참여하는 비공개 자습 랭킹전 및 공지사항 게시판 운영"),
        ("원장 승인제 멤버십", "원장 관제실에서 승인 버튼을 누른 재원생만 관제망에 등록되어 수강생 이탈 원천 봉쇄")
    ], INDIGO)

    # ==========================================
    # SLIDE 16: SaaS Pricing & Tier Matrix
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16)
    add_header(s16, "15. B2B 엔터프라이즈 요금제 & 티어별 라이선스 스펙 비교")

    add_card(s16, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥉 Tier 1: 베이직 (스타트업)", [
        ("월 구독료", "월 299,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 50명"),
        ("실시간 관제실", "실시간 레이더 & 출결 매트릭스 제공"),
        ("안심 알림톡", "월간 SMS/알림톡 3,000건 기본 충전"),
        ("VOD 스토리지", "50GB 고화질 인강 저장 공간"),
        ("AI 챗봇", "기본 입시 코칭 AI (Gemini 3.6 Flash)"),
        ("추천 학원", "신규 오픈 학원 및 중소형 교습소")
    ], GRAY)

    add_card(s16, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥈 Tier 2: 프로 (성장형 학원)", [
        ("월 구독료", "월 599,000원 (VAT 별도)"),
        ("수용 정원", "재원생 최대 150명"),
        ("AI 뇌 이식(RAG)", "원장님 커리큘럼/상담 대본 전용 RAG 탑재"),
        ("레드카드 에스크로", "금융 인질 보증금 벌금 차감 시스템 가동"),
        ("AI 주간 리포트", "매주 화요일 22:00 전교생 자동 발간"),
        ("VOD 스토리지", "200GB 고화질 저장 공간 & 스킵 감지"),
        ("안심 알림톡", "월간 SMS/알림톡 10,000건 기본 충전"),
        ("추천 학원", "수강생 100명 내외 지역 거점 중대형 학원")
    ], INDIGO)

    add_card(s16, Inches(8.8), Inches(1.5), Inches(3.6), Inches(5.4), "🥇 Tier 3: 엔터프라이즈 (대형)", [
        ("월 구독료", "월 999,000원 (VAT 별도)"),
        ("수용 정원", "재원생 무제한 (Unlimited)"),
        ("100% 화이트라벨링", "학원 로고, 색상, 자체 도메인 완벽 적용"),
        ("전용 AI 슈퍼 브레인", "원장님 전용 멀티 에이전트 커스텀"),
        ("VOD 스토리지", "무제한 초고화질 스토리지 + 화면 캡처 방지"),
        ("모의고사 진단", "주차별 엑셀 성적표 자동 채점 & 궤적 진단"),
        ("전담 엔지니어", "24시간 1:1 기술 지원 & 전용 온보딩"),
        ("추천 학원", "대형 단과학원, 재수종합반, 기숙학원")
    ], GOLD)

    # ==========================================
    # SLIDE 17: Implementation Roadmap
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17)
    add_header(s17, "16. 도입 및 온보딩 로드맵: 단 3일 만에 완성되는 학원 전산 혁신")

    add_card(s17, Inches(0.8), Inches(1.5), Inches(2.2), Inches(5.4), "Day 1: 가맹 신청", [
        ("도입 문의 접수", "이메일 또는 직통 전화로 학원 규모 및 요구사항 접수"),
        ("티어 선정 및 계약", "학원 정원에 맞춘 최적의 SaaS 라이선스 확정"),
        ("관리자 계정 생성", "원장님 전용 보안 PIN 및 마스터 관제실 즉시 개설")
    ], CYAN)

    add_card(s17, Inches(3.2), Inches(1.5), Inches(2.2), Inches(5.4), "Day 2: 브랜딩 세팅", [
        ("화이트라벨링 반영", "학원 로고, 대표 색상, 가맹 코드(예: ILWON-2027) 세팅"),
        ("AI 뇌 이식(RAG)", "원장님의 입시 자료 및 상담 대본 벡터 DB 업로드"),
        ("테스트 시뮬레이션", "가상 학생 계정으로 랭킹전 및 결제/알림톡 사전 점검")
    ], INDIGO)

    add_card(s17, Inches(5.6), Inches(1.5), Inches(2.2), Inches(5.4), "Day 3: 재원생 배포", [
        ("원생 일괄 엑셀 등록", "기존 원생 명단을 관제실에 1초 만에 일괄 업로드"),
        ("초대 알림톡 일괄 발송", "학생과 학부모에게 전용 앱 설치 링크 및 코드 안내"),
        ("앱 가동 & 로그인", "학생들이 즉시 랭킹전에 참여하며 자발적 자습 시작")
    ], GOLD)

    add_card(s17, Inches(8.0), Inches(1.5), Inches(2.2), Inches(5.4), "Week 1: 기강 확립", [
        ("기상/취침 미션 시작", "06:30 기상 및 자습실 출결 에스크로 시스템 본격 가동"),
        ("레드카드 규칙 정착", "지각 및 휴대폰 사용 시 원클릭 징계로 면학 분위기 완성"),
        ("학부모 안심 안착", "매일 밤 22:00 도착하는 알림톡으로 학부모 감동 시작")
    ], ROSE)

    add_card(s17, Inches(10.4), Inches(1.5), Inches(2.2), Inches(5.4), "Ongoing: 자동 성장", [
        ("화요일 AI 주간 리포트", "매주 화요일 22:00 전교생 학부모에게 AI 종합 리포트 자동 발송"),
        ("퇴원율 0% 달성", "학생의 슬럼프 조기 차단 및 학부모 록인(Lock-in) 완성"),
        ("신규 입학 문의 폭증", "학부모 입소문과 인스타 학생증 공유로 자발적 바이럴 확산")
    ], EMERALD)

    # ==========================================
    # SLIDE 18: Contact & Partnership Closing
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s18)

    tb18 = s18.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11), Inches(5.2))
    tf18 = tb18.text_frame
    p18_1 = tf18.paragraphs[0]
    p18_1.text = "지금, 귀 학원만의 독점 AI 관제 인프라를 구축하십시오."
    p18_1.font.size = Pt(26)
    p18_1.font.bold = True
    p18_1.font.color.rgb = GOLD
    p18_1.font.name = "Malgun Gothic"

    p18_2 = tf18.add_paragraph()
    p18_2.text = "학생의 퇴원율을 0%로 막고, 학부모의 신뢰를 100%로 끌어올리는 차세대 교육 OS"
    p18_2.font.size = Pt(15)
    p18_2.font.color.rgb = WHITE
    p18_2.font.name = "Malgun Gothic"
    p18_2.space_before = Pt(14)

    p18_3 = tf18.add_paragraph()
    p18_3.text = "PALIN OS는 단순한 학습 앱이 아닙니다. 원장님의 교육 철학과 입시 노하우를 완벽히 복제하여\n24시간 지치지 않고 일하는 '학원 전용 AI 수석 부원장'을 이식해 드리는 독점 솔루션입니다."
    p18_3.font.size = Pt(12)
    p18_3.font.color.rgb = GRAY
    p18_3.font.name = "Malgun Gothic"
    p18_3.space_before = Pt(16)

    # Contact Box
    contact_card = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(10.9), Inches(2.6))
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
    pc3.text = "• 문의 양식: [학원명 / 지역 / 원장님 성함 및 연락처 / 재원생 규모]를 적어 메일을 보내주시면 24시간 내 1:1 맞춤 제안서를 전달해 드립니다."
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

    # Save pptx to both pass-mate and PALIN_UPLOAD
    output_filename = "PALIN_OS_B2B_Director_Proposal.pptx"
    
    pass_mate_path = os.path.join(r"C:\Users\1286o\.gemini\antigravity\scratch\pass-mate", output_filename)
    prs.save(pass_mate_path)
    print(f"Saved PPTX to {pass_mate_path}")

    upload_dir = r"C:\Users\1286o\.gemini\antigravity\scratch\PALIN_UPLOAD"
    if os.path.exists(upload_dir):
        upload_path = os.path.join(upload_dir, output_filename)
        prs.save(upload_path)
        print(f"Saved PPTX to {upload_path}")

    desktop_dir = r"C:\Users\1286o\Desktop"
    if os.path.exists(desktop_dir):
        desktop_path = os.path.join(desktop_dir, output_filename)
        try:
            prs.save(desktop_path)
            print(f"Saved PPTX to {desktop_path}")
        except Exception as e:
            print(f"Could not save to desktop: {e}")

if __name__ == "__main__":
    build_presentation()
