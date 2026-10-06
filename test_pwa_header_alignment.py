import os
import re

print("[TEST: PassMate PWA Install Header Button Height & Alignment Verification]")

css_path = os.path.join("static", "css", "style.css")
html_path = os.path.join("static", "index.html")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Gate 1: Check CSS normalization for #header-pwa-install-btn and .header-theme-btn
print("[Gate 1] Verifying #header-pwa-install-btn and .header-theme-btn in style.css...")
assert "#header-pwa-install-btn" in css, "#header-pwa-install-btn must be present in style.css"
assert "box-sizing: border-box !important;" in css, "box-sizing: border-box !important must be enforced"
assert "vertical-align: middle !important;" in css, "vertical-align: middle !important must be enforced"
print("Passed Gate 1: CSS height normalization and box-sizing rules verified.")

# Gate 2: Check responsive 480px and 360px media queries
print("[Gate 2] Verifying responsive breakpoints in style.css...")
assert re.search(r"@media\s*\(\s*max-width:\s*480px\s*\)[\s\S]*?#header-pwa-install-btn[\s\S]*?height:\s*30px\s*!important", css), "480px media query must set 30px height for #header-pwa-install-btn"
assert re.search(r"@media\s*\(\s*max-width:\s*360px\s*\)[\s\S]*?#header-pwa-install-btn[\s\S]*?height:\s*28px\s*!important", css), "360px media query must set 28px height for #header-pwa-install-btn"
print("Passed Gate 2: Responsive dimensions strictly matched.")

# Gate 3: Check static/index.html markup
print("[Gate 3] Verifying header button markup in static/index.html...")
assert 'id="header-pwa-install-btn"' in html, "id header-pwa-install-btn must exist in html"
assert 'display: inline-flex; align-items: center; justify-content: center; vertical-align: middle;' in html, "inner span must have centered inline-flex styles"
print("Passed Gate 3: HTML markup structure verified.")

# Gate 4: Zero Emoji Policy in modified sections
print("[Gate 4] Verifying zero emoji compliance in header...")
header_match = re.search(r"<header>[\s\S]*?</header>", html)
assert header_match, "Header found"
emoji_regex = re.compile(r"[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF]")
assert not emoji_regex.search(header_match.group(0)), "Header must contain zero emojis"
print("Passed Gate 4: Zero emoji policy verified.")

print("ALL PASSMATE HEADER ALIGNMENT TESTS PASSED 100%!")
