#!/usr/bin/env python3
"""
validate_docx.py — 《历史研究》排版规范机器校验

用法:
    python3 validate_docx.py 排版后.docx
    python3 validate_docx.py 排版后.docx --strict

退出码:
    0  全部规则通过
    1  存在 FAIL 或参数错误
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn

from lib.specs import DEFAULT_SPEC, STYLE_NAMES
from lib.footnote_ooxml import has_footnote_restart_each_page

_SPEC = DEFAULT_SPEC
_TOL  = _SPEC.twip_tolerance

PASS  = "PASS"
FAIL  = "FAIL"
WARN  = "WARN"


def _approx(actual: int, expected: int, tol: int = _TOL) -> bool:
    return abs(actual - expected) <= tol


def _check(results: list, name: str, ok: bool, detail: str = "") -> None:
    status = PASS if ok else FAIL
    results.append((status, name, detail))


def _warn(results: list, name: str, detail: str = "") -> None:
    results.append((WARN, name, detail))


# ────────────────────────────── 规则实现 ──────────────────────────────────────

def check_margins(doc, results: list) -> None:
    sec = doc.sections[0]
    pairs = [
        ("margin_top",    int(sec.top_margin),    int(Cm(_SPEC.margin_top_cm))),
        ("margin_bottom", int(sec.bottom_margin), int(Cm(_SPEC.margin_bottom_cm))),
        ("margin_left",   int(sec.left_margin),   int(Cm(_SPEC.margin_left_cm))),
        ("margin_right",  int(sec.right_margin),  int(Cm(_SPEC.margin_right_cm))),
    ]
    for name, actual, expected in pairs:
        ok = _approx(actual, expected)
        _check(results, f"margins/{name}",
               ok, f"actual={actual} expected={expected} tol={_TOL}")


def check_styles_exist(doc, results: list) -> None:
    existing = {s.name for s in doc.styles}
    for key, name in STYLE_NAMES.items():
        _check(results, f"style_exists/{name}", name in existing)


def check_style_font_size(doc, results: list) -> None:
    size_map = {
        STYLE_NAMES["body"]:        _SPEC.body_pt,
        STYLE_NAMES["title_main"]:  _SPEC.title_main_pt,
        STYLE_NAMES["subtitle"]:    _SPEC.subtitle_pt,
        STYLE_NAMES["section_l2"]:  _SPEC.section_l2_pt,
        STYLE_NAMES["footnote"]:    _SPEC.footnote_pt,
    }
    existing = {s.name: s for s in doc.styles}
    for sname, expected_pt in size_map.items():
        if sname not in existing:
            _check(results, f"font_size/{sname}", False, "样式不存在")
            continue
        style = existing[sname]
        actual_half = style.font.size  # EMU
        if actual_half is None:
            _check(results, f"font_size/{sname}", False, "font.size=None")
            continue
        actual_pt = actual_half / 12700
        ok = abs(actual_pt - expected_pt) < 0.1
        _check(results, f"font_size/{sname}",
               ok, f"actual={actual_pt:.1f}pt expected={expected_pt}pt")


def check_style_line_spacing(doc, results: list) -> None:
    spacing_map = {
        STYLE_NAMES["body"]:     _SPEC.body_line_pt,
        STYLE_NAMES["footnote"]: _SPEC.footnote_line_pt,
    }
    existing = {s.name: s for s in doc.styles}
    for sname, expected_pt in spacing_map.items():
        if sname not in existing:
            _check(results, f"line_spacing/{sname}", False, "样式不存在")
            continue
        style = existing[sname]
        pf = style.paragraph_format
        rule_ok = pf.line_spacing_rule == WD_LINE_SPACING.EXACTLY
        if not rule_ok:
            _check(results, f"line_spacing/{sname}", False,
                   f"rule={pf.line_spacing_rule} 期望 EXACTLY")
            continue
        actual_emu = pf.line_spacing
        if actual_emu is None:
            _check(results, f"line_spacing/{sname}", False, "line_spacing=None")
            continue
        actual_pt  = actual_emu / 12700
        ok = abs(actual_pt - expected_pt) < 0.2
        _check(results, f"line_spacing/{sname}",
               ok, f"actual={actual_pt:.1f}pt expected={expected_pt}pt")


def check_style_fonts(doc, results: list) -> None:
    font_map = {
        STYLE_NAMES["body"]: (
            _SPEC.font_latin,
            _SPEC.font_body_east,
        ),
        STYLE_NAMES["footnote"]: (
            _SPEC.font_latin,
            _SPEC.font_footnote_east,
        ),
    }
    existing = {s.name: s for s in doc.styles}
    for sname, (expected_latin, expected_east) in font_map.items():
        if sname not in existing:
            _check(results, f"font/{sname}", False, "样式不存在")
            continue
        style = existing[sname]
        rPr = style.element.rPr
        if rPr is None:
            _check(results, f"font/{sname}", False, "rPr=None")
            continue
        rf = rPr.find(qn("w:rFonts"))
        if rf is None:
            _check(results, f"font/{sname}", False, "rFonts=None")
            continue
        ascii_val = rf.get(qn("w:ascii"))
        east_val  = rf.get(qn("w:eastAsia"))
        latin_ok  = ascii_val == expected_latin
        east_ok   = east_val  == expected_east
        _check(results, f"font/{sname}/latin",
               latin_ok, f"actual={ascii_val!r} expected={expected_latin!r}")
        _check(results, f"font/{sname}/eastAsia",
               east_ok,  f"actual={east_val!r} expected={expected_east!r}")


def check_footnote_restart(docx_path: str, results: list) -> None:
    ok = has_footnote_restart_each_page(docx_path)
    _check(results, "footnote/numRestart_eachPage", ok)


def check_needs_review_italic(doc, results: list) -> None:
    count = 0
    for para in doc.paragraphs:
        for run in para.runs:
            if run.italic and "NEEDS_REVIEW" not in run.text:
                count += 1
    if count > 0:
        _warn(results, "italic/needs_review",
              f"{count} 个斜体 run 未标记 NEEDS_REVIEW，请人工核查 PAS 规则")
    else:
        results.append((PASS, "italic/needs_review", "无未标注斜体"))


# ────────────────────────────── 主流程 ───────────────────────────────────────

def validate(docx_path: str) -> list:
    doc = Document(docx_path)
    results: list = []

    check_margins(doc, results)
    check_styles_exist(doc, results)
    check_style_font_size(doc, results)
    check_style_line_spacing(doc, results)
    check_style_fonts(doc, results)
    check_footnote_restart(docx_path, results)
    check_needs_review_italic(doc, results)

    return results


def _print_report(results: list) -> int:
    width = max(len(r[1]) for r in results) + 2
    fail_count = 0
    warn_count = 0
    for status, name, detail in results:
        marker = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️ "}.get(status, "?")
        line = f"  {marker} [{status}] {name:<{width}}"
        if detail:
            line += f"  {detail}"
        print(line)
        if status == FAIL:
            fail_count += 1
        elif status == WARN:
            warn_count += 1

    print()
    total = len(results)
    passed = total - fail_count - warn_count
    print(f"结果: {passed}/{total} 通过  {fail_count} 失败  {warn_count} 警告")
    return fail_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="校验 .docx 是否符合《历史研究》排版规范"
    )
    parser.add_argument("docx", help="待校验的 .docx 文件路径")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="WARN 也视为失败（exit 1）",
    )
    args = parser.parse_args()

    p = Path(args.docx)
    if not p.exists() or p.suffix.lower() != ".docx":
        print(f"ERROR: 文件不存在或非 .docx: {args.docx}", file=sys.stderr)
        sys.exit(1)

    print(f"校验: {p}\n")
    results = validate(str(p))
    fail_count = _print_report(results)

    if args.strict:
        warn_count = sum(1 for r in results if r[0] == WARN)
        if fail_count + warn_count > 0:
            sys.exit(1)
    else:
        if fail_count > 0:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
