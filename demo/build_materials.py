#!/usr/bin/env python3
"""Build the materials of the fictional demo company from demo/source/.

Usage: python3 demo/build_materials.py

Writes demo/materials/: docx, pptx, xlsx, csv, md, html, a PDF with a text
layer (macOS cupsfilter), a byte-identical duplicate and a file name in NFD
with a non-breaking space. Archives use a fixed timestamp, so rebuilding does
not change the files. Standard library only (plus cupsfilter for the PDF).
"""
import json
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
OUT = HERE / "materials"
sys.path.insert(0, str(HERE.parent / "scripts"))
import export_docx  # noqa: E402

FIXED = (2026, 1, 1, 0, 0, 0)


def zip_write(path: Path, parts: dict) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            info = zipfile.ZipInfo(name, date_time=FIXED)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)


def docx(md_file: str, out_name: str) -> None:
    body = export_docx.convert((SRC / md_file).read_text(encoding="utf-8"))
    zip_write(OUT / out_name, {
        "[Content_Types].xml": export_docx.CONTENT_TYPES,
        "_rels/.rels": export_docx.RELS,
        "word/_rels/document.xml.rels": export_docx.DOC_RELS,
        "word/styles.xml": export_docx.STYLES,
        "word/document.xml": body,
    })


def pptx(spec_file: str) -> None:
    spec = json.loads((SRC / spec_file).read_text(encoding="utf-8"))
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    parts = {}
    types = ['<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
             '<Default Extension="xml" ContentType="application/xml"/>',
             '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>']
    rels, ids = [], []
    for i, lines in enumerate(spec["slides"], 1):
        paras = "".join(f'<a:p><a:r><a:t>{escape(t)}</a:t></a:r></a:p>' for t in lines)
        parts[f"ppt/slides/slide{i}.xml"] = (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="{a}" xmlns:p="{p}" xmlns:r="{r}">'
            f'<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
            f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Text"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr/>'
            f'<p:txBody><a:bodyPr/>{paras}</p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
        types.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        rels.append(f'<Relationship Id="rId{i}" Type="{r}/slide" Target="slides/slide{i}.xml"/>')
        ids.append(f'<p:sldId id="{255 + i}" r:id="rId{i}"/>')
    parts["[Content_Types].xml"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">{"".join(types)}</Types>'
    parts["_rels/.rels"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{r}/officeDocument" Target="ppt/presentation.xml"/></Relationships>'
    parts["ppt/_rels/presentation.xml.rels"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{"".join(rels)}</Relationships>'
    parts["ppt/presentation.xml"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="{a}" xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst>{"".join(ids)}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'
    zip_write(OUT / spec["file"], parts)


def xlsx(spec_file: str) -> None:
    spec = json.loads((SRC / spec_file).read_text(encoding="utf-8"))
    s = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    strings, index = [], {}

    def sid(v: str) -> int:
        if v not in index:
            index[v] = len(strings)
            strings.append(v)
        return index[v]

    parts, sheets, rels, types = {}, [], [], []
    for n, (name, rows) in enumerate(spec["sheets"].items(), 1):
        xml_rows = []
        for ri, row in enumerate(rows, 1):
            cells = "".join(f'<c r="{chr(64 + ci)}{ri}" t="s"><v>{sid(v)}</v></c>' for ci, v in enumerate(row, 1))
            xml_rows.append(f'<row r="{ri}">{cells}</row>')
        parts[f"xl/worksheets/sheet{n}.xml"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="{s}"><sheetData>{"".join(xml_rows)}</sheetData></worksheet>'
        sheets.append(f'<sheet name="{escape(name)}" sheetId="{n}" r:id="rId{n}"/>')
        rels.append(f'<Relationship Id="rId{n}" Type="{r}/worksheet" Target="worksheets/sheet{n}.xml"/>')
        types.append(f'<Override PartName="/xl/worksheets/sheet{n}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    k = len(sheets) + 1
    rels.append(f'<Relationship Id="rId{k}" Type="{r}/sharedStrings" Target="sharedStrings.xml"/>')
    parts["xl/sharedStrings.xml"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sst xmlns="{s}" count="{len(strings)}" uniqueCount="{len(strings)}">' + "".join(f"<si><t>{escape(v)}</t></si>" for v in strings) + "</sst>"
    parts["xl/workbook.xml"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="{s}" xmlns:r="{r}"><sheets>{"".join(sheets)}</sheets></workbook>'
    parts["xl/_rels/workbook.xml.rels"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{"".join(rels)}</Relationships>'
    parts["_rels/.rels"] = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{r}/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    parts["[Content_Types].xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        + "".join(types) + "</Types>")
    zip_write(OUT / spec["file"], parts)


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    pptx("strategy_2026.json")
    docx("evp_v1_2024.md", "EVP_v1_2024.docx")
    docx("evp_v2_2025.md", "EVP_v2_2025_утверждено.docx")
    shutil.copy(OUT / "EVP_v2_2025_утверждено.docx", OUT / "EVP_v2_2025_утверждено (копия).docx")
    xlsx("results_2025.json")
    copies = {
        "newsletter_dec2025.md": "Рассылка_для_сотрудников_дек2025.md",
        "team_processes.md": "Как_работает_команда.md",
        "exit_interviews.csv": "Exit-интервью_выгрузка.csv",
        "reviews_hh.md": "Отзывы_hh_выгрузка.md",
        "students_presentation.html": "Презентация_для_студентов.html",
        "onboarding_schedule.md": "План_онбординга_I_кв_2026.md",
    }
    for src, dst in copies.items():
        shutil.copy(SRC / src, OUT / dst)
    # File name stored decomposed (NFD) with a non-breaking space, as macOS may do.
    shutil.copy(SRC / "voice_guide.md", OUT / unicodedata.normalize("NFD", "Голос бренда.md"))
    pdf = OUT / "Опрос_вовлечённости_2025.pdf"
    if shutil.which("cupsfilter"):
        with open(pdf, "wb") as f:
            subprocess.run(["cupsfilter", "-m", "application/pdf", str(SRC / "engagement_2025.md")],
                           stdout=f, stderr=subprocess.DEVNULL, check=True)
    else:
        print("cupsfilter not found: the PDF was not built", file=sys.stderr)
    for f in sorted(OUT.iterdir()):
        print(f"built {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
