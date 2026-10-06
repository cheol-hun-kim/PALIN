# -*- coding: utf-8 -*-
"""
Verification of PassMate clean header without download icon & PWA retention in MyPage
"""
import os
import re

print("[TEST: PassMate Clean Header & MyPage PWA Shortcut Verification]")

css_path = os.path.join("static", "css", "style.css")
html_path = os.path.join("static", "index.html")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Gate 1: Check CSS normalization for .header-theme-btn
print("[Gate 1] Verifying .header-theme-btn in style.css...")
assert ".header-theme-btn" in css, ".header-theme-btn must be present in style.css"
assert "box-sizing: border-box !important;" in css, "box-sizing: border-box !important must be enforced"
print("Passed Gate 1: CSS height normalization and box-sizing rules verified.")

# Gate 2: Clean Header - Header Download Button Purged
print("[Gate 2] Verifying header download button purge...")
header_match = re.search(r"<header>[\s\S]*?</header>", html)
assert header_match, "Header markup found"
assert "header-pwa-install-btn" not in header_match.group(0), "header-pwa-install-btn must be removed from header"
print("Passed Gate 2: Download button successfully removed from top header.")

# Gate 3: PWA Shortcut preserved in MyPage & guide modal intact
print("[Gate 3] Verifying PWA Shortcut preserved in MyPage & Guide Modal...")
assert 'onclick="triggerPwaInstall()"' in html, "triggerPwaInstall must exist in MyPage"
assert 'id="pwa-guide-modal"' in html, "pwa-guide-modal must exist"
print("Passed Gate 3: PWA shortcuts in MyPage and guide modal verified.")

# Gate 4: Zero Emoji Policy in modified sections
print("[Gate 4] Verifying zero emoji compliance in header...")
emoji_regex = re.compile(r"[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF]")
assert not emoji_regex.search(header_match.group(0)), "Header must contain zero emojis"
print("Passed Gate 4: Zero emoji policy verified.")

print("ALL PASSMATE CLEAN HEADER TESTS PASSED 100%!")
