// --- 전역 상태 관리 ---
let currentStudent = null;
let activeTab = "page1"; // page1: 생활, page2: 학습, page3: 매칭
let activeSubTabPage2 = "chat"; // chat, predict, archive
let activeSubTabPage3 = "qa"; // qa, matching
let activeRole = "student"; // student, tutor (과외선생 모드)
let timerInterval = null;
let timerSeconds = 0;
let activeSessionId = null;
let isTimerRunning = false;
let isDistracted = false; 
let chatHistory = []; // AI 챗봇 대화 기록

// --- 앱 초기화 및 로딩 ---
let UNIVERSITY_DEPARTMENTS = {};
const DEFAULT_REGIONS_DATA = {
  "서울특별시": [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구"
  ],
  "경기도": [
    "성남시 분당구",
    "성남시 수정구",
    "성남시 중원구",
    "수원시 영통구",
    "수원시 팔달구",
    "수원시 장안구",
    "수원시 권선구",
    "용인시 수지구",
    "용인시 기흥구",
    "용인시 처인구",
    "고양시 일산동구",
    "고양시 일산서구",
    "고양시 덕양구",
    "안양시 동안구",
    "안양시 만안구",
    "부천시",
    "화성시",
    "평택시",
    "남양주시",
    "안산시 상록구",
    "안산시 단원구",
    "시흥시",
    "파주시",
    "김포시",
    "의정부시",
    "광주시",
    "하남시",
    "광명시",
    "군포시",
    "양주시",
    "오산시",
    "이천시",
    "안성시",
    "구리시",
    "의왕시",
    "포천시",
    "양평군",
    "여주시",
    "동두천시",
    "가평군",
    "연천군"
  ],
  "인천광역시": [
    "중구",
    "동구",
    "미추홀구",
    "연수구",
    "남동구",
    "부평구",
    "계양구",
    "서구",
    "강화군",
    "옹진군"
  ],
  "부산광역시": [
    "중구",
    "서구",
    "동구",
    "영도구",
    "부산진구",
    "동래구",
    "남구",
    "북구",
    "해운대구",
    "사하구",
    "금정구",
    "강서구",
    "연제구",
    "수영구",
    "사상구",
    "기장군"
  ],
  "대구광역시": [
    "중구",
    "동구",
    "서구",
    "남구",
    "북구",
    "수성구",
    "달서구",
    "달성군",
    "군위군"
  ],
  "광주광역시": [
    "동구",
    "서구",
    "남구",
    "북구",
    "광산구"
  ],
  "대전광역시": [
    "동구",
    "중구",
    "서구",
    "유성구",
    "대덕구"
  ],
  "울산광역시": [
    "중구",
    "남구",
    "동구",
    "북구",
    "울주군"
  ],
  "세종특별자치시": [
    "세종특별자치시"
  ],
  "강원특별자치도": [
    "춘천시",
    "원주시",
    "강릉시",
    "동해시",
    "태백시",
    "속초시",
    "삼척시",
    "홍천군",
    "횡성군",
    "영월군",
    "평창군",
    "정선군",
    "철원군",
    "화천군",
    "양구군",
    "인제군",
    "고성군",
    "양양군"
  ],
  "충청북도": [
    "청주시 상당구",
    "청주시 서원구",
    "청주시 흥덕구",
    "청주시 청원구",
    "충주시",
    "제천시",
    "보은군",
    "옥천군",
    "영동군",
    "증평군",
    "진천군",
    "괴산군",
    "음성군",
    "단양군"
  ],
  "충청남도": [
    "천안시 동남구",
    "천안시 서북구",
    "공주시",
    "보령시",
    "아산시",
    "서산시",
    "논산시",
    "계룡시",
    "당진시",
    "금산군",
    "부여군",
    "서천군",
    "청양군",
    "홍성군",
    "예산군",
    "태안군"
  ],
  "전북특별자치도": [
    "전주시 완산구",
    "전주시 덕진구",
    "군산시",
    "익산시",
    "정읍시",
    "남원시",
    "김제시",
    "완주군",
    "진안군",
    "무주군",
    "장수군",
    "임실군",
    "순창군",
    "고창군",
    "부안군"
  ],
  "전라남도": [
    "목포시",
    "여수시",
    "순천시",
    "나주시",
    "광양시",
    "담양군",
    "곡성군",
    "구례군",
    "고흥군",
    "보성군",
    "화순군",
    "장흥군",
    "강진군",
    "해남군",
    "영암군",
    "무안군",
    "함평군",
    "영광군",
    "장성군",
    "완도군",
    "진도군",
    "신안군"
  ],
  "경상북도": [
    "포항시 남구",
    "포항시 북구",
    "경주시",
    "김천시",
    "안동시",
    "구미시",
    "영주시",
    "영천시",
    "상주시",
    "문경시",
    "경산시",
    "의성군",
    "청송군",
    "영양군",
    "영덕군",
    "청도군",
    "고령군",
    "성주군",
    "칠곡군",
    "예천군",
    "봉화군",
    "울진군",
    "울릉군"
  ],
  "경상남도": [
    "창원시 의창구",
    "창원시 성산구",
    "창원시 마산합포구",
    "창원시 마산회원구",
    "창원시 진해구",
    "진주시",
    "통영시",
    "사천시",
    "김해시",
    "밀양시",
    "거제시",
    "양산시",
    "의령군",
    "함안군",
    "창녕군",
    "고성군",
    "남해군",
    "하동군",
    "산청군",
    "함양군",
    "거창군",
    "합천군"
  ],
  "제주특별자치도": [
    "제주시",
    "서귀포시"
  ]
};
let REGIONS_DATA = DEFAULT_REGIONS_DATA;
const DEFAULT_HIGHSCHOOLS_DATA = [
  {
    "name": "휘문고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "자사고"
  },
  {
    "name": "중동고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "자사고"
  },
  {
    "name": "단국대학교사범대학부속고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "경기고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "개포고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "압구정고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "중산고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "숙명여자고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "은광여자고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "진선여자고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "경기여자고등학교",
    "sido": "서울특별시",
    "sigungu": "강남구",
    "type": "일반고"
  },
  {
    "name": "서울고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "일반고"
  },
  {
    "name": "상문고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "일반고"
  },
  {
    "name": "세화고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "자사고"
  },
  {
    "name": "세화여자고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "자사고"
  },
  {
    "name": "반포고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "일반고"
  },
  {
    "name": "서초고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "일반고"
  },
  {
    "name": "동덕여자고등학교",
    "sido": "서울특별시",
    "sigungu": "서초구",
    "type": "일반고"
  },
  {
    "name": "보성고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "자사고"
  },
  {
    "name": "배명고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "일반고"
  },
  {
    "name": "잠실고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "일반고"
  },
  {
    "name": "잠신고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "일반고"
  },
  {
    "name": "정신여자고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "일반고"
  },
  {
    "name": "창덕여자고등학교",
    "sido": "서울특별시",
    "sigungu": "송파구",
    "type": "일반고"
  },
  {
    "name": "한영고등학교",
    "sido": "서울특별시",
    "sigungu": "강동구",
    "type": "일반고"
  },
  {
    "name": "한영외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "강동구",
    "type": "외고"
  },
  {
    "name": "배재고등학교",
    "sido": "서울특별시",
    "sigungu": "강동구",
    "type": "자사고"
  },
  {
    "name": "명일여자고등학교",
    "sido": "서울특별시",
    "sigungu": "강동구",
    "type": "일반고"
  },
  {
    "name": "강서고등학교",
    "sido": "서울특별시",
    "sigungu": "양천구",
    "type": "일반고"
  },
  {
    "name": "양정고등학교",
    "sido": "서울특별시",
    "sigungu": "양천구",
    "type": "자사고"
  },
  {
    "name": "신목고등학교",
    "sido": "서울특별시",
    "sigungu": "양천구",
    "type": "일반고"
  },
  {
    "name": "목동고등학교",
    "sido": "서울특별시",
    "sigungu": "양천구",
    "type": "일반고"
  },
  {
    "name": "진명여자고등학교",
    "sido": "서울특별시",
    "sigungu": "양천구",
    "type": "일반고"
  },
  {
    "name": "대일고등학교",
    "sido": "서울특별시",
    "sigungu": "강서구",
    "type": "일반고"
  },
  {
    "name": "명덕고등학교",
    "sido": "서울특별시",
    "sigungu": "강서구",
    "type": "일반고"
  },
  {
    "name": "명덕외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "강서구",
    "type": "외고"
  },
  {
    "name": "구리고등학교",
    "sido": "서울특별시",
    "sigungu": "구로구",
    "type": "일반고"
  },
  {
    "name": "구로고등학교",
    "sido": "서울특별시",
    "sigungu": "구로구",
    "type": "일반고"
  },
  {
    "name": "여의도고등학교",
    "sido": "서울특별시",
    "sigungu": "영등포구",
    "type": "일반고"
  },
  {
    "name": "여의도여자고등학교",
    "sido": "서울특별시",
    "sigungu": "영등포구",
    "type": "일반고"
  },
  {
    "name": "장훈고등학교",
    "sido": "서울특별시",
    "sigungu": "영등포구",
    "type": "일반고"
  },
  {
    "name": "숭의여자고등학교",
    "sido": "서울특별시",
    "sigungu": "동작구",
    "type": "일반고"
  },
  {
    "name": "성남고등학교",
    "sido": "서울특별시",
    "sigungu": "동작구",
    "type": "일반고"
  },
  {
    "name": "미림여자고등학교",
    "sido": "서울특별시",
    "sigungu": "관악구",
    "type": "일반고"
  },
  {
    "name": "남강고등학교",
    "sido": "서울특별시",
    "sigungu": "관악구",
    "type": "일반고"
  },
  {
    "name": "서울과학고등학교",
    "sido": "서울특별시",
    "sigungu": "종로구",
    "type": "영재학교"
  },
  {
    "name": "중앙고등학교",
    "sido": "서울특별시",
    "sigungu": "종로구",
    "type": "자사고"
  },
  {
    "name": "경복고등학교",
    "sido": "서울특별시",
    "sigungu": "종로구",
    "type": "일반고"
  },
  {
    "name": "이화여자외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "중구",
    "type": "외고"
  },
  {
    "name": "이화여자고등학교",
    "sido": "서울특별시",
    "sigungu": "중구",
    "type": "자사고"
  },
  {
    "name": "용산고등학교",
    "sido": "서울특별시",
    "sigungu": "용산구",
    "type": "일반고"
  },
  {
    "name": "오산고등학교",
    "sido": "서울특별시",
    "sigungu": "용산구",
    "type": "일반고"
  },
  {
    "name": "한양대학교사범대학부속고등학교",
    "sido": "서울특별시",
    "sigungu": "성동구",
    "type": "자사고"
  },
  {
    "name": "대원외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "광진구",
    "type": "외고"
  },
  {
    "name": "대원고등학교",
    "sido": "서울특별시",
    "sigungu": "광진구",
    "type": "일반고"
  },
  {
    "name": "대원여자고등학교",
    "sido": "서울특별시",
    "sigungu": "광진구",
    "type": "일반고"
  },
  {
    "name": "경희고등학교",
    "sido": "서울특별시",
    "sigungu": "동대문구",
    "type": "자사고"
  },
  {
    "name": "대광고등학교",
    "sido": "서울특별시",
    "sigungu": "동대문구",
    "type": "자사고"
  },
  {
    "name": "중계고등학교",
    "sido": "서울특별시",
    "sigungu": "노원구",
    "type": "일반고"
  },
  {
    "name": "서라벌고등학교",
    "sido": "서울특별시",
    "sigungu": "노원구",
    "type": "일반고"
  },
  {
    "name": "대진고등학교",
    "sido": "서울특별시",
    "sigungu": "노원구",
    "type": "일반고"
  },
  {
    "name": "대진여자고등학교",
    "sido": "서울특별시",
    "sigungu": "노원구",
    "type": "일반고"
  },
  {
    "name": "재현고등학교",
    "sido": "서울특별시",
    "sigungu": "노원구",
    "type": "일반고"
  },
  {
    "name": "선덕고등학교",
    "sido": "서울특별시",
    "sigungu": "도봉구",
    "type": "자사고"
  },
  {
    "name": "정의여자고등학교",
    "sido": "서울특별시",
    "sigungu": "도봉구",
    "type": "일반고"
  },
  {
    "name": "신일고등학교",
    "sido": "서울특별시",
    "sigungu": "강북구",
    "type": "자사고"
  },
  {
    "name": "대일외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "성북구",
    "type": "외고"
  },
  {
    "name": "하나고등학교",
    "sido": "서울특별시",
    "sigungu": "은평구",
    "type": "자사고"
  },
  {
    "name": "숭실고등학교",
    "sido": "서울특별시",
    "sigungu": "은평구",
    "type": "일반고"
  },
  {
    "name": "이화여자대학교사범대학부속이화금란고등학교",
    "sido": "서울특별시",
    "sigungu": "서대문구",
    "type": "자사고"
  },
  {
    "name": "한성고등학교",
    "sido": "서울특별시",
    "sigungu": "서대문구",
    "type": "일반고"
  },
  {
    "name": "서울외국어고등학교",
    "sido": "서울특별시",
    "sigungu": "도봉구",
    "type": "외고"
  },
  {
    "name": "낙생고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "서현고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "분당대진고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "분당중앙고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "분당고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "수내고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "보평고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "판교고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "운중고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "태원고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "이매고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "야탑고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "돌마고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "불곡고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "구미고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "늘푸른고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "송림고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "영덕여자고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "일반고"
  },
  {
    "name": "성남외국어고등학교",
    "sido": "경기도",
    "sigungu": "성남시 분당구",
    "type": "외고"
  },
  {
    "name": "용인한국외국어대학교부설고등학교 (외대부고)",
    "sido": "경기도",
    "sigungu": "용인시 처인구",
    "type": "자사고"
  },
  {
    "name": "수지고등학교",
    "sido": "경기도",
    "sigungu": "용인시 수지구",
    "type": "일반고"
  },
  {
    "name": "풍덕고등학교",
    "sido": "경기도",
    "sigungu": "용인시 수지구",
    "type": "일반고"
  },
  {
    "name": "보정고등학교",
    "sido": "경기도",
    "sigungu": "용인시 기흥구",
    "type": "일반고"
  },
  {
    "name": "동백고등학교",
    "sido": "경기도",
    "sigungu": "용인시 기흥구",
    "type": "일반고"
  },
  {
    "name": "경기과학고등학교",
    "sido": "경기도",
    "sigungu": "수원시 장안구",
    "type": "영재학교"
  },
  {
    "name": "수원외국어고등학교",
    "sido": "경기도",
    "sigungu": "수원시 영통구",
    "type": "외고"
  },
  {
    "name": "유신고등학교",
    "sido": "경기도",
    "sigungu": "수원시 팔달구",
    "type": "일반고"
  },
  {
    "name": "창현고등학교",
    "sido": "경기도",
    "sigungu": "수원시 팔달구",
    "type": "일반고"
  },
  {
    "name": "화성고등학교",
    "sido": "경기도",
    "sigungu": "화성시",
    "type": "일반고"
  },
  {
    "name": "동탄국제고등학교",
    "sido": "경기도",
    "sigungu": "화성시",
    "type": "국제고"
  },
  {
    "name": "신성고등학교",
    "sido": "경기도",
    "sigungu": "안양시 만안구",
    "type": "일반고"
  },
  {
    "name": "안양외국어고등학교",
    "sido": "경기도",
    "sigungu": "안양시 만안구",
    "type": "외고"
  },
  {
    "name": "백영고등학교",
    "sido": "경기도",
    "sigungu": "안양시 동안구",
    "type": "일반고"
  },
  {
    "name": "평촌고등학교",
    "sido": "경기도",
    "sigungu": "안양시 동안구",
    "type": "일반고"
  },
  {
    "name": "고양국제고등학교",
    "sido": "경기도",
    "sigungu": "고양시 일산동구",
    "type": "국제고"
  },
  {
    "name": "고양외국어고등학교",
    "sido": "경기도",
    "sigungu": "고양시 덕양구",
    "type": "외고"
  },
  {
    "name": "백석고등학교",
    "sido": "경기도",
    "sigungu": "고양시 일산동구",
    "type": "일반고"
  },
  {
    "name": "운정고등학교",
    "sido": "경기도",
    "sigungu": "파주시",
    "type": "일반고"
  },
  {
    "name": "청심국제고등학교",
    "sido": "경기도",
    "sigungu": "가평군",
    "type": "국제고"
  },
  {
    "name": "김포외국어고등학교",
    "sido": "경기도",
    "sigungu": "김포시",
    "type": "외고"
  },
  {
    "name": "인천하늘고등학교",
    "sido": "인천광역시",
    "sigungu": "중구",
    "type": "자사고"
  },
  {
    "name": "인천포스코고등학교",
    "sido": "인천광역시",
    "sigungu": "연수구",
    "type": "자사고"
  },
  {
    "name": "인천과학예술영재학교",
    "sido": "인천광역시",
    "sigungu": "연수구",
    "type": "영재학교"
  },
  {
    "name": "인천국제고등학교",
    "sido": "인천광역시",
    "sigungu": "중구",
    "type": "국제고"
  },
  {
    "name": "인천외국어고등학교",
    "sido": "인천광역시",
    "sigungu": "부평구",
    "type": "외고"
  },
  {
    "name": "송도고등학교",
    "sido": "인천광역시",
    "sigungu": "연수구",
    "type": "일반고"
  },
  {
    "name": "인천고등학교",
    "sido": "인천광역시",
    "sigungu": "미추홀구",
    "type": "일반고"
  },
  {
    "name": "제물포고등학교",
    "sido": "인천광역시",
    "sigungu": "중구",
    "type": "일반고"
  },
  {
    "name": "한국과학영재학교",
    "sido": "부산광역시",
    "sigungu": "부산진구",
    "type": "영재학교"
  },
  {
    "name": "부산과학고등학교",
    "sido": "부산광역시",
    "sigungu": "금정구",
    "type": "과학고"
  },
  {
    "name": "해운대고등학교",
    "sido": "부산광역시",
    "sigungu": "해운대구",
    "type": "자사고"
  },
  {
    "name": "부산외국어고등학교",
    "sido": "부산광역시",
    "sigungu": "연제구",
    "type": "외고"
  },
  {
    "name": "부산국제고등학교",
    "sido": "부산광역시",
    "sigungu": "부산진구",
    "type": "국제고"
  },
  {
    "name": "동래고등학교",
    "sido": "부산광역시",
    "sigungu": "동래구",
    "type": "일반고"
  },
  {
    "name": "센텀고등학교",
    "sido": "부산광역시",
    "sigungu": "해운대구",
    "type": "일반고"
  },
  {
    "name": "남성여자고등학교",
    "sido": "부산광역시",
    "sigungu": "중구",
    "type": "일반고"
  },
  {
    "name": "대구과학고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "영재학교"
  },
  {
    "name": "대륜고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "일반고"
  },
  {
    "name": "경신고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "일반고"
  },
  {
    "name": "대구여자고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "일반고"
  },
  {
    "name": "정화여자고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "일반고"
  },
  {
    "name": "능인고등학교",
    "sido": "대구광역시",
    "sigungu": "수성구",
    "type": "일반고"
  },
  {
    "name": "계성고등학교",
    "sido": "대구광역시",
    "sigungu": "서구",
    "type": "자사고"
  },
  {
    "name": "대구외국어고등학교",
    "sido": "대구광역시",
    "sigungu": "중구",
    "type": "외고"
  },
  {
    "name": "광주과학고등학교",
    "sido": "광주광역시",
    "sigungu": "북구",
    "type": "영재학교"
  },
  {
    "name": "광주인성고등학교",
    "sido": "광주광역시",
    "sigungu": "남구",
    "type": "일반고"
  },
  {
    "name": "광덕고등학교",
    "sido": "광주광역시",
    "sigungu": "서구",
    "type": "일반고"
  },
  {
    "name": "숭덕고등학교",
    "sido": "광주광역시",
    "sigungu": "광산구",
    "type": "자사고"
  },
  {
    "name": "살레시오고등학교",
    "sido": "광주광역시",
    "sigungu": "서구",
    "type": "일반고"
  },
  {
    "name": "광주수피아여자고등학교",
    "sido": "광주광역시",
    "sigungu": "남구",
    "type": "일반고"
  },
  {
    "name": "대전과학고등학교",
    "sido": "대전광역시",
    "sigungu": "유성구",
    "type": "영재학교"
  },
  {
    "name": "대전대신고등학교",
    "sido": "대전광역시",
    "sigungu": "서구",
    "type": "자사고"
  },
  {
    "name": "대성고등학교",
    "sido": "대전광역시",
    "sigungu": "중구",
    "type": "자사고"
  },
  {
    "name": "대전외국어고등학교",
    "sido": "대전광역시",
    "sigungu": "유성구",
    "type": "외고"
  },
  {
    "name": "충남고등학교",
    "sido": "대전광역시",
    "sigungu": "서구",
    "type": "일반고"
  },
  {
    "name": "유성고등학교",
    "sido": "대전광역시",
    "sigungu": "유성구",
    "type": "일반고"
  },
  {
    "name": "현대청운고등학교",
    "sido": "울산광역시",
    "sigungu": "동구",
    "type": "자사고"
  },
  {
    "name": "울산과학고등학교",
    "sido": "울산광역시",
    "sigungu": "울주군",
    "type": "과학고"
  },
  {
    "name": "울산외국어고등학교",
    "sido": "울산광역시",
    "sigungu": "북구",
    "type": "외고"
  },
  {
    "name": "학성고등학교",
    "sido": "울산광역시",
    "sigungu": "남구",
    "type": "일반고"
  },
  {
    "name": "우신고등학교",
    "sido": "울산광역시",
    "sigungu": "남구",
    "type": "일반고"
  },
  {
    "name": "세종과학예술영재학교",
    "sido": "세종특별자치시",
    "sigungu": "세종특별자치시",
    "type": "영재학교"
  },
  {
    "name": "세종국제고등학교",
    "sido": "세종특별자치시",
    "sigungu": "세종특별자치시",
    "type": "국제고"
  },
  {
    "name": "한솔고등학교",
    "sido": "세종특별자치시",
    "sigungu": "세종특별자치시",
    "type": "일반고"
  },
  {
    "name": "도담고등학교",
    "sido": "세종특별자치시",
    "sigungu": "세종특별자치시",
    "type": "일반고"
  },
  {
    "name": "아름고등학교",
    "sido": "세종특별자치시",
    "sigungu": "세종특별자치시",
    "type": "일반고"
  },
  {
    "name": "민족사관고등학교 (민사고)",
    "sido": "강원특별자치도",
    "sigungu": "횡성군",
    "type": "자사고"
  },
  {
    "name": "강원과학고등학교",
    "sido": "강원특별자치도",
    "sigungu": "원주시",
    "type": "과학고"
  },
  {
    "name": "강원외국어고등학교",
    "sido": "강원특별자치도",
    "sigungu": "양구군",
    "type": "외고"
  },
  {
    "name": "춘천고등학교",
    "sido": "강원특별자치도",
    "sigungu": "춘천시",
    "type": "일반고"
  },
  {
    "name": "강릉고등학교",
    "sido": "강원특별자치도",
    "sigungu": "강릉시",
    "type": "일반고"
  },
  {
    "name": "충북과학고등학교",
    "sido": "충청북도",
    "sigungu": "청주시 상당구",
    "type": "과학고"
  },
  {
    "name": "청주외국어고등학교",
    "sido": "충청북도",
    "sigungu": "청주시 흥덕구",
    "type": "외고"
  },
  {
    "name": "청주고등학교",
    "sido": "충청북도",
    "sigungu": "청주시 서원구",
    "type": "일반고"
  },
  {
    "name": "세광고등학교",
    "sido": "충청북도",
    "sigungu": "청주시 서원구",
    "type": "일반고"
  },
  {
    "name": "충주고등학교",
    "sido": "충청북도",
    "sigungu": "충주시",
    "type": "일반고"
  },
  {
    "name": "공주사범대학부설고등학교 (공주사대부고)",
    "sido": "충청남도",
    "sigungu": "공주시",
    "type": "일반고(전국단위)"
  },
  {
    "name": "한일고등학교",
    "sido": "충청남도",
    "sigungu": "공주시",
    "type": "일반고(전국단위)"
  },
  {
    "name": "충남과학고등학교",
    "sido": "충청남도",
    "sigungu": "공주시",
    "type": "과학고"
  },
  {
    "name": "충남삼성고등학교",
    "sido": "충청남도",
    "sigungu": "아산시",
    "type": "자사고"
  },
  {
    "name": "충남외국어고등학교",
    "sido": "충청남도",
    "sigungu": "아산시",
    "type": "외고"
  },
  {
    "name": "천안고등학교",
    "sido": "충청남도",
    "sigungu": "천안시 동남구",
    "type": "일반고"
  },
  {
    "name": "북일고등학교",
    "sido": "충청남도",
    "sigungu": "천안시 동남구",
    "type": "자사고"
  },
  {
    "name": "상산고등학교",
    "sido": "전북특별자치도",
    "sigungu": "전주시 완산구",
    "type": "자사고"
  },
  {
    "name": "전북과학고등학교",
    "sido": "전북특별자치도",
    "sigungu": "익산시",
    "type": "과학고"
  },
  {
    "name": "전북외국어고등학교",
    "sido": "전북특별자치도",
    "sigungu": "군산시",
    "type": "외고"
  },
  {
    "name": "전주고등학교",
    "sido": "전북특별자치도",
    "sigungu": "전주시 완산구",
    "type": "일반고"
  },
  {
    "name": "군산고등학교",
    "sido": "전북특별자치도",
    "sigungu": "군산시",
    "type": "일반고"
  },
  {
    "name": "전남과학고등학교",
    "sido": "전라남도",
    "sigungu": "나주시",
    "type": "과학고"
  },
  {
    "name": "광양제철고등학교",
    "sido": "전라남도",
    "sigungu": "광양시",
    "type": "자사고"
  },
  {
    "name": "전남외국어고등학교",
    "sido": "전라남도",
    "sigungu": "나주시",
    "type": "외고"
  },
  {
    "name": "순천고등학교",
    "sido": "전라남도",
    "sigungu": "순천시",
    "type": "일반고"
  },
  {
    "name": "목포고등학교",
    "sido": "전라남도",
    "sigungu": "목포시",
    "type": "일반고"
  },
  {
    "name": "포항제철고등학교",
    "sido": "경상북도",
    "sigungu": "포항시 남구",
    "type": "자사고"
  },
  {
    "name": "김천고등학교",
    "sido": "경상북도",
    "sigungu": "김천시",
    "type": "자사고"
  },
  {
    "name": "경북과학고등학교",
    "sido": "경상북도",
    "sigungu": "포항시 남구",
    "type": "과학고"
  },
  {
    "name": "경북외국어고등학교",
    "sido": "경상북도",
    "sigungu": "구미시",
    "type": "외고"
  },
  {
    "name": "안동고등학교",
    "sido": "경상북도",
    "sigungu": "안동시",
    "type": "일반고"
  },
  {
    "name": "경남과학고등학교",
    "sido": "경상남도",
    "sigungu": "진주시",
    "type": "과학고"
  },
  {
    "name": "경남외국어고등학교",
    "sido": "경상남도",
    "sigungu": "양산시",
    "type": "외고"
  },
  {
    "name": "김해외국어고등학교",
    "sido": "경상남도",
    "sigungu": "김해시",
    "type": "외고"
  },
  {
    "name": "창원과학고등학교",
    "sido": "경상남도",
    "sigungu": "창원시 의창구",
    "type": "과학고"
  },
  {
    "name": "마산고등학교",
    "sido": "경상남도",
    "sigungu": "창원시 마산합포구",
    "type": "일반고"
  },
  {
    "name": "진주고등학교",
    "sido": "경상남도",
    "sigungu": "진주시",
    "type": "일반고"
  },
  {
    "name": "거제고등학교",
    "sido": "경상남도",
    "sigungu": "거제시",
    "type": "일반고"
  },
  {
    "name": "제주과학고등학교",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "과학고"
  },
  {
    "name": "제주외국어고등학교",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "외고"
  },
  {
    "name": "오현고등학교",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "일반고"
  },
  {
    "name": "대기고등학교",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "일반고"
  },
  {
    "name": "제주일고 (제주제일고등학교)",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "일반고"
  },
  {
    "name": "서귀포고등학교",
    "sido": "제주특별자치도",
    "sigungu": "서귀포시",
    "type": "일반고"
  },
  {
    "name": "신성여자고등학교",
    "sido": "제주특별자치도",
    "sigungu": "제주시",
    "type": "일반고"
  }
];
let HIGHSCHOOLS_DATA = DEFAULT_HIGHSCHOOLS_DATA;

document.addEventListener("DOMContentLoaded", async () => {
    initPALINThemeEngine();
    
    // 1. 내장 정적 지역 및 고등학교 데이터로 즉시 렌더링 (0.001초 즉시 렌더링 보장)
    populateSidoOptions("reg-sido");
    populateSidoOptions("edit-sido");
    filterHighSchoolsBySido("reg-sido", "highschool-datalist");
    filterHighSchoolsBySido("edit-sido", "edit-highschool-datalist");
    
    // 2. 비동기 데이터 로딩을 안전하게 병렬 처리
    try {
        await Promise.all([
            fetchUnivData(),
            loadRegionsData(),
            loadHighSchoolsData()
        ]);
    } catch (err) {
        console.error("Initial data loading error:", err);
    }
    
    checkAuth();
    setupEventListeners();
    setupDistractionDetection();
    
    document.getElementById("header-streak-badge")?.addEventListener("click", openStreakModal);
    document.getElementById("theme-toggle-btn")?.addEventListener("click", togglePALINTheme);
});

async function loadRegionsData() {
    try {
        const res = await fetch("/api/data/regions");
        if (res.ok) {
            REGIONS_DATA = await res.json();
            populateSidoOptions("reg-sido");
            populateSidoOptions("edit-sido");
        }
    } catch (e) { console.warn("Regions load error:", e); }
}

function populateSidoOptions(selectId) {
    const el = document.getElementById(selectId);
    if (!el) return;
    const currentVal = el.value;
    const sidos = Object.keys(REGIONS_DATA).length > 0 ? Object.keys(REGIONS_DATA) : Object.keys(DEFAULT_REGIONS_DATA);
    
    let html = '<option value="" disabled' + (!currentVal ? ' selected' : '') + '>시/도 선택</option>';
    sidos.forEach(sido => {
        const isSelected = sido === currentVal ? ' selected' : '';
        html += `<option value="${sido}"${isSelected}>${sido}</option>`;
    });
    el.innerHTML = html;
}

function onSidoChange(sidoSelectId, sigunguSelectId, defaultSigungu = "") {
    const sido = document.getElementById(sidoSelectId)?.value;
    const sigunguEl = document.getElementById(sigunguSelectId);
    if (!sigunguEl || !sido) return;
    
    const sigungus = REGIONS_DATA[sido] || DEFAULT_REGIONS_DATA[sido] || [];
    let html = '<option value="" disabled' + (!defaultSigungu ? ' selected' : '') + '>시/군/구 선택</option>';
    sigungus.forEach(sg => {
        const isSelected = sg === defaultSigungu ? " selected" : "";
        html += `<option value="${sg}"${isSelected}>${sg}</option>`;
    });
    sigunguEl.innerHTML = html;
}

async function loadHighSchoolsData() {
    try {
        const res = await fetch("/api/data/high-schools");
        if (res.ok) {
            HIGHSCHOOLS_DATA = await res.json();
            filterHighSchoolsBySido("reg-sido", "highschool-datalist");
            filterHighSchoolsBySido("edit-sido", "edit-highschool-datalist");
        }
    } catch (e) { console.warn("High schools load error:", e); }
}

// 🏫 선택된 시/도에 따라 고등학교 선택지(Datalist) 실시간 자동 필터링
function filterHighSchoolsBySido(sidoSelectId, datalistId) {
    const sido = document.getElementById(sidoSelectId)?.value;
    const dl = document.getElementById(datalistId);
    if (!dl || !HIGHSCHOOLS_DATA || HIGHSCHOOLS_DATA.length === 0) return;

    dl.innerHTML = "";
    
    let matchedSchools = [];
    let otherSpecialSchools = [];

    if (sido) {
        // 해당 시/도 소속 고등학교
        matchedSchools = HIGHSCHOOLS_DATA.filter(hs => (hs.sido === sido || hs.region === sido));
        // 전국 단위 자사/특목/영재고 중 타지역
        otherSpecialSchools = HIGHSCHOOLS_DATA.filter(hs => (hs.sido !== sido && hs.region !== sido) && (hs.type === "자사고" || hs.type === "영재고" || hs.type === "과학고" || hs.type === "과고" || hs.type === "외고" || hs.type === "국제고" || (hs.type && hs.type.includes("전국"))));
    } else {
        matchedSchools = HIGHSCHOOLS_DATA;
    }

    matchedSchools.forEach(hs => {
        const rName = hs.sido || hs.region || '지역';
        const sType = hs.type || '고교';
        const loc = hs.sigungu ? ` (${hs.sigungu})` : '';
        dl.innerHTML += `<option value="${hs.name}">[${rName} ${sType}] ${hs.name}${loc}</option>`;
    });

    otherSpecialSchools.forEach(hs => {
        const rName = hs.sido || hs.region || '전국';
        const sType = hs.type || '특목고';
        dl.innerHTML += `<option value="${hs.name}">[전국 ${sType}] ${hs.name} (${rName})</option>`;
    });
}

// 📱 아코디언 드롭다운 토글 제어 엔진
function toggleAccordion(bodyId, iconId) {
    const body = document.getElementById(bodyId);
    const icon = document.getElementById(iconId);
    if (!body) return;
    
    if (body.style.display === "none" || !body.style.display) {
        body.style.display = "block";
        if (icon) icon.style.transform = "rotate(180deg)";
    } else {
        body.style.display = "none";
        if (icon) icon.style.transform = "rotate(0deg)";
    }
}

// PALIN OS 타임라인 기반 자동 테마 전환 엔진 (06시~21시: 데이 모드, 21시~06시: 딥 블랙 야간 모드)
function initPALINThemeEngine() {
    const hour = new Date().getHours();
    const savedTheme = localStorage.getItem("palinTheme");
    const isDay = savedTheme === "day" || (savedTheme === null && hour >= 6 && hour < 21);
    if (isDay) {
        document.body.classList.add("day-mode");
    } else {
        document.body.classList.remove("day-mode");
    }
    updateThemeToggleIcon(isDay);
}

function updateThemeToggleIcon(isDay) {
    const iconEl = document.getElementById("theme-toggle-icon");
    if (iconEl) {
        iconEl.innerText = isDay ? "☀️" : "🌙";
    }
}

function togglePALINTheme() {
    document.body.classList.toggle("day-mode");
    const isDay = document.body.classList.contains("day-mode");
    localStorage.setItem("palinTheme", isDay ? "day" : "night");
    updateThemeToggleIcon(isDay);
}

async function fetchUnivData() {
    try {
        const res = await fetch("/api/univ-data");
        if (res.ok) {
            UNIVERSITY_DEPARTMENTS = await res.json();
            // 회원가입 모달 셀렉트 연결
            setupUnivDeptSelectors("reg-target-univ", "reg-target-dept");
            setupUnivDeptSelectors("reg-baseline-univ", "reg-baseline-dept");

            updateStudentUnivSelectors();
        } else {
            console.error("Failed to load university list.");
        }
    } catch (e) {
        console.error("Error fetching university data:", e);
    }
}

function updateStudentUnivSelectors() {
    if (!currentStudent || !UNIVERSITY_DEPARTMENTS || Object.keys(UNIVERSITY_DEPARTMENTS).length === 0) return;

    let targetUniv = "", targetDept = "";
    if (currentStudent.target_univ) {
        const idx = currentStudent.target_univ.indexOf(" ");
        if (idx !== -1) {
            targetUniv = currentStudent.target_univ.substring(0, idx).trim();
            targetDept = currentStudent.target_univ.substring(idx + 1).trim();
        } else {
            targetUniv = currentStudent.target_univ.trim();
        }
    }

    let baselineUniv = "", baselineDept = "";
    if (currentStudent.baseline_univ) {
        const idx = currentStudent.baseline_univ.indexOf(" ");
        if (idx !== -1) {
            baselineUniv = currentStudent.baseline_univ.substring(0, idx).trim();
            baselineDept = currentStudent.baseline_univ.substring(idx + 1).trim();
        } else {
            baselineUniv = currentStudent.baseline_univ.trim();
        }
    }

    const univKeys = Object.keys(UNIVERSITY_DEPARTMENTS);
    if (!targetUniv || !findMatchingUniv(targetUniv, univKeys)) {
        targetUniv = "가천대학교";
        targetDept = targetDept || "의예과";
    }
    if (!baselineUniv || !findMatchingUniv(baselineUniv, univKeys)) {
        baselineUniv = "연세대학교";
        baselineDept = baselineDept || "의예과";
    }

    setupUnivDeptSelectors("tutor-up-univ", "tutor-up-major", targetUniv, targetDept);
}

// --- 사용자 세션/인증 확인 ---
function checkAuth() {
    const studentId = localStorage.getItem("studentId");
    if (studentId && !isNaN(parseInt(studentId))) {
        fetchStudentInfo(parseInt(studentId));
    } else {
        currentStudent = null;
        localStorage.removeItem("studentId");
        clearAllSensitiveUI();
        showOverlay("register-overlay");
    }
}

function clearAllSensitiveUI() {
    const headerName = document.getElementById("header-student-name");
    if (headerName) headerName.innerText = "로그인 필요";
    const headerPoints = document.getElementById("header-points");
    if (headerPoints) headerPoints.innerText = "0 P";
    const targetUniv = document.getElementById("banner-target-univ");
    if (targetUniv) targetUniv.innerText = "로그인 필요";
    const baselineUniv = document.getElementById("banner-baseline-univ");
    if (baselineUniv) baselineUniv.innerText = "로그인 필요";
}

function showOverlay(id) {
    document.querySelectorAll(".loader-overlay").forEach(el => el.style.display = "none");
    const overlay = document.getElementById(id);
    if (overlay) {
        overlay.style.display = "flex";
    }
}

function hideOverlay(id) {
    const overlay = document.getElementById(id);
    if (overlay) {
        overlay.style.display = "none";
    }
}

// --- 공부 타이머 백그라운드 & 화면 꺼짐 방지(Wake Lock) 모듈 ---
let timerStartTime = null;
let wakeLockSentinel = null;

async function requestScreenWakeLock() {
    try {
        if ('wakeLock' in navigator) {
            wakeLockSentinel = await navigator.wakeLock.request('screen');
            wakeLockSentinel.addEventListener('release', () => {
                wakeLockSentinel = null;
            });
        }
    } catch (err) {
        console.log("Wake Lock not supported or denied:", err);
    }
}

function releaseScreenWakeLock() {
    if (wakeLockSentinel) {
        wakeLockSentinel.release().catch(() => {});
        wakeLockSentinel = null;
    }
}

function setupDistractionDetection() {
    document.addEventListener("visibilitychange", () => {
        if (!isTimerRunning) return;

        if (document.visibilityState === "visible") {
            // 화면 복귀 시 실제 경과 시간(Date.now - timerStartTime)으로 즉시 오차 없이 동기화
            if (timerStartTime) {
                const currentElapsed = Math.floor((Date.now() - timerStartTime) / 1000);
                if (currentElapsed >= 0) {
                    timerSeconds = currentElapsed;
                    updateTimerDisplay(timerSeconds);
                }
            }
            // 다시 활성화되면 Wake Lock 재요청
            requestScreenWakeLock();
        }
    });
}

function updateTimerDisplay(seconds) {
    const circle = document.getElementById("timer-circle");
    if (!circle) return;
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');
    circle.innerText = `${hrs}:${mins}:${secs}`;
}


// --- API 연동 함수들 ---

async function fetchStudentInfo(studentId) {
    try {
        const res = await fetch(`/api/student/${studentId}`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            if (res.status === 403) {
                alert(`⚠️ ${err.detail || "원장님에 의해 이용이 정지/퇴거된 계정입니다. 학원 집무실로 문의해 주세요."}`);
                localStorage.removeItem("studentId");
                showOverlay("register-overlay");
            }
            return;
        }
        currentStudent = await res.json();
        
        // 인증 성공 → 즉시 오버레이 완전 차단 및 UI 즉시 렌더링
        hideOverlay("register-overlay");
        updateHeaderUI();
        updateTargetBanner();
        updateStudentUnivSelectors();

        // 부가 데이터는 병렬 비동기(Promise.allSettled)로 즉각 백그라운드 로드
        Promise.allSettled([
            fetch(`/api/student/${studentId}/parent`).then(r => r.ok ? r.json() : null).then(p => { if (p) currentStudent.parent = p; }),
            fetchLeagueStatus(studentId),
            fetchNotices(),
            fetchMicroLeague(studentId),
            renderAdmissionCalendar(),
            loadPage1Data(),
            loadPage2Data(),
            loadPage3Data()
        ]).catch(err => console.warn("Background fetch warning:", err));
    } catch (e) {
        console.warn("fetchStudentInfo warning:", e);
        // 네트워크 일시 오류 시 이미 로그인된 세션을 날리지 않음
        hideOverlay("register-overlay");
    }
}

// 1. 회원가입 제출
async function handleRegister(e) {
    e.preventDefault();
    const targetUniv = document.getElementById("reg-target-univ").value;
    let targetDept = document.getElementById("reg-target-dept").value;
    if (targetDept === "__CUSTOM__") {
        targetDept = (document.getElementById("reg-target-dept-custom")?.value || "").trim();
    }

    const baselineUniv = document.getElementById("reg-baseline-univ").value;
    let baselineDept = document.getElementById("reg-baseline-dept").value;
    if (baselineDept === "__CUSTOM__") {
        baselineDept = (document.getElementById("reg-baseline-dept-custom")?.value || "").trim();
    }
    
    if (!targetUniv || !targetDept || !baselineUniv || !baselineDept) {
        alert("목표 대학/학과 및 마지노선 대학/학과를 모두 선택 또는 직접 입력해 주세요.");
        return;
    }

    const termsCheck = document.getElementById("reg-terms-check");
    const privacyCheck = document.getElementById("reg-privacy-check");
    if ((termsCheck && !termsCheck.checked) || (privacyCheck && !privacyCheck.checked)) {
        alert("서비스 이용약관 및 개인정보 수집 동의서에 모두 체크해 주셔야 가입이 완료됩니다.");
        return;
    }

    const sidoVal = document.getElementById("reg-sido")?.value || "경기도";
    const sigunguVal = document.getElementById("reg-sigungu")?.value || "성남시 분당구";
    const fullRegion = `${sidoVal} ${sigunguVal}`.trim();
    const schoolName = document.getElementById("reg-school")?.value || "낙생고등학교";

    const payload = {
        email: document.getElementById("reg-email").value,
        name: document.getElementById("reg-name").value,
        phone: document.getElementById("reg-phone").value,
        grade: parseInt(document.getElementById("reg-grade").value),
        region: fullRegion,
        high_school: schoolName,
        target_univ: `${targetUniv} ${targetDept}`,
        baseline_univ: `${baselineUniv} ${baselineDept}`,
        parent_name: document.getElementById("reg-pname").value,
        parent_phone: document.getElementById("reg-pphone").value,
        referred_by: (document.getElementById("reg-referred-by")?.value || "").trim().toUpperCase() || null
    };

    try {
        const res = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || "등록 실패");
            return;
        }
        const student = await res.json();
        localStorage.setItem("studentId", student.id);
        fetchStudentInfo(student.id);
        
        // 가입 완료 축하 팝업 후 학생증 발급 모달 오픈 안내
        setTimeout(() => {
            if (confirm("🎉 가입을 진심으로 축하합니다! 2027학번 목표 대학 가상 학생증을 지금 바로 발급하시겠습니까?")) {
                openStudentCardModal();
            }
        }, 500);
    } catch (e) {
        alert("서버 연결 실패");
    }
}

function toggleLoginForm() {
    const regForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const toggleArea = document.getElementById("login-toggle-area");
    
    if (!regForm || !loginForm) return;

    if (loginForm.style.display === "none" || !loginForm.style.display) {
        regForm.style.display = "none";
        if (toggleArea) toggleArea.style.display = "none";
        loginForm.style.display = "block";
        document.getElementById("login-email")?.focus();
    } else {
        loginForm.style.display = "none";
        regForm.style.display = "block";
        if (toggleArea) toggleArea.style.display = "block";
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const emailInput = document.getElementById("login-email");
    const email = (emailInput?.value || "").trim();
    if (!email) {
        alert("가입하신 이메일 주소를 입력해 주세요.");
        return;
    }
    
    const submitBtn = e.target.querySelector("button[type='submit']");
    const originalBtnText = submitBtn ? submitBtn.innerText : "로그인";
    if (submitBtn) {
        submitBtn.innerText = "로그인 확인 중...";
        submitBtn.disabled = true;
    }

    try {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email })
        });
        
        if (!res.ok) {
            let errorMsg = "로그인 실패";
            try {
                const err = await res.json();
                errorMsg = err.detail || errorMsg;
            } catch (jsonErr) {
                errorMsg = `서버 응답 오류 (HTTP ${res.status})`;
            }
            alert(errorMsg);
            if (res.status === 404) {
                // 가입되지 않은 이메일인 경우 친절하게 회원가입 폼으로 전환
                toggleLoginForm();
                const regEmail = document.getElementById("reg-email");
                if (regEmail) regEmail.value = email;
            }
            return;
        }
        
        const student = await res.json();
        localStorage.setItem("studentId", student.id);
        
        // 즉시 오버레이 완전 차단
        hideOverlay("register-overlay");
        
        // 학생 정보 및 화면 데이터 즉시 로드 (팝업 없이 자연스럽게 대시보드 진입)
        await fetchStudentInfo(student.id);
    } catch (e) {
        console.error("Login error:", e);
        alert(`⚠️ 서버 연결 실패: 인터넷 연결 또는 서버 상태를 확인해 주세요. (${e.message || e})`);
    } finally {
        if (submitBtn) {
            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        }
    }
}

// 학부모 결제 토글
async function togglePremium() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/student/${currentStudent.id}/toggle-premium`, { method: "POST" });
        const parent = await res.json();
        currentStudent.parent = parent;
        updateHeaderUI();
        alert(parent.is_premium_subscribed ? "학부모 유료 결제가 활성화되었습니다! (미션 포인트 2배, AI 챗봇 대화 무제한)" : "유료 결제가 비활성화되었습니다.");
        loadPage1Data();
    } catch (e) {
        console.error(e);
    }
}


// --- UI 업데이트 헬퍼 ---

function calculateDDay(dateStr) {
    let targetDateStr = (dateStr || "").trim();
    if (!targetDateStr || targetDateStr === "undefined" || targetDateStr === "null" || targetDateStr === "D-DAY" || targetDateStr.startsWith("D-")) {
        targetDateStr = "2026-11-19"; // 2027학년도 본 수능일 기본값
    }
    try {
        const parts = targetDateStr.split("-");
        let y = 2026, m = 11, d = 19;
        if (parts.length === 3) {
            y = parseInt(parts[0], 10);
            m = parseInt(parts[1], 10);
            d = parseInt(parts[2], 10);
        }
        const target = new Date(y, m - 1, d, 0, 0, 0);
        const today = new Date();
        const now = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0);
        
        const diffTime = target.getTime() - now.getTime();
        const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays > 0) return `D-${diffDays}`;
        if (diffDays === 0) return "D-DAY";
        return `D+${Math.abs(diffDays)}`;
    } catch (e) {
        return "D-DAY";
    }
}

function getMedicalSymbolIcon(symbolKey) {
    switch (symbolKey) {
        case "MED": return "⚕️"; // 의대 (아스클레피오스의 지팡이)
        case "DENT": return "🦷"; // 치대
        case "PHARM": return "💊"; // 약대
        case "KMED": return "🌿"; // 한의대
        case "VET": return "🐾"; // 수의대
        default: return "🦁"; // 일반 대학
    }
}

function updateHeaderUI() {
    if (!currentStudent) return;
    
    // 🪙 무료 성실 포인트
    const headerPoints = document.getElementById("header-points");
    if (headerPoints) headerPoints.innerText = `${currentStudent.current_points || 0} P`;
    const mypagePoints = document.getElementById("mypage-points");
    if (mypagePoints) mypagePoints.innerText = `${(currentStudent.current_points || 0).toLocaleString()} P`;
    
    // 💎 유료 PALIN 캐시
    const cashEl = document.getElementById("header-cash");
    if (cashEl) cashEl.innerText = `${(currentStudent.paid_cash || 0).toLocaleString()}`;
    const mypageCash = document.getElementById("mypage-cash");
    if (mypageCash) mypageCash.innerText = `${(currentStudent.paid_cash || 0).toLocaleString()}`;
    const cashModalBal = document.getElementById("cash-modal-balance");
    if (cashModalBal) cashModalBal.innerText = `${(currentStudent.paid_cash || 0).toLocaleString()}`;

    // 🎟️ 무료 리포트 티켓
    const ticketEl = document.getElementById("referral-ticket-count");
    if (ticketEl) ticketEl.innerText = `${currentStudent.free_report_tickets || 0}`;
    const mypageTickets = document.getElementById("mypage-tickets");
    if (mypageTickets) mypageTickets.innerText = `${currentStudent.free_report_tickets || 0}`;

    // 🔗 내 추천인 코드
    const refCodeEl = document.getElementById("referral-my-code");
    if (refCodeEl) refCodeEl.innerText = currentStudent.referral_code || `PL-${String(currentStudent.id).padStart(4, '0')}`;

    const studentNameEl = document.getElementById("header-student-name");
    if (studentNameEl) studentNameEl.innerText = `${currentStudent.name} 학생`;
    
    // 🔥 듀오링고 불꽃 (Streak) 렌더링
    const streakEl = document.getElementById("header-streak-count");
    if (streakEl) {
        const count = currentStudent.streak_days || 0;
        streakEl.innerText = `연속 ${count}일`;
    }

    // 마이페이지 모달 정보 갱신
    const fullname = document.getElementById("mypage-student-fullname");
    if (fullname) fullname.innerText = `${currentStudent.name} 학생`;
    const sub = document.getElementById("mypage-student-sub");
    const gradeText = currentStudent.grade === 4 ? "N수생" : currentStudent.grade === 0 ? "기타" : `${currentStudent.grade}학년`;
    if (sub) sub.innerText = `${currentStudent.high_school || "학교미설정"} ${gradeText} | ${currentStudent.region || "지역미설정"}`;

    // 메인화면 미션 라벨 업데이트 (이모지 없이 깔끔하게 표기)
    const wakeLabel = document.getElementById("mission-wakeup-label");
    if (wakeLabel) wakeLabel.innerText = `기상 미션 (${currentStudent.wake_target_time || "06:30"})`;
    const sleepLabel = document.getElementById("mission-sleep-label");
    if (sleepLabel) sleepLabel.innerText = `취침 미션 (${currentStudent.sleep_target_time || "23:30"})`;

    const premiumBtn = document.getElementById("premium-toggle-btn");
    if (premiumBtn) {
        if (currentStudent.parent && currentStudent.parent.is_premium_subscribed) {
            premiumBtn.innerText = "👑 프리미엄 회원 (부모 연동 완료)";
            premiumBtn.style.background = "linear-gradient(135deg, #fbbf24, #d97706)";
        } else {
            premiumBtn.innerText = "⚡ 프리미엄 구독 상태 전환 (부모결제)";
            premiumBtn.style.background = "";
        }
    }
}

async function fetchLeagueStatus(studentId) {
    try {
        const res = await fetch(`/api/league/${studentId}`);
        if (res.ok) {
            const data = await res.json();
            const badges = [document.getElementById("header-league-badge"), document.getElementById("mypage-league-badge")];
            badges.forEach(badge => {
                if (badge) {
                    badge.className = `league-badge league-${data.league_tier.toLowerCase()}`;
                    badge.innerText = `${data.league_tier} (${data.point_multiplier}x)`;
                }
            });
            const ticketCountEl = document.getElementById("golden-ticket-count");
            if (ticketCountEl) {
                ticketCountEl.innerText = `${data.golden_tickets_count}장`;
            }
        }
    } catch (e) {
        console.error("League status fetch error:", e);
    }
}

function updateTargetBanner() {
    if (!currentStudent) return;
    const targetUnivEl = document.getElementById("banner-target-univ");
    const baselineUnivEl = document.getElementById("banner-baseline-univ");
    if (targetUnivEl) targetUnivEl.innerText = currentStudent.target_univ || "미설정";
    if (baselineUnivEl) baselineUnivEl.innerText = currentStudent.baseline_univ || "미설정";

    // D-Day 계산 렌더링
    const ddayEl = document.getElementById("banner-dday");
    const ddayTitleEl = document.getElementById("banner-dday-title");
    if (ddayEl) ddayEl.innerText = calculateDDay(currentStudent.dday_date || "2026-11-19");
    if (ddayTitleEl) ddayTitleEl.innerText = currentStudent.dday_title || "2027 수능";

    // 🌲 포레스트 목표 대학 로고 & 엠블럼 렌더링
    const emblemEl = document.getElementById("target-symbol-emblem");
    const logoNameEl = document.getElementById("target-logo-name");
    if (emblemEl) emblemEl.innerText = getMedicalSymbolIcon(currentStudent.medical_symbol);
    if (logoNameEl) logoNameEl.innerText = `${currentStudent.target_univ || "목표 대학"} 수호 중`;
}

// 💥 포레스트 균열(Crack) 애니메이션 및 딴짓 타격감 발동
function triggerLogoCrackEffect() {
    const box = document.getElementById("univ-target-box");
    if (box) {
        box.classList.add("crack-active");
        setTimeout(() => {
            box.classList.remove("crack-active");
        }, 2000);
    }
}

async function fetchNotices() {
    try {
        const res = await fetch("/api/notices");
        if (res.ok) {
            const notices = await res.json();
            const banner = document.getElementById("notice-banner-container");
            const textEl = document.getElementById("notice-banner-text");
            if (banner && textEl && notices.length > 0) {
                const latest = notices[0];
                textEl.innerHTML = `<strong>[${latest.category}]</strong> ${latest.title} - ${latest.content}`;
                banner.style.display = "flex";
            }
        }
    } catch (e) {
        console.warn("Notice load:", e);
    }
}

async function fetchMicroLeague(studentId) {
    try {
        const res = await fetch(`/api/micro-league/${studentId}`);
        if (res.ok) {
            const data = await res.json();
            const titleEl = document.getElementById("micro-league-title");
            const contentEl = document.getElementById("micro-league-content");
            if (titleEl) titleEl.innerText = data.region_title;
            if (contentEl) {
                let html = `<div style="display:flex; flex-direction:column; gap:4px;">`;
                data.region_rankings.forEach((r, idx) => {
                    const highlight = r.is_me ? "color: #fcd34d; font-weight: 800;" : "";
                    html += `<div style="display:flex; justify-content:space-between; ${highlight}"><span>${idx + 1}위 ${r.name} (${r.school})</span><span>+${r.score}점</span></div>`;
                });
                html += `</div>`;
                contentEl.innerHTML = html;
            }
        }
    } catch (e) {
        console.warn("Micro league load:", e);
    }
}

function renderAdmissionCalendar() {
    const calendarData = [
        { title: "2026학년도 3월 전국연합학력평가", date: "2026-03-26", dday: calculateDDay("2026-03-26"), cat: "모의고사" },
        { title: "2026학년도 6월 모의평가 (평가원 출제)", date: "2026-06-04", dday: calculateDDay("2026-06-04"), cat: "평가원" },
        { title: "2026학년도 9월 모의평가 (수능 바로미터)", date: "2026-09-02", dday: calculateDDay("2026-09-02"), cat: "평가원" },
        { title: "2027학년도 대입 수시모집 원서접수", date: "2026-09-07", dday: calculateDDay("2026-09-07"), cat: "원서접수" },
        { title: "2027학년도 대학수학능력시험 (본 수능)", date: "2026-11-19", dday: calculateDDay("2026-11-19"), cat: "수능시험" },
        { title: "2027학년도 대입 정시모집 원서접수", date: "2026-12-28", dday: calculateDDay("2026-12-28"), cat: "원서접수" }
    ];

    const listEl = document.getElementById("admission-calendar-list");
    if (!listEl) return;
    listEl.innerHTML = "";
    calendarData.forEach(item => {
        const isUrgent = item.dday.startsWith("D-") && parseInt(item.dday.replace("D-", "")) <= 30;
        const ddayColor = isUrgent ? "background: #ef4444; color: white;" : "background: #3b82f6; color: white;";
        listEl.innerHTML += `
            <div class="calendar-card">
                <div>
                    <div class="calendar-item-title" style="font-weight: 800; font-size: 0.88rem;">${item.title}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px;">📅 ${item.date} (${item.cat})</div>
                </div>
                <div class="calendar-dday" style="${ddayColor}">
                    ${item.dday}
                </div>
            </div>
        `;
    });
}

function openMyPageModal() {
    updateHeaderUI();
    if (currentStudent) {
        document.getElementById("edit-high-school").value = currentStudent.high_school || "";
        
        // 지역 (시도 / 시군구 분리 바인딩)
        const curRegion = currentStudent.region || "서울특별시 강남구";
        const rParts = curRegion.split(" ");
        let rawSido = rParts[0] || "서울특별시";
        let curSigungu = rParts.slice(1).join(" ") || "강남구";
        
        // 17개 시도 키값과 정확 매칭
        const allSidos = Object.keys(DEFAULT_REGIONS_DATA);
        const curSido = allSidos.find(s => s === rawSido || s.startsWith(rawSido) || rawSido.startsWith(s.slice(0, 2))) || "서울특별시";
        
        // 1. 시도 옵션 렌더링 후 값 설정
        populateSidoOptions("edit-sido");
        const sidoEl = document.getElementById("edit-sido");
        if (sidoEl) {
            sidoEl.value = curSido;
            onSidoChange("edit-sido", "edit-sigungu", curSigungu);
            filterHighSchoolsBySido("edit-sido", "edit-highschool-datalist");
        }
        
        document.getElementById("edit-grade").value = currentStudent.grade !== undefined ? currentStudent.grade : "3";
        document.getElementById("edit-medical-symbol").value = currentStudent.medical_symbol || "GENERAL";
        document.getElementById("edit-dday-title").value = currentStudent.dday_title || "2027 수능";
        document.getElementById("edit-dday-date").value = currentStudent.dday_date || "2026-11-19";
        document.getElementById("edit-wake-time").value = currentStudent.wake_target_time || "06:30";
        document.getElementById("edit-sleep-time").value = currentStudent.sleep_target_time || "23:30";

        // 금융 인질 에스크로 잔액 조회
        fetchEscrowStatus(currentStudent.id);

        // 대학 드롭다운 초기화
        setupUnivDeptSelectors("edit-target-univ-select", "edit-target-dept-select");
        setupUnivDeptSelectors("edit-baseline-univ-select", "edit-baseline-dept-select");
    }
    document.getElementById("mypage-modal").style.display = "flex";
}

function closeMyPageModal() {
    document.getElementById("mypage-modal").style.display = "none";
}

async function saveStudentProfileSettings() {
    if (!currentStudent) return;
    const highSchool = document.getElementById("edit-high-school").value.trim();
    const editSido = document.getElementById("edit-sido")?.value || "경기도";
    const editSigungu = document.getElementById("edit-sigungu")?.value || "성남시 분당구";
    const region = `${editSido} ${editSigungu}`.trim();
    const grade = parseInt(document.getElementById("edit-grade").value);
    const medicalSymbol = document.getElementById("edit-medical-symbol").value;
    const ddayTitle = document.getElementById("edit-dday-title").value.trim();
    const ddayDate = document.getElementById("edit-dday-date").value;
    const wakeTime = document.getElementById("edit-wake-time").value;
    const sleepTime = document.getElementById("edit-sleep-time").value;

    const tUniv = document.getElementById("edit-target-univ-select")?.value;
    let tDept = document.getElementById("edit-target-dept-select")?.value;
    if (tDept === "__CUSTOM__") {
        tDept = (document.getElementById("edit-target-dept-custom")?.value || "").trim();
    }

    const bUniv = document.getElementById("edit-baseline-univ-select")?.value;
    let bDept = document.getElementById("edit-baseline-dept-select")?.value;
    if (bDept === "__CUSTOM__") {
        bDept = (document.getElementById("edit-baseline-dept-custom")?.value || "").trim();
    }

    const targetUniv = (tUniv && tDept) ? `${tUniv} ${tDept}` : currentStudent.target_univ;
    const baselineUniv = (bUniv && bDept) ? `${bUniv} ${bDept}` : currentStudent.baseline_univ;

    try {
        const res = await fetch("/api/student/profile", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                high_school: highSchool,
                region: region,
                grade: grade,
                medical_symbol: medicalSymbol,
                dday_title: ddayTitle,
                dday_date: ddayDate,
                target_univ: targetUniv,
                baseline_univ: baselineUniv,
                wake_target_time: wakeTime,
                sleep_target_time: sleepTime
            })
        });
        if (!res.ok) {
            alert("프로필 및 미션 시간 변경 실패");
            return;
        }
        const updated = await res.json();
        currentStudent = updated;
        updateHeaderUI();
        updateTargetBanner();
        alert("✅ 목표 대학 및 기상/취침 미션 설정이 성공적으로 변경되었습니다.");
    } catch (e) {
        console.error("saveStudentProfileSettings error:", e);
        alert("설정 저장 중 오류가 발생했습니다.");
    }
}

function openFeedbackModal() {
    closeMyPageModal();
    document.getElementById("feedback-modal").style.display = "flex";
}

function closeFeedbackModal() {
    document.getElementById("feedback-modal").style.display = "none";
}

async function handleSendFeedback(e) {
    e.preventDefault();
    const category = document.getElementById("feedback-category").value;
    const content = document.getElementById("feedback-content").value.trim();
    if (!content) {
        alert("내용을 입력해주세요.");
        return;
    }

    try {
        const res = await fetch("/api/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent ? currentStudent.id : null,
                user_email: currentStudent ? currentStudent.email : null,
                category: category,
                content: content
            })
        });
        if (!res.ok) {
            alert("건의 제출 실패");
            return;
        }
        alert("✅ 건의사항이 정상 접수되었습니다. 개발팀에 전달되었습니다. 감사합니다!");
        document.getElementById("feedback-content").value = "";
        closeFeedbackModal();
    } catch (e) {
        console.error("handleSendFeedback error:", e);
        alert("건의 제출 중 오류가 발생했습니다.");
    }
}

function logoutStudent() {
    if (confirm("로그아웃 하시겠습니까? 계정이 초기화되고 신규 가입/로그인 창으로 이동합니다.")) {
        localStorage.removeItem("studentId");
        sessionStorage.clear();
        currentStudent = null;
        if ('caches' in window) {
            caches.keys().then(names => {
                for (let name of names) caches.delete(name);
            });
        }
        location.reload();
    }
}

async function generateGoldenTicket() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/referral/generate-ticket/${currentStudent.id}`, { method: "POST" });
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || "골든 티켓 발급 실패");
            return;
        }
        const ticket = await res.json();
        const display = document.getElementById("ticket-display");
        display.style.display = "block";
        display.innerText = `🎫 생성된 골든 티켓: ${ticket.code}`;
        alert(`🎉 골든 티켓이 생성되었습니다!\n코드: ${ticket.code}\n친구에게 전달해 50P + 5% 영구 복리 혜택을 함께 누리세요!`);
        fetchLeagueStatus(currentStudent.id);
    } catch (e) {
        alert("골든 티켓 발급 실패");
    }
}

async function claimGoldenTicket() {
    if (!currentStudent) return;
    const input = document.getElementById("claim-ticket-input");
    const code = input.value.trim();
    if (!code) {
        alert("골든 티켓 코드를 입력해 주세요.");
        return;
    }
    try {
        const res = await fetch("/api/referral/claim-ticket", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                ticket_code: code
            })
        });
        const result = await res.json();
        if (!res.ok) {
            alert(result.detail || "티켓 등록 실패");
            return;
        }
        alert(result.message);
        input.value = "";
        fetchStudentInfo(currentStudent.id);
    } catch (e) {
        alert("티켓 등록 처리 실패");
    }
}

function updateTargetBanner() {
    if (!currentStudent) return;
    document.getElementById("banner-target-univ").innerText = currentStudent.target_univ || "미설정";
    document.getElementById("banner-baseline-univ").innerText = currentStudent.baseline_univ || "미설정";
}


// --- 탭 컨트롤 및 네비게이션 ---

function switchTab(tabId) {
    activeTab = tabId;
    document.querySelectorAll(".page-view").forEach(el => el.style.display = "none");
    document.getElementById(tabId).style.display = "block";

    document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
    document.querySelector(`.nav-item[data-tab="${tabId}"]`).classList.add("active");
}

function switchSubTabPage2(subTab) {
    activeSubTabPage2 = subTab;
    document.querySelectorAll(".subtab-view-p2").forEach(el => el.style.display = "none");
    document.getElementById(`p2-${subTab}`).style.display = "block";

    document.querySelectorAll("#p2-tabs .tab-btn").forEach(el => el.classList.remove("active"));
    document.querySelector(`#p2-tabs .tab-btn[data-sub="${subTab}"]`).classList.add("active");

    if (subTab === "predict") {
        updateStudentUnivSelectors();
        if (typeof loadUniversityList === 'function') {
            loadUniversityList();
        }
        if (typeof updateUnivDisplay === 'function') {
            updateUnivDisplay();
        }
    } else if (subTab === "archive") {
        loadExamMaterials();
    }
}

function switchSubTabPage3(subTab) {
    activeSubTabPage3 = subTab;
    document.querySelectorAll(".subtab-view-p3").forEach(el => el.style.display = "none");
    const targetEl = document.getElementById(`p3-${subTab}`);
    if (targetEl) targetEl.style.display = "block";

    document.querySelectorAll("#p3-tabs .tab-btn").forEach(el => el.classList.remove("active"));
    document.querySelector(`#p3-tabs .tab-btn[data-sub="${subTab}"]`)?.classList.add("active");

    if (subTab === "ranking") {
        loadMicroRankings();
    } else if (subTab === "blacklounge") {
        loadBlackLoungePosts();
    }
}

// 신규: 과외선생님 ⇄ 학생 역할 전환 토글
function switchRole(role) {
    activeRole = role;
    document.querySelectorAll(".role-toggle-btn").forEach(el => el.classList.remove("active"));
    document.querySelector(`.role-toggle-btn[data-role="${role}"]`).classList.add("active");
    
    // 역할별 화면 노출 제어
    if (role === "tutor") {
        document.getElementById("tutor-only-views").style.display = "block";
        document.getElementById("student-only-views").style.display = "none";
        
        // 내 선생님 프로필 정보 바인딩
        if (currentStudent && currentStudent.tutor_profile) {
            const tp = currentStudent.tutor_profile;
            document.getElementById("tutor-my-univ-badge").innerText = tp.univ_emblem || `🎓 ${tp.university}`;
            document.getElementById("tutor-my-school-badge").innerText = tp.high_school_emblem || `🏫 ${tp.high_school_type || '출신고'}`;
            document.getElementById("edit-tutor-bio").value = tp.bio || "";
            document.getElementById("edit-tutor-link").value = tp.contact_link || "";

            // 🎯 원장 승인 상태 실시간 반영
            const statusBadge = document.getElementById("tutor-verify-status-badge");
            if (statusBadge) {
                if (tp.is_verified) {
                    statusBadge.innerHTML = `<span style="color: #10b981; font-weight: 800; background: rgba(16, 185, 129, 0.15); padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3);">✅ 인증 승인완료</span>`;
                } else {
                    statusBadge.innerHTML = `<span style="color: #f59e0b; font-weight: 800; background: rgba(245, 158, 11, 0.15); padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);">⏳ 원장 승인심사중...</span>`;
                }
            }
        }
    } else {
        document.getElementById("tutor-only-views").style.display = "none";
        document.getElementById("student-only-views").style.display = "block";
    }
}


// --- 이벤트 리스너 바인딩 ---
function setupEventListeners() {
    document.getElementById("register-form").addEventListener("submit", handleRegister);
    document.getElementById("login-form")?.addEventListener("submit", handleLogin);
    document.getElementById("tutor-upgrade-form")?.addEventListener("submit", upgradeStudentToTutor);

    // 📊 정시 예측 점수 실시간 강제 제한 (100 / 50 초과 원천 차단)
    ['pred-kor', 'pred-math', 'pred-eng', 'pred-tam1', 'pred-tam2'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            ['input', 'keyup', 'change', 'blur'].forEach(evt => {
                input.addEventListener(evt, () => {
                    if (input.value !== "" && Number(input.value) > 100) input.value = 100;
                    if (input.value !== "" && Number(input.value) < 0) input.value = 0;
                });
            });
        }
    });
    const histInput = document.getElementById('pred-hist');
    if (histInput) {
        ['input', 'keyup', 'change', 'blur'].forEach(evt => {
            histInput.addEventListener(evt, () => {
                if (histInput.value !== "" && Number(histInput.value) > 50) histInput.value = 50;
                if (histInput.value !== "" && Number(histInput.value) < 0) histInput.value = 0;
            });
        });
    }
    
    document.querySelectorAll(".nav-item").forEach(item => {
        item.addEventListener("click", () => {
            switchTab(item.getAttribute("data-tab"));
        });
    });

    document.querySelectorAll("#p2-tabs .tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            switchSubTabPage2(btn.getAttribute("data-sub"));
        });
    });

    document.querySelectorAll("#p3-tabs .tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            switchSubTabPage3(btn.getAttribute("data-sub"));
        });
    });

    // 신규: 과외선생님 역할 토글 이벤트 바인딩
    document.querySelectorAll(".role-toggle-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            switchRole(btn.getAttribute("data-role"));
        });
    });
}


// ==========================================
// 1페이지: 생활관리 동작
// ==========================================

async function loadPage1Data() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/study/report/${currentStudent.id}`);
        const report = await res.json();
        document.getElementById("report-study-hours").innerText = `${report.total_study_hours}시간`;
        document.getElementById("report-mission-rate").innerText = `${report.mission_success_rate}%`;
        document.getElementById("report-total-sessions").innerText = `${report.total_sessions}회`;

        const mRes = await fetch(`/api/mission/logs/${currentStudent.id}`);
        const logs = await mRes.json();
        const listContainer = document.getElementById("recent-mission-logs");
        listContainer.innerHTML = "";
        
        if (logs.length === 0) {
            listContainer.innerHTML = "<div style='color: var(--text-secondary); font-size: 0.82rem;'>최근 수행된 미션이 없습니다.</div>";
        } else {
            logs.forEach(log => {
                const dateStr = new Date(log.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                const statusColor = log.status === "SUCCESS" ? "var(--color-success)" : "var(--color-danger)";
                listContainer.innerHTML += `
                    <div class="mission-row" style="font-size: 0.82rem; padding: 6px 0;">
                        <span style="font-weight:600;">[${log.mission_type === "WAKEUP" ? "기상" : "취침"}]</span>
                        <span style="color: var(--text-secondary);">${dateStr}</span>
                        <span style="color: ${statusColor}; font-weight:700;">${log.status === "SUCCESS" ? "성공" : "실패(경고발송)"}</span>
                    </div>
                `;
            });
        }

        loadTimetable();
        await updateDailyMissionUI();
    } catch (e) {
        console.error(e);
    }
}

async function updateDailyMissionUI() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/mission/status/${currentStudent.id}`);
        if (res.ok) {
            const data = await res.json();
            const wakeupBtn = document.getElementById("btn-mission-wakeup");
            const sleepBtn = document.getElementById("btn-mission-sleep");
            if (wakeupBtn) {
                if (data.wakeup_done) {
                    wakeupBtn.innerText = "✅ 오늘 완료";
                    wakeupBtn.style.opacity = "0.65";
                    wakeupBtn.onclick = () => alert("오늘의 기상 미션은 이미 성공 인증을 완료하셨습니다. (1일 1회)");
                } else {
                    wakeupBtn.innerText = "성공인증";
                    wakeupBtn.style.opacity = "1.0";
                    wakeupBtn.onclick = () => verifyMission('WAKEUP');
                }
            }
            if (sleepBtn) {
                if (data.sleep_done) {
                    sleepBtn.innerText = "✅ 오늘 완료";
                    sleepBtn.style.opacity = "0.65";
                    sleepBtn.onclick = () => alert("오늘의 취침 미션은 이미 성공 인증을 완료하셨습니다. (1일 1회)");
                } else {
                    sleepBtn.innerText = "성공인증";
                    sleepBtn.style.opacity = "1.0";
                    sleepBtn.onclick = () => verifyMission('SLEEP');
                }
            }
        }
    } catch (e) {
        console.error(e);
    }
}

// === 🗓️ 시간표 과목 퀵버튼 & 원터치 등록 엔진 ===
let currentQuickSubject = "수학";
let currentQuickDuration = 2.0; // 기본 2시간

function setQuickSubject(subject, btnEl) {
    currentQuickSubject = subject;
    
    // 1. 버튼 액티브 스타일 즉시 갱신
    document.querySelectorAll(".quick-sub-btn").forEach(btn => {
        btn.classList.remove("active");
        btn.style.background = "#334155";
        btn.style.color = "#cbd5e1";
    });
    if (btnEl) {
        btnEl.classList.add("active");
        btnEl.style.background = "#6366f1";
        btnEl.style.color = "#ffffff";
    }
    
    // 2. 상단 라벨 변경
    updateQuickHeaderLabel();
    
    // 3. 하단 폼 계획명 입력창에 자동 반영
    const planTitleInput = document.getElementById("plan-title");
    if (planTitleInput) {
        planTitleInput.value = `${subject} 집중 학습`;
    }
}

function setQuickDuration(hours, btnEl) {
    currentQuickDuration = parseFloat(hours);
    
    document.querySelectorAll(".quick-dur-btn").forEach(btn => {
        btn.classList.remove("active");
        btn.classList.add("btn-secondary");
        btn.style.background = "";
        btn.style.color = "";
    });
    if (btnEl) {
        btnEl.classList.remove("btn-secondary");
        btnEl.classList.add("active");
        btnEl.style.background = "#6366f1";
        btnEl.style.color = "#ffffff";
    }
    
    updateQuickHeaderLabel();
    syncPlanEndTime();
}

function updateQuickHeaderLabel() {
    const labelEl = document.getElementById("quick-subject-selected");
    if (labelEl) {
        const durText = currentQuickDuration === 1.0 ? "1시간" : currentQuickDuration === 1.5 ? "1.5시간" : currentQuickDuration === 2.0 ? "2시간" : `${currentQuickDuration}시간`;
        labelEl.innerText = `[${currentQuickSubject}] ${durText}`;
    }
}

function syncPlanEndTime() {
    const startInput = document.getElementById("plan-start");
    const endInput = document.getElementById("plan-end");
    if (!startInput || !endInput) return;
    
    const startVal = startInput.value || "09:00";
    const parts = startVal.split(":");
    let h = parseInt(parts[0], 10);
    let m = parseInt(parts[1], 10);
    
    let totalMinutes = h * 60 + m + Math.round(currentQuickDuration * 60);
    let endH = Math.floor(totalMinutes / 60);
    let endM = totalMinutes % 60;
    if (endH > 24) { endH = 24; endM = 0; }
    
    endInput.value = `${String(endH).padStart(2, '0')}:${String(endM).padStart(2, '0')}`;
}

function openTimePicker(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (typeof input.showPicker === 'function') {
        try {
            input.showPicker();
        } catch (e) {
            input.focus();
        }
    } else {
        input.focus();
    }
}

async function handleTimetableGridClick(dayIndex, event) {
    if (!currentStudent) {
        alert("로그인이 필요합니다.");
        return;
    }
    
    // 삭제 버튼이나 기존 블록 클릭 시 중복 추가 방지
    if (event.target.closest(".timetable-block")) return;
    
    const col = event.currentTarget;
    const rect = col.getBoundingClientRect();
    const clickY = event.clientY - rect.top; // 컬럼 내부 Y좌표 (0 ~ 540px)
    
    // 30px = 1시간 (06:00 ~ 24:00 총 18시간)
    let startHourFloat = 6 + (clickY / 30);
    let startHour = Math.floor(startHourFloat);
    let startMin = Math.floor((startHourFloat - startHour) * 60);
    // 30분 단위로 스냅(Snap)
    startMin = startMin < 30 ? 0 : 30;
    if (startHour < 6) startHour = 6;
    if (startHour >= 24) startHour = 23;
    
    let durationMin = Math.round(currentQuickDuration * 60);
    let totalEndMinutes = (startHour * 60 + startMin) + durationMin;
    let endHour = Math.floor(totalEndMinutes / 60);
    let endMin = totalEndMinutes % 60;
    if (endHour > 24) {
        endHour = 24;
        endMin = 0;
    }
    
    const startTimeStr = `${String(startHour).padStart(2, '0')}:${String(startMin).padStart(2, '0')}`;
    const endTimeStr = `${String(endHour).padStart(2, '0')}:${String(endMin).padStart(2, '0')}`;
    const titleStr = `${currentQuickSubject || '자습'} 집중 학습`;
    
    // 하단 폼 입력값도 동기화
    const daySelect = document.getElementById("plan-day");
    const startInput = document.getElementById("plan-start-time") || document.getElementById("plan-start");
    const endInput = document.getElementById("plan-end-time") || document.getElementById("plan-end");
    const titleInput = document.getElementById("plan-title");
    if (daySelect) daySelect.value = String(dayIndex);
    if (startInput) startInput.value = startTimeStr;
    if (endInput) endInput.value = endTimeStr;
    if (titleInput) titleInput.value = titleStr;
    
    // 즉시 시간표 블록 추가
    try {
        const res = await fetch("/api/planner/block", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                day_of_week: dayIndex,
                start_time: startTimeStr,
                end_time: endTimeStr,
                title: titleStr
            })
        });
        if (res.ok) {
            await loadTimetable();
        }
    } catch (e) {
        console.error("Grid click add block error:", e);
    }
}

// === 📅 타이머 요일별 맞춤 할 일 필터 엔진 ===
let allPlannerBlocksCache = [];
let currentTimerSelectedDay = null; // null이면 오늘 요일

function getTodayDayIndex() {
    // JS getDay(): 0(일), 1(월), 2(화), 3(수), 4(목), 5(금), 6(토)
    // 앱 기준: 0(월), 1(화), 2(수), 3(목), 4(금), 5(토), 6(일)
    const jsDay = new Date().getDay();
    return jsDay === 0 ? 6 : jsDay - 1;
}

function filterTimerScheduleByDay(dayIndex, btnEl) {
    currentTimerSelectedDay = dayIndex;
    
    // 버튼 액티브 스타일 갱신
    document.querySelectorAll(".timer-day-btn").forEach(btn => {
        btn.classList.remove("active");
        btn.classList.add("btn-secondary");
        btn.style.background = "#334155";
        btn.style.color = "#cbd5e1";
    });
    if (btnEl) {
        btnEl.classList.remove("btn-secondary");
        btnEl.classList.add("active");
        btnEl.style.background = "#6366f1";
        btnEl.style.color = "#ffffff";
    }
    
    // 상단 라벨 갱신
    const dayNames = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"];
    const labelEl = document.getElementById("timer-selected-day-label");
    if (labelEl) {
        if (dayIndex === 'all') {
            labelEl.innerText = "전체 요일";
        } else {
            const todayIdx = getTodayDayIndex();
            labelEl.innerText = dayIndex === todayIdx ? `오늘 (${dayNames[dayIndex]})` : dayNames[dayIndex];
        }
    }
    
    // 셀렉트 박스 갱신
    populateTimerSelect();
}

function populateTimerSelect() {
    const timerSelect = document.getElementById("timer-schedule-select");
    if (!timerSelect) return;
    
    const dayNames = ["월", "화", "수", "목", "금", "토", "일"];
    timerSelect.innerHTML = "<option value='none'>직접 자유 공부하기</option>";
    
    const targetDay = currentTimerSelectedDay === null ? getTodayDayIndex() : currentTimerSelectedDay;
    
    let filteredBlocks = allPlannerBlocksCache;
    if (targetDay !== 'all') {
        filteredBlocks = allPlannerBlocksCache.filter(b => b.day_of_week === targetDay);
    }
    
    if (filteredBlocks.length === 0 && targetDay !== 'all') {
        timerSelect.innerHTML += `<option disabled value="">${dayNames[targetDay]}요일에 등록된 시간표 계획이 없습니다</option>`;
    } else {
        filteredBlocks.forEach(block => {
            const dayPrefix = targetDay === 'all' ? `[${dayNames[block.day_of_week]}] ` : '';
            timerSelect.innerHTML += `<option value="${block.id}" data-title="${block.title}">${dayPrefix}${block.title} (${block.start_time}~${block.end_time})</option>`;
        });
    }
}

async function loadTimetable() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/planner/blocks/${currentStudent.id}`);
        const blocks = await res.json();
        allPlannerBlocksCache = blocks || [];
        
        const dayColumns = [
            document.getElementById("col-day-0"),
            document.getElementById("col-day-1"),
            document.getElementById("col-day-2"),
            document.getElementById("col-day-3"),
            document.getElementById("col-day-4"),
            document.getElementById("col-day-5"),
            document.getElementById("col-day-6")
        ];
        
        dayColumns.forEach((col, dayIdx) => {
            if (col) {
                // 06:00 ~ 24:00 (18시간) 전체를 덮는 18개 명시적 격자 라인 생성 (총 540px)
                let gridLinesHtml = '';
                for (let h = 0; h < 18; h++) {
                    gridLinesHtml += `<div class="grid-hour-line" style="position:absolute; top:${h*30}px; left:0; right:0; height:30px; border-bottom:1px solid rgba(255,255,255,0.08); pointer-events:none; box-sizing:border-box;"></div>`;
                }
                col.innerHTML = gridLinesHtml;
                // 원터치 터치/클릭 이벤트 등록
                col.onclick = (e) => handleTimetableGridClick(dayIdx, e);
            }
        });

        // 오늘 요일 기본 탭 활성화 및 타이머 셀렉트 채우기
        const todayIdx = getTodayDayIndex();
        const tabs = document.querySelectorAll(".timer-day-btn");
        if (tabs && tabs.length > todayIdx && currentTimerSelectedDay === null) {
            tabs[todayIdx].classList.add("active");
            tabs[todayIdx].style.background = "#6366f1";
            tabs[todayIdx].style.color = "#ffffff";
        }
        populateTimerSelect();

        blocks.forEach((block, index) => {
            const col = dayColumns[block.day_of_week];
            if (!col) return;

            const startParts = block.start_time.split(":");
            const endParts = block.end_time.split(":");
            
            let startHour = parseInt(startParts[0], 10) + (parseInt(startParts[1], 10) || 0)/60;
            let endHour = parseInt(endParts[0], 10) + (parseInt(endParts[1], 10) || 0)/60;
            
            // 06:00 ~ 24:00 범위 보정 (시간표 이탈 방지)
            if (startHour < 6) startHour = 6;
            if (endHour > 24) endHour = 24;
            if (endHour <= startHour) endHour = startHour + 1;
            
            const topPx = Math.max(0, Math.min(510, (startHour - 6) * 30));
            const heightPx = Math.max(22, Math.min(540 - topPx, (endHour - startHour) * 30));
            
            const colorClass = `color-${index % 7}`;

            const blockEl = document.createElement("div");
            blockEl.className = `timetable-block ${colorClass}`;
            blockEl.style.top = `${topPx}px`;
            blockEl.style.height = `${heightPx}px`;
            blockEl.innerHTML = `
                <div class="block-title">${block.title}</div>
                <div class="block-time">${block.start_time}~${block.end_time}</div>
                <button class="btn-delete-block" title="계획 삭제" onclick="deletePlannerBlock(event, ${block.id})">&times;</button>
            `;
            col.appendChild(blockEl);
        });
    } catch (e) {
        console.error("시간표 로드 오류:", e);
    }
}

async function addPlannerBlock(e) {
    if (e && e.preventDefault) e.preventDefault();
    if (!currentStudent) {
        alert("로그인이 필요합니다.");
        return;
    }
    
    const day = parseInt(document.getElementById("plan-day")?.value || "0");
    const start = (document.getElementById("plan-start-time") || document.getElementById("plan-start"))?.value || "09:00";
    const end = (document.getElementById("plan-end-time") || document.getElementById("plan-end"))?.value || "11:30";
    let title = (document.getElementById("plan-title")?.value || "").trim();

    // 계획명이 비어있으면 현재 선택된 퀵과목(예: 수학, 국어, 영어 등)으로 자동 지정
    if (!title) {
        const quickSub = currentQuickSubject || "자습";
        title = `${quickSub} 집중 학습`;
    }

    if (start >= end) {
        alert("종료 시간은 시작 시간보다 늦어야 합니다.");
        return;
    }

    try {
        const res = await fetch("/api/planner/block", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                day_of_week: day,
                start_time: start,
                end_time: end,
                title: title
            })
        });
        if (res.ok) {
            const titleInput = document.getElementById("plan-title");
            if (titleInput) titleInput.value = "";
            await loadTimetable();
        } else {
            const err = await res.json().catch(() => ({}));
            alert(err.detail || "계획 추가 실패");
        }
    } catch (e) {
        console.error("addPlannerBlock error:", e);
        alert("계획 저장 중 통신 오류가 발생했습니다.");
    }
}

async function deletePlannerBlock(e, blockId) {
    e.stopPropagation();
    if (!confirm("해당 계획 시간표를 삭제하시겠습니까?")) return;
    try {
        const res = await fetch(`/api/planner/block/${blockId}`, { method: "DELETE" });
        if (res.ok) {
            loadTimetable();
        }
    } catch (e) {
        console.error(e);
    }
}

async function verifyMission(type, triggerFail = false) {
    if (!currentStudent) return;
    try {
        const payload = {
            student_id: currentStudent.id,
            mission_type: type,
            img_data: triggerFail ? "fail" : "success"
        };
        const res = await fetch("/api/mission/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (!res.ok) {
            alert(result.detail || "미션 인증 오류");
            await updateDailyMissionUI();
            return;
        }
        
        if (result.status === "SUCCESS") {
            alert(`🎉 ${type === 'WAKEUP' ? '기상' : '취침'} 미션 성공! +${result.earned_points}P가 안전하게 적립되었습니다.`);
        } else {
            alert(`⚠️ 미션 인증 실패! 부모님께 안내 메시지가 발송되었습니다. sms_log.txt에서 발송 이력을 확인하세요.`);
        }
        
        currentStudent.current_points = result.current_points;
        updateHeaderUI();
        loadPage1Data();
        await updateDailyMissionUI();
    } catch (e) {
        alert("미션 요청 실패");
    }
}

// 🔒 마이크로 결의 서약 모달 제어
function requestStartTimer() {
    if (isTimerRunning) {
        stopTimerForcefully(false);
        return;
    }
    const modal = document.getElementById("micro-pledge-modal");
    const input = document.getElementById("pledge-input-text");
    if (modal) {
        if (input) input.value = "";
        modal.style.display = "flex";
        setTimeout(() => input?.focus(), 100);
    } else {
        startTimer();
    }
}

function closeMicroPledgeModal() {
    const modal = document.getElementById("micro-pledge-modal");
    if (modal) modal.style.display = "none";
}

async function submitMicroPledge() {
    const input = document.getElementById("pledge-input-text");
    const textVal = (input?.value || "").trim();
    if (!textVal) {
        alert("서약 문구를 입력해 주세요.");
        return;
    }

    if (!currentStudent) {
        alert("로그인이 필요합니다.");
        return;
    }

    try {
        const res = await fetch("/api/timer/pledge", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                pledge_text: textVal
            })
        });

        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || "서약 문구가 일치하지 않습니다.");
            return;
        }

        closeMicroPledgeModal();
        startTimer();
    } catch (e) {
        alert("서약 처리 중 오류가 발생했습니다.");
    }
}

async function toggleTimer() {
    requestStartTimer();
}

async function startTimer() {
    const scheduleSelect = document.getElementById("timer-schedule-select");
    const selectedOption = scheduleSelect.options[scheduleSelect.selectedIndex];
    
    let studyTitle = "자유 몰입 공부";
    if (scheduleSelect.value !== "none") {
        studyTitle = selectedOption.getAttribute("data-title");
    }
    
    try {
        const res = await fetch("/api/study/session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                action: "START"
            })
        });
        const session = await res.json();
        activeSessionId = session.id;
        isTimerRunning = true;
        isDistracted = false;
        
        timerStartTime = Date.now();
        timerSeconds = 0;
        const circle = document.getElementById("timer-circle");
        circle.classList.add("active");
        updateTimerDisplay(0);
        
        // 💡 화면 꺼짐 방지(Screen Wake Lock) 즉시 활성화
        requestScreenWakeLock();
        
        const timerBtn = document.getElementById("timer-toggle-btn");
        timerBtn.innerText = "집중 종료";
        timerBtn.style.backgroundColor = "var(--color-danger)";
        
        document.getElementById("timer-current-study").innerText = `🎯 진행 중: ${studyTitle}`;
        
        timerInterval = setInterval(() => {
            if (timerStartTime) {
                timerSeconds = Math.floor((Date.now() - timerStartTime) / 1000);
                updateTimerDisplay(timerSeconds);
            }
        }, 1000);
    } catch (e) {
        alert("타이머 시작 실패");
    }
}

async function stopTimerForcefully(triggeredByDistraction = false) {
    if (!isTimerRunning) return;
    
    // 💡 화면 꺼짐 방지 해제
    releaseScreenWakeLock();
    
    clearInterval(timerInterval);
    timerInterval = null;
    isTimerRunning = false;
    
    const finalSeconds = timerStartTime ? Math.floor((Date.now() - timerStartTime) / 1000) : timerSeconds;
    timerStartTime = null;
    
    const circle = document.getElementById("timer-circle");
    circle.classList.remove("active");
    circle.innerText = "00:00:00";
    
    const timerBtn = document.getElementById("timer-toggle-btn");
    timerBtn.innerText = "공부 시작";
    timerBtn.style.backgroundColor = "var(--color-success)";
    document.getElementById("timer-current-study").innerText = "🎯 대기 중: 할 일을 골라 측정을 시작하세요";

    try {
        const res = await fetch("/api/study/session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                action: "STOP",
                session_id: activeSessionId,
                is_distracted: triggeredByDistraction
            })
        });
        const session = await res.json();
        
        if (triggeredByDistraction) {
            try {
                const whRes = await fetch("/api/timer/webhook-distraction", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        student_id: currentStudent.id,
                        event_type: "DISTRACTION_DETECTED",
                        details: "공부 타이머 실행 중 타 앱 전환(딴짓) 감지"
                    })
                });
                const whData = await whRes.json();
                alert(`⚠️ 집중 중 딴짓이 감지되었습니다!\n성실 보증금 1,000원이 차감되었으며 학부모님께 긴급 경고 문자가 발송되었습니다.`);
            } catch (whErr) {
                alert(`⚠️ 집중 중 딴짓이 기록되었습니다. 포인트가 지급되지 않으며 학부모님께 즉시 문자가 발송되었습니다.`);
            }
        } else {
            const displayMin = Math.floor((session.duration_sec || finalSeconds) / 60);
            alert(`⏱️ 정상 공부 완료! ${displayMin}분간 정성껏 집중하여 공부 시간이 안전하게 기록되었습니다.`);
        }
        
        fetchStudentInfo(currentStudent.id);
    } catch (e) {
        console.error("타이머 종료 연동 오류:", e);
    }
}


// ==========================================
// 2페이지: 학습공간 동작
// ==========================================

function loadPage2Data() {
    if (currentStudent) {
        document.getElementById("pred-target-univ").value = currentStudent.target_univ || "";
        document.getElementById("pred-baseline-univ").value = currentStudent.baseline_univ || "";
    }
}

async function sendChatMessage() {
    const input = document.getElementById("chat-input");
    const msg = input.value.trim();
    if (!msg) return;
    
    input.value = "";
    appendChatBubble("user", msg);
    
    // 대화 기록에 사용자 메시지 추가
    chatHistory.push({ role: "user", content: msg });
    
    // 🤖 심도 있는 분석 로딩 버블 임시 노출
    const loadingBubble = appendChatBubble("bot", "🤖 패스봇이 백서 지식을 기반으로 심도 있는 답변을 작성 중입니다... (약 10~20초 소요)");
    if (loadingBubble) {
        loadingBubble.style.opacity = "0.7";
        loadingBubble.style.fontStyle = "italic";
    }

    try {
        // 최근 20개 대화 기록만 전송 (토큰 제한 고려)
        const recentHistory = chatHistory.slice(-21, -1); // 현재 메시지 제외한 이전 대화
        
        const res = await fetch("/api/ai/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: (currentStudent && currentStudent.id) ? currentStudent.id : 1,
                message: msg,
                history: recentHistory.length > 0 ? recentHistory : null
            })
        });
        
        if (!res.ok) {
            const errData = await res.json().catch(() => null);
            const errMsg = errData?.detail || `서버 오류 (HTTP ${res.status})`;
            if (loadingBubble) {
                loadingBubble.innerText = `⚠️ ${errMsg}`;
                loadingBubble.style.opacity = "1";
                loadingBubble.style.fontStyle = "normal";
            } else {
                appendChatBubble("bot", `⚠️ ${errMsg}`);
            }
            return;
        }
        
        const data = await res.json();
        if (loadingBubble) {
            loadingBubble.innerText = data.reply;
            loadingBubble.style.opacity = "1";
            loadingBubble.style.fontStyle = "normal";
        } else {
            appendChatBubble("bot", data.reply);
        }
        
        // 대화 기록에 봇 응답 추가
        chatHistory.push({ role: "bot", content: data.reply });
        
        document.getElementById("chat-limit-label").innerText = `오늘 남은 무료 대화: ${data.remaining_chats}회`;
    } catch (e) {
        console.error("Chat error:", e);
        if (loadingBubble) {
            loadingBubble.innerText = `서버 연결 오류: ${e.message || "네트워크 문제"}`;
            loadingBubble.style.opacity = "1";
            loadingBubble.style.fontStyle = "normal";
        } else {
            appendChatBubble("bot", `서버 연결 오류: ${e.message || "네트워크 문제"}`);
        }
    }
}

function appendChatBubble(sender, text) {
    const container = document.getElementById("chat-box");
    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", sender);
    bubble.innerText = text;
    
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
    return bubble;
}

// === Prediction State ===
let predictionResults = null;
let currentFilter = '전체';

// 영어 원점수 → 등급 변환
function engRawToGrade(raw) {
    if (raw >= 90) return 1;
    if (raw >= 80) return 2;
    if (raw >= 70) return 3;
    if (raw >= 60) return 4;
    if (raw >= 50) return 5;
    if (raw >= 40) return 6;
    if (raw >= 30) return 7;
    if (raw >= 20) return 8;
    return 9;
}

function histRawToGrade(raw) {
    if (raw >= 40) return 1;
    if (raw >= 35) return 2;
    if (raw >= 30) return 3;
    if (raw >= 25) return 4;
    if (raw >= 20) return 5;
    if (raw >= 15) return 6;
    if (raw >= 10) return 7;
    if (raw >= 5) return 8;
    return 9;
}

function getVerdictColor(verdict) {
    switch(verdict) {
        case '안정': return '#166534';  // dark green
        case '적정': return '#22c55e';  // light green
        case '소신': return '#eab308';  // yellow
        case '위험': return '#dc2626';  // red
        default: return '#666';
    }
}

function getVerdictBgColor(verdict) {
    switch(verdict) {
        case '안정': return 'rgba(22, 101, 52, 0.15)';
        case '적정': return 'rgba(34, 197, 94, 0.15)';
        case '소신': return 'rgba(234, 179, 8, 0.15)';
        case '위험': return 'rgba(220, 38, 38, 0.15)';
        default: return 'rgba(100,100,100,0.1)';
    }
}

// 📊 백분위 및 원점수 최대값(100/50) 실시간 강제 제한 헬퍼
function validatePercentileInput(el, maxVal = 100) {
    if (!el || el.value === "") return;
    let val = parseFloat(el.value);
    if (isNaN(val)) {
        el.value = "";
        return;
    }
    if (val < 0) {
        el.value = 0;
    } else if (val > maxVal) {
        el.value = maxVal;
    }
}

async function loadUniversityList() {
    try {
        const res = await fetch('/api/predict/universities');
        if (res.ok) {
            const univs = await res.json();
            const datalist = document.getElementById('univ-list');
            if (datalist) {
                datalist.innerHTML = '';
                univs.forEach(u => {
                    datalist.innerHTML += `<option value="${u}">`;
                });
            }
        }
    } catch (e) { console.error(e); }
}

async function runPrediction() {
    let kor = parseFloat(document.getElementById('pred-kor').value);
    let math = parseFloat(document.getElementById('pred-math').value);
    let eng = parseInt(document.getElementById('pred-eng').value);
    let hist = parseInt(document.getElementById('pred-hist').value);
    let tam1 = parseFloat(document.getElementById('pred-tam1').value);
    let tam2 = parseFloat(document.getElementById('pred-tam2').value);
    const mathType = document.getElementById('pred-math-type')?.value || '미적';
    const tam1Type = document.getElementById('pred-tam1-type')?.value || '과탐';
    const tam2Type = document.getElementById('pred-tam2-type')?.value || '과탐';
    
    if (isNaN(kor) || isNaN(math) || isNaN(eng) || isNaN(tam1) || isNaN(tam2) || isNaN(hist)) {
        alert('모든 성적(국어, 수학, 영어, 한국사, 탐구1, 탐구2)을 빠짐없이 입력해주세요.');
        return;
    }
    
    // 최대치 초과 자동 보정 및 방어
    if (kor > 100 || math > 100 || tam1 > 100 || tam2 > 100) {
        alert('백분위는 최대 100을 넘을 수 없습니다. 0~100 사이로 입력해주세요.');
        return;
    }
    if (eng > 100) {
        alert('영어 원점수는 최대 100점입니다.');
        return;
    }
    if (hist > 50) {
        alert('한국사 원점수는 최대 50점입니다.');
        return;
    }
    
    // 음수 방지
    if (kor < 0 || math < 0 || eng < 0 || hist < 0 || tam1 < 0 || tam2 < 0) {
        alert('성적은 0 이상이어야 합니다.');
        return;
    }
    
    // Show loading
    document.getElementById('predict-result').style.display = 'block';
    document.getElementById('pred-results-list').innerHTML = '<div style="text-align:center; padding: 20px;">사탐/과탐 교차지원 및 대학별 환산점수 계산 중...</div>';
    
    try {
        const res = await fetch('/api/ai/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                kor_pct: kor,
                math_pct: math,
                eng_raw: eng,
                tam1_pct: tam1,
                tam2_pct: tam2,
                hist_raw: hist,
                math_type: mathType,
                tam1_type: tam1Type,
                tam2_type: tam2Type,
                target_univ: '',
                target_dept: ''
            })
        });
        
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || '예측 실패');
            return;
        }
        
        const data = await res.json();
        predictionResults = data;
        
        // Update summary counts
        document.getElementById('pred-count-safe').innerText = data.summary['안정'] || 0;
        document.getElementById('pred-count-proper').innerText = data.summary['적정'] || 0;
        document.getElementById('pred-count-sosin').innerText = data.summary['소신'] || 0;
        document.getElementById('pred-count-danger').innerText = data.summary['위험'] || 0;
        
        // 학생 설정에서 희망대학/마지노선 대학 가져오기
        const targetUnivStr = currentStudent ? (currentStudent.target_univ || '') : '';
        const baselineUnivStr = currentStudent ? (currentStudent.baseline_univ || '') : '';
        
        // "서울대학교 화학생물공학부" 형태에서 대학명과 학과명 분리
        const targetParts = targetUnivStr.split(' ');
        const tUniv = targetParts[0] || '';
        const tDept = targetParts.slice(1).join(' ') || '';
        
        const baselineParts = baselineUnivStr.split(' ');
        const bUniv = baselineParts[0] || '';
        const bDept = baselineParts.slice(1).join(' ') || '';
        
        // 결과에서 대학 찾기 (정확 매칭 우선)
        function findUnivResult(results, univName, deptName) {
            if (!univName) return null;
            // 1. 대학교명 + 학과명 정확 매칭
            let found = results.find(r => r.대학교 === univName && deptName && r.전공 === deptName);
            if (found) return found;
            // 2. 대학교명 정확 + 학과명 포함
            found = results.find(r => r.대학교 === univName && deptName && r.전공 && r.전공.includes(deptName));
            if (found) return found;
            // 3. 대학교명만 정확 매칭 (첫 번째 결과)
            found = results.find(r => r.대학교 === univName);
            if (found) return found;
            // 4. 대학약칭으로 정확 매칭
            found = results.find(r => r.대학약칭 === univName);
            return found;
        }
        
        // 희망대학 카드 업데이트
        const targetResult = findUnivResult(data.results, tUniv, tDept);
        if (targetResult) {
            const tc = getVerdictColor(targetResult.verdict);
            const vtc = targetResult.verdict === '소신' ? '#92400e' : 'white';
            document.getElementById('pred-target-univ-name').innerText = targetResult.대학약칭 || targetResult.대학교;
            document.getElementById('pred-target-dept-name').innerText = targetResult.전공약칭 || targetResult.전공;
            const tv = document.getElementById('pred-target-verdict');
            tv.innerText = targetResult.verdict;
            tv.style.background = targetResult.verdict === '소신' ? '#eab308' : tc;
            tv.style.color = vtc;
        } else {
            document.getElementById('pred-target-univ-name').innerText = tUniv || '미설정';
            document.getElementById('pred-target-dept-name').innerText = tDept || '-';
            const tv = document.getElementById('pred-target-verdict');
            tv.innerText = '데이터 없음';
            tv.style.background = '#666';
            tv.style.color = 'white';
        }
        
        // 마지노선 대학 카드 업데이트
        const baselineResult = findUnivResult(data.results, bUniv, bDept);
        if (baselineResult) {
            const bc = getVerdictColor(baselineResult.verdict);
            const vbc = baselineResult.verdict === '소신' ? '#92400e' : 'white';
            document.getElementById('pred-baseline-univ-name').innerText = baselineResult.대학약칭 || baselineResult.대학교;
            document.getElementById('pred-baseline-dept-name').innerText = baselineResult.전공약칭 || baselineResult.전공;
            const bv = document.getElementById('pred-baseline-verdict');
            bv.innerText = baselineResult.verdict;
            bv.style.background = baselineResult.verdict === '소신' ? '#eab308' : bc;
            bv.style.color = vbc;
        } else {
            document.getElementById('pred-baseline-univ-name').innerText = bUniv || '미설정';
            document.getElementById('pred-baseline-dept-name').innerText = bDept || '-';
            const bv = document.getElementById('pred-baseline-verdict');
            bv.innerText = '데이터 없음';
            bv.style.background = '#666';
            bv.style.color = 'white';
        }
        
        // Render results
        currentFilter = '전체';
        renderPredResults();
        
    } catch (e) {
        console.error(e);
        alert('합격 예측 요청 중 오류가 발생했습니다.');
    }
}

function filterPredResults(filter) {
    if (filter) currentFilter = filter;
    renderPredResults();
}

function renderPredResults() {
    if (!predictionResults) return;
    
    const search = (document.getElementById('pred-search').value || '').trim().toLowerCase();
    let results = predictionResults.results;
    
    // Apply filter
    if (currentFilter !== '전체') {
        results = results.filter(r => r.verdict === currentFilter);
    }
    
    // Apply search
    if (search) {
        results = results.filter(r => 
            r.대학교.toLowerCase().includes(search) || 
            r.전공.toLowerCase().includes(search) ||
            (r.대학약칭 && r.대학약칭.toLowerCase().includes(search))
        );
    }
    
    // Limit display to 100
    const displayed = results.slice(0, 100);
    
    const container = document.getElementById('pred-results-list');
    container.innerHTML = '';
    
    displayed.forEach(r => {
        const color = getVerdictColor(r.verdict);
        const bgColor = getVerdictBgColor(r.verdict);
        const verdictTextColor = r.verdict === '소신' ? '#92400e' : 'white';
        const verdictBg = r.verdict === '소신' ? '#eab308' : color;
        container.innerHTML += `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 8px; border-bottom: 1px solid rgba(255,255,255,0.06); background: ${bgColor}; border-radius: 6px; margin-bottom: 4px;">
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${r.대학약칭 || r.대학교}</div>
                    <div style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${r.전공약칭 || r.전공} · ${r.모집군}군 · ${r.시도}</div>
                </div>
                <div style="background: ${verdictBg}; color: ${verdictTextColor}; padding: 3px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem; flex-shrink: 0; margin-left: 8px;">
                    ${r.verdict}
                </div>
            </div>
        `;
    });
    
    document.getElementById('pred-results-count').innerText = 
        `${results.length}개 중 ${displayed.length}개 표시 (${currentFilter} 필터)`;
}


// ==========================================
// 3페이지: 커뮤니티 공간 동작 (역할 전환 추가)
// ==========================================

function loadPage3Data() {
    if (!currentStudent) return;

    // 1. 선배 승격 상태 확인 -> 헤더 역할 토글 바 노출 제어
    const toggleBar = document.getElementById("role-toggle-bar");
    const upgradeBanner = document.getElementById("tutor-upgrade-banner");
    
    if (currentStudent.tutor_profile) {
        toggleBar.style.display = "flex";
        upgradeBanner.style.display = "none";
        
        // 기본 롤 세팅
        switchRole(activeRole);
    } else {
        toggleBar.style.display = "none";
        upgradeBanner.style.display = "block";
        switchRole("student");
    }

    loadQAPosts();
    loadTutors();
    loadTutorRequests();
    loadReceivedProposals();
}

// 신규: 대학 합격생 과외 선생님 승격 요청 API 통신
async function upgradeStudentToTutor(e) {
    e.preventDefault();
    if (!currentStudent) return;
    
    const univ = document.getElementById("tutor-up-univ").value;
    const major = document.getElementById("tutor-up-major").value;
    
    if (!univ || !major) {
        alert("합격 대학과 학과를 선택해 주세요.");
        return;
    }

    const payload = {
        student_id: currentStudent.id,
        university: univ,
        major: major,
        admission_year: parseInt(document.getElementById("tutor-up-year").value),
        high_school: currentStudent.high_school || "대치고",
        bio: document.getElementById("tutor-up-bio").value.trim(),
        contact_link: document.getElementById("tutor-up-link").value.trim()
    };

    if (!payload.bio || !payload.contact_link) {
        alert("자기소개 글과 오픈카톡 링크를 입력해 주세요.");
        return;
    }

    try {
        const res = await fetch("/api/tutor/upgrade", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            const data = await res.json();
            alert(data.message || "🎉 과외선생님 신청이 원장님께 제출되었습니다. 원장님이 서류(합격증 및 성적표)를 별도 확인 후 최종 승인하면 프로필이 공개됩니다.");
            
            // 입력 초기화
            document.getElementById("tutor-up-bio").value = "";
            document.getElementById("tutor-up-link").value = "";
            
            // 팝업 닫기 (존재 시)
            const modal = document.getElementById("tutor-upgrade-modal");
            if (modal) modal.style.display = "none";
        } else {
            const err = await res.json();
            alert(err.detail || "승격 실패");
        }
    } catch (e) {
        console.error(e);
    }
}

// 신규: 과외 선생님 프로필 편집 API 통신
async function handleUpdateTutorProfile(e) {
    e.preventDefault();
    if (!currentStudent || !currentStudent.tutor_profile) return;

    const bio = document.getElementById("edit-tutor-bio").value.trim();
    const contact = document.getElementById("edit-tutor-link").value.trim();

    if (!bio || !contact) {
        alert("수정할 소개글과 오픈카톡 주소를 작성해 주세요.");
        return;
    }

    try {
        const res = await fetch("/api/tutor/update-profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tutor_id: currentStudent.tutor_profile.id,
                bio: bio,
                contact_link: contact
            })
        });
        if (res.ok) {
            alert("✍️ 과외 모집글이 성공적으로 수정되어 목록에 반영되었습니다.");
            fetchStudentInfo(currentStudent.id);
        }
    } catch (e) {
        console.error(e);
    }
}


// Q&A 게시판 관련
async function loadQAPosts() {
    try {
        const res = await fetch("/api/qa/posts");
        const posts = await res.json();
        const container = document.getElementById("qa-list-container");
        container.innerHTML = "";
        
        posts.forEach(post => {
            const resolvedText = post.is_resolved ? "[채택완료]" : "[질문중]";
            const resolvedColor = post.is_resolved ? "var(--color-success)" : "var(--color-warning)";
            
            let commentsHtml = "";
            post.comments.forEach(c => {
                const acceptBtn = (!post.is_resolved && post.student_id === currentStudent.id) 
                    ? `<button class="btn" style="padding: 2px 6px; font-size: 0.65rem;" onclick="acceptQAComment(${c.id})">채택하기</button>` 
                    : (c.is_accepted ? `<span style="color:var(--color-success); font-weight:700;">[채택됨]</span>` : '');
                
                commentsHtml += `
                    <div style="background: rgba(255,255,255,0.03); border:1px solid var(--glass-border); padding: 8px; border-radius:6px; margin-top:6px; font-size:0.8rem; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:600; color:#a78bfa;">${c.student_name}:</span>
                            <span>${c.content}</span>
                        </div>
                        <div>${acceptBtn}</div>
                    </div>
                `;
            });

            container.innerHTML += `
                <div class="forum-item" style="cursor: default;">
                    <div class="forum-header">
                        <span>${post.student_name} (${post.subject})</span>
                        <span style="color: ${resolvedColor}">${resolvedText}</span>
                    </div>
                    <div class="forum-title" style="font-size:0.95rem;">${post.title}</div>
                    <div style="font-size:0.82rem; color:var(--text-secondary); margin-top:4px;">${post.content}</div>
                    <div class="forum-footer">
                        <span>보상 포인트: <span class="reward-tag">${post.reward_points}P</span></span>
                        <span style="color: var(--text-secondary); font-size: 0.75rem;">답변 ${post.comments.length}개</span>
                    </div>
                    <div style="margin-top: 10px; border-top: 1px dashed rgba(255,255,255,0.05); padding-top: 8px;">
                        <div style="font-size:0.75rem; font-weight:600; color:var(--text-secondary);">답변 피드</div>
                        ${commentsHtml}
                        <div style="display:flex; gap:6px; margin-top:8px;">
                            <input type="text" id="comment-input-${post.id}" class="form-input" style="padding: 6px 10px; font-size:0.75rem;" placeholder="답변을 작성해주세요..">
                            <button class="btn" style="padding: 6px 12px; font-size:0.75rem;" onclick="submitComment(${post.id})">답변</button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function submitComment(postId) {
    const input = document.getElementById(`comment-input-${postId}`);
    const content = input.value.trim();
    if (!content) return;
    
    try {
        const res = await fetch(`/api/qa/post/${postId}/comment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                content: content
            })
        });
        if (res.ok) {
            input.value = "";
            loadQAPosts();
        }
    } catch (e) {
        console.error(e);
    }
}

async function acceptQAComment(commentId) {
    try {
        const res = await fetch(`/api/qa/comment/${commentId}/accept?student_id=${currentStudent.id}`, { method: "POST" });
        if (res.ok) {
            alert("답변이 채택되었습니다! 설정된 보상 포인트가 답변 작성자에게 전송되었습니다.");
            fetchStudentInfo(currentStudent.id);
            loadQAPosts();
        } else {
            const err = await res.json();
            alert(err.detail);
        }
    } catch (e) {
        console.error(e);
    }
}

async function createQAPost() {
    const subject = document.getElementById("qa-post-subject").value;
    const title = document.getElementById("qa-post-title").value.trim();
    const content = document.getElementById("qa-post-content").value.trim();
    const reward = parseInt(document.getElementById("qa-post-reward").value) || 0;
    
    if (!title || !content) {
        alert("제목과 내용을 입력해 주세요.");
        return;
    }
    
    if (reward > currentStudent.current_points) {
        alert("보유 포인트 한도 내에서만 에스크로 보상을 설정할 수 있습니다.");
        return;
    }

    const isAnonymous = document.getElementById("qa-post-anonymous")?.checked || false;

    try {
        const res = await fetch("/api/qa/post", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                subject,
                title,
                content,
                reward_points: reward,
                is_anonymous: isAnonymous
            })
        });
        if (res.ok) {
            alert(isAnonymous ? "🔒 익명으로 질문이 등록되었습니다!" : "질문이 업로드되었습니다.");
            document.getElementById("qa-post-title").value = "";
            document.getElementById("qa-post-content").value = "";
            document.getElementById("qa-post-reward").value = "50";
            if (document.getElementById("qa-post-anonymous")) {
                document.getElementById("qa-post-anonymous").checked = false;
            }
            fetchStudentInfo(currentStudent.id);
            loadQAPosts();
        }
    } catch (e) {
        console.error(e);
    }
}

// 과외 매칭 관련
async function loadTutors() {
    try {
        const res = await fetch("/api/tutor/list");
        const tutors = await res.json();
        const container = document.getElementById("tutor-list-container");
        container.innerHTML = "";
        
        tutors.forEach(tutor => {
            const univEmblemText = tutor.univ_emblem || `🎓 ${tutor.university}`;
            const schoolEmblemText = tutor.high_school_emblem || `🏫 출신고`;
            
            container.innerHTML += `
                <div class="tutor-card">
                    <div class="tutor-header">
                        <span class="tutor-name">${tutor.name} 선배</span>
                        <span class="tutor-univ">${tutor.university} ${tutor.major}</span>
                    </div>
                    
                    <div class="badge-container">
                        <span class="badge-emblem badge-univ">${univEmblemText}</span>
                        <span class="badge-emblem badge-school">${schoolEmblemText}</span>
                    </div>
                    
                    <div class="tutor-bio" style="margin-top: 6px;">${tutor.bio}</div>
                    
                    <div style="font-size:0.75rem; color:var(--text-secondary); display:flex; justify-content:space-between; align-items:center; margin-top: 6px;">
                        <span style="color:#10b981; font-weight:700;">원장 합격증 검증 완료 ✅</span>
                        <button class="btn" style="padding: 6px 12px; font-size:0.75rem; background: linear-gradient(135deg, #3b82f6, #6366f1); font-weight:800;" onclick="requestTutorMatch(${tutor.id})">1:1 과외 매칭 신청 (29,000 캐시)</button>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function createTutorRequest() {
    const subject = document.getElementById("tr-subject").value;
    const budget = document.getElementById("tr-budget").value.trim();
    const details = document.getElementById("tr-details").value.trim();
    
    if (!budget || !details) {
        alert("희망조건을 입력해 주세요.");
        return;
    }

    try {
        const res = await fetch("/api/tutoring/request", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                subject,
                budget,
                details
            })
        });
        if (res.ok) {
            alert("과외 요청서가 등록되었습니다! 대학생 선배들이 이를 열람하고 제안서를 보낼 수 있습니다.");
            document.getElementById("tr-budget").value = "";
            document.getElementById("tr-details").value = "";
            loadTutorRequests();
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadTutorRequests() {
    try {
        const res = await fetch("/api/tutoring/requests");
        const requests = await res.json();
        const container = document.getElementById("tutor-requests-list-container");
        container.innerHTML = "";
        
        if (requests.length === 0) {
            container.innerHTML = "<div style='color: var(--text-secondary); font-size: 0.82rem;'>등록된 요청서가 없습니다.</div>";
        } else {
            requests.forEach(r => {
                // 내 튜터 프로필 번호 매핑 (선생님 모드 제안 시 필수)
                const myTutorId = currentStudent && currentStudent.tutor_profile ? currentStudent.tutor_profile.id : 1;
                
                container.innerHTML += `
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); border-radius:10px; padding:12px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:600;">
                            <span>👤 ${r.student_name} 학생의 과외 요청</span>
                            <span style="color:var(--color-accent);">${r.subject}</span>
                        </div>
                        <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:4px;">희망 과외비: ${r.budget}</div>
                        <div style="font-size:0.78rem; margin-top:6px;">요구 조건: ${r.details}</div>
                        
                        <div style="margin-top: 10px; border-top:1px dashed rgba(255,255,255,0.04); padding-top:8px; display:flex; gap:6px;">
                            <input type="text" id="proposal-msg-${r.id}" class="form-input" style="padding: 6px; font-size:0.72rem;" placeholder="제안 메시지 입력..">
                            <button class="btn" style="padding: 6px; font-size:0.72rem;" onclick="sendProposalFromTutor(${r.id}, ${myTutorId})">제안발송(100P)</button>
                        </div>
                    </div>
                `;
            });
        }
    } catch (e) {
        console.error(e);
    }
}

async function sendProposalFromTutor(requestId, tutorId) {
    const input = document.getElementById(`proposal-msg-${requestId}`);
    const msg = input.value.trim();
    if (!msg) {
        alert("제안 제안글 내용을 작성해주세요.");
        return;
    }

    try {
        const res = await fetch("/api/tutoring/propose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tutor_id: tutorId,
                request_id: requestId,
                message: msg
            })
        });
        if (res.ok) {
            alert("🎉 선배 제안서가 등록되었습니다! 학생의 '받은 제안서' 함에 즉시 업데이트됩니다.");
            input.value = "";
            loadReceivedProposals();
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadReceivedProposals() {
    try {
        const res = await fetch(`/api/tutoring/proposals/${currentStudent.id}`);
        const proposals = await res.json();
        const container = document.getElementById("received-proposals-container");
        container.innerHTML = "";
        
        if (proposals.length === 0) {
            container.innerHTML = "<div style='color: var(--text-secondary); font-size: 0.82rem;'>받은 과외 제안서가 없습니다.</div>";
        } else {
            proposals.forEach(p => {
                const isAccepted = p.status === "ACCEPTED";
                const actionBtn = isAccepted 
                    ? `<span style="color: var(--color-success); font-weight:700;">수락완료</span>`
                    : `<button class="btn" style="padding: 4px 8px; font-size:0.75rem;" onclick="acceptProposal(${p.id})">수락하기</button>`;
                
                container.innerHTML += `
                    <div class="tutor-card" style="border-left: 3px solid var(--color-accent); margin-bottom:8px;">
                        <div class="tutor-header">
                            <span class="tutor-name">${p.tutor_name} (${p.tutor_univ} ${p.tutor_major})</span>
                            <span>${actionBtn}</span>
                        </div>
                        <div class="tutor-bio">제안서 내용: ${p.message}</div>
                        ${isAccepted ? `<div style="font-size:0.8rem; color:var(--color-warning); font-weight:500; margin-top:4px;">연락처: ${p.tutor_contact || '010-1111-2222'} / 카톡링크: ${p.contact_link || 'open.kakao.com/o/sSNU1'}</div>` : ''}
                    </div>
                `;
            });
        }
    } catch (e) {
        console.error(e);
    }
}

async function acceptProposal(proposalId) {
    try {
        const res = await fetch("/api/tutoring/accept", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                proposalId: proposalId,
                studentId: currentStudent.id
            })
        });
        const data = await res.json();
        alert(`🎉 과외 매칭 완료! 선배의 상세 정보가 잠금해제 되었습니다.\n선배 연락처: ${data.tutor_contact}\n오픈카톡: ${data.contact_link}`);
        loadReceivedProposals();
    } catch (e) {
        console.error(e);
    }
}

function requestTutorDirect(tutorId) {
    if (currentStudent.current_points < 150) {
        alert("과외 매칭 신청에 필요한 포인트(150P)가 부족합니다.");
        return;
    }
    alert("선배에게 매칭 요청이 발송되었습니다. 선배가 제안을 수락할 시 포인트가 차감되고 매칭이 완료됩니다.");
}

// --- 대학 및 학과 동적 목록 데이터 매칭 헬퍼 ---

function findMatchingUniv(cleanInitUniv, univList) {
    if (!cleanInitUniv) return "";
    const clean = cleanInitUniv.trim();
    if (univList.includes(clean)) return clean;
    let match = univList.find(u => u.trim() === clean);
    if (match) return match;
    match = univList.find(u => u.includes(clean) || clean.includes(u));
    if (match) return match;
    return "";
}

// --- 예체능/자율전공 직접 입력 토글 헬퍼 ---
function checkCustomDept(selectEl, customInputId) {
    const customInput = document.getElementById(customInputId);
    if (!customInput) return;
    if (selectEl.value === "__CUSTOM__") {
        customInput.style.display = "block";
        customInput.focus();
    } else {
        customInput.style.display = "none";
    }
}

// --- 대학교 학과 드롭다운 연결 헬퍼 (예체능 직접입력 지원) ---
function setupUnivDeptSelectors(univSelId, deptSelId, initialUniv = "", initialDept = "") {
    const univSelect = document.getElementById(univSelId);
    const deptSelect = document.getElementById(deptSelId);
    if (!univSelect || !deptSelect) return;

    const univList = Object.keys(UNIVERSITY_DEPARTMENTS).sort((a, b) => a.localeCompare(b, 'ko'));
    const cleanInitUniv = (initialUniv || "").trim();
    const cleanInitDept = (initialDept || "").trim();
    const matchedUniv = findMatchingUniv(cleanInitUniv, univList);

    // 1. 대학 옵션 렌더링
    univSelect.innerHTML = "";
    const defaultUnivOpt = document.createElement("option");
    defaultUnivOpt.value = "";
    defaultUnivOpt.textContent = "대학 선택";
    defaultUnivOpt.disabled = true;
    if (!matchedUniv) defaultUnivOpt.selected = true;
    univSelect.appendChild(defaultUnivOpt);

    univList.forEach(univ => {
        const opt = document.createElement("option");
        opt.value = univ;
        opt.textContent = univ;
        if (univ === matchedUniv) opt.selected = true;
        univSelect.appendChild(opt);
    });
    if (matchedUniv) {
        univSelect.value = matchedUniv;
    }

    // 2. 대학 변경 리스너
    univSelect.onchange = () => {
        const selectedUniv = univSelect.value;
        const depts = UNIVERSITY_DEPARTMENTS[selectedUniv] || [];
        deptSelect.innerHTML = "";
        const defaultDeptOpt = document.createElement("option");
        defaultDeptOpt.value = "";
        defaultDeptOpt.textContent = "학과 선택";
        defaultDeptOpt.disabled = true;
        defaultDeptOpt.selected = true;
        deptSelect.appendChild(defaultDeptOpt);

        depts.forEach(dept => {
            const opt = document.createElement("option");
            opt.value = dept;
            opt.textContent = dept;
            deptSelect.appendChild(opt);
        });

        // 예체능/자율전공 직접 입력 옵션 추가
        const customOpt = document.createElement("option");
        customOpt.value = "__CUSTOM__";
        customOpt.textContent = "✏️ 직접 입력 (예체능/자율전공 등)";
        deptSelect.appendChild(customOpt);
    };

    // 3. 초기 학과 옵션 렌더링
    if (matchedUniv) {
        const depts = UNIVERSITY_DEPARTMENTS[matchedUniv] || [];
        deptSelect.innerHTML = "";
        const defaultDeptOpt = document.createElement("option");
        defaultDeptOpt.value = "";
        defaultDeptOpt.textContent = "학과 선택";
        defaultDeptOpt.disabled = true;
        if (!cleanInitDept) defaultDeptOpt.selected = true;
        deptSelect.appendChild(defaultDeptOpt);

        let isDeptInList = false;
        depts.forEach(dept => {
            const opt = document.createElement("option");
            opt.value = dept;
            opt.textContent = dept;
            if (dept === cleanInitDept) {
                opt.selected = true;
                isDeptInList = true;
            }
            deptSelect.appendChild(opt);
        });

        // 예체능/자율전공 직접 입력 옵션 추가
        const customOpt = document.createElement("option");
        customOpt.value = "__CUSTOM__";
        customOpt.textContent = "✏️ 직접 입력 (예체능/자율전공 등)";
        deptSelect.appendChild(customOpt);

        if (cleanInitDept && !isDeptInList) {
            // 기존 등록된 학과가 목록에 없으면(예체능 직접입력 학과인 경우)
            customOpt.selected = true;
            const customInputId = deptSelId === "edit-target-dept-select" ? "edit-target-dept-custom" : (deptSelId === "edit-baseline-dept-select" ? "edit-baseline-dept-custom" : "");
            if (customInputId) {
                const cInput = document.getElementById(customInputId);
                if (cInput) {
                    cInput.value = cleanInitDept;
                    cInput.style.display = "block";
                }
            }
        } else if (cleanInitDept && isDeptInList) {
            deptSelect.value = cleanInitDept;
        }
    } else {
        deptSelect.innerHTML = `<option value="" disabled selected>학과 선택</option><option value="__CUSTOM__">✏️ 직접 입력 (예체능/자율전공 등)</option>`;
    }
}

// === 수시/정시/입시전략리포트 3대 탭 전환 ===
function switchAdmissionTab(tab) {
    const susiSection = document.getElementById('susi-section');
    const jeongsiSection = document.getElementById('jeongsi-section');
    const reportSection = document.getElementById('report-tab-section');
    const btnSusi = document.getElementById('btn-susi');
    const btnJeongsi = document.getElementById('btn-jeongsi');
    const btnReport = document.getElementById('btn-report');
    
    if (tab === 'susi') {
        if (susiSection) susiSection.style.display = 'block';
        if (jeongsiSection) jeongsiSection.style.display = 'none';
        if (reportSection) reportSection.style.display = 'none';
        if (btnSusi) {
            btnSusi.className = 'btn';
            btnSusi.style.background = 'linear-gradient(135deg, #6366f1, #8b5cf6)';
        }
        if (btnJeongsi) {
            btnJeongsi.className = 'btn btn-secondary';
            btnJeongsi.style.background = '';
        }
        if (btnReport) {
            btnReport.className = 'btn btn-secondary';
            btnReport.style.background = '';
        }
    } else if (tab === 'jeongsi') {
        if (susiSection) susiSection.style.display = 'none';
        if (jeongsiSection) jeongsiSection.style.display = 'block';
        if (reportSection) reportSection.style.display = 'none';
        if (btnJeongsi) {
            btnJeongsi.className = 'btn';
            btnJeongsi.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        }
        if (btnSusi) {
            btnSusi.className = 'btn btn-secondary';
            btnSusi.style.background = '';
        }
        if (btnReport) {
            btnReport.className = 'btn btn-secondary';
            btnReport.style.background = '';
        }
    } else if (tab === 'report') {
        if (susiSection) susiSection.style.display = 'none';
        if (jeongsiSection) jeongsiSection.style.display = 'none';
        if (reportSection) reportSection.style.display = 'block';
        if (btnReport) {
            btnReport.className = 'btn';
            btnReport.style.background = 'linear-gradient(135deg, #6366f1, #8b5cf6)';
        }
        if (btnSusi) {
            btnSusi.className = 'btn btn-secondary';
            btnSusi.style.background = '';
        }
        if (btnJeongsi) {
            btnJeongsi.className = 'btn btn-secondary';
            btnJeongsi.style.background = '';
        }
    }
}

// === 목표/마지노선 대학 설정 ===
function toggleUnivSettings() {
    const form = document.getElementById('univ-settings-form');
    if (form.style.display === 'none') {
        form.style.display = 'block';
        // 현재 학생 설정으로 셀렉터 초기화
        if (currentStudent) {
            const tParts = (currentStudent.target_univ || '').split(' ');
            const bParts = (currentStudent.baseline_univ || '').split(' ');
            setupUnivDeptSelectors('up-univ', 'up-major', tParts[0] || '', tParts.slice(1).join(' ') || '');
            setupUnivDeptSelectors('up-base-univ', 'up-base-major', bParts[0] || '', bParts.slice(1).join(' ') || '');
        }
    } else {
        form.style.display = 'none';
    }
}

async function saveUnivSettings() {
    if (!currentStudent) {
        alert('로그인이 필요합니다.');
        return;
    }
    const targetUniv = document.getElementById('up-univ').value;
    const targetMajor = document.getElementById('up-major').value;
    const baseUniv = document.getElementById('up-base-univ').value;
    const baseMajor = document.getElementById('up-base-major').value;
    
    if (!targetUniv || !targetMajor || !baseUniv || !baseMajor) {
        alert('모든 항목을 선택해주세요.');
        return;
    }
    
    try {
        const res = await fetch(`/api/student/${currentStudent.id}/update-univ`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_univ: `${targetUniv} ${targetMajor}`,
                baseline_univ: `${baseUniv} ${baseMajor}`
            })
        });
        
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || '저장 실패');
            return;
        }
        
        const updated = await res.json();
        currentStudent.target_univ = updated.target_univ;
        currentStudent.baseline_univ = updated.baseline_univ;
        
        updateUnivDisplay();
        updateTargetBanner();
        document.getElementById('univ-settings-form').style.display = 'none';
        alert('목표 대학이 변경되었습니다!');
    } catch(e) {
        console.error(e);
        alert('서버 연결 실패');
    }
}

function updateUnivDisplay() {
    const targetStr = currentStudent ? (currentStudent.target_univ || '') : '';
    const baselineStr = currentStudent ? (currentStudent.baseline_univ || '') : '';
    
    const dispTarget = document.getElementById('disp-target-univ');
    const dispBaseline = document.getElementById('disp-baseline-univ');
    
    if (dispTarget) {
        const parts = targetStr.split(' ');
        dispTarget.innerHTML = `<div>${parts[0] || '-'}</div><div style="font-size:0.7rem;color:var(--text-secondary);font-weight:400;">${parts.slice(1).join(' ') || ''}</div>`;
    }
    if (dispBaseline) {
        const parts = baselineStr.split(' ');
        dispBaseline.innerHTML = `<div>${parts[0] || '-'}</div><div style="font-size:0.7rem;color:var(--text-secondary);font-weight:400;">${parts.slice(1).join(' ') || ''}</div>`;
    }
}

// === 서비스 불편사항 & 아이디어 건의함 모달 ===
function openFeedbackModal() {
    const modal = document.getElementById("feedback-modal");
    if (modal) modal.style.display = "flex";
}

function closeFeedbackModal() {
    const modal = document.getElementById("feedback-modal");
    if (modal) modal.style.display = "none";
}

async function submitStudentFeedback() {
    const contentEl = document.getElementById("feedback-content");
    const categoryEl = document.getElementById("feedback-category");
    const emailEl = document.getElementById("feedback-email");
    
    const content = contentEl ? contentEl.value.trim() : "";
    if (!content) {
        alert("건의사항 또는 의견 내용을 작성해 주세요.");
        return;
    }
    
    const category = categoryEl ? categoryEl.value : "불편사항";
    const userEmail = emailEl ? emailEl.value.trim() : (currentStudent ? currentStudent.email : "");
    
    try {
        const res = await fetch("/api/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent ? currentStudent.id : null,
                user_email: userEmail,
                category: category,
                content: content
            })
        });
        if (res.ok) {
            alert("💡 건의해주신 소중한 의견이 원장님 및 개발팀으로 실시간 접수되었습니다. 빠르게 확인 후 반영하겠습니다!");
            if (contentEl) contentEl.value = "";
            closeFeedbackModal();
        } else {
            alert("등록 실패. 잠시 후 다시 시도해주세요.");
        }
    } catch(e) {
        console.error(e);
        alert("서버 연결 실패");
    }
}

// === 📚 기출문제 및 수험자료실 프론트엔드 연동 ===
let currentExamSubject = "전체";
let currentExamYear = 0;

function switchExamSubject(subject, btnEl) {
    currentExamSubject = subject;
    document.querySelectorAll(".exam-subj-btn").forEach(b => {
        b.classList.remove("active");
        b.classList.add("btn-secondary");
    });
    if (btnEl) {
        btnEl.classList.add("active");
        btnEl.classList.remove("btn-secondary");
    }
    loadExamMaterials();
}

function switchExamYear(year, btnEl) {
    currentExamYear = parseInt(year) || 0;
    document.querySelectorAll(".exam-year-btn").forEach(b => {
        b.classList.remove("active");
        b.classList.add("btn-secondary");
    });
    if (btnEl) {
        btnEl.classList.add("active");
        btnEl.classList.remove("btn-secondary");
    }
    loadExamMaterials();
}

function switchExamYearSelect(yearVal) {
    currentExamYear = parseInt(yearVal) || 0;
    loadExamMaterials();
}

function onExamSubjectSelectChange(subject) {
    currentExamSubject = subject;
    loadExamMaterials();
}

async function filterExamMaterials(subject, btnEl) {
    switchExamSubject(subject, btnEl);
}

async function loadExamMaterials() {
    const container = document.getElementById("exam-materials-container");
    if (!container) return;
    
    try {
        let params = [];
        if (currentExamSubject && currentExamSubject !== "전체") {
            params.push(`subject=${encodeURIComponent(currentExamSubject)}`);
        }
        if (currentExamYear && currentExamYear !== 0) {
            params.push(`year=${currentExamYear}`);
        }
        const url = params.length > 0 ? `/api/materials?${params.join("&")}` : "/api/materials";
        const res = await fetch(url);
        if (!res.ok) {
            container.innerHTML = `<div style="text-align: center; color: var(--text-secondary); padding: 20px;">자료를 불러오지 못했습니다.</div>`;
            return;
        }
        const materials = await res.json();
        if (materials.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; color: var(--text-secondary); padding: 30px 10px; background: rgba(255,255,255,0.02); border-radius: 12px; border: 1px dashed rgba(255,255,255,0.08);">
                    <span class="material-symbols-rounded" style="font-size: 2rem; color: #64748b; margin-bottom: 6px;">folder_open</span>
                    <div style="font-size: 0.85rem; font-weight: 600;">선택하신 조건의 기출 자료가 없습니다.</div>
                    <div style="font-size: 0.72rem; margin-top: 4px;">원장님이 새로운 기출자료를 업로드하면 실시간 노출됩니다.</div>
                </div>
            `;
            return;
        }

        container.innerHTML = "";
        materials.forEach(m => {
            const subjectBadges = {
                "국어": { bg: "rgba(239, 68, 68, 0.15)", color: "#f87171", icon: "📖" },
                "수학": { bg: "rgba(99, 102, 241, 0.15)", color: "#818cf8", icon: "📐" },
                "영어": { bg: "rgba(16, 185, 129, 0.15)", color: "#34d399", icon: "🔤" },
                "과탐": { bg: "rgba(245, 158, 11, 0.15)", color: "#fbbf24", icon: "🔬" },
                "사탐": { bg: "rgba(59, 130, 246, 0.15)", color: "#60a5fa", icon: "🌏" },
                "논술": { bg: "rgba(168, 85, 247, 0.15)", color: "#c084fc", icon: "✍️" }
            };
            const badgeInfo = subjectBadges[m.subject] || { bg: "rgba(255,255,255,0.1)", color: "#e2e8f0", icon: "📄" };
            
            const hasAnswer = !!m.answer_file_url;
            const answerBtn = hasAnswer ? `
                <a href="/api/materials/${m.id}/download-answer" target="_blank" download class="btn btn-secondary" style="padding: 6px 10px; font-size: 0.75rem; font-weight: 700; color: #10b981 !important; border-color: #10b981; border-radius: 8px; white-space: nowrap; display: inline-flex; align-items: center; gap: 4px;">
                    <span>📝</span> 정답/해설
                </a>
            ` : '';

            container.innerHTML += `
                <div class="material-card" style="margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
                    <div style="flex: 1; min-width: 0;">
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                            <span style="background: ${badgeInfo.bg}; color: ${badgeInfo.color}; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">${badgeInfo.icon} ${m.subject}</span>
                            ${m.year ? `<span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700;">${m.year}학년도</span>` : ''}
                        </div>
                        <div class="material-title" style="font-size: 0.88rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${m.title}</div>
                        ${m.description ? `<div class="material-desc" style="font-size: 0.72rem; color: var(--text-secondary); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${m.description}</div>` : ''}
                    </div>
                    <div style="display: flex; gap: 6px; flex-shrink: 0; align-items: center;">
                        <a href="/api/materials/${m.id}/download" target="_blank" download class="btn" style="padding: 6px 12px; font-size: 0.75rem; font-weight: 700; background: linear-gradient(135deg, #6366f1, #4f46e5); color: white !important; text-decoration: none; border-radius: 8px; white-space: nowrap; display: inline-flex; align-items: center; gap: 4px;">
                            <span>📖</span> 문제지
                        </a>
                        ${answerBtn}
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error("Exam materials load error:", e);
        container.innerHTML = `<div style="text-align: center; color: #ef4444; padding: 14px; font-size: 0.8rem;">자료 로딩 오류 발생</div>`;
    }
}

// ==========================================
// 🪪 1. 2027학번 목표 대학 가상 학생증 발급 & PNG 다운로드
// ==========================================

function openStudentCardModal() {
    if (!currentStudent) return;
    const modal = document.getElementById("student-card-modal");
    if (!modal) return;

    const tUniv = currentStudent.target_univ || "서울대학교 의예과";
    const parts = tUniv.split(" ");
    const univName = parts[0] || "서울대학교";
    const deptName = parts.slice(1).join(" ") || "전공선택";

    document.getElementById("card-univ-title").innerText = univName;
    document.getElementById("card-name").innerText = `${currentStudent.name} 학생`;
    document.getElementById("card-school").innerText = `${currentStudent.high_school || "일반고"} (${currentStudent.grade === 4 ? 'N수생' : currentStudent.grade + '학년'})`;
    document.getElementById("card-dept").innerText = deptName;
    document.getElementById("card-id-code").innerText = currentStudent.referral_code || `PL-2027-${String(currentStudent.id).padStart(4, '0')}`;

    modal.style.display = "flex";
}

function downloadStudentIDCard() {
    if (!currentStudent) {
        alert("로그인 정보가 없습니다.");
        return;
    }

    const tUniv = currentStudent.target_univ || "서울대학교 의예과";
    const parts = tUniv.split(" ");
    const univName = parts[0] || "서울대학교";
    const deptName = parts.slice(1).join(" ") || "전공선택";
    
    // HTML5 Canvas로 1080x1350 인스타그램 스토리 규격 렌더링
    const canvas = document.createElement("canvas");
    canvas.width = 1080;
    canvas.height = 1350;
    const ctx = canvas.getContext("2d");

    // 1. 다크 그라데이션 배경
    const bgGrad = ctx.createLinearGradient(0, 0, 1080, 1350);
    bgGrad.addColorStop(0, "#080c14");
    bgGrad.addColorStop(0.5, "#0f172a");
    bgGrad.addColorStop(1, "#020617");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1080, 1350);

    // 2. 배경 장식 원/글로우
    const glowGrad = ctx.createRadialGradient(540, 500, 50, 540, 500, 600);
    glowGrad.addColorStop(0, "rgba(99, 102, 241, 0.25)");
    glowGrad.addColorStop(1, "rgba(99, 102, 241, 0)");
    ctx.fillStyle = glowGrad;
    ctx.fillRect(0, 0, 1080, 1350);

    // 3. 학생증 카드 바디 (둥근 사각형)
    const cardX = 90, cardY = 160, cardW = 900, cardH = 1020, radius = 40;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(cardX + radius, cardY);
    ctx.lineTo(cardX + cardW - radius, cardY);
    ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + radius);
    ctx.lineTo(cardX + cardW, cardY + cardH - radius);
    ctx.quadraticCurveTo(cardX + cardW, cardY + cardH, cardX + cardW - radius, cardY + cardH);
    ctx.lineTo(cardX + radius, cardY + cardH);
    ctx.quadraticCurveTo(cardX, cardY + cardH, cardX, cardY + cardH - radius);
    ctx.lineTo(cardX, cardY + radius);
    ctx.quadraticCurveTo(cardX, cardY, cardX + radius, cardY);
    ctx.closePath();

    const cardGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY + cardH);
    cardGrad.addColorStop(0, "#131b2e");
    cardGrad.addColorStop(0.6, "#0b0f19");
    cardGrad.addColorStop(1, "#040711");
    ctx.fillStyle = cardGrad;
    ctx.fill();

    ctx.lineWidth = 6;
    ctx.strokeStyle = "#6366f1";
    ctx.stroke();
    ctx.restore();

    // 4. 2027 기하학적 미니멀 워터마크 (배경 우측 하단)
    ctx.save();
    ctx.globalAlpha = 0.06;
    ctx.fillStyle = "#ffffff";
    ctx.font = "900 320px monospace";
    ctx.textAlign = "right";
    ctx.textBaseline = "bottom";
    ctx.fillText("27", cardX + cardW - 30, cardY + cardH - 20);
    ctx.restore();

    // 5. 헤더 텍스트
    ctx.fillStyle = "#a5b4fc";
    ctx.font = "bold 28px Pretendard, sans-serif";
    ctx.fillText("STUDENT IDENTIFICATION CARD", 150, 250);

    ctx.fillStyle = "#ffffff";
    ctx.font = "900 68px Pretendard, sans-serif";
    ctx.fillText(univName, 150, 340);

    // 27학번 엠블럼 뱃지
    ctx.fillStyle = "rgba(99, 102, 241, 0.35)";
    ctx.fillRect(700, 280, 230, 64);
    ctx.strokeStyle = "#818cf8";
    ctx.lineWidth = 2;
    ctx.strokeRect(700, 280, 230, 64);

    ctx.fillStyle = "#c7d2fe";
    ctx.font = "bold 32px Pretendard, sans-serif";
    ctx.fillText("27학번 합격생", 725, 324);

    // 증명사진 플레이스홀더
    ctx.fillStyle = "rgba(255, 255, 255, 0.05)";
    ctx.fillRect(150, 420, 240, 310);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
    ctx.strokeRect(150, 420, 240, 310);

    ctx.fillStyle = "#818cf8";
    ctx.font = "bold 80px sans-serif";
    ctx.fillText("👤", 230, 595);

    // 학생 정보 필드
    ctx.fillStyle = "#94a3b8";
    ctx.font = "bold 32px Pretendard, sans-serif";
    ctx.fillText("성  명 :", 430, 490);
    ctx.fillText("소  속 :", 430, 560);
    ctx.fillText("목  표 :", 430, 630);
    ctx.fillText("식  별 :", 430, 700);

    ctx.fillStyle = "#ffffff";
    ctx.font = "900 44px Pretendard, sans-serif";
    ctx.fillText(`${currentStudent.name} 학생`, 560, 490);

    ctx.fillStyle = "#e2e8f0";
    ctx.font = "600 34px Pretendard, sans-serif";
    ctx.fillText(`${currentStudent.high_school || "일반고"} (${currentStudent.grade === 4 ? 'N수생' : currentStudent.grade + '학년'})`, 560, 560);

    ctx.fillStyle = "#fcd34d";
    ctx.font = "900 38px Pretendard, sans-serif";
    ctx.fillText(deptName, 560, 630);

    ctx.fillStyle = "#a5b4fc";
    ctx.font = "bold 32px monospace";
    ctx.fillText(currentStudent.referral_code || `PL-2027-${String(currentStudent.id).padStart(4, '0')}`, 560, 700);

    // 하단 구분선 및 직인
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(150, 830);
    ctx.lineTo(930, 830);
    ctx.stroke();

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 28px Pretendard, sans-serif";
    ctx.fillText("🏛️ PALIN OS 초정밀 데이터 기반 합격 궤적", 150, 920);

    ctx.fillStyle = "#60a5fa";
    ctx.font = "bold 26px Pretendard, sans-serif";
    ctx.fillText("[ PALIN VERIFIED ]", 730, 920);

    // 하단 인스타그램 바이럴 문구
    ctx.fillStyle = "#64748b";
    ctx.font = "bold 24px Pretendard, sans-serif";
    ctx.fillText("공부 행동통제 및 1:1 과외 매칭 OS ➔ https://palin-os.onrender.com", 220, 1260);

    // 이미지 데이터 생성
    const dataUrl = canvas.toDataURL("image/png");
    const fileName = `PALIN_2027_${currentStudent.name}_학생증.png`;

    // 1. 모달 내부 렌더링 뷰어에 즉시 표시 (모바일에서 길게 눌러 사진 저장 가능하도록 100% 보장)
    const imgContainer = document.getElementById("student-card-img-container");
    const renderedImg = document.getElementById("student-card-rendered-img");
    if (imgContainer && renderedImg) {
        renderedImg.src = dataUrl;
        imgContainer.style.display = "block";
        const modalContent = document.querySelector("#student-card-modal .trigger-content");
        if (modalContent) {
            modalContent.scrollTo({ top: modalContent.scrollHeight, behavior: 'smooth' });
        }
    }

    // 2. 파일 다운로드 링크 자동 트리거
    try {
        const link = document.createElement("a");
        link.download = fileName;
        link.href = dataUrl;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (e) {
        console.error("Direct link click failed:", e);
    }

    // 3. 모바일 Web Share API 시도
    if (navigator.canShare) {
        canvas.toBlob(async (blob) => {
            if (!blob) return;
            const file = new File([blob], fileName, { type: "image/png" });
            if (navigator.canShare({ files: [file] })) {
                try {
                    await navigator.share({
                        files: [file],
                        title: "2027학번 목표대학 가상 학생증",
                        text: `PALIN OS에서 발급받은 2027학번 가상 학생증입니다!`
                    });
                } catch (shareErr) {
                    // 공유 취소 시 무시
                }
            }
        }, "image/png");
    }
}



// ==========================================
// 📊 3. 3-Tier 대입 전략 리포트 & VIP 1:1 직접 컨설팅
// ==========================================

let selectedReportTier = 3;
let isVIPInPerson = false;

function openReportTierModal() {
    if (!currentStudent) return;
    const modal = document.getElementById("report-tier-modal");
    if (!modal) return;

    document.getElementById("tier-modal-my-cash").innerText = (currentStudent.paid_cash || 0).toLocaleString();
    document.getElementById("tier-modal-my-tickets").innerText = currentStudent.free_report_tickets || 0;

    selectTier(3); // 기본값 Tier 3 BEST 선택
    modal.style.display = "flex";
}

function selectTier(tier) {
    selectedReportTier = tier;
    
    // 카드 활성화 스타일 갱신
    for (let t = 1; t <= 4; t++) {
        const card = document.getElementById(`tier-card-${t}`);
        if (!card) continue;
        if (t === tier) {
            card.style.borderColor = (t === 4) ? "#f59e0b" : "#818cf8";
            card.style.background = (t === 4) ? "rgba(245, 158, 11, 0.12)" : "rgba(99, 102, 241, 0.12)";
        } else {
            card.style.borderColor = "rgba(255,255,255,0.1)";
            card.style.background = "rgba(255,255,255,0.02)";
        }
    }

    // Tier 1 서브옵션 노출
    const t1Opt = document.getElementById("tier-1-options");
    if (t1Opt) t1Opt.style.display = (tier === 1) ? "block" : "none";

    // VIP 서브옵션 노출
    const vipOpt = document.getElementById("vip-options");
    if (vipOpt) vipOpt.style.display = (tier === 4) ? "block" : "none";

    updateTierModalPayAmount();
}

function toggleVIPInPerson(checked) {
    isVIPInPerson = checked;
    const priceDisplay = document.getElementById("vip-price-display");
    if (priceDisplay) {
        priceDisplay.innerText = checked ? "500,000원 (대면 50분)" : "300,000원 (전화 30~40분)";
    }
    updateTierModalPayAmount();
}

function updateTierModalPayAmount() {
    const payEl = document.getElementById("tier-modal-pay-amount");
    if (!payEl) return;

    const tickets = currentStudent.free_report_tickets || 0;

    if (selectedReportTier === 1) {
        if (tickets > 0) {
            payEl.innerHTML = `<span style="color:#fcd34d;">🎟️ 무료권 1장 적용 (0원 결제)</span>`;
        } else {
            payEl.innerText = "결제 예정: 16,900원";
        }
    } else if (selectedReportTier === 2) {
        if (tickets > 0) {
            payEl.innerHTML = `<span style="color:#fcd34d;">🎟️ 무료권 1장 적용 (-19,000원 할인) ➔ 10,900원</span>`;
        } else {
            payEl.innerText = "결제 예정: 29,900원";
        }
    } else if (selectedReportTier === 3) {
        if (tickets > 0) {
            payEl.innerHTML = `<span style="color:#fcd34d;">🎟️ 무료권 1장 적용 (-19,000원 할인) ➔ 15,900원</span>`;
        } else {
            payEl.innerText = "결제 예정: 34,900원";
        }
    } else if (selectedReportTier === 4) {
        const vipCost = isVIPInPerson ? 500000 : 300000;
        payEl.innerText = `결제 예정: ${vipCost.toLocaleString()}원`;
    }
}

async function executeTierOrder() {
    if (!currentStudent) return;

    // 1. VIP 원장 직접 컨설팅 신청인 경우
    if (selectedReportTier === 4) {
        const vipCost = isVIPInPerson ? 500000 : 300000;
        const consultType = isVIPInPerson ? "대면 50분 집무실 상담" : "유선 심층 전화 상담 (30~40분)";
        if (!confirm(`👑 [김철훈 원장 1:1 ${consultType}]\n\n비용: ${vipCost.toLocaleString()} PALIN 캐시\n\n신청 시 원장이 직접 24시간 내 유선으로 일정을 조율합니다. 신청하시겠습니까?`)) {
            return;
        }

        try {
            const res = await fetch("/api/consulting/vip-request", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    student_id: currentStudent.id,
                    is_in_person: isVIPInPerson,
                    preferred_phone: currentStudent.parent ? currentStudent.parent.phone : currentStudent.phone,
                    memo: "VIP 직접 컨설팅 신청"
                })
            });
            const data = await res.json();
            if (res.ok) {
                currentStudent.paid_cash = data.remaining_cash;
                updateHeaderUI();
                document.getElementById("report-tier-modal").style.display = "none";
                alert(`🎉 ${data.message}`);
            } else {
                if (res.status === 402) {
                    if (confirm("💎 캐시가 부족합니다. 캐시 충전소로 이동하시겠습니까?")) {
                        document.getElementById("report-tier-modal").style.display = "none";
                        openCashModal();
                    }
                } else {
                    alert(data.detail || "신청 실패");
                }
            }
        } catch (e) {
            console.error(e);
            alert("서버 연결 실패");
        }
        return;
    }

    // 2. AI 리포트 (Tier 1 / Tier 2 / Tier 3) 신청인 경우
    document.getElementById("report-tier-modal").style.display = "none";

    const kor = parseFloat(document.getElementById('pred-kor')?.value) || 85;
    const math = parseFloat(document.getElementById('pred-math')?.value) || 85;
    const eng = parseInt(document.getElementById('pred-eng')?.value) || 85;
    const hist = parseInt(document.getElementById('pred-hist')?.value) || 40;
    const tam1 = parseFloat(document.getElementById('pred-tam1')?.value) || 85;
    const tam2 = parseFloat(document.getElementById('pred-tam2')?.value) || 85;
    const mathType = document.getElementById('pred-math-type')?.value || '미적';
    const gyeyeol = document.getElementById('pred-gyeyeol')?.value || '이과';
    const trackChoice = document.getElementById('tier-1-track')?.value || '정시전형';

    const modal = document.getElementById("deep-report-modal");
    const content = document.getElementById("deep-report-content");
    modal.style.display = "flex";
    content.innerHTML = `<div style="text-align:center; padding: 40px;"><span class="material-symbols-rounded" style="font-size:3.2rem; color:#6366f1; animation: spin 1s infinite linear;">sync</span><div style="font-weight:900; font-size:1.15rem; margin-top:14px; color:#ffffff;">PALIN 대입 데이터 분석실에서 Tier ${selectedReportTier} 맞춤형 전략 백서를 분석/작성 중입니다... (약 10초)</div></div>`;

    try {
        const res = await fetch("/api/ai/deep-report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                kor_pct: kor,
                math_pct: math,
                eng_raw: eng,
                tam1_pct: tam1,
                tam2_pct: tam2,
                hist_raw: hist,
                gyeyeol: gyeyeol,
                math_type: mathType,
                target_univ: currentStudent.target_univ,
                baseline_univ: currentStudent.baseline_univ,
                tier: selectedReportTier,
                track_choice: trackChoice
            })
        });

        if (!res.ok) {
            const err = await res.json();
            content.innerHTML = `
                <div style="text-align: center; padding: 30px;">
                    <div style="color: #ef4444; font-weight: 800; font-size: 1.1rem; margin-bottom: 8px;">❌ 리포트 열람 실패</div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 16px;">${err.detail || "캐시가 부족합니다."}</div>
                    <button onclick="document.getElementById('deep-report-modal').style.display='none'; openCashModal();" class="btn" style="padding: 10px 20px; background: #2563eb; font-weight: 700;">💎 PALIN 캐시 충전하러 가기</button>
                </div>
            `;
            return;
        }

        const data = await res.json();
        currentStudent.paid_cash = data.remaining_cash;
        currentStudent.free_report_tickets = data.remaining_tickets;
        updateHeaderUI();

        renderDeepReport(data.report, data.used_ticket, data.charged_cost);
    } catch (e) {
        console.error(e);
        content.innerHTML = `<div style="text-align:center; color:#ef4444; padding:30px;">리포트 생성 중 통신 오류가 발생했습니다.</div>`;
    }
}

function renderDeepReport(report, usedTicket, chargedCost) {
    const content = document.getElementById("deep-report-content");
    const viewTitle = document.getElementById("report-view-title");
    if (!content || !report) return;

    const tier = report.tier || 3;
    if (viewTitle) viewTitle.innerText = `📊 Tier ${tier} 맞춤형 대입 전략 백서`;

    const chapters = report.chapters || [];
    const subjects = report.subject_strategies || {};
    const timetable = report.timetable_168h || {};

    let html = `
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 12px; padding: 16px; margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.75rem; color: #a5b4fc; font-weight: 800;">🎯 총괄 전략 디렉션 (Tier ${tier})</span>
                ${usedTicket ? '<span style="font-size:0.7rem; background:#ec4899; color:white; padding:2px 8px; border-radius:10px; font-weight:800;">🎟️ 무료권 적용</span>' : ''}
            </div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff; margin-top: 6px;">${report.summary_headline || "정시 100% 집중 포트폴리오"}</div>
            <div style="font-size: 0.85rem; color: #34d399; font-weight: 800; margin-top: 4px;">추천 전형: ${report.admission_track_recommendation || "정시 위주"}</div>
        </div>

        <!-- 대학 진단 -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 18px;">
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px;">
                <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 4px;">🎯 목표 대학 진단</div>
                <div style="font-size: 0.82rem; color: #fcd34d; font-weight: 700; line-height: 1.4;">${report.target_univ_diagnosis || "-"}</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px;">
                <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 4px;">🛡️ 마지노선 대학 분석</div>
                <div style="font-size: 0.82rem; color: #60a5fa; font-weight: 700; line-height: 1.4;">${report.baseline_univ_diagnosis || "-"}</div>
            </div>
        </div>
    `;

    // 챕터 목록
    chapters.forEach(ch => {
        html += `
            <div style="margin-bottom: 16px; background: rgba(255,255,255,0.02); padding: 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
                <div style="font-size: 0.98rem; font-weight: 800; color: #818cf8; margin-bottom: 8px;">${ch.title}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.65; white-space: pre-wrap;">${ch.content}</div>
            </div>
        `;
    });

    // Tier 3 전용 프리미엄 섹션: 168시간 시간표 & 4과목 1등급 비법
    if (tier === 3) {
        html += `
            <!-- 168시간 시간표 -->
            <div style="margin-bottom: 16px; background: rgba(16, 185, 129, 0.05); padding: 16px; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.25);">
                <div style="font-size: 1rem; font-weight: 800; color: #34d399; margin-bottom: 8px;">⏰ [🥇 Tier 3 독점] 주간 168시간 순공 극대화 타임테이블</div>
                <div style="font-size: 0.85rem; color: #e2e8f0; margin-bottom: 6px;">📅 <strong>평일 루틴:</strong> ${timetable.weekday || ""}</div>
                <div style="font-size: 0.85rem; color: #e2e8f0; margin-bottom: 6px;">🔥 <strong>주말 몰입:</strong> ${timetable.weekend || ""}</div>
                <div style="font-size: 0.82rem; color: #a7f3d0; font-weight: 700;">과목별 배분: ${timetable.ratios || ""}</div>
            </div>

            <!-- 과목별/시험별 만점 비법 -->
            <div style="margin-bottom: 16px; background: rgba(245, 158, 11, 0.05); padding: 16px; border-radius: 10px; border: 1px solid rgba(245, 158, 11, 0.25);">
                <div style="font-size: 1rem; font-weight: 800; color: #fbbf24; margin-bottom: 10px;">📖 [🥇 Tier 3 독점] 과목별 · 시험별 만점 극대화 비법 지침</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.6;">
                    • <strong>국어:</strong> ${subjects.korean || ""}<br>
                    • <strong>수학:</strong> ${subjects.math || ""}<br>
                    • <strong>영어:</strong> ${subjects.english || ""}<br>
                    • <strong>탐구:</strong> ${subjects.tamgu || ""}
                </div>
            </div>
        `;
    }

    // 원장님 결의 메시지
    if (report.mentor_closing) {
        html += `
            <div style="font-size: 0.85rem; font-style: italic; color: #fca5a5; background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); padding: 12px 16px; border-radius: 8px;">
                "${report.mentor_closing}"
            </div>
        `;
    }

    content.innerHTML = html;
}

// ==========================================
// 🔗 4. 친구 초대 & 무료권 모달
// ==========================================

function openReferralModal() {
    if (!currentStudent) return;
    const modal = document.getElementById("referral-modal");
    if (!modal) return;
    document.getElementById("referral-my-code").innerText = currentStudent.referral_code || `PL-${String(currentStudent.id).padStart(4, '0')}`;
    document.getElementById("referral-ticket-count").innerText = currentStudent.free_report_tickets || 0;
    modal.style.display = "flex";
}

function copyReferralLink() {
    if (!currentStudent) return;
    const code = currentStudent.referral_code || `PL-${String(currentStudent.id).padStart(4, '0')}`;
    const textToCopy = `[PALIN OS] 목표 대학 27학번 가상 학생증 발급 & 19,000원 입시 심층 리포트 무료권 획득!\n가입할 때 내 초대코드 [ ${code} ] 를 입력하면 500P 웰컴 보너스 즉시 지급!\n👉 접속: https://palin-os.onrender.com`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert(`🔗 초대 링크와 코드(${code})가 클립보드에 복사되었습니다!\n친구들에게 카카오톡으로 공유해 보세요!`);
    }).catch(() => {
        prompt("아래 초대 텍스트를 복사하세요:", textToCopy);
    });
}

// ==========================================
// 💎 5. PALIN 캐시 충전 모달
// ==========================================

function openCashModal() {
    if (!currentStudent) return;
    const modal = document.getElementById("cash-modal");
    if (!modal) return;
    document.getElementById("cash-modal-balance").innerText = (currentStudent.paid_cash || 0).toLocaleString();
    modal.style.display = "flex";
}

async function chargeCash(amount) {
    if (!currentStudent) return;
    if (!confirm(`💎 ${amount.toLocaleString()}원 상당의 PALIN 캐시를 충전하시겠습니까?`)) return;

    try {
        const res = await fetch("/api/cash/charge", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ student_id: currentStudent.id, amount: amount })
        });
        const data = await res.json();
        if (data.status === "ok") {
            currentStudent.paid_cash = data.paid_cash;
            updateHeaderUI();
            alert(data.message);
        } else {
            alert(data.detail || "충전 실패");
        }
    } catch (e) {
        console.error(e);
        alert("충전 서버 연결 오류");
    }
}

// ==========================================
// ⚖️ 6. 이용약관 & 개인정보 동의서 전문 모달
// ==========================================

function openTermsModal(type) {
    const modal = document.getElementById("terms-modal");
    const title = document.getElementById("terms-modal-title");
    const body = document.getElementById("terms-modal-body");
    if (!modal || !title || !body) return;

    if (type === "terms") {
        title.innerText = "📜 PALIN OS 서비스 이용약관";
        body.innerText = `[제1조 목적]
본 약관은 PALIN OS(이하 '회사/학원')가 제공하는 학습 행동 통제, 대입 예측 및 1:1 과외 매칭 서비스의 이용 조건 및 절차를 규정합니다.

[제2조 원장의 회원 제재 및 강제 퇴거 권한]
1. 회원은 학원의 학습 분위기 저해, 무단결석, 딴짓 방조, 타 회원에 대한 불쾌감 조성 시 원장의 직권으로 즉시 경고 또는 영구 계정 제재(강제 퇴거 및 블랙리스트 등록) 처분을 받을 수 있습니다.
2. 강제 퇴거된 회원은 동일한 이메일 및 전화번호로 재가입이 영구 금지됩니다.

[제3조 유료 결제 및 환불 규정]
1. PALIN 캐시 및 1:1 과외 매칭 요청서, AI 심층 리포트 등 디지털 콘텐츠는 열람 또는 매칭 정보 제공 즉시 서비스가 완료된 것으로 간주되어 환불이 제한됩니다.
2. 단순 변심에 의한 환불은 디지털 콘텐츠 특성상 전자상거래법에 의거하여 제한될 수 있습니다.`;
    } else {
        title.innerText = "🔒 개인정보 수집·이용 및 학부모 문자 발송 동의서";
        body.innerText = `[1. 수집 항목]
- 필수항목: 학생 이름, 이메일, 휴대전화번호, 학교, 학년, 목표 대학, 학부모 이름, 학부모 휴대전화번호
- 학습데이터: 기상/취침 미션 인증 사진 및 시간, 순공 타이머 기록, 모의고사 성적

[2. 수집 및 이용 목적]
- 수험생 일일 생활 패턴 및 자습 몰입도 AI 분석
- 기상 실패, 딴짓 발생 시 학부모 휴대전화로 실시간 SMS/알림톡 발송
- 맞춤형 1:1 과외 선생님 매칭 및 대입 예측 서비스 제공

[3. 보유 및 이용 기간]
- 회원 탈퇴 시 또는 입시 종료 시까지 안전하게 보관 후 파기됩니다.`;
    }

    modal.style.display = "flex";
}

// ==========================================
// 🎓 7. 과외선생님 1:1 매칭 신청
// ==========================================

async function requestTutorMatch(tutorId) {
    if (!currentStudent) return;
    if (!confirm("🎓 해당 과외선생님에게 1:1 매칭 요청서를 발송하시겠습니까?\n(필요 캐시: 29,000 PALIN 캐시 차감)")) return;

    try {
        const res = await fetch("/api/tutor/request-match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ student_id: currentStudent.id, tutor_id: tutorId })
        });
        const data = await res.json();
        if (data.status === "ok") {
            currentStudent.paid_cash = data.remaining_cash;
            updateHeaderUI();
            alert(`🎉 ${data.message}\n선생님 카카오톡 링크: ${data.tutor_contact}\n연락처: ${data.tutor_phone}`);
        } else {
            if (res.status === 402) {
                if (confirm("💎 캐시가 부족합니다. 캐시 충전소로 이동하시겠습니까?")) {
                    openCashModal();
                }
            } else {
                alert(data.detail || "매칭 요청 실패");
            }
        }
    } catch (e) {
        console.error(e);
        alert("서버 연결 실패");
    }
}

// ==========================================
// 🏆 8. 마이크로 지역/고교 랭킹 리더보드 (Strava 모델)
// ==========================================

async function loadMicroRankings() {
    const listEl = document.getElementById("micro-ranking-list");
    if (!listEl) return;
    
    const myRegion = currentStudent?.region || "성남시 분당구";
    const mySchool = currentStudent?.high_school || "낙생고등학교";
    
    document.getElementById("my-ranking-region-name").innerText = myRegion;
    document.getElementById("my-ranking-school-name").innerText = mySchool;
    
    // 시뮬레이션 및 실시간 랭킹 목록 렌더링
    const dummyRankers = [
        { rank: 1, name: currentStudent?.name || "나", school: mySchool, region: myRegion, studyHours: "14시간 20분", streak: 18, isMe: true },
        { rank: 2, name: "이*준", school: mySchool, region: myRegion, studyHours: "13시간 50분", streak: 14, isMe: false },
        { rank: 3, name: "박*우", school: "분당대진고", region: myRegion, studyHours: "12시간 40분", streak: 12, isMe: false },
        { rank: 4, name: "최*진", school: "서현고", region: myRegion, studyHours: "11시간 10분", streak: 9, isMe: false },
        { rank: 5, name: "정*원", school: "중앙고", region: myRegion, studyHours: "10시간 30분", streak: 8, isMe: false }
    ];
    
    listEl.innerHTML = "";
    dummyRankers.forEach(r => {
        const medal = r.rank === 1 ? "🥇" : (r.rank === 2 ? "🥈" : (r.rank === 3 ? "🥉" : `${r.rank}위`));
        const bg = r.isMe ? "rgba(234, 179, 8, 0.15)" : "rgba(255,255,255,0.03)";
        const border = r.isMe ? "1.5px solid #eab308" : "1px solid rgba(255,255,255,0.06)";
        
        listEl.innerHTML += `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: ${bg}; border-radius: 8px; border: ${border};">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-weight: 800; font-size: 0.95rem; min-width: 24px;">${medal}</span>
                    <div>
                        <div style="font-weight: 700; font-size: 0.85rem; color: #ffffff;">
                            ${r.name} ${r.isMe ? '<span style="font-size:0.68rem; background:#eab308; color:#000; padding:1px 6px; border-radius:8px; font-weight:800; margin-left:4px;">ME</span>' : ''}
                        </div>
                        <div style="font-size: 0.72rem; color: var(--text-secondary);">${r.school} · ${r.region}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.82rem; font-weight: 800; color: #fbbf24;">${r.studyHours}</div>
                    <div style="font-size: 0.68rem; color: #34d399;">연속 ${r.streak}일 달성 🔥</div>
                </div>
            </div>
        `;
    });
}

// ==========================================
// 👑 9. VIP 1% 블랙 라운지
// ==========================================

async function loadBlackLoungePosts() {
    const container = document.getElementById("black-lounge-posts-container");
    if (!container) return;
    
    try {
        const res = await fetch("/api/black-lounge/posts");
        if (res.ok) {
            const posts = await res.json();
            container.innerHTML = "";
            if (posts.length === 0) {
                container.innerHTML = "<div style='text-align:center; color:#94a3b8; font-size:0.8rem; padding:16px;'>등록된 VIP 게시글이 없습니다. 첫 질문을 남겨보세요!</div>";
            } else {
                posts.forEach(p => {
                    container.innerHTML += `
                        <div style="padding: 12px; background: rgba(255,255,255,0.03); border-radius: 8px; border: 1px solid rgba(217, 119, 6, 0.25);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <div style="font-weight: 800; font-size: 0.85rem; color: #f59e0b;">${p.title}</div>
                                <span style="font-size: 0.7rem; color: #64748b;">${p.created_at}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #e2e8f0; line-height: 1.45; white-space: pre-wrap; margin-bottom: 6px;">${p.content}</div>
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: var(--text-secondary);">
                                <span>✍️ ${p.author_name} (${p.author_univ_target || '의치한약수/SKY 목표'})</span>
                                <span style="color: #fbbf24; font-weight: 700;">멘토 피드백 대기중 💬</span>
                            </div>
                        </div>
                    `;
                });
            }
        }
    } catch (e) {
        console.warn(e);
    }
}

async function submitBlackLoungePost() {
    const title = document.getElementById("black-post-title")?.value.trim();
    const content = document.getElementById("black-post-content")?.value.trim();
    if (!title || !content) {
        alert("제목과 내용을 모두 입력해 주세요.");
        return;
    }
    if (!currentStudent) {
        alert("로그인이 필요합니다.");
        return;
    }

    try {
        const res = await fetch("/api/black-lounge/posts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                title: title,
                content: content
            })
        });
        if (res.ok) {
            alert("👑 VIP 블랙 라운지에 질문이 등록되었습니다!");
            document.getElementById("black-post-title").value = "";
            document.getElementById("black-post-content").value = "";
            loadBlackLoungePosts();
        } else {
            const err = await res.json();
            alert(err.detail || "작성 실패");
        }
    } catch (e) {
        alert("서버 통신 오류");
    }
}

// ==========================================
// 🛡️ 10. 금융 인질 에스크로 잔액 조회
// ==========================================

async function fetchEscrowStatus(studentId) {
    try {
        const res = await fetch(`/api/escrow/status/${studentId}`);
        if (res.ok) {
            const data = await res.json();
            const depEl = document.getElementById("mypage-escrow-deposit");
            const dedEl = document.getElementById("mypage-escrow-deductions");
            if (depEl) depEl.innerText = `${(data.escrow_deposit || 50000).toLocaleString()}원`;
            if (dedEl) dedEl.innerText = `${(data.escrow_deductions || 0).toLocaleString()}원`;
        }
    } catch (e) { console.warn("Escrow status error:", e); }
}
