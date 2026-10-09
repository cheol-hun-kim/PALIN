import os, sys, re, json

ROOT_DIR = r'C:\Users\1286o\.gemini\antigravity\scratch\pass-mate'

patterns = {
    'master_or_id1_overrides': r'(student\.id\s*==\s*1|1286orbital21|sid\s*==\s*1|is_master)',
    'hardcoded_numbers_in_metrics': r'(streak_days|current_points|wallet_balance|chat_tokens|diligence_score|study_mins|study_hours)\s*=\s*(?:[0-9]{2,}|max\([0-9])',
    'js_math_max_fallbacks': r'Math\.max\(\s*[0-9]+',
    'fake_or_dummy_keywords': r'\b(dummy|mock|fake|sample_data|fake_data|hardcoded)\b',
    'hardcoded_html_metrics': r'(연속\s*[0-9]+일|[0-9]+,?[0-9]*\s*P\b|[0-9]+\s*시간\s*[0-9]+\s*분)',
    'fallback_or_operators': r'\|\|\s*(?:\[\s*\{|\"[^\"]{10,}\"|[0-9]{2,})'
}

files_to_check = [
    'app/main.py',
    'app/models.py',
    'app/database.py',
    'app/schemas.py',
    'static/js/app.js',
    'static/index.html',
    'static/admin.html',
    'static/master.html'
]

results = {}

for rel_path in files_to_check:
    fpath = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        line_str = line.strip()
        # skip comments
        if line_str.startswith('#') or line_str.startswith('//') or line_str.startswith('/*') or line_str.startswith('*'):
            continue
        for cat, pat in patterns.items():
            if re.search(pat, line_str, re.IGNORECASE):
                results.setdefault(f"{rel_path} :: {cat}", []).append((i+1, line_str))

out_file = os.path.join(ROOT_DIR, 'audit_report.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Audit completed. Found categories: {len(results)}")
for k, v in results.items():
    print(f"\n--- {k} ({len(v)} matches) ---")
    for lno, text in v[:8]:
        print(f"  L{lno}: {text[:140]}")
    if len(v) > 8:
        print(f"  ... and {len(v)-8} more matches")
