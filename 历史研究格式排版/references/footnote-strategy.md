# 脚注每页重排技术方案 — OOXML 版

## 方案概述

通过直接修改 .docx 压缩包内 `word/settings.xml` 注入 OOXML 节点，实现 Word 原生"每页脚注重新编号"。

## 实现原理

在 `<w:settings>` 根节点下添加：

```xml
<w:footnotePr>
  <w:numRestart w:val="eachPage"/>
</w:footnotePr>
```

Word 读取此节点后，每页脚注序号从 1 重新开始。

## Python 实现

```python
import zipfile, shutil
from pathlib import Path
from lxml import etree

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def _w(tag):
    return f"{{{_W}}}{tag}"

def set_footnote_restart_each_page(docx_path):
    p = Path(docx_path)
    tmp = p.with_suffix(".tmp.docx")
    shutil.copy2(p, tmp)

    with zipfile.ZipFile(tmp, "r") as zin, \
         zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/settings.xml":
                root = etree.fromstring(data)
                fpr = root.find(_w("footnotePr"))
                if fpr is None:
                    fpr = etree.SubElement(root, _w("footnotePr"))
                nr = fpr.find(_w("numRestart"))
                if nr is None:
                    nr = etree.SubElement(fpr, _w("numRestart"))
                nr.set(_w("val"), "eachPage")
                data = etree.tostring(root, xml_declaration=True,
                                      encoding="UTF-8", standalone=True)
            zout.writestr(item, data)

    tmp.unlink()
```

## 注意事项

- 必须在 `doc.save()` **之后**调用，否则保存动作会覆盖补丁
- lxml 为必需依赖（`pip install lxml`）
- 该方案只设置编号重排策略，脚注内容本身仍由 Word 正常管理

## 版本历史

- **v2.0** (2026-02-23): 重写为 OOXML 方案，替代原 CSS Counter 方案
