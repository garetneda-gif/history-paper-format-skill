from docx.shared import Cm, Pt
from docx.enum.text import WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE

from .specs import LayoutSpec, DEFAULT_SPEC, STYLE_NAMES


def _get_or_add_style(doc, name: str, style_type=WD_STYLE_TYPE.PARAGRAPH):
    if name in [s.name for s in doc.styles]:
        return doc.styles[name]
    return doc.styles.add_style(name, style_type)


def _set_para_fmt(style, size_pt: float, line_pt: float,
                  first_indent: float = 0.0, left_indent: float = 0.0,
                  right_indent: float = 0.0, space_before: float = 0.0,
                  space_after: float = 0.0, align: int = -1) -> None:
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(line_pt)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_indent:
        pf.first_line_indent = Pt(first_indent)
    if left_indent:
        pf.left_indent = Pt(left_indent)
    if right_indent:
        pf.right_indent = Pt(right_indent)
    if align >= 0:
        pf.alignment = align
    style.font.size = Pt(size_pt)


def ensure_paragraph_styles(doc, spec: LayoutSpec = DEFAULT_SPEC) -> None:
    char = spec.body_pt
    indent2 = char * spec.body_first_indent_chars
    indent1 = char * spec.abstract_indent_chars

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["body"]),
                  spec.body_pt, spec.body_line_pt, first_indent=indent2)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["quote"]),
                  spec.body_pt, spec.body_line_pt,
                  left_indent=indent2, right_indent=indent2)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["footnote"]),
                  spec.footnote_pt, spec.footnote_line_pt,
                  left_indent=indent1, right_indent=indent1)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["title_main"]),
                  spec.title_main_pt, spec.title_main_pt * 1.5,
                  space_before=6.0, space_after=6.0, align=1)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["subtitle"]),
                  spec.subtitle_pt, spec.subtitle_pt * 1.5,
                  space_before=3.0, space_after=3.0, align=1)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["section_l2"]),
                  spec.section_l2_pt, spec.section_l2_pt * 1.5,
                  space_before=6.0, space_after=3.0)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["abstract_label"]),
                  spec.abstract_label_pt, spec.body_line_pt, left_indent=indent1)

    _set_para_fmt(_get_or_add_style(doc, STYLE_NAMES["abstract_text"]),
                  spec.abstract_text_pt, spec.body_line_pt,
                  left_indent=indent1, right_indent=indent1)


def apply_base_page_setup(doc, spec: LayoutSpec = DEFAULT_SPEC) -> None:
    for section in doc.sections:
        section.top_margin = Cm(spec.margin_top_cm)
        section.bottom_margin = Cm(spec.margin_bottom_cm)
        section.left_margin = Cm(spec.margin_left_cm)
        section.right_margin = Cm(spec.margin_right_cm)
