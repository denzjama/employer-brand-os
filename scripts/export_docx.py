#!/usr/bin/env python3
"""Export a Markdown draft to .docx for an owner without access to the system
(methodology/assembly.md §6).

Usage: python3 export_docx.py <draft.md> <out.docx>

Handles headings, paragraphs, bullet and numbered lists, **bold** and
*italic*, and tables as tab-separated lines. Standard library only.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
</w:styles>"""
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def runs(text: str) -> str:
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part:
            continue
        props = ""
        if part.startswith("**") and part.endswith("**"):
            part, props = part[2:-2], "<w:rPr><w:b/></w:rPr>"
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, props = part[1:-1], "<w:rPr><w:i/></w:rPr>"
        out.append(f'<w:r>{props}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def paragraph(text: str, style: str = "", indent: int = 0) -> str:
    ppr = ""
    if style or indent:
        ppr = "<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "") + (f'<w:ind w:left="{indent}"/>' if indent else "") + "</w:pPr>"
    return f"<w:p>{ppr}{runs(text)}</w:p>"


def convert(md: str) -> str:
    body = []
    for line in md.splitlines():
        s = line.rstrip()
        if not s.strip() or re.match(r"^\|?\s*-{3,}", s.strip()):
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", s)
        if m:
            body.append(paragraph(m.group(2), f"Heading{len(m.group(1))}"))
        elif re.match(r"^\s*[-*]\s+", s):
            body.append(paragraph("• " + re.sub(r"^\s*[-*]\s+", "", s), indent=360))
        elif re.match(r"^\s*\d+[.)]\s+", s):
            body.append(paragraph(s.strip(), indent=360))
        elif s.strip().startswith("|"):
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            body.append(paragraph("\t".join(cells)))
        else:
            body.append(paragraph(s.strip()))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>{"".join(body)}<w:sectPr/></w:body></w:document>'


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", convert(src.read_text(encoding="utf-8")))
    print(f"written {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
