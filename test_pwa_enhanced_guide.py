# -*- coding: utf-8 -*-
"""
Verification suite for PassMate Enhanced PWA & Android 14+ Guide
"""
import os
import re
import json

def test_pwa_enhanced():
    print("[TEST: PassMate PWA Android 14+ Guide & Standards]")
    
    # Gate 1: static/manifest.json
    print("[Gate 1] Verifying manifest.json configuration...")
    with open("static/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("id") == "/", "manifest id must be '/'"
    assert manifest.get("scope") == "/", "manifest scope must be '/'"
    icons = manifest.get("icons", [])
    sizes = [i.get("sizes") for i in icons]
    assert "192x192" in sizes, "manifest must contain 192x192 icon"
    assert "512x512" in sizes, "manifest must contain 512x512 icon"
    print("Passed Gate 1: manifest id, scope, and standard icons verified.")

    # Gate 2: sw.js
    print("[Gate 2] Verifying sw.js does not self-unregister...")
    with open("static/sw.js", "r", encoding="utf-8") as f:
        sw_code = f.read()
    assert "unregister" not in sw_code, "sw.js must not unregister itself"
    assert "skipWaiting" in sw_code, "sw.js must activate quickly"
    print("Passed Gate 2: Service worker lifecycle verified.")

    # Gate 3: static/index.html PWA guide & triggers
    print("[Gate 3] Verifying static/index.html guide elements and feedback...")
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "passmate-pwa-android-box" in html, "passmate-pwa-android-box must exist"
    assert "passmate-pwa-action-feedback" in html, "passmate-pwa-action-feedback must exist"
    assert "방법 1. 경고 없이 1초 추가 (가장 추천)" in html, "Method 1 guide must exist"
    assert "방법 2. '앱 설치' 시 Play 프로텍트 경고가 뜰 때" in html, "Method 2 guide must exist"
    assert "navigator.serviceWorker.register('/sw.js'" in html, "SW registration must be present"
    print("Passed Gate 3: HTML guide markup and dynamic feedback verified.")

    # Gate 4: Zero Emoji Compliance
    print("[Gate 4] Verifying zero emoji compliance...")
    emoji_regex = re.compile(r'[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF]')
    modal_match = re.search(r'id="pwa-guide-modal"[\s\S]*?id="passmate-pwa-action-feedback"[\s\S]*?<\/div>\s*<\/div>', html)
    assert modal_match, "pwa-guide-modal markup found"
    assert not emoji_regex.search(modal_match.group(0)), "pwa-guide-modal must contain zero emojis"
    assert not emoji_regex.search(sw_code), "sw.js must contain zero emojis"
    print("Passed Gate 4: Zero emoji policy verified.")

    print("ALL PASSMATE ENHANCED PWA TESTS PASSED 100%!")

if __name__ == "__main__":
    test_pwa_enhanced()
