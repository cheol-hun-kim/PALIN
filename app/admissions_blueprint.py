# -*- coding: utf-8 -*-
"""
PassMate 2026 Admissions Blueprint Engine (대입 학종/생기부 AI 역설계 엔진)
Generates:
1. 2026 Target University/Major GPA Cut vs Current Gap Analysis
2. Subject-Specific High-Impact Record Sentences (과세특 역설계 텍스트)
3. Advanced Mathematical In-Depth Exploration Report Blueprints (수학 심화 탐구 보고서 2선)
4. Director Consultation Speech Script (원장 상담용 1분 스크립트)
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/admissions", tags=["2026 Admissions Blueprint"])

class BlueprintRequest(BaseModel):
    student_name: str = "김민우"
    student_grade: str = "고2"           # '고1', '고2', '고3'
    target_univ: str = "서울대학교"
    target_major: str = "컴퓨터공학과"
    current_gpa: float = 1.85           # 평균 내신 등급
    selected_math: Optional[str] = "미적분"  # '미적분', '확률과통계', '기하', '공통수학'

# Benchmark 2026 Target Database Cutoffs
BENCHMARK_CUTOFFS = {
    "의예과": {"tier1": 1.15, "tier2": 1.35, "keywords": ["생명과학", "약물동태학", "미분방정식", "수치해석", "생체신호"]},
    "치의예과": {"tier1": 1.25, "tier2": 1.45, "keywords": ["생체재료", "응력분포", "3D스캔", "기하벡터"]},
    "컴퓨터공학과": {"tier1": 1.40, "tier2": 1.75, "keywords": ["경사하강법", "확률밀도함수", "알고리즘복잡도", "행렬연산", "이산수학"]},
    "인공지능학과": {"tier1": 1.45, "tier2": 1.80, "keywords": ["신경망가중치", "다변수미적분", "베이즈통계", "손실함수"]},
    "전자공학과": {"tier1": 1.50, "tier2": 1.85, "keywords": ["푸리에변환", "신호처리", "복소평면", "전자기학"]},
    "기계공학과": {"tier1": 1.55, "tier2": 1.95, "keywords": ["유체역학", "미분방정식", "정사영", "응력텐서"]},
    "화학생명공학과": {"tier1": 1.48, "tier2": 1.85, "keywords": ["반응속도론", "지수감소모델", "통계적유의성"]},
    "경영학과": {"tier1": 1.60, "tier2": 2.05, "keywords": ["포트폴리오최적화", "정규분포", "게임이론", "선형계획법"]},
    "경제학과": {"tier1": 1.55, "tier2": 1.95, "keywords": ["한계효용", "미분탄력성", "시계열분석", "회귀분석"]},
    "수학교육과": {"tier1": 1.65, "tier2": 2.10, "keywords": ["수학교육공학", "개념형성", "증명지도", "시각화"]},
    "기타공학": {"tier1": 1.70, "tier2": 2.20, "keywords": ["수학적모델링", "오차분석", "최적화"]}
}

@router.post("/blueprint")
def generate_admissions_blueprint(req: BlueprintRequest) -> Dict[str, Any]:
    """
    Generates high-ticket admissions consulting blueprint for academy directors.
    """
    major_key = "기타공학"
    for k in BENCHMARK_CUTOFFS:
        if k in req.target_major:
            major_key = k
            break
            
    cut_info = BENCHMARK_CUTOFFS[major_key]
    avg_cut = cut_info["tier1"] if "서울" in req.target_univ or "연세" in req.target_univ or "고려" in req.target_univ else cut_info["tier2"]
    gap = round(req.current_gpa - avg_cut, 2)
    
    if gap <= 0:
        prediction_status = "안정 합격권 (생기부 심화 시 최상위 장학생)"
        status_color = "#10B981"
        gap_desc = f"목표 학과 평균 내신({avg_cut:.2f})보다 {abs(gap):.2f}등급 앞서며, 정량 평가에서 확실한 우위를 점하고 있습니다."
    elif gap <= 0.4:
        prediction_status = "소신 지원권 (생기부 과세특 심화로 역전 가능 구간)"
        status_color = "#38BDF8"
        gap_desc = f"목표 학과 평균({avg_cut:.2f})과 {gap:.2f}등급 격차로, 수학/과학 심화 탐구 보고서와 교과 과세특으로 충분히 뒤집을 수 있는 최적의 학종 타깃입니다."
    else:
        prediction_status = "상향 도전권 (수학 탐구 보고서 독보적 차별화 필수)"
        status_color = "#F59E0B"
        gap_desc = f"내신 정량 차이({gap:.2f}등급)를 극복하기 위해 대치동 최상위급 '수학 탐구 보고서'와 전공 연계 세특 키워드가 반드시 뒷받침되어야 합니다."

    # Subject-Specific Setek (과세특) Sentences
    setek_sentences = [
        {
            "subject": req.selected_math or "미적분",
            "title": f"전공 연계 수학 모델링 및 심층 탐구 역량",
            "content": f"[수학 모델링 역량] {req.target_major} 분야의 핵심 알고리즘과 수학적 기초 원리를 연계하여 주도적인 탐구를 수행함. 교과서에 등장하는 함수의 증가·감소 및 극값의 성질을 단순 수식 계산에 그치지 않고, {cut_info['keywords'][0]}에 적용되는 {cut_info['keywords'][1]} 원리로 확장하여 수학적 정밀성을 증명함. 복잡한 미분방정식의 수치해석적 해법을 스스로 도출하고 결과를 시각화하여 동료들에게 논리적으로 설명하는 등 탁월한 학문적 호기심과 수리적 사고력을 입증함.",
            "competency_highlight": "지적 호기심 및 비판적 수학적 사고력 (평가관 최고 등급)"
        },
        {
            "subject": "확률과 통계",
            "title": "데이터 분석 및 통계적 추론 역량",
            "content": f"[통계적 추론 역량] {req.target_major}의 실제 데이터셋에서 발생하는 노이즈와 오차를 분석하기 위해 정규분포와 신뢰구간의 수학적 원리를 심층 분석함. 표본오차가 전체 결론에 미치는 영향을 검증하고, 베이즈 정리를 활용한 조건부 확률 기반의 분류 모델을 설계함. 단순 공식 대입이 아닌 데이터의 본질적 특성을 수리적으로 해석하는 우수한 통계적 통찰력을 발휘함.",
            "competency_highlight": "데이터 기반 문제 해결력 및 통계 모델링"
        },
        {
            "subject": "기하 / 공통수학",
            "title": "공간 지각 및 기하학적 엄밀성",
            "content": f"[기하학적 공간 모델링] 3차원 공간에서의 좌표계 변환과 벡터의 내적을 활용하여 {cut_info['keywords'][-1]} 시스템의 위치 관계를 기하학적으로 증명함. 수식으로만 전개하기 어려운 다차원 기하학적 성질을 정확한 도해와 작도를 통해 모델링하고, 사영 기하학의 원리를 전공 탐구에 창의적으로 접목함.",
            "competency_highlight": "다차원 시각화 및 수리 기하 분석력"
        }
    ]

    # In-Depth Math Exploration Reports
    research_topics = [
        {
            "id": "topic_1",
            "title": f"전공 융합 심화 탐구: {cut_info['keywords'][0]} 최적화를 위한 다변수 함수의 극대·극소 판별 및 경사하강법의 수학적 엄밀성 분석",
            "motive": f"{req.target_major} 분야에서 널리 쓰이는 최적화 과정이 고교 미적분의 접선의 방정식 및 이계도함수 판정법과 어떻게 직결되는지 규명하고자 함.",
            "math_concepts": ["편미분과 그래디언트(Gradient)", "이계도함수와 볼록성(Convexity)", "테일러 2차 근사", "학습률에 따른 수렴 경계 조건"],
            "procedure": "1단계: 1차원 함수의 극값 판별을 2차원 공간으로 확장\n2단계: 손실함수의 국소 극솟값(Local Minimum) 도달 조건 유도\n3단계: 고교 교육과정 미적분의 롤의 정리 및 평균값 정리와의 연결고리 증명\n4단계: 파이썬 시각화 도구를 활용한 수렴 곡선 오차 그래프 분석",
            "expected_outcome": "입학사정관에게 '교과서 개념을 대학 수준의 전공 기초 원리와 직접 연결할 수 있는 독보적 학업 역량'을 각인시킴."
        },
        {
            "id": "topic_2",
            "title": f"확률적 모델링 탐구: 마르코프 체인(Markov Chain)과 조건부 확률 행렬을 활용한 {cut_info['keywords'][1]} 전이 확률 수리 분석",
            "motive": f"단순 확률 계산을 넘어 시간의 흐름에 따른 상태 변화를 수학적 전이 행렬로 모델링하여 {req.target_major}의 예측 신뢰도를 평가함.",
            "math_concepts": ["조건부 확률과 전확률의 정리", "전이 확률 행렬(Transition Matrix)", "행렬의 거듭제곱과 극한", "정상 상태(Steady State)의 고유값 분석"],
            "procedure": "1단계: 현실 상황의 전이 상태를 3개 노드로 추상화\n2단계: 확률과 통계의 독립시행 및 조건부확률로 전이 행렬 도출\n3단계: 행렬 연산과 수열의 극한을 결합하여 장기적 수렴 확률 계산\n4단계: 예측 오차에 대한 민감도 분석 및 보고서 작성",
            "expected_outcome": "단순 암기형 학생과 완전히 차별화되는 '수학적 구조화 및 전공 융합적 분석력' 증명."
        }
    ]

    # Director Consultation Script
    director_script = f"""
[학부모 상담용 원장 1분 브리핑 대본]
"어머님, {req.student_name}의 현재 내신 등급은 {req.current_gpa:.2f}등급으로, {req.target_univ} {req.target_major}의 평균 컷({avg_cut:.2f})과 약 {gap:.2f}등급 격차가 있습니다.
일반적인 학원에서는 '내신이 부족하니 대학을 낮추자'고 하겠지만, 저희 학원의 분석은 다릅니다.
학생부 종합전형은 정량 내신만으로 뽑지 않습니다. 0.3~0.4등급의 차이는 '수학 교과의 심화 탐구 보고서와 과세특 역량'으로 얼마든지 뒤집을 수 있습니다.
저희가 설계한 이번 학기 {req.student_name} 맞춤형 탐구 주제는 '{cut_info['keywords'][0]} 최적화와 미적분 모델링'입니다. 이 한 편의 보고서로 서울대/명문대 사정관의 최고 평가를 이끌어내어 역전 합격을 완성하겠습니다."
"""

    return {
        "success": True,
        "student_info": {
            "name": req.student_name,
            "grade": req.student_grade,
            "target_univ": req.target_univ,
            "target_major": req.target_major,
            "current_gpa": req.current_gpa
        },
        "diagnosis": {
            "target_avg_gpa": avg_cut,
            "gpa_gap": gap,
            "status": prediction_status,
            "status_color": status_color,
            "description": gap_desc
        },
        "setek_recommendations": setek_sentences,
        "research_topics": research_topics,
        "director_consultation_script": director_script.strip()
    }
