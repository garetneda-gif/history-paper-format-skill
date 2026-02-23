import re
from .specs import STYLE_NAMES


_TITLE_MAIN_RE = re.compile(r"^#\s+|^第.{1,4}[章节篇]|^[一二三四五六七八九十百千]+、")
_SUBTITLE_RE = re.compile(r"^副标题[:：]|^——")
_SECTION_L2_RE = re.compile(r"^[（(]?[一二三四五六七八九十]+[）)、]|^\d+[\.、．]\d*\s")
_QUOTE_RE = re.compile(r"^[""\"]|^摘引|^引文")
_ABSTRACT_LABEL_RE = re.compile(r"^(摘\s*要|关\s*键\s*词)\s*[：:]")
_ABSTRACT_TEXT_RE = re.compile(r"^(摘\s*要|关\s*键\s*词)")
_FOOTNOTE_RE = re.compile(r"^\[?\d+\]?\s")


def classify_paragraph(paragraph) -> str:
    text = paragraph.text.strip()
    if not text:
        return STYLE_NAMES["body"]

    existing = paragraph.style.name if paragraph.style else ""
    if existing in STYLE_NAMES.values():
        return existing

    if existing in ("Heading 1", "Title"):
        return STYLE_NAMES["title_main"]
    if existing in ("Heading 2", "Subtitle"):
        return STYLE_NAMES["subtitle"]
    if existing in ("Heading 3", "Heading 4"):
        return STYLE_NAMES["section_l2"]
    if "Quote" in existing or "Block" in existing:
        return STYLE_NAMES["quote"]
    if "Footnote" in existing:
        return STYLE_NAMES["footnote"]

    if _ABSTRACT_LABEL_RE.match(text):
        return STYLE_NAMES["abstract_label"]
    if _ABSTRACT_TEXT_RE.match(text):
        return STYLE_NAMES["abstract_text"]
    if _SECTION_L2_RE.match(text):
        return STYLE_NAMES["section_l2"]
    if _FOOTNOTE_RE.match(text):
        return STYLE_NAMES["footnote"]

    return STYLE_NAMES["body"]


def apply_paragraph_style(paragraph, style_name: str) -> None:
    try:
        paragraph.style = style_name
    except KeyError:
        pass
