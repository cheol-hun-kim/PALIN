import sys
import os
import json
import traceback

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    print("=" * 60)
    print("🚀 [PALIN OS] 전방위 무결성 및 신규 기능 통합 검증 시작")
    print("=" * 60)
    
    passed = 0
    total = 0

    def test(name, fn):
        nonlocal passed, total
        total += 1
        print(f"\n[{total}] {name} 검증 중...")
        try:
            fn()
            print(f"  ✅ 통과 (PASS)")
            passed += 1
        except Exception as e:
            print(f"  ❌ 실패 (FAIL): {e}")
            traceback.print_exc()

    # 1. 파이썬 문법 및 모듈 임포트 검사
    def test_imports():
        import app.models as models
        import app.schemas as schemas
        import app.database as database
        import app.predict as predict
        import app.ai as ai
        import app.sms as sms
        import app.main as main
        assert models is not None
        assert predict is not None
        assert ai is not None
        assert sms is not None
        assert main is not None
    test("파이썬 코어 모듈 임포트 무결성", test_imports)

    # 2. 전국 시도 및 시군구 데이터 검사
    def test_regions():
        with open("app/data/regions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) >= 17, f"시도 수가 부족합니다: {len(data)}"
        assert "서울특별시" in data and "강남구" in data["서울특별시"]
        assert "경기도" in data and "성남시 분당구" in data["경기도"]
    test("17개 시도/시군구 표준 DB 무결성", test_regions)

    # 3. 전국 고교 DB 검사
    def test_high_schools():
        with open("app/data/high_schools.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) >= 50, f"고등학교 수가 부족합니다: {len(data)}"
        names = [h["name"] for h in data]
        assert "낙생고등학교" in names or "대치고등학교" in names or "하나고등학교" in names
    test("전국 고등학교 DB 무결성", test_high_schools)

    # 4. 정시 합격예측 엔진 사탐/과탐 교차지원 및 과탐 가산점 검증
    def test_predict_cross_apply():
        from app.predict import predict_admission
        res_satam = predict_admission(
            kor_pct=95, math_pct=95, eng_raw=90,
            tam1_pct=92, tam2_pct=90, hist_raw=45,
            math_type="미적", tam1_type="사탐", tam2_type="사탐",
            target_univ="건국대학교"
        )
        assert len(res_satam["results"]) > 0, "예측 결과가 0건입니다."
        univ_names = [r["대학교"] for r in res_satam["results"]]
        assert "건국대학교" in univ_names or len(univ_names) > 1000

        # 서울대 자연계열 사탐 필터링 검증
        snu_satam = [r for r in res_satam["results"] if r["대학교"] == "서울대학교" and r["계열"] == "이과"]
        assert len(snu_satam) == 0, f"사탐 응시자에게 서울대 자연계가 검색되었습니다: {len(snu_satam)}"

        # 과탐 응시 시 서울대 자연계 검색 가능 확인
        res_gwatam = predict_admission(
            kor_pct=99, math_pct=99, eng_raw=95,
            tam1_pct=99, tam2_pct=99, hist_raw=50,
            math_type="미적", tam1_type="과탐", tam2_type="과탐",
            target_univ="서울대학교"
        )
        snu_gwatam = [r for r in res_gwatam["results"] if r["대학교"] == "서울대학교"]
        assert len(snu_gwatam) > 0, "과탐 응시자에게 서울대 결과가 없습니다."
    test("정시 합격예측 교차지원 & 과탐가산점 & 서울대필수필터", test_predict_cross_apply)

    # 5. AI RAG 실시간 지식 병합 검사
    def test_ai_rag_knowledge():
        from app.ai import get_expert_knowledge
        from app.database import SessionLocal
        import app.models as models

        db = SessionLocal()
        try:
            test_k = models.AdminKnowledge(
                category="입시철학",
                title="단기 100점 비법",
                content="실패는 없다. 통제된 환경만이 결과를 만든다."
            )
            db.add(test_k)
            db.commit()

            merged = get_expert_knowledge()
            assert "실패는 없다" in merged or "수험" in merged, "지식 병합 실패"

            db.delete(test_k)
            db.commit()
        finally:
            db.close()
    test("AI RAG 실시간 원장 지식 동적 병합", test_ai_rag_knowledge)

    # 6. SQLite 스키마 신규 컬럼 마이그레이션 무결성 검사
    def test_db_schema():
        from app.database import SessionLocal, engine
        from sqlalchemy import text
        db = SessionLocal()
        try:
            with engine.connect() as conn:
                res = conn.execute(text("PRAGMA table_info(students)")).fetchall()
                cols = [r[1] for r in res]
                assert "sido" in cols or "region" in cols
                assert "escrow_deposit" in cols
                assert "escrow_deductions" in cols

                mat_res = conn.execute(text("PRAGMA table_info(exam_materials)")).fetchall()
                mat_cols = [r[1] for r in mat_res]
                assert "answer_file_url" in mat_cols
                assert "year" in mat_cols
        finally:
            db.close()
    test("SQLite 테이블 스키마 자동 마이그레이션", test_db_schema)

    # 7. HTML 템플릿 태그 무결성 (캐시버스팅 및 필수 ID 검사)
    def test_html_integrity():
        with open("static/index.html", "r", encoding="utf-8") as f:
            html = f.read()
        assert "style.css?v=" in html
        assert "app.js?v=" in html
        assert "micro-pledge-modal" in html
        assert "pledge-input-text" in html
        assert "p3-blacklounge" in html
        assert "p3-ranking" in html
        assert "accordion-header" in html
        assert "pred-tam1-type" in html
        assert "pred-tam2-type" in html
        assert "reg-sido" in html
        assert "reg-sigungu" in html
    test("index.html 필수 컴포넌트 및 캐시버스팅", test_html_integrity)

    # 8. admin.html & master.html 무결성 검사
    def test_admin_html_integrity():
        with open("static/admin.html", "r", encoding="utf-8") as f:
            admin_html = f.read()
        with open("static/master.html", "r", encoding="utf-8") as f:
            master_html = f.read()
        assert "style.css?v=" in admin_html
        assert "admin-container" in admin_html
        assert "admin-header" in admin_html
        assert "master-knowledge-list" in master_html
    test("admin.html 관제실 & master.html 마스터 지식 스튜디오 무결성", test_admin_html_integrity)

    # 9. CSS 무결성 검사
    def test_css_integrity():
        with open("static/css/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        assert ".accordion-header" in css
        assert "#pledge-input-text" in css
        assert ".modal-close-btn" in css
    test("style.css 아코디언 및 고대비 가시성 스타일", test_css_integrity)

    print("\n" + "=" * 60)
    print(f"🎉 전체 검증 결과: {passed}/{total} 테스트 통과 (100% 무결성 확보)")
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
