---
name: 历史研究格式排版
description: 将 Word 文档（.docx）按《历史研究》期刊排版规范重新排版，输出符合规格的 .docx 文件。触发词：历史排版、历史研究格式
---

# 历史研究格式排版

本 Skill 将用户提供的 Word 文档（.docx）按《历史研究》核心期刊规范重新排版，输出 .docx 文件。

## 触发条件

用户提及以下关键词时触发：
- 历史排版
- 历史研究格式
- 历史学期刊排版

## 使用方式

### 输入

- Word 文档（.docx）

### 排版命令

```bash
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/format_docx.py \
  --input 论文.docx \
  --output 排版后.docx
```

默认会在输入文件同目录生成 `.bak.docx` 备份。若不需要备份：

```bash
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/format_docx.py \
  --input 论文.docx \
  --output 排版后.docx \
  --no-backup
```

### 校验命令

```bash
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/validate_docx.py 排版后.docx
```

期望输出：全部 PASS，退出码 0。

### 完整工作流程

1. 用户提供 .docx 文件路径
2. 调用 `format_docx.py` 执行排版
3. 调用 `validate_docx.py` 进行机器校验（exit 0 表示通过）
4. 将排版后 .docx 交付用户

---

## 排版规格速查

| 元素 | 东亚字体 | 拉丁字体 | 字号 | 行距 | 缩进 |
|------|---------|---------|------|------|------|
| 正文 | 宋体 | Times New Roman | 小4（12pt） | 17.9pt | 首行2字符 |
| 大标题 | 宋体 | Times New Roman | 1号（26pt） | — | 居中 |
| 副标题 | 仿宋 | Times New Roman | 小2（18pt） | — | 居中 |
| 二级标题 | 宋体 | Times New Roman | 3号（16pt） | — | — |
| 摘要/关键词标签 | 黑体 | Times New Roman | 小4（12pt） | 17.9pt | 左缩进1字符 |
| 摘要/关键词内容 | 仿宋 | Times New Roman | 小4（12pt） | 17.9pt | 左右各1字符 |
| 独立引文 | 楷体 | Times New Roman | 小4（12pt） | 17.9pt | 左右各2字符 |
| 脚注 | 楷体 | Times New Roman | 5号（10.5pt） | 14.5pt | 左右各1字符 |

### 页边距

| 上 | 下 | 左 | 右 |
|----|----|----|-----|
| 3.3cm | 2.7cm | 2.4cm | 2.3cm |

---

## 命名样式（8个，前缀 HR-）

| 样式名 | 对应元素 |
|--------|---------|
| `HR-Body` | 普通正文 |
| `HR-QuoteBlock` | 独立引文块 |
| `HR-FootnoteText` | 脚注正文 |
| `HR-TitleMain` | 文章大标题 |
| `HR-Subtitle` | 副标题 |
| `HR-AbstractLabel` | 摘要/关键词标签 |
| `HR-AbstractText` | 摘要/关键词内容 |
| `HR-SectionL2` | 二级标题 |

---

## 段落自动分类规则

`format_docx.py` 根据以下优先级分类段落：

1. **已有 HR- 样式** → 保留不变
2. **Word 内置标题样式** → 映射到对应 HR- 样式
   - `Heading 1` / `Title` → `HR-TitleMain`
   - `Heading 2` / `Subtitle` → `HR-Subtitle`
   - `Heading 3/4` → `HR-SectionL2`
   - `Quote` / `Block` → `HR-QuoteBlock`
   - `Footnote` → `HR-FootnoteText`
3. **文本特征匹配**（正则）
   - `摘要：` / `关键词：` 开头 → `HR-AbstractLabel`
   - `一、` / `（一）` 等 → `HR-SectionL2`
4. **默认** → `HR-Body`

---

## 脚注每页重排

通过 OOXML 直改 `word/settings.xml` 注入：

```xml
<w:footnotePr>
  <w:numRestart w:val="eachPage"/>
</w:footnotePr>
```

---

## PAS 斜体规则

低置信度斜体（无法确认是否符合 PAS 规范）的 run 将被标记 `NEEDS_REVIEW: italic`，禁止自动改写。校验器会统计未标注的斜体 run 并以 WARN 形式输出，不导致 exit 1。

---

## 校验规则（共 25 条）

| 类别 | 条数 | 示例 |
|------|------|------|
| 边距 | 4 | margin_top ≈ 1188000 twips |
| 样式存在性 | 8 | HR-Body 等 8 个 HR- 样式存在 |
| 字号 | 5 | HR-Body=12pt, HR-TitleMain=26pt |
| 行距 | 2 | HR-Body=17.9pt, HR-FootnoteText=14.5pt |
| 字体 | 4 | latin=TNR, eastAsia=宋体/楷体 |
| 脚注结构 | 1 | numRestart=eachPage |
| PAS 斜体 | 1 | WARN 未标注斜体 run |

---

## 错误处理

| 错误 | 退出码 | 说明 |
|------|--------|------|
| 输入文件不存在 | 1 | 输出到 stderr |
| 输入非 .docx | 1 | 输出到 stderr |
| 校验存在 FAIL | 1 | 输出失败条目 |
| 全部 PASS | 0 | — |

---

## 不实现的功能

- 文献 DOI/PubMed/Crossref 自动补链
- 大体积字体文件内嵌
- 人工目测验收

---

## 文件目录

```
历史研究格式排版/
├── SKILL.md
├── references/
│   ├── style-mapping.md          排版规格映射表（docx 版）
│   ├── italic-rules-pas.md       PAS 斜体规则
│   └── footnote-strategy.md      脚注 OOXML 方案
└── scripts/
    ├── format_docx.py            排版主入口
    ├── validate_docx.py          机器校验（25 条规则）
    └── lib/
        ├── specs.py              规格常量
        ├── io_utils.py           文件 I/O
        ├── style_factory.py      命名样式注册
        ├── font_utils.py         中西文字体分离
        ├── paragraph_rules.py    段落分类 + 样式应用
        └── footnote_ooxml.py     脚注 OOXML 操作
```
