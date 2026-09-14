# -*- coding: utf-8 -*-
"""
PALIN OS Phase 11.3: 100-Title Master Gamification Catalog
Complete 100-title matrix across 10 strategic achievement domains.
"""

MASTER_TITLES_CATALOG = [
    # =========================================================================
    # 1. 연속 출석 & 불꽃 루틴 (Streak & Habit) - 10종
    # =========================================================================
    {
        "condition_code": "STARTER_TIER",
        "category": "출석루틴",
        "title_name": "[콘크리트 1등급]",
        "description": "PALIN OS 몰입 시작 기본 칭호",
        "condition_desc": "회원가입 완료",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },
    {
        "condition_code": "STREAK_3D",
        "category": "출석루틴",
        "title_name": "[작심삼일 브레이커]",
        "description": "3일 연속 출석 및 타이머 작동 완료",
        "condition_desc": "연속 3일 달성",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 3
    },
    {
        "condition_code": "STREAK_5D",
        "category": "출석루틴",
        "title_name": "[불씨의 시작]",
        "description": "5일 연속 출석 및 학습 루틴 정착",
        "condition_desc": "연속 5일 달성",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 5
    },
    {
        "condition_code": "STREAK_7D",
        "category": "출석루틴",
        "title_name": "[새벽의 지배자]",
        "description": "7일 연속 기상/자습 미션 달성",
        "condition_desc": "연속 7일 달성",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "STREAK_14D",
        "category": "출석루틴",
        "title_name": "[2주 습관의 기적]",
        "description": "14일(2주) 연속 빈틈없는 출석 달성",
        "condition_desc": "연속 14일 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 14
    },
    {
        "condition_code": "STREAK_21D",
        "category": "출석루틴",
        "title_name": "[뇌가 적응한 자]",
        "description": "21일간의 완벽한 뇌 습관 회로 형성",
        "condition_desc": "연속 21일 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 21
    },
    {
        "condition_code": "STREAK_30D",
        "category": "출석루틴",
        "title_name": "[한 달 무결점]",
        "description": "30일(1개월) 무결점 출석 대기록",
        "condition_desc": "연속 30일 달성",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 30
    },
    {
        "condition_code": "STREAK_50D",
        "category": "출석루틴",
        "title_name": "[불꽃의 질주]",
        "description": "50일 연속 흔들림 없는 완주",
        "condition_desc": "연속 50일 달성",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 50
    },
    {
        "condition_code": "STREAK_100D",
        "category": "출석루틴",
        "title_name": "[100일의 기적]",
        "description": "100일 연속 몰입 기적 달성",
        "condition_desc": "연속 100일 달성",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 100
    },
    {
        "condition_code": "STREAK_200D",
        "category": "출석루틴",
        "title_name": "[살아있는 캘린더]",
        "description": "200일 연속 학습 기계의 증명",
        "condition_desc": "연속 200일 달성",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 200
    },

    # =========================================================================
    # 2. 누적 순공 & 한계 돌파 (Cumulative Study Hours) - 10종
    # =========================================================================
    {
        "condition_code": "STUDY_10H",
        "category": "순공한계",
        "title_name": "[공부 시동 완료]",
        "description": "누적 순공 시간 10시간 돌파",
        "condition_desc": "순공 10시간 누적",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 10.0
    },
    {
        "condition_code": "STUDY_30H",
        "category": "순공한계",
        "title_name": "[집중력 예열]",
        "description": "누적 순공 시간 30시간 돌파",
        "condition_desc": "순공 30시간 누적",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 30.0
    },
    {
        "condition_code": "STUDY_50H",
        "category": "순공한계",
        "title_name": "[불꽃의 수험생]",
        "description": "누적 순공 50시간 돌파",
        "condition_desc": "순공 50시간 누적",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 or strk >= 5
    },
    {
        "condition_code": "STUDY_100H",
        "category": "순공한계",
        "title_name": "[고독한 완주자]",
        "description": "순공 누적 100시간 극강 몰입",
        "condition_desc": "순공 100시간 누적",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0
    },
    {
        "condition_code": "STUDY_200H",
        "category": "순공한계",
        "title_name": "[200시간의 내공]",
        "description": "누적 순공 200시간의 탄탄한 기본기",
        "condition_desc": "순공 200시간 누적",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 200.0
    },
    {
        "condition_code": "STUDY_300H",
        "category": "순공한계",
        "title_name": "[300시간의 집념]",
        "description": "누적 순공 300시간 불굴의 끈기",
        "condition_desc": "순공 300시간 누적",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 300.0
    },
    {
        "condition_code": "STUDY_500H",
        "category": "순공한계",
        "title_name": "[순공 500시간 괴물]",
        "description": "누적 순공 500시간 괴물급 학습량",
        "condition_desc": "순공 500시간 누적",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 500.0
    },
    {
        "condition_code": "STUDY_1000H",
        "category": "순공한계",
        "title_name": "[1,000시간의 지배자]",
        "description": "누적 순공 1,000시간 수능의 지배자",
        "condition_desc": "순공 1,000시간 누적",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 1000.0
    },
    {
        "condition_code": "DAILY_10H",
        "category": "순공한계",
        "title_name": "[하루 10시간의 전설]",
        "description": "단일 하루 순공 10시간 돌파",
        "condition_desc": "일일 10시간 이상 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 25.0 or th >= 50.0
    },
    {
        "condition_code": "DAILY_14H",
        "category": "순공한계",
        "title_name": "[인간 한계 돌파자]",
        "description": "단일 하루 순공 14시간 초인적 집중력",
        "condition_desc": "일일 14시간 이상 자습",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 40.0 or th >= 150.0
    },

    # =========================================================================
    # 3. 시간대 & 라이프스타일 (Time Attack & Lifestyle) - 10종
    # =========================================================================
    {
        "condition_code": "TIME_5AM",
        "category": "시간대",
        "title_name": "[새벽 5시 미라클]",
        "description": "새벽 05:00~06:00 미라클 모닝 자습",
        "condition_desc": "새벽 5시 기상 자습 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 4 or th >= 15.0
    },
    {
        "condition_code": "TIME_7AM",
        "category": "시간대",
        "title_name": "[아침을 여는 자]",
        "description": "오전 07:00 이전 학습 10회 완료",
        "condition_desc": "아침 7시 이전 학습 기록",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2 or th >= 8.0
    },
    {
        "condition_code": "NIGHT_OWL_12AM",
        "category": "시간대",
        "title_name": "[심야의 독주자]",
        "description": "자정(00:00) 이후 2시간 이상 몰입 자습",
        "condition_desc": "자정 이후 심야 자습 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 20.0 or strk >= 3
    },
    {
        "condition_code": "NIGHT_OWL_2AM",
        "category": "시간대",
        "title_name": "[새벽 2시의 불침번]",
        "description": "새벽 02:00까지 꺼지지 않는 공부 불꽃",
        "condition_desc": "새벽 2시 심야 학습 5회",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 45.0 or wh >= 20.0
    },
    {
        "condition_code": "BEFORE_SCHOOL",
        "category": "시간대",
        "title_name": "[등교 전 30분]",
        "description": "등교 전 틈새 30분 순공 확보",
        "condition_desc": "아침 틈새 자습 달성",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 5.0
    },
    {
        "condition_code": "AFTER_SCHOOL_0SEC",
        "category": "시간대",
        "title_name": "[하교 직후 0초 컷]",
        "description": "하교 후 지체 없이 바로 타이머 가동",
        "condition_desc": "하교 직후 학습 즉시 시작",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 12.0
    },
    {
        "condition_code": "WEEKEND_RUSH",
        "category": "시간대",
        "title_name": "[주말 순공 폭격기]",
        "description": "토·일 양일 합산 순공 20시간 돌파",
        "condition_desc": "주말 순공 20시간 이상",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 20.0
    },
    {
        "condition_code": "FRIDAY_HERMIT",
        "category": "시간대",
        "title_name": "[금요일의 은둔자]",
        "description": "불타는 금요일 밤 유혹을 뿌리친 독서실 자습",
        "condition_desc": "금요일 야간 풀 자습 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 15.0 or strk >= 5
    },
    {
        "condition_code": "SUNDAY_CLOSER",
        "category": "시간대",
        "title_name": "[일요일의 마침표]",
        "description": "일요일 밤 주간 학습 계획 100% 완수",
        "condition_desc": "일요일 주간 목표 완수",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 10.0
    },
    {
        "condition_code": "DAY_AND_NIGHT",
        "category": "시간대",
        "title_name": "[낮과 밤을 잊은 자]",
        "description": "오전·오후·심야 전 시간대 풀 가동 몬스터",
        "condition_desc": "올 타임 집중 모드 달성",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 35.0 and th >= 60.0
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
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(u in tu for u in ["서울", "연세", "고려", "의예", "의대", "SNU", "KAIST", "포스텍"])
    },
    {
        "condition_code": "SNU_ASPIRANT",
        "category": "목표대학",
        "title_name": "[샤(SNU)의 문을 두드리는 자]",
        "description": "서울대학교 지망 및 주간 순공 30시간 이상",
        "condition_desc": "서울대 목표 & 주간 30시간",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("서울" in tu or "SNU" in tu) and wh >= 15.0
    },
    {
        "condition_code": "YONSEI_BLUE",
        "category": "목표대학",
        "title_name": "[아카라카 블루 크루]",
        "description": "연세대학교 지망 및 독보적 페이스 유지",
        "condition_desc": "연세대 목표 & 주간 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("연세" in tu or "연대" in tu)
    },
    {
        "condition_code": "KOREA_CRIMSON",
        "category": "목표대학",
        "title_name": "[안암의 붉은 호랑이]",
        "description": "고려대학교 지망 및 꺾이지 않는 투지",
        "condition_desc": "고려대 목표 & 주간 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("고려" in tu or "고대" in tu)
    },
    {
        "condition_code": "MEDICAL_WHITE",
        "category": "목표대학",
        "title_name": "[하얀 가운의 지망생]",
        "description": "의치한약수 메디컬 계열 지망 수험생",
        "condition_desc": "의학/치의/한의/약학 목표",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(m in tu for m in ["의예", "의대", "치의", "한의", "약학", "수의"])
    },
    {
        "condition_code": "SCHWEITZER_PACE",
        "category": "목표대학",
        "title_name": "[미래의 슈바이처]",
        "description": "메디컬 목표 + 주간 순공 40시간 초인 페이스",
        "condition_desc": "메디컬 목표 & 주간 40시간",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(m in tu for m in ["의예", "의대", "치의", "한의", "약학"]) and wh >= 30.0
    },
    {
        "condition_code": "KAIST_ENGINEER",
        "category": "목표대학",
        "title_name": "[공학의 카이스트 크루]",
        "description": "KAIST / POSTECH 이공계 최정상 지망",
        "condition_desc": "KAIST/포스텍 목표",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("KAIST" in tu.upper() or "포스텍" in tu or "과기원" in tu)
    },
    {
        "condition_code": "SKKU_SCHOLAR",
        "category": "목표대학",
        "title_name": "[명륜당 예비 유생]",
        "description": "성균관대학교 지망 전통의 학구열",
        "condition_desc": "성균관대 목표",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("성균관" in tu or "성대" in tu)
    },
    {
        "condition_code": "HANYANG_ENGINE",
        "category": "목표대학",
        "title_name": "[한양 공대 엔진]",
        "description": "한양대학교 지망 대한민국 공학의 심장",
        "condition_desc": "한양대 목표",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: ("한양" in tu or "한대" in tu)
    },
    {
        "condition_code": "FREE_MAJOR",
        "category": "목표대학",
        "title_name": "[자유전공 개척자]",
        "description": "무전공 / 자율전공학부 지망 융합 인재",
        "condition_desc": "자율전공/학부대학 목표",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: any(f in tu for f in ["자율", "자유", "통합", "융합"])
    },

    # =========================================================================
    # 5. OMR & 모의고사 실전 (Mock Exams & Grades) - 10종
    # =========================================================================
    {
        "condition_code": "OMR_FIRST",
        "category": "OMR실전",
        "title_name": "[디지털 OMR 개척자]",
        "description": "인앱 디지털 OMR 모의고사 첫 응시 및 채점",
        "condition_desc": "OMR 첫 응시 완료",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 1 or pts >= 150
    },
    {
        "condition_code": "MOCK_MARCH",
        "category": "OMR실전",
        "title_name": "[3모 실전 격파]",
        "description": "3월 학력평가 실전 분석 완료",
        "condition_desc": "3모 채점 및 분석",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 2 or pts >= 200
    },
    {
        "condition_code": "MOCK_JUNE",
        "category": "OMR실전",
        "title_name": "[6모 킬러 사냥꾼]",
        "description": "6월 평가원 모의고사 킬러문항 완벽 분석",
        "condition_desc": "6모 분석 완료",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 3 or pts >= 300
    },
    {
        "condition_code": "MOCK_SEPT",
        "category": "OMR실전",
        "title_name": "[9모 최종 점검]",
        "description": "9월 평가원 모의고사 실전 감각 완성",
        "condition_desc": "9모 분석 완료",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 4 or pts >= 400
    },
    {
        "condition_code": "MOCK_10X",
        "category": "OMR실전",
        "title_name": "[실전 모의고사 10회 완주]",
        "description": "디지털 OMR 모의고사 10회 완주",
        "condition_desc": "OMR 누적 10회 응시",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 10 or pts >= 800
    },
    {
        "condition_code": "MOCK_30X",
        "category": "OMR실전",
        "title_name": "[모의고사 30회 마스터]",
        "description": "실전 모의고사 30회 응시 기출의 달인",
        "condition_desc": "OMR 누적 30회 응시",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 30 or pts >= 1500
    },
    {
        "condition_code": "WRONG_NOTE_MASTER",
        "category": "OMR실전",
        "title_name": "[오답노트 집착광]",
        "description": "약점 오답 정밀 피드백 50회 누적",
        "condition_desc": "오답노트 50회 분석",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 5 or pts >= 500
    },
    {
        "condition_code": "KILLER_CRUSHER",
        "category": "OMR실전",
        "title_name": "[킬러문항 분쇄기]",
        "description": "최고난도 4점 킬러문항 정복",
        "condition_desc": "킬러문항 정답률 인증",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: omr >= 8 or pts >= 700
    },
    {
        "condition_code": "GRADE_SURGE",
        "category": "OMR실전",
        "title_name": "[등급 수직 상승러]",
        "description": "전회 대비 백분위 10% 이상 수직 상승",
        "condition_desc": "성적 상승 인증",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.diligence_score or 0) >= 500
    },
    {
        "condition_code": "PERFECT_SCORE",
        "category": "OMR실전",
        "title_name": "[만점 수렴의 경지]",
        "description": "전 과목 1등급 컷 통과 및 만점 도전",
        "condition_desc": "전 과목 1등급 달성",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.diligence_score or 0) >= 900 or vip
    },

    # =========================================================================
    # 6. 학교 대항전 & 로컬 제왕 (School Guild & Geo Throne) - 10종
    # =========================================================================
    {
        "condition_code": "SCHOOL_HONOR",
        "category": "로컬길드",
        "title_name": "[모교의 명예]",
        "description": "학교 대항전에 첫 자습 포인트 기여",
        "condition_desc": "학교 랭킹 포인트 기여",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 5.0
    },
    {
        "condition_code": "SCHOOL_TOP1",
        "category": "로컬길드",
        "title_name": "[전교 1위의 위엄]",
        "description": "우리 학교 주간 자습 순위 1위 석권",
        "condition_desc": "교내 자습 1위 달성",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 25.0
    },
    {
        "condition_code": "SCHOOL_CARRY",
        "category": "로컬길드",
        "title_name": "[우리 학교 캐리머신]",
        "description": "학교 전체 포인트의 20% 이상 독점 기여",
        "condition_desc": "학교 포인트 독보적 기여",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 80.0
    },
    {
        "condition_code": "DAECHI_ACE",
        "category": "로컬길드",
        "title_name": "[대치동 1타 열공러]",
        "description": "강남/대치 지역 실시간 랭킹 TOP 3 진입",
        "condition_desc": "강남/대치 TOP 3 랭크",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: "강남" in (s.region or "") or "대치" in (s.region or "") or wh >= 30.0
    },
    {
        "condition_code": "BUNDANG_GUARDIAN",
        "category": "로컬길드",
        "title_name": "[분당학군 수호자]",
        "description": "성남/분당 지역 실시간 랭킹 TOP 3 진입",
        "condition_desc": "성남/분당 TOP 3 랭크",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: "분당" in (s.region or "") or "성남" in (s.region or "") or wh >= 30.0
    },
    {
        "condition_code": "MOKDONG_LORD",
        "category": "로컬길드",
        "title_name": "[목동의 맹주]",
        "description": "양천/목동 지역 랭킹 상위권 석권",
        "condition_desc": "목동 상위 랭크",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: "목동" in (s.region or "") or "양천" in (s.region or "") or wh >= 30.0
    },
    {
        "condition_code": "SUSEONG_TOPTIER",
        "category": "로컬길드",
        "title_name": "[수성구 탑티어]",
        "description": "대구/수성 지역 랭킹 상위권 석권",
        "condition_desc": "수성구 상위 랭크",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: "수성" in (s.region or "") or "대구" in (s.region or "") or wh >= 30.0
    },
    {
        "condition_code": "GEO_THRONE_KING",
        "category": "로컬길드",
        "title_name": "[구(區) 단위 로컬 제왕]",
        "description": "동네/구 단위 1위 등극 및 전체 전광판 브로드캐스트",
        "condition_desc": "지역 1위 전광판 등록",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 35.0 or vip
    },
    {
        "condition_code": "ACADEMY_FLAGSHIP",
        "category": "로컬길드",
        "title_name": "[학원 대표 에이스]",
        "description": "가맹 학원 전체 원생 중 주간 자습 1위",
        "condition_desc": "학원 내 1위 달성",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 22.0
    },
    {
        "condition_code": "RIVAL_CONQUEROR",
        "category": "로컬길드",
        "title_name": "[라이벌 제압자]",
        "description": "인접 순위 라이벌과의 주간 누적 대결 승리",
        "condition_desc": "라이벌 대결 승리",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 6 or th >= 25.0
    },

    # =========================================================================
    # 7. 콕 찌르기 & 성실 소셜 (Social & Diligence) - 10종
    # =========================================================================
    {
        "condition_code": "POKE_ALARM",
        "category": "성실소셜",
        "title_name": "[잠 깨우는 알람시계]",
        "description": "멈춘 라이벌 콕 찌르기 5회 이상 발송",
        "condition_desc": "콕 찌르기 5회 발송",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 10.0
    },
    {
        "condition_code": "POKE_SNIPER",
        "category": "성실소셜",
        "title_name": "[저격수]",
        "description": "나태해진 동료를 깨우는 콕 찌르기 20회 누적",
        "condition_desc": "콕 찌르기 20회 발송",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 30.0
    },
    {
        "condition_code": "POKE_RESPONDER",
        "category": "성실소셜",
        "title_name": "[자극 수용자]",
        "description": "콕 찌르기 알림을 받고 즉시 타이머 가동",
        "condition_desc": "찌르기 알림 즉시 반응",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 2
    },
    {
        "condition_code": "QA_QUESTIONER",
        "category": "성실소셜",
        "title_name": "[질문 마스터]",
        "description": "Q&A 게시판에 수준 높은 질문 5회 등록",
        "condition_desc": "Q&A 5회 등록",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 200
    },
    {
        "condition_code": "BIBLE_CONTRIBUTOR",
        "category": "성실소셜",
        "title_name": "[학교 족보 기여자]",
        "description": "학교 기출/족보 자료 검증 및 공유 기여",
        "condition_desc": "기출 자료 공유 완료",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 300
    },
    {
        "condition_code": "TICKET_INVITER",
        "category": "성실소셜",
        "title_name": "[골든티켓 추천인]",
        "description": "친구에게 골든티켓 초대 링크 공유 성공",
        "condition_desc": "친구 1명 초대 완료",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.golden_tickets_count or 0) >= 1 or pts >= 250
    },
    {
        "condition_code": "CREW_FOUNDER",
        "category": "성실소셜",
        "title_name": "[스터디 크루 결성자]",
        "description": "친구 3명 이상 초대하여 열공 연합 결성",
        "condition_desc": "친구 3명 이상 초대",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.golden_tickets_count or 0) >= 3 or pts >= 500
    },
    {
        "condition_code": "POINTS_1000P",
        "category": "성실소셜",
        "title_name": "[성실도 천점 돌파]",
        "description": "성실도 포인트 누적 1,000P 돌파",
        "condition_desc": "1,000P 누적 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 1000
    },
    {
        "condition_code": "POINTS_5000P",
        "category": "성실소셜",
        "title_name": "[성실의 화신]",
        "description": "성실도 포인트 누적 5,000P 금자탑",
        "condition_desc": "5,000P 누적 달성",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: pts >= 5000
    },
    {
        "condition_code": "TUTOR_ASPIRANT",
        "category": "성실소셜",
        "title_name": "[예비 명문대 튜터]",
        "description": "합격 후 후배들을 가르칠 과외 프로필 사전 연동",
        "condition_desc": "튜터 프로필 연동",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0 and strk >= 10
    },

    # =========================================================================
    # 8. 멘탈 & 수험생 의지 (Mental & Iron Will) - 10종
    # =========================================================================
    {
        "condition_code": "CONCRETE_MENTAL",
        "category": "멘탈의지",
        "title_name": "[콘크리트 멘탈]",
        "description": "슬럼프 없이 4주 연속 주간 목표 100% 달성",
        "condition_desc": "4주 연속 목표 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 28 or th >= 70.0
    },
    {
        "condition_code": "NEVER_GIVE_UP",
        "category": "멘탈의지",
        "title_name": "[중꺾마 (중요한 건 꺾이지 않는 마음)]",
        "description": "어떤 난관에도 굴하지 않고 일어나는 불굴의 정신",
        "condition_desc": "위기 극복 및 반등 성공",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 10 or th >= 40.0
    },
    {
        "condition_code": "HEAVY_CHAIR",
        "category": "멘탈의지",
        "title_name": "[엉덩이 무거운 자]",
        "description": "일시정지 없이 단일 4시간 연속 집중 자습",
        "condition_desc": "4시간 논스톱 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 35.0
    },
    {
        "condition_code": "STUDYROOM_GHOST",
        "category": "멘탈의지",
        "title_name": "[독서실 지박령]",
        "description": "주간 독서실/학원 체류 순공 40시간 이상",
        "condition_desc": "주간 40시간 독서실 체류",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 35.0
    },
    {
        "condition_code": "PHONE_SEALER",
        "category": "멘탈의지",
        "title_name": "[스마트폰 봉인자]",
        "description": "타이머 작동 중 이탈 없이 완벽한 몰입 유지",
        "condition_desc": "딴짓 없는 순공 7일 유지",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 7
    },
    {
        "condition_code": "ENJOY_THE_STORM",
        "category": "멘탈의지",
        "title_name": "[피할 수 없으면 즐겨라]",
        "description": "수능 D-50 압박 속에서도 주간 40시간 돌파",
        "condition_desc": "파이널 압박 극복",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 30.0
    },
    {
        "condition_code": "ROMANTIC_STUDENT",
        "category": "멘탈의지",
        "title_name": "[낭만 수험생]",
        "description": "비 오는 날도, 휴일에도 변함없는 학습 루틴",
        "condition_desc": "무휴일 학습 기록",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 20.0
    },
    {
        "condition_code": "STUDY_VENDING",
        "category": "멘탈의지",
        "title_name": "[공부 자판기]",
        "description": "책상에 앉으면 0초 만에 집중 모드 자동 진입",
        "condition_desc": "연속 14일 즉시 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 14
    },
    {
        "condition_code": "SENIOR_DIGNITY",
        "category": "멘탈의지",
        "title_name": "[고3의 품격]",
        "description": "온갖 유혹을 차단하고 수험생 본분에 몰입한 자",
        "condition_desc": "고3 올 데이 몰입",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 15.0
    },
    {
        "condition_code": "PERFECT_DREAM",
        "category": "멘탈의지",
        "title_name": "[수능 만점의 꿈]",
        "description": "목표 대학 및 수능 만점 각오 등록 완료",
        "condition_desc": "목표 다짐 설정",
        "tier": "입문",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: True
    },

    # =========================================================================
    # 9. 시즌 & 모멘텀 특화 (Season & Milestones) - 10종
    # =========================================================================
    {
        "condition_code": "WINTER_SURVIVOR",
        "category": "시즌특화",
        "title_name": "[겨울방학 윈터스쿨 생존자]",
        "description": "겨울방학 4주 연속 주간 40시간 이상 풀 완주",
        "condition_desc": "윈터스쿨 4주 완주",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0 or strk >= 20
    },
    {
        "condition_code": "CHERRY_BLOSSOM",
        "category": "시즌특화",
        "title_name": "[벚꽃 엔딩 방어자]",
        "description": "4월 벚꽃 시즌에도 흔들리지 않고 중간고사 집중",
        "condition_desc": "4월 봄시즌 순공 방어",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 25.0
    },
    {
        "condition_code": "SUMMER_BURNING",
        "category": "시즌특화",
        "title_name": "[여름방학 썸머버닝]",
        "description": "무더운 여름방학 순공 150시간 돌파",
        "condition_desc": "여름방학 150시간 돌파",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 150.0 or wh >= 35.0
    },
    {
        "condition_code": "D_100_COUNT",
        "category": "시즌특화",
        "title_name": "[D-100 카운트다운]",
        "description": "수능 D-100 시점 순공 10시간 이상 불꽃 자습",
        "condition_desc": "D-100 당일 10시간 자습",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 50.0
    },
    {
        "condition_code": "D_30_SPURT",
        "category": "시즌특화",
        "title_name": "[D-30 파이널 스퍼트]",
        "description": "수능 D-30 파이널 주간 45시간 풀 가동",
        "condition_desc": "D-30 주간 45시간",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 35.0 or th >= 120.0
    },
    {
        "condition_code": "WINTER_COLD_WIN",
        "category": "시즌특화",
        "title_name": "[수능 한파 정복자]",
        "description": "11월 수능 직전 흔들림 없는 컨디션 조절 완주",
        "condition_desc": "수능 직전 완주",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 15
    },
    {
        "condition_code": "EXAM_HELL_ESCAPE",
        "category": "시즌특화",
        "title_name": "[내신 지옥 탈출]",
        "description": "내신 직전 2주간 누적 80시간 달성",
        "condition_desc": "내신 기간 80시간 달성",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 60.0
    },
    {
        "condition_code": "REPEAT_RESOLVE",
        "category": "시즌특화",
        "title_name": "[N수의 결의]",
        "description": "더 높은 정상을 향한 N수생의 굳은 결의",
        "condition_desc": "N수생 결의 등록",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.grade or 3) >= 4 or th >= 20.0
    },
    {
        "condition_code": "SUSHI_6_PASS",
        "category": "시즌특화",
        "title_name": "[수시 6장 섭렵]",
        "description": "수시 원서 접수 기간에도 흔들리지 않는 학습 유지",
        "condition_desc": "수시 시즌 순공 유지",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 15.0
    },
    {
        "condition_code": "JEONGSI_FIGHTER",
        "category": "시즌특화",
        "title_name": "[정시 파이터의 길]",
        "description": "오직 수능 성적으로 정면 돌파하는 강자의 길",
        "condition_desc": "정시 집중 몰입",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 80.0 and strk >= 14
    },

    # =========================================================================
    # 10. 희귀 & 히든 / 레전더리 (Hidden & Legendary Tier) - 10종
    # =========================================================================
    {
        "condition_code": "VIP_1PCT",
        "category": "히든전설",
        "title_name": "[VIP 1% 블랙 라운더]",
        "description": "전국 주간 백분위 상위 1% 진입 (블랙 라운지 입성)",
        "condition_desc": "전국 상위 1% 달성",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: vip or wh >= 40.0
    },
    {
        "condition_code": "DIRECTOR_PICK",
        "category": "히든전설",
        "title_name": "[원장님의 원픽]",
        "description": "학원 관리자 관제실 선정 '이달의 모범 수험생'",
        "condition_desc": "학원장 추천 모범생",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: strk >= 10 and th >= 30.0
    },
    {
        "condition_code": "ALL_NIGHT_24H",
        "category": "히든전설",
        "title_name": "[24시간 철야의 기적]",
        "description": "24시간 동안 총합 16시간 이상 기록한 불굴의 하루",
        "condition_desc": "하루 16시간 순공 기록",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 45.0 or th >= 200.0
    },
    {
        "condition_code": "PAYMENT_FREEPASS",
        "category": "히든전설",
        "title_name": "[결제선생 프리패스]",
        "description": "수강료 정시 납부 및 락인 해제 완료",
        "condition_desc": "가맹 수강료 완납",
        "tier": "일반",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: (s.academy_code is not None and s.academy_code != "")
    },
    {
        "condition_code": "PALIN_MASTER",
        "category": "히든전설",
        "title_name": "[PALIN OS 마스터]",
        "description": "전체 칭호 중 20개 이상 수집 달성한 마스터",
        "condition_desc": "칭호 20개 이상 해금",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 100.0 and strk >= 20
    },
    {
        "condition_code": "ABSOLUTE_DEFENSE",
        "category": "히든전설",
        "title_name": "[절대 방어선]",
        "description": "마지노선 대학 벤치마크 4주 연속 '안정' 유지",
        "condition_desc": "마지노선 4주 연속 방어",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 28.0 and strk >= 14
    },
    {
        "condition_code": "TARGET_LOCKED",
        "category": "히든전설",
        "title_name": "[목표대학 1지망 굳히기]",
        "description": "1지망 목표대학 벤치마크 4주 연속 상위 달성",
        "condition_desc": "1지망 벤치마크 4주 연속 안정",
        "tier": "레전드",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: wh >= 38.0 and strk >= 14
    },
    {
        "condition_code": "ASMR_ADDICT",
        "category": "히든전설",
        "title_name": "[공부 ASMR 중독자]",
        "description": "목표대학 ASMR 사운드와 함께 20시간 이상 몰입",
        "condition_desc": "ASMR 청취 자습 20시간",
        "tier": "레어",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 20.0
    },
    {
        "condition_code": "OWL_AND_LARK",
        "category": "히든전설",
        "title_name": "[올빼미와 종달새]",
        "description": "새벽 5시 기상과 밤 12시 심야 자습을 모두 해낸 자",
        "condition_desc": "새벽/심야 양방향 정복",
        "tier": "에픽",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: th >= 40.0 and strk >= 7
    },
    {
        "condition_code": "CSAT_LEGEND",
        "category": "히든전설",
        "title_name": "[수능 대박의 전설]",
        "description": "최종 합격 후 PALIN OS 명예의 전당에 등재된 전설",
        "condition_desc": "수능 합격 인증",
        "tier": "신화",
        "check": lambda s, th, strk, wh, tu, omr, pts, vip: vip or th >= 300.0
    }
]

def get_all_master_titles():
    return MASTER_TITLES_CATALOG
