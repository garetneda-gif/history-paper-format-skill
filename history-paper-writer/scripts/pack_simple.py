#!/usr/bin/env python3
"""
Simple pack script for Python 3.9 compatibility

Creates a .docx file from an unpacked directory without validation.
"""

import sys
import zipfile
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: pack_simple.py <input_directory> <output_file>")
    sys.exit(1)

input_dir = Path(sys.argv[1])
output_file = Path(sys.argv[2])

if not input_dir.is_dir():
    print(f"Error: {input_dir} is not a directory")
    sys.exit(1)

output_file.parent.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in input_dir.rglob("*"):
        if f.is_file():
            zf.write(f, f.relative_to(input_dir))

print(f"✅ Packed {output_file}")
