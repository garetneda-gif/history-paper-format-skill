import shutil
import sys
from pathlib import Path


def resolve_input(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        print(f"ERROR: 输入文件不存在: {path}", file=sys.stderr)
        sys.exit(1)
    if p.suffix.lower() != ".docx":
        print(f"ERROR: 输入文件必须是 .docx 格式: {path}", file=sys.stderr)
        sys.exit(1)
    return p


def resolve_output(path: str, input_path: Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def backup_input(input_path: Path) -> Path:
    backup = input_path.with_suffix(".bak.docx")
    shutil.copy2(input_path, backup)
    return backup
