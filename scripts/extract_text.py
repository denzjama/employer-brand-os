#!/usr/bin/env python3
"""Extract plain text from .docx, .pptx and .xlsx files (methodology/workspace.md §4).

Usage: python3 extract_text.py <inbox-dir>

Writes <inbox-dir>/_text/<relative path>.txt for each supported file, skipping
extracts that are newer than their source. Standard library only.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}
SUPPORTED = {".docx", ".pptx", ".xlsx"}


MAX_PART_BYTES = 50 * 1024 * 1024


class UnsafeDocument(ValueError):
    """A document part that is oversized or declares a DTD."""


def _xml(z: zipfile.ZipFile, name: str) -> ET.Element:
    # Client files are untrusted: refuse zip bombs and DTDs (entity expansion).
    if z.getinfo(name).file_size > MAX_PART_BYTES:
        raise UnsafeDocument(f"{name} is larger than {MAX_PART_BYTES} bytes")
    data = z.read(name)
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise UnsafeDocument(f"{name} declares a DTD or entities")
    return ET.fromstring(data)


def docx_text(z: zipfile.ZipFile) -> str:
    root = _xml(z, "word/document.xml")
    lines = []
    for p in root.iter(f"{{{NS['w']}}}p"):
        text = "".join(t.text or "" for t in p.iter(f"{{{NS['w']}}}t"))
        if text.strip():
            lines.append(text)
    return "\n".join(lines)


def pptx_text(z: zipfile.ZipFile) -> str:
    def num(name: str) -> int:
        return int(re.search(r"(\d+)\.xml$", name).group(1))

    slides = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=num)
    out = []
    for name in slides:
        root = _xml(z, name)
        paras = []
        for p in root.iter(f"{{{NS['a']}}}p"):
            text = "".join(t.text or "" for t in p.iter(f"{{{NS['a']}}}t"))
            if text.strip():
                paras.append(text)
        notes = f"ppt/notesSlides/notesSlide{num(name)}.xml"
        if notes in z.namelist():
            note_text = " ".join(t.text or "" for t in _xml(z, notes).iter(f"{{{NS['a']}}}t")).strip()
            if note_text:
                paras.append(f"[notes] {note_text}")
        out.append(f"--- slide {num(name)} ---\n" + "\n".join(paras))
    return "\n\n".join(out)


def xlsx_text(z: zipfile.ZipFile) -> str:
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in _xml(z, "xl/sharedStrings.xml").iter(f"{{{NS['s']}}}si"):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['s']}}}t")))
    names = {}
    if "xl/workbook.xml" in z.namelist():
        for i, sheet in enumerate(_xml(z, "xl/workbook.xml").iter(f"{{{NS['s']}}}sheet"), start=1):
            names[i] = sheet.get("name")
    sheets = sorted(
        (n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)),
        key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)),
    )
    out = []
    for name in sheets:
        idx = int(re.search(r"(\d+)\.xml$", name).group(1))
        rows = []
        for row in _xml(z, name).iter(f"{{{NS['s']}}}row"):
            cells = []
            for c in row.iter(f"{{{NS['s']}}}c"):
                v = c.find(f"{{{NS['s']}}}v")
                if c.get("t") == "s" and v is not None:
                    cells.append(shared[int(v.text)])
                elif c.get("t") == "inlineStr":
                    cells.append("".join(t.text or "" for t in c.iter(f"{{{NS['s']}}}t")))
                else:
                    cells.append(v.text if v is not None and v.text else "")
            if any(cells):
                rows.append("\t".join(cells))
        out.append(f"--- sheet {names.get(idx, idx)} ---\n" + "\n".join(rows))
    return "\n\n".join(out)


EXTRACTORS = {".docx": docx_text, ".pptx": pptx_text, ".xlsx": xlsx_text}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    inbox = Path(sys.argv[1]).expanduser().resolve()
    out_root = inbox / "_text"
    count = 0
    for src in sorted(inbox.rglob("*")):
        if src.suffix.lower() not in SUPPORTED or out_root in src.parents or src.name.startswith("~$"):
            continue
        dst = out_root / (str(src.relative_to(inbox)) + ".txt")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(src) as z:
                text = EXTRACTORS[src.suffix.lower()](z)
        except (zipfile.BadZipFile, KeyError, ET.ParseError, UnsafeDocument) as exc:
            print(f"failed {src.relative_to(inbox)}: {exc}")
            continue
        dst.write_text(text, encoding="utf-8")
        count += 1
        print(f"extracted {src.relative_to(inbox)} -> {dst.relative_to(inbox)} ({len(text)} chars)")
    print(f"{count} file(s) extracted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
