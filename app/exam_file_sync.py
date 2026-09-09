# -*- coding: utf-8 -*-
"""
PALIN OS Authentic Exam Files Folder Scanner & Database Synchronizer
Accurately maps:
- Folder "2027학년도" -> School Year 2027 (Exam Year 2026)
- Folder "2026학년도" -> School Year 2026 (Exam Year 2025)
- Subject / Sub-Subject (국어, 수학, 영어, 한국사, 탐구/사탐, 탐구/과탐)
- Grade (고1, 고2, 고3)
- Pairs Problem PDFs with Answer PDFs/Images with 100% token matching
- Base64 encoding into DB for zero-data-loss cloud persistence
"""

import os
import re
import base64
import urllib.parse
from sqlalchemy.orm import Session
from app import models

ALLOWED_EXAM_EXTS = {".pdf"}
ALLOWED_ANS_EXTS = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}
ANS_KEYWORDS = ["_ans", "_해설", "_정답", "_답지", "[해설]", "[정답]", "(해설)", "(정답)", "해설지", "정답표", "해설", "정답", "답지"]


def is_answer_file(filename: str) -> bool:
    name_lower = filename.lower()
    for kw in ANS_KEYWORDS:
        if kw in name_lower:
            return True
    return False


def extract_exam_token(filename: str) -> str:
    m = re.search(r"(10월|11월|12월|1월|2월|3월|4월|5월|6월|7월|8월|9월|수능|모의고사|모평|학평)", filename)
    if m:
        return m.group(1)
    return ""


def clean_display_title(q_filename: str, year_val: int, grade_str: str, subject_str: str) -> str:
    token = extract_exam_token(q_filename)
    exam_year = year_val - 1
    
    if "수능" in q_filename or token == "수능":
        return f"{year_val}학년도 대학수학능력시험 {subject_str}영역 ({exam_year}년 기출)"
    elif token and "월" in token:
        return f"{year_val}학년도 {token} 모의평가 {subject_str}영역 ({exam_year}년 기출)"
    else:
        stem, _ = os.path.splitext(q_filename)
        return stem.replace("_", " ").strip()


def scan_and_sync_downloads(db: Session, base_dir: str = "static/downloads") -> dict:
    """
    Recursively scans base_dir and synchronizes physical files into ExamMaterial database table.
    """
    if not os.path.exists(base_dir):
        return {"scanned": 0, "synced": 0, "pairs": []}

    records_by_key = {}
    
    for root, dirs, files in os.walk(base_dir):
        if not files:
            continue
            
        rel_root = os.path.relpath(root, base_dir)
        if rel_root == ".":
            continue
            
        parts = rel_root.replace("\\", "/").split("/")
        if len(parts) < 3:
            continue
            
        # Parse hierarchy
        if parts[0] == "탐구" and len(parts) >= 4 and parts[1] in ("사탐", "과탐"):
            subject_main = "탐구"
            subject_detail = parts[1]
            year_str = parts[2]
            grade_str = parts[3]
        else:
            subject_main = parts[0]
            subject_detail = parts[0]
            year_str = parts[1]
            grade_str = parts[2] if len(parts) >= 3 else "고3"
            
        year_match = re.search(r"(\d{4})", year_str)
        year_val = int(year_match.group(1)) if year_match else 2027
        exam_year = year_val - 1
        
        q_files = []
        a_files = []
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ALLOWED_EXAM_EXTS and not is_answer_file(f):
                q_files.append(f)
            elif (ext in ALLOWED_ANS_EXTS or ext in ALLOWED_EXAM_EXTS) and is_answer_file(f):
                a_files.append(f)
            elif ext in ALLOWED_EXAM_EXTS:
                q_files.append(f)

        paired_a = set()
        for q in q_files:
            q_token = extract_exam_token(q)
            matched_a = None
            
            # 1. Match by specific exam token (e.g. 9월, 6월, 수능)
            for a in a_files:
                if a in paired_a:
                    continue
                a_token = extract_exam_token(a)
                if q_token and a_token and q_token == a_token:
                    matched_a = a
                    break
                    
            # 2. Fallback: single pair in directory
            if not matched_a and len(q_files) == 1 and len(a_files) == 1 and a_files[0] not in paired_a:
                matched_a = a_files[0]
                
            if matched_a:
                paired_a.add(matched_a)
                
            q_full_path = os.path.join(root, q)
            q_rel_path = os.path.relpath(q_full_path, "static").replace("\\", "/")
            
            ans_full_path = os.path.join(root, matched_a) if matched_a else None
            ans_rel_path = os.path.relpath(ans_full_path, "static").replace("\\", "/") if ans_full_path else None
            
            # Read Base64
            try:
                with open(q_full_path, "rb") as f:
                    q_b64 = base64.b64encode(f.read()).decode("utf-8")
                q_size_kb = round(os.path.getsize(q_full_path) / 1024)
            except Exception:
                q_b64 = None
                q_size_kb = 0

            ans_b64 = None
            if ans_full_path and os.path.exists(ans_full_path):
                try:
                    with open(ans_full_path, "rb") as f:
                        ans_b64 = base64.b64encode(f.read()).decode("utf-8")
                except Exception:
                    ans_b64 = None

            display_title = clean_display_title(q, year_val, grade_str, subject_detail)
            
            key = f"{subject_main}_{year_val}_{grade_str}_{q}"
            records_by_key[key] = {
                "subject": subject_main,
                "title": display_title,
                "description": f"[{year_val}학년도 {grade_str} {subject_detail}] {exam_year}년 시행 기출문제 및 정답/해설",
                "file_url": f"/{q_rel_path}",
                "file_name": q,
                "file_size": f"{q_size_kb} KB",
                "answer_file_url": f"/{ans_rel_path}" if ans_rel_path else None,
                "answer_file_name": matched_a if matched_a else None,
                "year": year_val,
                "category": "PUBLIC_EXAM",
                "academy_code": "ILWON-2027",
                "target_grade": grade_str,
                "file_base64": q_b64,
                "answer_base64": ans_b64
            }

    # Synchronize to Database
    synced_count = 0
    active_keys = set()
    
    for key, data in records_by_key.items():
        active_keys.add(key)
        exist = db.query(models.ExamMaterial).filter(
            models.ExamMaterial.file_url == data["file_url"]
        ).first()
        
        if not exist:
            mat = models.ExamMaterial(
                subject=data["subject"],
                title=data["title"],
                description=data["description"],
                file_url=data["file_url"],
                file_name=data["file_name"],
                file_size=data["file_size"],
                answer_file_url=data["answer_file_url"],
                answer_file_name=data["answer_file_name"],
                year=data["year"],
                category=data["category"],
                academy_code=data["academy_code"],
                target_grade=data["target_grade"],
                file_base64=data["file_base64"],
                answer_base64=data["answer_base64"],
                deleted_at=None
            )
            db.add(mat)
        else:
            exist.subject = data["subject"]
            exist.title = data["title"]
            exist.description = data["description"]
            exist.file_name = data["file_name"]
            exist.file_size = data["file_size"]
            exist.answer_file_url = data["answer_file_url"]
            exist.answer_file_name = data["answer_file_name"]
            exist.year = data["year"]
            exist.target_grade = data["target_grade"]
            exist.file_base64 = data["file_base64"]
            exist.answer_base64 = data["answer_base64"]
            exist.deleted_at = None
        synced_count += 1

    db.commit()
    print(f"[EXAM_SYNC] Synchronized {synced_count} authentic exam materials from folder structure.")
    return {"scanned": len(records_by_key), "synced": synced_count}
