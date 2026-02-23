# 《历史研究》排版规格映射表 — docx 版

## 页面设置

| 参数 | 值 | python-docx 实现 |
|------|---|-----------------|
| 上边距 | 3.3cm | `section.top_margin = Cm(3.3)` |
| 下边距 | 2.7cm | `section.bottom_margin = Cm(2.7)` |
| 左边距 | 2.4cm | `section.left_margin = Cm(2.4)` |
| 右边距 | 2.3cm | `section.right_margin = Cm(2.3)` |

## 命名样式规格

| 样式名 | 东亚字体 | 拉丁字体 | 字号 | 行距规则 | 行距值 | 缩进 |
|--------|---------|---------|------|---------|-------|------|
| HR-Body | 宋体 | Times New Roman | 12pt | EXACTLY | 17.9pt | 首行 24pt（2×12pt） |
| HR-QuoteBlock | 楷体 | Times New Roman | 12pt | EXACTLY | 17.9pt | 左右各 24pt |
| HR-FootnoteText | 楷体 | Times New Roman | 10.5pt | EXACTLY | 14.5pt | 左右各 12pt |
| HR-TitleMain | 宋体 | Times New Roman | 26pt | EXACTLY | 39pt | 居中 |
| HR-Subtitle | 仿宋 | Times New Roman | 18pt | EXACTLY | 27pt | 居中 |
| HR-AbstractLabel | 黑体 | Times New Roman | 12pt | EXACTLY | 17.9pt | 左缩进 12pt |
| HR-AbstractText | 仿宋 | Times New Roman | 12pt | EXACTLY | 17.9pt | 左右各 12pt |
| HR-SectionL2 | 宋体 | Times New Roman | 16pt | EXACTLY | 24pt | — |

## 中西文字体分离实现

python-docx 的 `run.font.name` 只覆盖 `w:ascii`/`w:hAnsi`，需额外写 `w:eastAsia`：

```python
from docx.oxml.ns import qn

def set_run_fonts(run, latin, east_asia):
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
```

## 行距设置

必须同时设置 rule 和 spacing：

```python
from docx.enum.text import WD_LINE_SPACING
pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
pf.line_spacing = Pt(17.9)
```

## 版本历史

- **v2.0** (2026-02-23): 重写为 docx 版，移除 HTML/CSS 实现
