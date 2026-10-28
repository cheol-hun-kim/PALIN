# 👵 PALIN SILVER-MATE (시니어 만능 구독 비서 및 효도 관제 시스템)

PALIN OS 생태계의 핵심 축인 **SILVER-MATE**는 중장년·노년층의 디지털 장벽을 허무는 **양면(Two-Sided) 대칭형 안부 관제 시스템**입니다.

---

## 🚀 실시간 접속 URL (로컬 및 배포 공통)

1. **부모님용 'Zero-UI' 초대형 포털**:
   - URL: [`/silver/senior-home`](/silver/senior-home) 또는 [`/silvermate/senior-home`](/silvermate/senior-home)
   - 특징: 메뉴 탐색 배제, 화면 전체 4대 초대형 카드 버튼 (`🎙️ 말씀하세요`, `📸 찍으세요`, `💝 자식에게 부탁`, `🚨 응급 SOS`), 보이스피싱 전신 적색 경보 화면(Zero-Touch 방어망), TTS 음성 환영 인사.

2. **자녀용 원격 안부 관제탑 (Control Tower)**:
   - URL: [`/silver/guardian`](/silver/guardian) 또는 [`/silvermate/guardian`](/silvermate/guardian)
   - 특징: 비침습적 라이프시그널(기상 시간, 아침 복약 확인, 걸음 수, 배터리), "시간 날 때 전화해~" 비동기 Ping 인박스, 원격 대행 승인 큐(KTX 예매 1초 결제, 재산세 고지서 납부, 장보기 승인), 보이스피싱 실시간 경보 연동.

3. **추억의 AI 디지털 사진관 & 스마트 액자**:
   - URL: [`/silver/photo-album`](/silver/photo-album) 또는 [`/silvermate/photo-album`](/silvermate/photo-album)
   - 특징: 4대 클러스터(`👨‍👩‍👧‍👦 사람별`, `⛰️ 장소·여행별`, `🌺 주제별`, `✨ AI 사진정리`), 말로 찾는 음성 검색, 전체화면 디지털 액자 슬라이드쇼 및 사진 설명 음성(TTS) 읽어주기.

---

## 📂 파일 구성
- `senior-home.html`: 부모님용 Zero-UI 프론트엔드 인터페이스
- `guardian.html`: 자녀용 안부 모니터링 및 대행 승인 관제 인터페이스
- `photo-album.html`: 시니어 맞춤형 디지털 액자 및 AI 사진첩 인터페이스
- 백엔드 엔드포인트: `app/main.py` (`/api/silver/...`, `/silver/...`)
