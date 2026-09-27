# -*- coding: utf-8 -*-
import sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

files = ['static/index.html', 'static/admin.html', 'static/master.html', 'static/js/app.js']
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27ff]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299]')

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    matches_count = 0
    sample_matches = []
    for line_idx, line in enumerate(lines, 1):
        found = emoji_pattern.findall(line)
        if found:
            matches_count += len(found)
            if len(sample_matches) < 25:
                sample_matches.append(f"Line {line_idx} ({''.join(set(found))}): {line.strip()[:110]}")
    print(f"=== {f}: {matches_count} emojis found ===")
    for sm in sample_matches:
        print("  ", sm)
