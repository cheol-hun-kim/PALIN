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
document.addEventListener("DOMContentLoaded", async () => {
    initPALINThemeEngine();
    await fetchUnivData();
    checkAuth();
    setupEventListeners();
    setupDistractionDetection();
    setupUnivDeptSelectors("reg-target-univ", "reg-target-dept");
    setupUnivDeptSelectors("reg-baseline-univ", "reg-baseline-dept");
    setupUnivDeptSelectors("tutor-up-univ", "tutor-up-major");
    
    document.getElementById("theme-toggle-btn")?.addEventListener("click", togglePALINTheme);
});

// PALIN OS 타임라인 기반 자동 테마 전환 엔진 (06시~21시: 데이 모드, 21시~06시: 딥 블랙 야간 모드)
function initPALINThemeEngine() {
    const hour = new Date().getHours();
    const savedTheme = localStorage.getItem("palinTheme");
    if (savedTheme === "day" || (savedTheme === null && hour >= 6 && hour < 21)) {
        document.body.classList.add("day-mode");
    } else {
        document.body.classList.remove("day-mode");
    }
}

function togglePALINTheme() {
    document.body.classList.toggle("day-mode");
    const isDay = document.body.classList.contains("day-mode");
    localStorage.setItem("palinTheme", isDay ? "day" : "night");
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
    if (studentId) {
        fetchStudentInfo(studentId);
    } else {
        showOverlay("register-overlay");
    }
}

function showOverlay(id) {
    document.querySelectorAll(".loader-overlay").forEach(el => el.style.display = "none");
    document.getElementById(id).style.display = "flex";
}

function hideOverlay(id) {
    document.getElementById(id).style.display = "none";
}

// --- 딴짓 감지 모듈 (OS 화면 꺼짐 허용 & 타 앱 전환 감지 고도화) ---
let isScreenOffGrace = false;
let screenOffCheckTimeout = null;

function setupDistractionDetection() {
    // 1. 화면 꺼짐(Screen Off) vs 타 앱 전환(App Switch) 구분 로직
    document.addEventListener("visibilitychange", () => {
        if (!isTimerRunning) return;

        if (document.visibilityState === "hidden") {
            // 모바일 화면 꺼짐일 수 있으므로 1.5초 유예 타이머 시작
            isScreenOffGrace = true;
            screenOffCheckTimeout = setTimeout(() => {
                // 백그라운드에서 타임스탬프 계산이 계속 유지되므로 화면 꺼짐 상태는 정상 자습 누적 인정!
                isScreenOffGrace = false;
            }, 1500);
        } else if (document.visibilityState === "visible") {
            if (screenOffCheckTimeout) {
                clearTimeout(screenOffCheckTimeout);
                screenOffCheckTimeout = null;
            }
            isScreenOffGrace = false;
        }
    });

    // 2. 화면이 켜진 상태에서 타 브라우저 탭/타 앱으로 포커스 이탈 시 명백한 딴짓으로 판정
    window.addEventListener("blur", () => {
        if (isTimerRunning && !isScreenOffGrace) {
            // 사용자가 화면이 켜진 상태에서 다른 창이나 앱을 조작한 경우
            setTimeout(() => {
                if (isTimerRunning && document.hasFocus && !document.hasFocus()) {
                    isDistracted = true;
                    pauseTimerOnDistraction();
                }
            }, 500);
        }
    });
}

function pauseTimerOnDistraction() {
    triggerLogoCrackEffect(); // 🌲 포레스트 목표 대학 로고 균열 애니메이션
    alert("⚠️ [딴짓 감지!] 집중 타이머 측정 중 다른 앱으로 전환하여 목표 대학 로고에 금이 가고 측정이 강제 종료되었습니다. 학부모님께 경고 메시지가 전달됩니다.");
    stopTimerForcefully(true);
}


// --- API 연동 함수들 ---

async function fetchStudentInfo(studentId) {
    try {
        const res = await fetch(`/api/student/${studentId}`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            if (res.status === 403) {
                alert(`⚠️ ${err.detail || "원장님에 의해 이용이 정지/퇴거된 계정입니다. 학원 집무실로 문의해 주세요."}`);
            }
            localStorage.removeItem("studentId");
            showOverlay("register-overlay");
            return;
        }
        currentStudent = await res.json();
        
        // 학부모 프리미엄 구독 여부 가져오기
        try {
            const pRes = await fetch(`/api/student/${studentId}/parent`);
            const parent = await pRes.json();
            currentStudent.parent = parent;
        } catch (pe) {
            console.warn("학부모 정보 로드 실패:", pe);
        }

        // 인증 성공 → 즉시 오버레이 숨김 (이후 데이터 로드 실패와 무관)
        hideOverlay("register-overlay");

        // UI 업데이트 (개별 try-catch로 하나가 실패해도 나머지 진행)
        try { updateHeaderUI(); } catch(e) { console.warn("updateHeaderUI:", e); }
        try { updateTargetBanner(); } catch(e) { console.warn("updateTargetBanner:", e); }
        try { await fetchLeagueStatus(studentId); } catch(e) { console.warn("fetchLeagueStatus:", e); }
        try { updateStudentUnivSelectors(); } catch(e) { console.warn("updateStudentUnivSelectors:", e); }
        
        // 데이터 로드
        try { fetchNotices(); } catch(e) { console.warn("fetchNotices:", e); }
        try { fetchMicroLeague(studentId); } catch(e) { console.warn("fetchMicroLeague:", e); }
        try { renderAdmissionCalendar(); } catch(e) { console.warn("renderAdmissionCalendar:", e); }
        try { loadPage1Data(); } catch(e) { console.warn("loadPage1Data:", e); }
        try { loadPage2Data(); } catch(e) { console.warn("loadPage2Data:", e); }
        try { loadPage3Data(); } catch(e) { console.warn("loadPage3Data:", e); }
    } catch (e) {
        console.error("인증 실패:", e);
        localStorage.removeItem("studentId");
        showOverlay("register-overlay");
    }
}

// 1. 회원가입 제출
async function handleRegister(e) {
    e.preventDefault();
    const targetUniv = document.getElementById("reg-target-univ").value;
    const targetDept = document.getElementById("reg-target-dept").value;
    const baselineUniv = document.getElementById("reg-baseline-univ").value;
    const baselineDept = document.getElementById("reg-baseline-dept").value;
    
    if (!targetUniv || !targetDept || !baselineUniv || !baselineDept) {
        alert("목표 대학/학과 및 마지노선 대학/학과를 모두 선택해 주세요.");
        return;
    }

    const privacyCheck = document.getElementById("reg-privacy-check");
    if (privacyCheck && !privacyCheck.checked) {
        alert("개인정보 수집·이용 동의서 항목에 동의해주셔야 가입 및 서비스 이용이 가능합니다.");
        return;
    }

    const payload = {
        email: document.getElementById("reg-email").value,
        name: document.getElementById("reg-name").value,
        phone: document.getElementById("reg-phone").value,
        grade: parseInt(document.getElementById("reg-grade").value),
        region: document.getElementById("reg-region").value,
        high_school: document.getElementById("reg-school").value,
        target_univ: `${targetUniv} ${targetDept}`,
        baseline_univ: `${baselineUniv} ${baselineDept}`,
        parent_name: document.getElementById("reg-pname").value,
        parent_phone: document.getElementById("reg-pphone").value
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
    } catch (e) {
        alert("서버 연결 실패");
    }
}

function toggleLoginForm() {
    const regForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const toggleArea = regForm.nextElementSibling; // the toggle button div
    if (loginForm.style.display === "none") {
        regForm.style.display = "none";
        if (toggleArea && toggleArea.tagName !== "FORM") toggleArea.style.display = "none";
        loginForm.style.display = "block";
    } else {
        loginForm.style.display = "none";
        regForm.style.display = "block";
        if (toggleArea && toggleArea.tagName !== "FORM") toggleArea.style.display = "block";
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById("login-email").value.trim();
    if (!email) {
        alert("이메일을 입력해 주세요.");
        return;
    }
    try {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email })
        });
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || "로그인 실패");
            return;
        }
        const student = await res.json();
        localStorage.setItem("studentId", student.id);
        fetchStudentInfo(student.id);
    } catch (e) {
        alert("서버 연결 실패");
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
    if (!dateStr) return "D-250";
    try {
        const target = new Date(dateStr);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        target.setHours(0, 0, 0, 0);
        const diffTime = target - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        if (diffDays > 0) return `D-${diffDays}`;
        if (diffDays === 0) return "D-DAY";
        return `D+${Math.abs(diffDays)}`;
    } catch (e) {
        return "D-250";
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
    document.getElementById("header-points").innerText = `${currentStudent.current_points} P`;
    document.getElementById("header-student-name").innerText = `${currentStudent.name} 학생`;
    
    // 🔥 듀오링고 불꽃 (Streak) 렌더링
    const streakEl = document.getElementById("header-streak-count");
    if (streakEl) {
        const count = currentStudent.streak_days || 0;
        streakEl.innerText = `${count}일 연속`;
    }

    // 마이페이지 모달 정보 갱신
    const fullname = document.getElementById("mypage-student-fullname");
    if (fullname) fullname.innerText = `${currentStudent.name} 학생`;
    const sub = document.getElementById("mypage-student-sub");
    const gradeText = currentStudent.grade === 4 ? "N수생" : currentStudent.grade === 0 ? "기타" : `${currentStudent.grade}학년`;
    if (sub) sub.innerText = `${currentStudent.high_school || "학교미설정"} ${gradeText} | ${currentStudent.region || "지역미설정"}`;

    // 메인화면 미션 라벨 업데이트
    const wakeLabel = document.getElementById("mission-wakeup-label");
    if (wakeLabel) wakeLabel.innerText = `🌅 기상 미션 (${currentStudent.wake_target_time || "06:30"})`;
    const sleepLabel = document.getElementById("mission-sleep-label");
    if (sleepLabel) sleepLabel.innerText = `🌃 취침 미션 (${currentStudent.sleep_target_time || "23:30"})`;

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
                    <div style="font-weight: 700; font-size: 0.88rem; color: #f8fafc;">${item.title}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">📅 ${item.date} (${item.cat})</div>
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
        document.getElementById("edit-region").value = currentStudent.region || "";
        document.getElementById("edit-grade").value = currentStudent.grade !== undefined ? currentStudent.grade : "3";
        document.getElementById("edit-medical-symbol").value = currentStudent.medical_symbol || "GENERAL";
        document.getElementById("edit-dday-title").value = currentStudent.dday_title || "2027 수능";
        document.getElementById("edit-dday-date").value = currentStudent.dday_date || "2026-11-19";
        document.getElementById("edit-wake-time").value = currentStudent.wake_target_time || "06:30";
        document.getElementById("edit-sleep-time").value = currentStudent.sleep_target_time || "23:30";

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
    const region = document.getElementById("edit-region").value.trim();
    const grade = parseInt(document.getElementById("edit-grade").value);
    const medicalSymbol = document.getElementById("edit-medical-symbol").value;
    const ddayTitle = document.getElementById("edit-dday-title").value.trim();
    const ddayDate = document.getElementById("edit-dday-date").value;
    const wakeTime = document.getElementById("edit-wake-time").value;
    const sleepTime = document.getElementById("edit-sleep-time").value;

    const tUniv = document.getElementById("edit-target-univ-select")?.value;
    const tDept = document.getElementById("edit-target-dept-select")?.value;
    const bUniv = document.getElementById("edit-baseline-univ-select")?.value;
    const bDept = document.getElementById("edit-baseline-dept-select")?.value;

    const targetUniv = (tUniv && tDept) ? `${tUniv} ${tDept}` : currentStudent.target_univ;
    const baselineUniv = (bUniv && bDept) ? `${bUniv} ${bDept}` : currentStudent.baseline_univ;

    try {
        const res = await fetch("/api/student/profile", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
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
    if (confirm("로그아웃 하시겠습니까? 계정이 변경되거나 신규 로그인 창으로 이동합니다.")) {
        localStorage.removeItem("studentId");
        closeMyPageModal();
        showOverlay("register-overlay");
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
    }
}

function switchSubTabPage3(subTab) {
    activeSubTabPage3 = subTab;
    document.querySelectorAll(".subtab-view-p3").forEach(el => el.style.display = "none");
    document.getElementById(`p3-${subTab}`).style.display = "block";

    document.querySelectorAll("#p3-tabs .tab-btn").forEach(el => el.classList.remove("active"));
    document.querySelector(`#p3-tabs .tab-btn[data-sub="${subTab}"]`).classList.add("active");
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
            document.getElementById("tutor-my-univ-badge").innerText = currentStudent.tutor_profile.univ_emblem;
            document.getElementById("tutor-my-school-badge").innerText = currentStudent.tutor_profile.high_school_emblem;
            document.getElementById("edit-tutor-bio").value = currentStudent.tutor_profile.bio;
            document.getElementById("edit-tutor-link").value = currentStudent.tutor_profile.contact_link;
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

async function loadTimetable() {
    if (!currentStudent) return;
    try {
        const res = await fetch(`/api/planner/blocks/${currentStudent.id}`);
        const blocks = await res.json();
        
        const dayColumns = [
            document.getElementById("col-day-0"),
            document.getElementById("col-day-1"),
            document.getElementById("col-day-2"),
            document.getElementById("col-day-3"),
            document.getElementById("col-day-4"),
            document.getElementById("col-day-5"),
            document.getElementById("col-day-6")
        ];
        
        dayColumns.forEach(col => {
            if (col) col.innerHTML = "";
        });

        const timerSelect = document.getElementById("timer-schedule-select");
        timerSelect.innerHTML = "<option value='none'>직접 자유 공부하기</option>";

        blocks.forEach((block, index) => {
            const col = dayColumns[block.day_of_week];
            if (!col) return;

            const startParts = block.start_time.split(":");
            const endParts = block.end_time.split(":");
            
            const startHour = parseInt(startParts[0]) + parseInt(startParts[1])/60;
            const endHour = parseInt(endParts[0]) + parseInt(endParts[1])/60;
            
            const topPx = (startHour - 9) * 30;
            const heightPx = (endHour - startHour) * 30;
            
            const colorClass = `color-${index % 7}`;

            const blockEl = document.createElement("div");
            blockEl.className = `timetable-block ${colorClass}`;
            blockEl.style.top = `${topPx}px`;
            blockEl.style.height = `${heightPx}px`;
            blockEl.innerHTML = `
                <div class="block-title">${block.title}</div>
                <div class="block-time">${block.start_time}~${block.end_time}</div>
                <button class="btn-delete-block" onclick="deletePlannerBlock(event, ${block.id})">&times;</button>
            `;
            col.appendChild(blockEl);

            timerSelect.innerHTML += `<option value="${block.id}" data-title="${block.title}">${block.title} (${block.start_time}~${block.end_time})</option>`;
        });
    } catch (e) {
        console.error("시간표 로드 오류:", e);
    }
}

async function addPlannerBlock(e) {
    e.preventDefault();
    if (!currentStudent) return;
    
    const day = parseInt(document.getElementById("plan-day").value);
    const start = document.getElementById("plan-start").value;
    const end = document.getElementById("plan-end").value;
    const title = document.getElementById("plan-title").value.trim();

    if (!start || !end || !title) {
        alert("시간 및 계획명을 모두 기입해 주세요.");
        return;
    }

    if (start >= end) {
        alert("종료 시간은 시작 시간보다 늦어야 합니다.");
        return;
    }

    if (start < "09:00" || end > "24:00") {
        alert("공부 계획표는 아침 09:00부터 밤 24:00까지만 계획할 수 있습니다.");
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
            document.getElementById("plan-title").value = "";
            loadTimetable();
        }
    } catch (e) {
        console.error(e);
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
            alert(`🎉 미션 성공! +${result.earned_points}P 적립되었습니다.`);
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

async function toggleTimer() {
    if (isTimerRunning) {
        stopTimerForcefully(false);
    } else {
        startTimer();
    }
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
        
        timerSeconds = 0;
        const circle = document.getElementById("timer-circle");
        circle.classList.add("active");
        
        const timerBtn = document.getElementById("timer-toggle-btn");
        timerBtn.innerText = "집중 종료";
        timerBtn.style.backgroundColor = "var(--color-danger)";
        
        document.getElementById("timer-current-study").innerText = `🎯 진행 중: ${studyTitle}`;
        
        timerInterval = setInterval(() => {
            timerSeconds++;
            const hrs = String(Math.floor(timerSeconds / 3600)).padStart(2, '0');
            const mins = String(Math.floor((timerSeconds % 3600) / 60)).padStart(2, '0');
            const secs = String(timerSeconds % 60).padStart(2, '0');
            circle.innerText = `${hrs}:${mins}:${secs}`;
        }, 1000);
    } catch (e) {
        alert("타이머 시작 실패");
    }
}

async function stopTimerForcefully(triggeredByDistraction = false) {
    if (!isTimerRunning) return;
    
    clearInterval(timerInterval);
    timerInterval = null;
    isTimerRunning = false;
    
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
            alert(`⚠️ 집중 중 딴짓이 기록되었습니다. 포인트가 지급되지 않으며 학부모님께 즉시 문자가 발송되었습니다. (sms_log.txt 파일 확인)`);
        } else {
            alert(`⏱️ 정상 공부 완료! ${Math.floor(session.duration_sec/60)}분간 정상 집중하여 포인트가 정산 지급되었습니다.`);
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
            appendChatBubble("bot", `⚠️ ${errMsg}`);
            return;
        }
        
        const data = await res.json();
        appendChatBubble("bot", data.reply);
        
        // 대화 기록에 봇 응답 추가
        chatHistory.push({ role: "bot", content: data.reply });
        
        document.getElementById("chat-limit-label").innerText = `오늘 남은 무료 대화: ${data.remaining_chats}회`;
    } catch (e) {
        console.error("Chat error:", e);
        appendChatBubble("bot", `서버 연결 오류: ${e.message || "네트워크 문제"}`);
    }
}

function appendChatBubble(sender, text) {
    const container = document.getElementById("chat-box");
    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", sender);
    bubble.innerText = text;
    
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
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
    const kor = parseFloat(document.getElementById('pred-kor').value);
    const math = parseFloat(document.getElementById('pred-math').value);
    const eng = parseInt(document.getElementById('pred-eng').value);
    const hist = parseInt(document.getElementById('pred-hist').value);
    const tam1 = parseFloat(document.getElementById('pred-tam1').value);
    const tam2 = parseFloat(document.getElementById('pred-tam2').value);
    const mathType = document.getElementById('pred-math-type').value;
    const gyeyeol = document.getElementById('pred-gyeyeol').value;
    
    if (isNaN(kor) || isNaN(math) || isNaN(eng) || isNaN(tam1) || isNaN(tam2) || isNaN(hist)) {
        alert('모든 성적을 입력해주세요.');
        return;
    }
    
    // Show loading
    document.getElementById('predict-result').style.display = 'block';
    document.getElementById('pred-results-list').innerHTML = '<div style="text-align:center; padding: 20px;">분석 중...</div>';
    
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
                gyeyeol: gyeyeol,
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

    try {
        const res = await fetch("/api/qa/post", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: currentStudent.id,
                subject,
                title,
                content,
                reward_points: reward
            })
        });
        if (res.ok) {
            alert("질문이 업로드되었습니다.");
            document.getElementById("qa-post-title").value = "";
            document.getElementById("qa-post-content").value = "";
            document.getElementById("qa-post-reward").value = "0";
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
                    
                    <div style="font-size:0.75rem; color:var(--text-secondary); display:flex; justify-content:space-between; align-items:center; margin-top: 4px;">
                        <span>학적 및 생기부 검증 완료 ✅</span>
                        <button class="btn" style="padding: 4px 10px; font-size:0.7rem;" onclick="requestTutorDirect(${tutor.id})">과외 신청 (150P)</button>
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

// --- 대학 및 학과 동적 목록 데이터 ---
let UNIVERSITY_DEPARTMENTS = {};

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

// --- 대학교 학과 드롭다운 연결 헬퍼 ---
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

        depts.forEach(dept => {
            const opt = document.createElement("option");
            opt.value = dept;
            opt.textContent = dept;
            if (dept === cleanInitDept) opt.selected = true;
            deptSelect.appendChild(opt);
        });
        if (cleanInitDept && depts.includes(cleanInitDept)) {
            deptSelect.value = cleanInitDept;
        }
    } else {
        deptSelect.innerHTML = `<option value="" disabled selected>학과 선택</option>`;
    }
}

// === 수시/정시 탭 전환 ===
function switchAdmissionTab(tab) {
    const susiSection = document.getElementById('susi-section');
    const jeongsiSection = document.getElementById('jeongsi-section');
    const btnSusi = document.getElementById('btn-susi');
    const btnJeongsi = document.getElementById('btn-jeongsi');
    
    if (tab === 'susi') {
        susiSection.style.display = 'block';
        jeongsiSection.style.display = 'none';
        btnSusi.className = 'btn';
        btnSusi.style.background = 'linear-gradient(135deg, #6366f1, #8b5cf6)';
        btnJeongsi.className = 'btn btn-secondary';
        btnJeongsi.style.background = '';
    } else {
        susiSection.style.display = 'none';
        jeongsiSection.style.display = 'block';
        btnJeongsi.className = 'btn';
        btnJeongsi.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        btnSusi.className = 'btn btn-secondary';
        btnSusi.style.background = '';
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
