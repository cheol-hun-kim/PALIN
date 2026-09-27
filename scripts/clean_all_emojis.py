# -*- coding: utf-8 -*-
import os, sys, re

# Emoji replacement dictionary for key UI components to replace with clean Material Symbols or pure text
EMOJI_REPLACEMENTS = {
    # Double icon removals & specific phrases
    "📊 이번 주 학부모 안심 정밀 진단 리포트": "이번 주 학부모 안심 정밀 진단 리포트",
    "❓ 공부 Q&A": "공부 Q&A",
    "🎓 선배 과외": "선배 과외",
    "🏆 동네/학교 랭킹": "동네/학교 랭킹",
    "👑 1% 라운지": "1% 라운지",
    "📡 실시간 Wi-Fi 출결 로그": "실시간 Wi-Fi 출결 로그",
    "📡 학원 Wi-Fi 공인 IP 설정": "학원 Wi-Fi 공인 IP 설정",
    "🔑 내 학원 초대 코드": "내 학원 초대 코드",
    "⚡ 재원생 일괄 청구서 생성": "재원생 일괄 청구서 생성",
    "🏦 정산 계좌 설정": "정산 계좌 설정",
    "📨 당월 총 청구액": "당월 총 청구액",
    "💳 실시간 수납완료": "실시간 수납완료",
    "🚨 미납 / 인질 잠김": "미납 / 인질 잠김",
    "🏦 원장 실입금 정산액": "원장 실입금 정산액",
    "📋 전체 청구서": "전체 청구서",
    "✨ 수납완료": "수납완료",
    "🚨 미납 / 연체": "미납 / 연체",
    "📑 선택 청구서 알림톡 재발송": "선택 청구서 알림톡 재발송",
    "✅ 선택 수납 완료 처리": "선택 수납 완료 처리",
    "📋 현재 게시 중인 학사일정 & 특별 공지사항 목록": "현재 게시 중인 학사일정 & 특별 공지사항 목록",
    "📁 [우리 학원 재원생 전용] 학습자료 & 워크북/자체 모의고사 업로드": "[우리 학원 재원생 전용] 학습자료 & 워크북/자체 모의고사 업로드",
    "🎯 대상 학년": "대상 학년",
    "💻 과목 영역": "과목 영역",
    "📝 자료명 / 워크북 제목": "자료명 / 워크북 제목",
    "💬 상세 설명 & 과제 안내": "상세 설명 & 과제 안내",
    "📄 문제지 파일 (PDF/HWP 첨부 또는 다운로드 링크)": "문제지 파일 (PDF/HWP 첨부 또는 다운로드 링크)",
    "🔑 정답/해설지 파일 (PDF/HWP 첨부 또는 링크)": "정답/해설지 파일 (PDF/HWP 첨부 또는 링크)",
    "🔒 [모델하우스 체험 모드]": "[체험 모드]",
    "👑 [총괄 제작자 마스터 계정]": "[마스터 계정]",
    "🏫 [우리 학원]": "[우리 학원]",
}

# General standalone emoji stripper regex for Korean UI elements
# Matches emojis at the start of span/div/button text, e.g. "<span>🚨 텍스트</span>" -> "<span>텍스트</span>"
pattern_bracket_emoji = re.compile(r'<!--\s*[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\u2b50-\u2b55]\s*')
pattern_tag_lead_emoji = re.compile(r'(>)\s*([\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\u2b50-\u2b55\u2705\u274c\u2728\u26a0\ufe0f]+)\s*([가-힣A-Za-z0-9\[])')
pattern_alert_emoji = re.compile(r'(alert\(["\'])\s*[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\u2b50-\u2b55\u2705\u274c\u2728\u26a0\ufe0f]+\s*')

target_files = ['static/index.html', 'static/admin.html', 'static/master.html', 'static/js/app.js']

for filepath in target_files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Apply explicit replacements
    for k, v in EMOJI_REPLACEMENTS.items():
        content = content.replace(k, v)

    # 2. Apply tag leading emoji stripper
    content = pattern_tag_lead_emoji.sub(r'\1\3', content)
    content = pattern_alert_emoji.sub(r'\1', content)

    # Remove remaining common emojis from UI buttons/spans
    raw_emojis = [
        "📊", "❓", "🎓", "🏆", "👑", "📡", "🔑", "⚡", "🏦", "📨", "💳", "🚨", "📋", "✨",
        "📑", "✅", "📁", "🎯", "💻", "📝", "💬", "📄", "🔒", "🏫", "🌟", "⚠️", "💡", "🏢",
        "🔥", "👋", "🎉", "✉️", "⏱️", "✏️", "🗑️", "📖", "📐", "🔤", "🔬", "🌏", "✍️", "🗣️",
        "🎨", "🧭", "🐣", "🎭", "🚀", "👁️", "🧠", "🛡️", "🐱", "🐶", "🐰", "🐻", "☀️", "🌙"
    ]
    for em in raw_emojis:
        # If preceded by whitespace or tag and followed by text
        content = content.replace(f">{em} ", ">")
        content = content.replace(f">{em}", ">")
        content = content.replace(f" {em} ", " ")
        content = content.replace(f"'{em} ", "'")
        content = content.replace(f'"{em} ', '"')
        content = content.replace(f"'{em}'", "''")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[CLEANED] Emojis successfully scrubbed from {filepath}")

print("[COMPLETE] All files cleaned!")
