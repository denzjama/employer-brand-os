#!/usr/bin/env python3
"""Inventory of materials in eb/inbox (methodology/workspace.md §3.1).

Usage: python3 inventory.py <inbox-dir>

Writes <inbox-dir>/_inventory.md: every file with its path exactly as on disk,
format, size, page count where it can be read, whether a PDF has a text layer,
byte-identical duplicates, and the extract path. Standard library only; uses
`pdftotext` for the text-layer check when it is installed.
"""
import hashlib
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

SKIP = {"_index.md", "_inventory.md"}
SKIP_DIRS = {"_text", "_notes"}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".tif", ".tiff", ".bmp"}
EXTRACTED = {".docx", ".pptx", ".xlsx", ".html", ".htm"}


def normalise(rel: str) -> str:
    return unicodedata.normalize("NFC", rel).replace(" ", " ")


def office_pages(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if path.suffix.lower() == ".pptx":
                return str(sum(1 for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)))
            if path.suffix.lower() == ".xlsx":
                sheets = sum(1 for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
                return f"{sheets} sheets"
            if "docProps/app.xml" in names:
                m = re.search(rb"<Pages>(\d+)</Pages>", z.read("docProps/app.xml"))
                if m:
                    return m.group(1).decode()
    except zipfile.BadZipFile:
        return "broken"
    return "?"


def pdf_info(path: Path) -> tuple:
    data = path.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page(?!s)", data)) or "?"
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(
                ["pdftotext", "-l", "3", str(path), "-"],
                capture_output=True, timeout=60, check=False,
            ).stdout
            return pages, "yes" if out.strip() else "no (scan)"
        except (OSError, subprocess.TimeoutExpired):
            pass
    return pages, "likely" if b"/Font" in data else "likely no (scan)"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    inbox = Path(sys.argv[1]).expanduser().resolve()
    files = []
    for path in sorted(inbox.rglob("*")):
        rel_parts = path.relative_to(inbox).parts
        if not path.is_file() or path.name in SKIP or path.name.startswith((".", "~$")) or rel_parts[0] in SKIP_DIRS:
            continue
        files.append(path)
    # Of byte-identical files, the one with the shortest name is the original
    # ("EVP.docx" rather than "EVP (copy).docx"); ties go to sort order.
    rows, seen = [], {}
    for path in sorted(files, key=lambda f: (len(f.name), str(f))):
        seen.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), str(path.relative_to(inbox)))
    for path in files:
        rel = str(path.relative_to(inbox))
        ext = path.suffix.lower()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        duplicate = "" if seen[digest] == rel else seen[digest]
        pages, text_layer = "", ""
        if ext == ".pdf":
            pages, text_layer = pdf_info(path)
        elif ext in {".docx", ".pptx", ".xlsx"}:
            pages, text_layer = office_pages(path), "extract"
        elif ext in {".html", ".htm"}:
            pages, text_layer = "", "extract"
        elif ext in IMAGES:
            pages, text_layer = "1", "image"
        else:
            text_layer = "text"
        extract = f"_text/{normalise(rel)}.txt" if ext in EXTRACTED else ""
        odd = " (NFD or non-breaking space in name)" if normalise(rel) != rel else ""
        rows.append((rel + odd, ext.lstrip(".") or "?", f"{path.stat().st_size / 1024:.0f}", str(pages), text_layer, digest[:10], duplicate, extract))

    lines = [
        "# Inventory",
        "",
        "| File (as on disk) | Format | KB | Pages | Text layer | SHA-256 | Duplicate of | Extract |",
        "|---|---|---|---|---|---|---|---|",
    ]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    scans = sum(1 for r in rows if "scan" in r[4])
    dups = sum(1 for r in rows if r[6])
    lines += ["", f"{len(rows)} files; {scans} PDF scans to be read as images; {dups} byte-identical duplicates."]
    (inbox / "_inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
