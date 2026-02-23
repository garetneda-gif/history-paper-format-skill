import zipfile
import shutil
from pathlib import Path
from lxml import etree

_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _w(tag: str) -> str:
    return f"{{{_W}}}{tag}"


def set_footnote_restart_each_page(docx_path: str) -> None:
    p = Path(docx_path)
    tmp = p.with_suffix(".tmp.docx")
    shutil.copy2(p, tmp)

    with zipfile.ZipFile(tmp, "r") as zin, zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/settings.xml":
                data = _patch_settings(data)
            zout.writestr(item, data)

    tmp.unlink()


def _patch_settings(xml_bytes: bytes) -> bytes:
    root = etree.fromstring(xml_bytes)
    ns_w = _W

    fpr = root.find(_w("footnotePr"))
    if fpr is None:
        fpr = etree.SubElement(root, _w("footnotePr"))

    nr = fpr.find(_w("numRestart"))
    if nr is None:
        nr = etree.SubElement(fpr, _w("numRestart"))
    nr.set(_w("val"), "eachPage")

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def has_footnote_restart_each_page(docx_path: str) -> bool:
    with zipfile.ZipFile(docx_path, "r") as z:
        if "word/settings.xml" not in z.namelist():
            return False
        data = z.read("word/settings.xml")
    root = etree.fromstring(data)
    fpr = root.find(_w("footnotePr"))
    if fpr is None:
        return False
    nr = fpr.find(_w("numRestart"))
    if nr is None:
        return False
    return nr.get(_w("val")) == "eachPage"


def has_footnotes_part(docx_path: str) -> bool:
    with zipfile.ZipFile(docx_path, "r") as z:
        return "word/footnotes.xml" in z.namelist()
