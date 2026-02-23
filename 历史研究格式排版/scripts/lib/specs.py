from dataclasses import dataclass
from docx.shared import Cm, Pt


@dataclass(frozen=True)
class LayoutSpec:
    margin_top_cm: float = 3.3
    margin_bottom_cm: float = 2.7
    margin_left_cm: float = 2.4
    margin_right_cm: float = 2.3

    body_pt: float = 12.0
    body_line_pt: float = 17.9
    body_first_indent_chars: float = 2.0

    quote_indent_chars: float = 2.0

    footnote_pt: float = 10.5
    footnote_line_pt: float = 14.5
    footnote_indent_chars: float = 1.0

    title_main_pt: float = 26.0
    subtitle_pt: float = 18.0
    section_l2_pt: float = 16.0
    abstract_label_pt: float = 12.0
    abstract_text_pt: float = 12.0
    abstract_indent_chars: float = 1.0

    font_latin: str = "Times New Roman"
    font_body_east: str = "宋体"
    font_quote_east: str = "楷体"
    font_footnote_east: str = "楷体"
    font_title_east: str = "宋体"
    font_subtitle_east: str = "仿宋"
    font_abstract_label_east: str = "黑体"
    font_abstract_text_east: str = "仿宋"
    font_section_l2_east: str = "宋体"

    twip_tolerance: int = 300  # Cm() EMU 转换精度损失最大约 235 twips（<0.001cm）

    def margin_top(self) -> int:
        return int(Cm(self.margin_top_cm))

    def margin_bottom(self) -> int:
        return int(Cm(self.margin_bottom_cm))

    def margin_left(self) -> int:
        return int(Cm(self.margin_left_cm))

    def margin_right(self) -> int:
        return int(Cm(self.margin_right_cm))

    def body_size(self) -> int:
        return int(Pt(self.body_pt))

    def body_line(self) -> int:
        return int(Pt(self.body_line_pt))

    def footnote_size(self) -> int:
        return int(Pt(self.footnote_pt))

    def footnote_line(self) -> int:
        return int(Pt(self.footnote_line_pt))

    def first_indent(self) -> int:
        return int(Pt(self.body_pt * self.body_first_indent_chars))

    def quote_left_indent(self) -> int:
        return int(Pt(self.body_pt * self.quote_indent_chars))

    def abstract_left_indent(self) -> int:
        return int(Pt(self.body_pt * self.abstract_indent_chars))


DEFAULT_SPEC = LayoutSpec()

STYLE_NAMES = {
    "body": "HR-Body",
    "quote": "HR-QuoteBlock",
    "footnote": "HR-FootnoteText",
    "title_main": "HR-TitleMain",
    "subtitle": "HR-Subtitle",
    "abstract_label": "HR-AbstractLabel",
    "abstract_text": "HR-AbstractText",
    "section_l2": "HR-SectionL2",
}
