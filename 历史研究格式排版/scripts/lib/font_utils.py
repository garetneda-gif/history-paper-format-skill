from docx.oxml.ns import qn


def set_run_fonts(run, latin: str, east_asia: str) -> None:
    run.font.name = latin
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        from docx.oxml import OxmlElement
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), east_asia)


def set_style_fonts(style, latin: str, east_asia: str) -> None:
    style.font.name = latin
    rPr = style.element.rPr
    if rPr is None:
        from docx.oxml import OxmlElement
        rPr = OxmlElement("w:rPr")
        style.element.append(rPr)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        from docx.oxml import OxmlElement
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), east_asia)


def get_rfonts(element) -> dict:
    rPr = getattr(element, "rPr", None) or getattr(element, "_element", element)
    if hasattr(rPr, "rPr"):
        rPr = rPr.rPr
    if rPr is None:
        return {}
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        return {}
    return {
        "ascii": rf.get(qn("w:ascii")),
        "hAnsi": rf.get(qn("w:hAnsi")),
        "eastAsia": rf.get(qn("w:eastAsia")),
    }
