#!/usr/bin/env python3
"""
OOXML Footnote Postprocessor

Injects footnote properties into unpacked DOCX XML:
- numRestart="eachPage" (restart numbering per page)
- numFmt="decimalEnclosedCircle" (circled numbers ①②③)

Usage:
    python postprocess_footnotes.py --dir <unpacked-docx-dir>
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# XML namespace for Word
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def inject_footnote_properties(settings_path):
    """Modify word/settings.xml to add footnote properties"""
    ET.register_namespace(
        "w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    )

    tree = ET.parse(settings_path)
    root = tree.getroot()

    # Check if footnotePr already exists
    footnote_pr = root.find(f"{WORD_NS}footnotePr")

    if footnote_pr is None:
        # Create new footnotePr element
        footnote_pr = ET.SubElement(root, f"{WORD_NS}footnotePr")

    # Add or update numRestart
    num_restart = footnote_pr.find(f"{WORD_NS}numRestart")
    if num_restart is None:
        num_restart = ET.SubElement(footnote_pr, f"{WORD_NS}numRestart")
    num_restart.set(f"{WORD_NS}val", "eachPage")

    # Add or update numFmt
    num_fmt = footnote_pr.find(f"{WORD_NS}numFmt")
    if num_fmt is None:
        num_fmt = ET.SubElement(footnote_pr, f"{WORD_NS}numFmt")
    num_fmt.set(f"{WORD_NS}val", "decimalEnclosedCircle")

    # Write back with XML declaration
    tree.write(settings_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ Injected footnote properties into {settings_path}")


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--dir":
        print("Usage: postprocess_footnotes.py --dir <unpacked-docx-dir>")
        sys.exit(1)

    docx_dir = Path(sys.argv[2])
    settings_path = docx_dir / "word" / "settings.xml"

    if not settings_path.exists():
        print(f"Error: {settings_path} not found")
        sys.exit(1)

    inject_footnote_properties(settings_path)


if __name__ == "__main__":
    main()
