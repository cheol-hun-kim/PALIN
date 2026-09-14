# -*- coding: utf-8 -*-
"""
PALIN OS Phase 11.3: 100-Title Master Gamification Catalog
Complete 100-title matrix across 10 strategic achievement domains.
Includes tier weights and priority indices for automatic highest-tier equipping.
"""

MASTER_TITLES_CATALOG = [
    # =========================================================================
    # 1. 연속 출석 & 습관 루틴 (Streak & Habit) - 10종
    # =========================================================================
    {
        "condition_code": "STARTER_TIER",
        "category": "출석루틴",
        "title_name": "[트랙 인: 1열 탑승자]",
        "description": "PALIN OS 입시 레이스 공식 진입",
        "condition_desc": "회원가입 완료",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 1,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "STREAK_3D",
        "category": "출석루틴",
        "title_name": "[작심삼일 소멸자]",
        "description": "의지력 한계를 넘어선 첫 번째 턴",
        "condition_desc": "연속 3일 달성",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 3,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "STREAK_5D",
        "category": "출석루틴",
        "title_name": "[루틴의 지배자]",
        "description": "평일 5일 전일 출석 & 완벽한 관성 형성",
        "condition_desc": "연속 5일 달성",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 5,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 5
    },
    {
        "condition_code": "STREAK_7D",
        "category": "출석루틴",
        "title_name": "[새벽 6시의 공기]",
        "description": "7일 연속 빈틈없는 기상 & 자습 완료",
        "condition_desc": "연속 7일 달성",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 7,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "STREAK_14D",
        "category": "출석루틴",
        "title_name": "[대치동 페이스메이커]",
        "description": "2주 연속 상위 1% 완벽 출석 유지",
        "condition_desc": "연속 14일 달성",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 14,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 14
    },
    {
        "condition_code": "STREAK_21D",
        "category": "출석루틴",
        "title_name": "[신경망 재설계자]",
        "description": "21일 뇌 가소성 습관 회로 완성",
        "condition_desc": "연속 21일 달성",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 21,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 21
    },
    {
        "condition_code": "STREAK_30D",
        "category": "출석루틴",
        "title_name": "[30일의 무결점 궤도]",
        "description": "한 달간 단 하루의 이탈도 없는 절대 궤적",
        "condition_desc": "연속 30일 달성",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 30,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 30
    },
    {
        "condition_code": "STREAK_50D",
        "category": "출석루틴",
        "title_name": "[불수능 방파제]",
        "description": "50일 연속 슬럼프 없는 멘탈 방어선 구축",
        "condition_desc": "연속 50일 달성",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 50,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 50
    },
    {
        "condition_code": "STREAK_100D",
        "category": "출석루틴",
        "title_name": "[100일의 절대 독점]",
        "description": "100일 연속 흔들림 없는 만점 집념",
        "condition_desc": "연속 100일 달성",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 100,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 100
    },
    {
        "condition_code": "STREAK_200D",
        "category": "출석루틴",
        "title_name": "[살아있는 입시 전설]",
        "description": "200일 연속 학습 머신의 압도적 증명",
        "condition_desc": "연속 200일 달성",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 200,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 200
    },

    # =========================================================================
    # 2. 누적 순공 & 한계 돌파 (Cumulative Study Hours) - 10종
    # =========================================================================
    {
        "condition_code": "STUDY_10H",
        "category": "순공한계",
        "title_name": "[도파민 디톡서]",
        "description": "누적 순공 10시간, 스마트폰을 이겨낸 자",
        "condition_desc": "순공 10시간 누적",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 10,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 10.0
    },
    {
        "condition_code": "STUDY_30H",
        "category": "순공한계",
        "title_name": "[의자 일체화 1단계]",
        "description": "누적 순공 30시간의 탄탄한 집중 예열",
        "condition_desc": "순공 30시간 누적",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 30,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 30.0
    },
    {
        "condition_code": "STUDY_50H",
        "category": "순공한계",
        "title_name": "[하이퍼 포커스]",
        "description": "누적 순공 50시간 초몰입 궤도 안착",
        "condition_desc": "순공 50시간 누적",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 50,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 or strk >= 5
    },
    {
        "condition_code": "STUDY_100H",
        "category": "순공한계",
        "title_name": "[100시간의 정적]",
        "description": "순공 누적 100시간 고독한 독주",
        "condition_desc": "순공 100시간 누적",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 100,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0
    },
    {
        "condition_code": "STUDY_200H",
        "category": "순공한계",
        "title_name": "[단권화의 달인]",
        "description": "누적 순공 200시간 흔들리지 않는 기본기",
        "condition_desc": "순공 200시간 누적",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 200,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 200.0
    },
    {
        "condition_code": "STUDY_300H",
        "category": "순공한계",
        "title_name": "[300시간의 마지노선]",
        "description": "누적 순공 300시간 절대 영역 구축",
        "condition_desc": "순공 300시간 누적",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 300,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 300.0
    },
    {
        "condition_code": "STUDY_500H",
        "category": "순공한계",
        "title_name": "[킬러 문항 분쇄기]",
        "description": "누적 순공 500시간 준킬러·킬러 완전 정복",
        "condition_desc": "순공 500시간 누적",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 500,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 500.0
    },
    {
        "condition_code": "STUDY_700H",
        "category": "순공한계",
        "title_name": "[수석의 무게]",
        "description": "누적 순공 700시간 전국 수석급 공부량",
        "condition_desc": "순공 700시간 누적",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 700,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 700.0
    },
    {
        "condition_code": "STUDY_1000H",
        "category": "순공한계",
        "title_name": "[만점 수렴의 법칙]",
        "description": "순공 1,000시간 수능 만점의 임계점 도달",
        "condition_desc": "순공 1,000시간 돌파",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 1000,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 1000.0
    },
    {
        "condition_code": "STUDY_1500H",
        "category": "순공한계",
        "title_name": "[관악산 정상 원정대장]",
        "description": "순공 1,500시간 전설의 신화적 경지",
        "condition_desc": "순공 1,500시간 돌파",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 1500,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 1500.0
    },

    # =========================================================================
    # 3. 시간대 & 타임 블록 (Time Slots & Hyper-Focus) - 10종
    # =========================================================================
    {
        "condition_code": "DAWN_WARRIOR",
        "category": "시간대",
        "title_name": "[새벽 5시의 침묵]",
        "description": "모두가 잠든 새벽 타임 집중 자습",
        "condition_desc": "새벽(04~07시) 집중 학습",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 50,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "MORNING_GLORY",
        "category": "시간대",
        "title_name": "[1교시 뇌 최적화]",
        "description": "오전 8:40 수능 국어 뇌파 동기화",
        "condition_desc": "오전(08~12시) 3시간 이상",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 80,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "AFTERNOON_RUSH",
        "category": "시간대",
        "title_name": "[식곤증 면역자]",
        "description": "오후 1~4시 탐구·영어 황금시간 장악",
        "condition_desc": "오후 집중 학습",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 90,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4
    },
    {
        "condition_code": "NIGHT_OWL",
        "category": "시간대",
        "title_name": "[심야의 지배자]",
        "description": "밤 10시~새벽 1시 야간 자습 독주",
        "condition_desc": "야간 집중 학습",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 6
    },
    {
        "condition_code": "MIDNIGHT_EMPEROR",
        "category": "시간대",
        "title_name": "[새벽 4시의 절대 고요]",
        "description": "새벽 심야 극한의 순공 돌파",
        "condition_desc": "심야 집중 몰입",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 140,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 8
    },
    {
        "condition_code": "GOLDEN_TIME_MASTER",
        "category": "시간대",
        "title_name": "[수능 타임테이블 마스터]",
        "description": "실제 수능 시간표 완벽 일치 학습",
        "condition_desc": "주간 15시간 이상",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 200,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 10.0
    },
    {
        "condition_code": "WEEKEND_BERSERK",
        "category": "시간대",
        "title_name": "[주말 30시간 폭주 기관차]",
        "description": "주말 집중 30시간 초격차 자습",
        "condition_desc": "주간 20시간 이상",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 250,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 15.0
    },
    {
        "condition_code": "HOLIDAY_DESTROYER",
        "category": "시간대",
        "title_name": "[공휴일 무자비한 자습]",
        "description": "빨간 날 전일 자습관 점령",
        "condition_desc": "주말/공휴일 자습 달성",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 160,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 5
    },
    {
        "condition_code": "LUNCH_SKILL",
        "category": "시간대",
        "title_name": "[자투리 15분의 마법사]",
        "description": "쉬는 시간·자투리 영단어 100% 암기",
        "condition_desc": "자투리 시간 학습",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 60,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "ALL_DAY_FOCUS",
        "category": "시간대",
        "title_name": "[하루 14시간의 벽 파괴자]",
        "description": "일일 순공 14시간 돌파 달성",
        "condition_desc": "올 타임 집중 모드 달성",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 350,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 25.0 or th >= 50.0
    },

    # =========================================================================
    # 4. 목표 대학 & 계열 연합군 (Target University & Major) - 10종
    # =========================================================================
    {
        "condition_code": "SKY_LEGION",
        "category": "목표대학",
        "title_name": "[SKY 결사대]",
        "description": "서울대·연세대·고려대·의예과 목표",
        "condition_desc": "목표대학 설정",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 220,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["서울", "연세", "고려", "의예", "의대", "SNU", "KAIST", "포스텍"])
    },
    {
        "condition_code": "SNU_ASPIRANT",
        "category": "목표대학",
        "title_name": "[샤(SNU)의 문을 두드리는 자]",
        "description": "서울대학교 지망 및 주간 순공 15시간 이상",
        "condition_desc": "서울대 목표 & 주간 15시간",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 240,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("서울" in tu or "SNU" in tu) and wh >= 10.0
    },
    {
        "condition_code": "YONSEI_BLUE",
        "category": "목표대학",
        "title_name": "[아카라카 블루 크루]",
        "description": "연세대학교 지망 및 독보적 페이스 유지",
        "condition_desc": "연세대 목표 & 주간 자습",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 230,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("연세" in tu or "연대" in tu)
    },
    {
        "condition_code": "KOREA_CRIMSON",
        "category": "목표대학",
        "title_name": "[안암의 붉은 호랑이]",
        "description": "고려대학교 지망 및 꺾이지 않는 투지",
        "condition_desc": "고려대 목표 & 주간 자습",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 230,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("고려" in tu or "고대" in tu)
    },
    {
        "condition_code": "MEDICAL_WHITE",
        "category": "목표대학",
        "title_name": "[의치한약수 정복단]",
        "description": "전국 의치한약수 메디컬 합격권 정조준",
        "condition_desc": "메디컬 목표 & 주간 자습",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 550,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(m in tu for m in ["의예", "의대", "치의", "한의", "약학", "수의", "의예과"])
    },
    {
        "condition_code": "KAIST_TECH",
        "category": "목표대학",
        "title_name": "[미래 테크노크라트]",
        "description": "KAIST·포스텍·과기원 이공계 최정예",
        "condition_desc": "과기원/공학 특화 목표",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 230,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(k in tu for k in ["KAIST", "카이스트", "포스텍", "POSTECH", "과기원", "공대", "컴퓨터", "인공지능"])
    },
    {
        "condition_code": "SEODANG_LAW",
        "category": "목표대학",
        "title_name": "[서성한 정예 타격대]",
        "description": "서강·성균관·한양대 상위 1% 합격 궤도",
        "condition_desc": "서성한 목표 설정",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 210,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["서강", "성균관", "한양"])
    },
    {
        "condition_code": "CENTRAL_UNION",
        "category": "목표대학",
        "title_name": "[중경외시 진격군]",
        "description": "중앙·경희·한국외대·시립대 승부수",
        "condition_desc": "중경외시 목표 설정",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 180,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["중앙", "경희", "외대", "시립", "이화"])
    },
    {
        "condition_code": "TEACHER_CREED",
        "category": "목표대학",
        "title_name": "[교대·사범대 교단 선서자]",
        "description": "전국 교대 및 사범대 수석 목표",
        "condition_desc": "교대/사범대 목표 설정",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 170,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["교대", "사범", "교육"])
    },
    {
        "condition_code": "POLICE_HERO",
        "category": "목표대학",
        "title_name": "[사관·경찰대 특수 전선]",
        "description": "육해공 사관학교 및 경찰대 진출",
        "condition_desc": "사관/경찰대 목표 설정",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 170,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["사관", "경찰", "육사", "해사", "공사", "국간사"])
    },

    # =========================================================================
    # 5. 실전 OMR & 모의고사 (OMR & Exam Master) - 10종
    # =========================================================================
    {
        "condition_code": "OMR_FIRST_SHOT",
        "category": "OMR실전",
        "title_name": "[컴싸의 첫 터치]",
        "description": "첫 실전 OMR 카드 마킹 완료",
        "condition_desc": "OMR 1회 제출",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 15,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 1 or strk >= 1
    },
    {
        "condition_code": "OMR_3_STRIKES",
        "category": "OMR실전",
        "title_name": "[시간 분배 설계자]",
        "description": "실전 모의고사 시간 배분 및 타임어택 훈련",
        "condition_desc": "OMR 3회 이상 제출",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 40,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 3 or strk >= 3
    },
    {
        "condition_code": "OMR_5_MASTER",
        "category": "OMR실전",
        "title_name": "[마킹 실수 제로]",
        "description": "OMR 5회 이상 완벽 제출 및 무결점 마킹",
        "condition_desc": "OMR 5회 이상 제출",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 80,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 5 or strk >= 5
    },
    {
        "condition_code": "OMR_10_LEGEND",
        "category": "OMR실전",
        "title_name": "[실전 모의고사 10회독]",
        "description": "실전 OMR 10회 완주 & 현장감 체화",
        "condition_desc": "OMR 10회 이상 제출",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 150,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 10 or strk >= 10
    },
    {
        "condition_code": "KILLER_DESTROYER",
        "category": "OMR실전",
        "title_name": "[22번·30번 정밀 타격]",
        "description": "최고난도 수학 킬러 문항 분쇄",
        "condition_desc": "킬러 문항 극복",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 190,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 or strk >= 8
    },
    {
        "condition_code": "TIME_SAVER",
        "category": "OMR실전",
        "title_name": "[마킹 종료 10분 전]",
        "description": "시험 종료 10분 전 마킹 및 검토 완료",
        "condition_desc": "실전 검토 루틴 체화",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 90,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4
    },
    {
        "condition_code": "PERFECT_OMR",
        "category": "OMR실전",
        "title_name": "[수능 출제진의 악몽]",
        "description": "출제진의 함정을 완벽히 간파하는 실전 감각",
        "condition_desc": "OMR 고득점 달성",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 320,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0 or strk >= 12
    },
    {
        "condition_code": "MOCK_EXAM_SLAYER",
        "category": "OMR실전",
        "title_name": "[평가원 코드 해독가]",
        "description": "6월·9월 평가원 기출 논리 완벽 체화",
        "condition_desc": "평가원 기출 마스터",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 100,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "FEEDBACK_GENIUS",
        "category": "OMR실전",
        "title_name": "[오답 노트 완전 분해]",
        "description": "틀린 문항 원인 100% 피드백 분석",
        "condition_desc": "오답 분석 체화",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 50,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "RANK_ONE_OMR",
        "category": "OMR실전",
        "title_name": "[전국구 슬롯 머신]",
        "description": "전국 모의고사 최상위 백분위 기록",
        "condition_desc": "전국 모의고사 1등급",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 500,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 120.0 and strk >= 15
    },

    # =========================================================================
    # 6. 로컬 학군 & 거점 길드 (Local Guild & Battleground) - 10종
    # =========================================================================
    {
        "condition_code": "DAETCHIDONG_HEIR",
        "category": "로컬길드",
        "title_name": "[대치동 1열의 공기]",
        "description": "대치동 학원가 실전 현강의 숨결",
        "condition_desc": "대치/강남 거점",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 210,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "MOKDONG_ELITE",
        "category": "로컬길드",
        "title_name": "[목동 하이페리온의 침묵]",
        "description": "목동 학군 최상위 자습러의 묵직함",
        "condition_desc": "목동 거점 자습",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 210,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "BUNDANG_TOP",
        "category": "로컬길드",
        "title_name": "[분당 낙생·수내 맹주]",
        "description": "분당 학군 1티어 순공 독주",
        "condition_desc": "분당/성남 거점 자습",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 210,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "SUNGJEONG_SHIELD",
        "category": "로컬길드",
        "title_name": "[중계동 은행사거리 수호자]",
        "description": "강북 교육특구 은행사거리 맹장",
        "condition_desc": "중계/노원 거점 자습",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "SUSEONG_TIGER",
        "category": "로컬길드",
        "title_name": "[대구 수성구 범어 늑대]",
        "description": "영남 최강 수성 학군의 매서운 독기",
        "condition_desc": "대구 수성 거점 자습",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 210,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4
    },
    {
        "condition_code": "CENTUM_WAVE",
        "category": "로컬길드",
        "title_name": "[부산 센텀 마린 크루]",
        "description": "부산·경남 거점 정예 순공러",
        "condition_desc": "부산 센텀 거점 자습",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "YUSEONG_BRAIN",
        "category": "로컬길드",
        "title_name": "[대전 유성 카이스트 벨트]",
        "description": "중부 과학 교육특구 두뇌 집합소",
        "condition_desc": "대전 유성 거점 자습",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "GWANGJU_BONGSEON",
        "category": "로컬길드",
        "title_name": "[광주 봉선동 독주자]",
        "description": "호남 1번가 봉선 학군 대표",
        "condition_desc": "광주 봉선 거점 자습",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "GUILD_FOUNDER",
        "category": "로컬길드",
        "title_name": "[자습관 길드 마스터]",
        "description": "스터디 그룹 및 길드 연합 리더",
        "condition_desc": "길드/소속 학원 활동",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 150,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: bool(getattr(s, 'academy_id', None)) or strk >= 4
    },
    {
        "condition_code": "CAMPUS_CONQUEROR",
        "category": "로컬길드",
        "title_name": "[목표대학 점령전 패자]",
        "description": "목표대학 캠퍼스 점령전 기여도 1위",
        "condition_desc": "점령전 최상위 기여",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 330,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 and strk >= 8
    },

    # =========================================================================
    # 7. 성실 지수 & 소셜 시너지 (Diligence & Social) - 10종
    # =========================================================================
    {
        "condition_code": "DILIGENCE_100",
        "category": "성실소셜",
        "title_name": "[성실 지표 그린 라이트]",
        "description": "성실도 점수 100점 돌파",
        "condition_desc": "성실도 100점 달성",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 20,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 100 or strk >= 2
    },
    {
        "condition_code": "DILIGENCE_500",
        "category": "성실소셜",
        "title_name": "[강철의 페이스메이커]",
        "description": "성실도 점수 500점 달성",
        "condition_desc": "성실도 500점 달성",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 70,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 500 or strk >= 5
    },
    {
        "condition_code": "DILIGENCE_1000",
        "category": "성실소셜",
        "title_name": "[원장님의 무한 신뢰]",
        "description": "성실도 1000점 최우수 성실 학생",
        "condition_desc": "성실도 1,000점 달성",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 130,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 1000 or strk >= 10
    },
    {
        "condition_code": "PEER_POKER",
        "category": "성실소셜",
        "title_name": "[자극 유발자]",
        "description": "나태해진 친구에게 콕 찌르기 1회 전송",
        "condition_desc": "찌르기 1회 전송",
        "tier": "입문",
        "tier_weight": 100,
        "difficulty_weight": 10,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "POKE_KING",
        "category": "성실소셜",
        "title_name": "[전국구 찌르기 스나이퍼]",
        "description": "지속적인 동료 자극 5회 이상 완료",
        "condition_desc": "찌르기 5회 이상 전송",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 60,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4
    },
    {
        "condition_code": "STUDY_INSPIRER",
        "category": "성실소셜",
        "title_name": "[러닝메이트의 빛]",
        "description": "동료들에게 강력한 학습 동기부여 전파",
        "condition_desc": "소셜 시너지 기여",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 110,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "QA_HELPER",
        "category": "성실소셜",
        "title_name": "[질문방 해결사]",
        "description": "커뮤니티 Q&A 집단지성 답변 기여",
        "condition_desc": "Q&A 답변 기여",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 55,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "CHALLENGE_WINNER",
        "category": "성실소셜",
        "title_name": "[주간 챌린지 1위]",
        "description": "주간 성실도 챌린지 최상위 챔피언",
        "condition_desc": "주간 챌린지 우승",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 140,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 12.0 or strk >= 8
    },
    {
        "condition_code": "POINT_RICH",
        "category": "성실소셜",
        "title_name": "[장학 포인트 부호]",
        "description": "누적 10,000 장학 포인트 보유",
        "condition_desc": "10,000P 이상 누적",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 220,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 3000 or th >= 40.0
    },
    {
        "condition_code": "DONATION_ANGEL",
        "category": "성실소셜",
        "title_name": "[장학 티켓 기부 천사]",
        "description": "골든티켓/장학금 친구 초대 3회 달성",
        "condition_desc": "친구 초대 3회 완료",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 310,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: bool(getattr(s, 'golden_tickets_count', 0) >= 1) or strk >= 12
    },

    # =========================================================================
    # 8. 멘탈 케어 & 회복 탄력성 (Mental Resilience & Willpower) - 10종
    # =========================================================================
    {
        "condition_code": "SLUMP_IMMUNE",
        "category": "멘탈의지",
        "title_name": "[슬럼프 브레이커]",
        "description": "성적 정체기 마인드를 깨부순 자",
        "condition_desc": "슬럼프 극복",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 50,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "ANXIETY_DEFENDER",
        "category": "멘탈의지",
        "title_name": "[백색소음 마스터]",
        "description": "ASMR 몰입 사운드로 주변 잡음 완벽 차단",
        "condition_desc": "ASMR 집중 청취",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 40,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "MINDFUL_STUDENT",
        "category": "멘탈의지",
        "title_name": "[강철 멘탈리티]",
        "description": "D-100 압박감을 차분한 평정심으로 전환",
        "condition_desc": "멘탈 평정심 유지",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 110,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 6
    },
    {
        "condition_code": "PRESSURE_TAMER",
        "category": "멘탈의지",
        "title_name": "[실전 마인드컨트롤]",
        "description": "수능 시험장 중압감 완벽 제어",
        "condition_desc": "긴장 제어 훈련 완료",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 130,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 8
    },
    {
        "condition_code": "UNBREAKABLE_WILL",
        "category": "멘탈의지",
        "title_name": "[꺾이지 않는 중꺾마]",
        "description": "모의고사 등락에도 흔들림 없는 완주 태도",
        "condition_desc": "연속 자습 루틴 유지",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 200,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 10
    },
    {
        "condition_code": "REST_MASTER",
        "category": "멘탈의지",
        "title_name": "[완벽한 15분 파워냅]",
        "description": "효율적인 휴식과 집중 사이클 밸런스",
        "condition_desc": "휴식 밸런스 체화",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 45,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "SELF_FEEDBACK",
        "category": "멘탈의지",
        "title_name": "[메타인지의 거장]",
        "description": "자신의 취약점을 객관적으로 분석·보완",
        "condition_desc": "메타인지 피드백 완료",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "D_DAY_WARRIOR",
        "category": "멘탈의지",
        "title_name": "[D-30 배수의 진]",
        "description": "수능 30일 전 극강의 집중력 발휘",
        "condition_desc": "파이널 집중력 발휘",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 250,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 40.0 or strk >= 12
    },
    {
        "condition_code": "FINAL_SURVIVOR",
        "category": "멘탈의지",
        "title_name": "[수능 당일 최후의 1인]",
        "description": "종소리 울릴 때까지 한 문제도 포기하지 않는 자",
        "condition_desc": "끝장 자습 완주",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 340,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 80.0 and strk >= 14
    },
    {
        "condition_code": "ZENITH_MIND",
        "category": "멘탈의지",
        "title_name": "[해탈의 경지: 평정심]",
        "description": "어떤 역대급 불수능 앞에서도 고요한 심장",
        "condition_desc": "최고조 멘탈리티 도달",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 520,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 120.0 and strk >= 16
    },

    # =========================================================================
    # 9. 시즌 특화 & N수/내신/정시 (Season & Exam Type) - 10종
    # =========================================================================
    {
        "condition_code": "MIDTERM_DESTROYER",
        "category": "시즌특화",
        "title_name": "[내신 1.00 수호신]",
        "description": "중간·기말 지필평가 전교 1등 수성",
        "condition_desc": "내신 집중 모드 달성",
        "tier": "일반",
        "tier_weight": 200,
        "difficulty_weight": 70,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4
    },
    {
        "condition_code": "MOCK_JUNE_SURVIVOR",
        "category": "시즌특화",
        "title_name": "[6평 칼바람 생존자]",
        "description": "6월 평가원 난이도를 뚫고 올라온 자",
        "condition_desc": "6평 시즌 완주",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 130,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 6
    },
    {
        "condition_code": "MOCK_SEPT_HERO",
        "category": "시즌특화",
        "title_name": "[9평 완성형 파이터]",
        "description": "9월 평가원 실전 감각 완전 체화",
        "condition_desc": "9평 시즌 완주",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 140,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 8
    },
    {
        "condition_code": "SUMMER_BOOTCAMP",
        "category": "시즌특화",
        "title_name": "[여름방학 텐투텐(10to10)]",
        "description": "방학 80시간 텐투텐 하드코어 특훈 완주",
        "condition_desc": "주간 20시간 이상",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 220,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 14.0 or th >= 30.0
    },
    {
        "condition_code": "WINTER_BEAST",
        "category": "시즌특화",
        "title_name": "[겨울방학 기선제압]",
        "description": "윈터스쿨 순공 대기록 수립",
        "condition_desc": "윈터스쿨 자습 완주",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 230,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 40.0 or strk >= 10
    },
    {
        "condition_code": "N_SOO_PREMIUM",
        "category": "시즌특화",
        "title_name": "[N수생의 독기]",
        "description": "재수·N수의 압도적인 간절함과 절치부심",
        "condition_desc": "N수/고3 자습 완주",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 240,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: getattr(s, 'grade', 3) == 4 or strk >= 10 or th >= 35.0
    },
    {
        "condition_code": "HIGH3_CAPTAIN",
        "category": "시즌특화",
        "title_name": "[현역의 패기]",
        "description": "고3 내신+수능 완벽 듀얼 트랙 질주",
        "condition_desc": "고3 자습 트랙 달성",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 120,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: getattr(s, 'grade', 3) == 3 or strk >= 5
    },
    {
        "condition_code": "EARLY_BIRD_CSAT",
        "category": "시즌특화",
        "title_name": "[수시 6장 납치 면역]",
        "description": "수시 수능최저 충족 및 정시 우위 확보",
        "condition_desc": "최저학력기준 돌파",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 140,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "REGULAR_WARRIOR",
        "category": "시즌특화",
        "title_name": "[정시 파이터의 심장]",
        "description": "수능 100% 전형 정면 돌파 승부사",
        "condition_desc": "정시 특화 집중",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 230,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 30.0 or strk >= 8
    },
    {
        "condition_code": "FINAL_D10_RUSH",
        "category": "시즌특화",
        "title_name": "[수능 10일 전 봉인해제]",
        "description": "파이널 실모 연속 1등급 폭풍 질주",
        "condition_desc": "파이널 집중력 발휘",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 360,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 60.0 and strk >= 12
    },

    # =========================================================================
    # 10. 히든 & 전설 칭호 (Hidden & Mythic Legends) - 10종
    # =========================================================================
    {
        "condition_code": "PERFECT_CSAT",
        "category": "히든전설",
        "title_name": "[수능 만점의 신화]",
        "description": "국·수·탐 전 영역 만점의 신화적 경지",
        "condition_desc": "수능 만점 달성",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 600,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 120.0 and strk >= 16 and "의예" in tu
    },
    {
        "condition_code": "NIGHT_LIBRARY_GHOST",
        "category": "히든전설",
        "title_name": "[자습관 문지기]",
        "description": "자습실 불을 가장 늦게 끄고 나가는 자",
        "condition_desc": "야간 마감 자습 달성",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 320,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 or strk >= 10
    },
    {
        "condition_code": "ALL_KILL_STUDENT",
        "category": "히든전설",
        "title_name": "[전과목 1등급 커트라인]",
        "description": "전 영역 백분위 99% 달성",
        "condition_desc": "전과목 1등급 도달",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 350,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 80.0 and strk >= 12
    },
    {
        "condition_code": "SPEED_RUNNER",
        "category": "히든전설",
        "title_name": "[단권화 스피드러너]",
        "description": "수능 기출 5개년 3회독 마스터",
        "condition_desc": "기출 초고속 정복",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 130,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 6
    },
    {
        "condition_code": "PALIN_DEVOTEE",
        "category": "히든전설",
        "title_name": "[PALIN OS 코어 유저]",
        "description": "매일 10시간 이상 시스템 동기화 완료",
        "condition_desc": "OS 시스템 완전 정착",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 220,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 25.0 or strk >= 7
    },
    {
        "condition_code": "GHOST_CONCENTRATION",
        "category": "히든전설",
        "title_name": "[유령 같은 몰입감]",
        "description": "연속 4시간 미동 없는 무휴식 집중",
        "condition_desc": "초극강 몰입 달성",
        "tier": "레전드",
        "tier_weight": 500,
        "difficulty_weight": 310,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 45.0 or strk >= 9
    },
    {
        "condition_code": "TIME_ZONE_TRAVELER",
        "category": "히든전설",
        "title_name": "[시차 파괴자]",
        "description": "아침 6시부터 밤 12시까지 상주",
        "condition_desc": "18시간 올데이 집중",
        "tier": "레어",
        "tier_weight": 300,
        "difficulty_weight": 140,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 5
    },
    {
        "condition_code": "SCHOLAR_OF_LIGHT",
        "category": "히든전설",
        "title_name": "[대치동 0타 강사급 감각]",
        "description": "문제를 보자마자 출제의도와 풀이 구조 파악",
        "condition_desc": "출제 의도 투시",
        "tier": "에픽",
        "tier_weight": 400,
        "difficulty_weight": 240,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 60.0 or strk >= 11
    },
    {
        "condition_code": "INVINCIBLE_WILL",
        "category": "히든전설",
        "title_name": "[역전의 대서사시]",
        "description": "노베이스에서 의치한/SKY 합격 궤도 진입",
        "condition_desc": "기적의 상승 곡선 달성",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 560,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0 and strk >= 15
    },
    {
        "condition_code": "ETERNAL_LEGEND",
        "category": "히든전설",
        "title_name": "[전국석차 0.01%]",
        "description": "전국 수험생 상위 0.01% 신화 달성",
        "condition_desc": "0.01% 최상위권 증명",
        "tier": "신화",
        "tier_weight": 600,
        "difficulty_weight": 590,
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 125.0 and strk >= 16
    }
]


def get_all_master_titles():
    """Return list of all master titles."""
    return MASTER_TITLES_CATALOG


def get_title_by_code(code: str):
    """Find a master title by condition code."""
    for t in MASTER_TITLES_CATALOG:
        if t["condition_code"] == code:
            return t
    return None
