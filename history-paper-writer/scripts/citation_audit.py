#!/usr/bin/env python3
"""
citation_audit.py - NotebookLM 来源引注审计

验证每条引注必须具备三要素：
1. notebooklm_source - NotebookLM 返回的文献来源（必须非空）
2. page_locator      - 页码或"页码待核"（必须非空）
3. quote_snippet     - NotebookLM 返回的原始文字片段（必须非空）

用法：
    python citation_audit.py --input citations.json --report audit_report.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


class AuditResult:
    PASS = "PASS"
    FAIL = "FAIL"

    ERROR_MISSING_SOURCE = "MISSING_SOURCE"
    ERROR_MISSING_SNIPPET = "MISSING_SNIPPET"
    ERROR_MISSING_FIELD = "MISSING_FIELD"


def load_json(file_path: str) -> Dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def validate_citation(citation: Dict, citation_index: int) -> List[Dict]:
    """
    验证单条引注的三要素。
    返回违规列表（空列表 = 通过）。
    """
    violations = []
    claim = citation.get("claim", f"Citation #{citation_index}")

    notebooklm_source = citation.get("notebooklm_source", "").strip()
    page_locator = citation.get("page_locator", "").strip()
    quote_snippet = citation.get("quote_snippet", "").strip()

    if not notebooklm_source:
        violations.append({
            "citation_index": citation_index,
            "claim_preview": claim[:80],
            "error_type": AuditResult.ERROR_MISSING_SOURCE,
            "field": "notebooklm_source",
            "details": "notebooklm_source 不得为空，必须来自 NotebookLM 的实际回答",
        })

    if not page_locator:
        violations.append({
            "citation_index": citation_index,
            "claim_preview": claim[:80],
            "error_type": AuditResult.ERROR_MISSING_FIELD,
            "field": "page_locator",
            "details": "page_locator 不得为空；若 NotebookLM 未提供页码，填写'页码待核'",
        })

    if not quote_snippet:
        violations.append({
            "citation_index": citation_index,
            "claim_preview": claim[:80],
            "error_type": AuditResult.ERROR_MISSING_SNIPPET,
            "field": "quote_snippet",
            "details": "quote_snippet 不得为空，必须是 NotebookLM 返回的原始文字",
        })

    return violations


def audit_citations(citations: List[Dict]) -> Dict:
    all_violations = []
    unconfirmed_pages = []

    for idx, citation in enumerate(citations):
        violations = validate_citation(citation, idx)
        all_violations.extend(violations)

        page = citation.get("page_locator", "").strip()
        if page == "页码待核":
            unconfirmed_pages.append({
                "citation_index": idx,
                "claim_preview": citation.get("claim", f"Citation #{idx}")[:80],
                "notebooklm_source": citation.get("notebooklm_source", ""),
            })

    report = {
        "status": AuditResult.PASS if not all_violations else AuditResult.FAIL,
        "total_citations": len(citations),
        "violations_count": len(all_violations),
        "unconfirmed_pages_count": len(unconfirmed_pages),
        "violations": all_violations,
        "unconfirmed_pages": unconfirmed_pages,
    }

    return report


def print_report_summary(report: Dict):
    print("\n" + "=" * 60, file=sys.stderr)
    print("CITATION AUDIT REPORT (NotebookLM 模式)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"状态: {report['status']}", file=sys.stderr)
    print(f"总引注数: {report['total_citations']}", file=sys.stderr)
    print(f"违规数: {report['violations_count']}", file=sys.stderr)
    print(f"页码待核数: {report['unconfirmed_pages_count']}", file=sys.stderr)

    if report["violations"]:
        print("\n违规详情:", file=sys.stderr)
        for v in report["violations"]:
            print(f"\n  引注 #{v['citation_index']}:", file=sys.stderr)
            print(f"    陈述: {v['claim_preview']}", file=sys.stderr)
            print(f"    错误类型: {v['error_type']}", file=sys.stderr)
            print(f"    说明: {v['details']}", file=sys.stderr)
    else:
        print("\n✓ 所有引注通过验证", file=sys.stderr)

    if report["unconfirmed_pages"]:
        print("\n⚠ 以下引注页码待核（需用户手动确认）:", file=sys.stderr)
        for up in report["unconfirmed_pages"]:
            print(f"  #{up['citation_index']}: {up['claim_preview']}", file=sys.stderr)
            print(f"    来源: {up['notebooklm_source'][:60]}", file=sys.stderr)

    print("=" * 60 + "\n", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="对 NotebookLM 来源的引注进行三要素审计"
    )
    parser.add_argument("--input", required=True, help="含 citations 数组的输入 JSON 文件")
    parser.add_argument("--report", required=True, help="审计报告输出路径")

    args = parser.parse_args()

    citation_data = load_json(args.input)
    citations = citation_data.get("citations", [])

    if not citations:
        print("Warning: 输入文件中未找到 citations 数组", file=sys.stderr)

    print(f"正在审计 {len(citations)} 条引注...", file=sys.stderr)
    report = audit_citations(citations)

    output_path = Path(args.report)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print_report_summary(report)
    print(f"报告已保存至: {args.report}", file=sys.stderr)

    sys.exit(1 if report["status"] == AuditResult.FAIL else 0)


if __name__ == "__main__":
    main()
