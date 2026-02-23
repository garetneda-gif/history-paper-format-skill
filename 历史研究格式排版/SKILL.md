---
name: 历史研究格式排版
description: 将学术论文按历史研究格式规范排版为 HTML，支持单栏连续（在线预览）和双栏分页（PDF 友好）两种输出。触发词：历史排版、历史研究格式
---

# 历史研究格式排版

本 Skill 用于将学术论文转换为符合《历史研究》等历史学核心期刊规范的 HTML 格式。支持两种主要输出模式：适合在线阅读的单栏连续页面，以及适合打印和导出 PDF 的双栏分页排版。

## 触发条件
当用户提及以下关键词时触发：
- 历史排版
- 历史研究格式
- 历史学期刊排版

## 使用方式

### 输入格式
- Markdown 文件（.md）
- 或直接粘贴文本（代理将创建临时 .md 文件后调用渲染脚本）

### 渲染命令

```bash
# 单栏连续（在线预览）
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/render.py \
  --mode single \
  --input 论文.md \
  --output 单栏连续-论文.html

# 双栏分页（PDF 打印）
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/render.py \
  --mode two-column \
  --input 论文.md \
  --output 双栏分页-论文.html
```

### 工作流程
1. 用户提供论文内容（Word/Markdown/粘贴文本）
2. 代理将内容整理为 Markdown 格式
3. 调用 render.py 选择输出模式
4. 验证输出 HTML 的字体、边距、行距规格
5. 交付两种格式的 HTML 文件

### 排版规格速查
| 元素 | 字体 | 字号 | 行距 |
|------|------|------|------|
| 正文 | 宋体 + Times New Roman | 小4(12pt) | 17.9pt |
| 大标题 | 宋体 | 1号(26pt) | — |
| 副标题 | 仿宋 | 小2(18pt) | — |
| 二级标题 | 宋体 | 3号(16pt) | — |
| 摘要/关键词标签 | 黑体 | 小4(12pt) | — |
| 摘要/关键词内容 | 仿宋 | 小4(12pt) | — |
| 独立引文 | 楷体 | 小4(12pt) | — |
| 脚注 | 楷体 | 5号(10.5pt) | 14.5pt |

### 模式选择说明

**单栏连续模式（single）**：
- 适用场景：在线阅读、网页发布
- 特点：连续滚动，无分页符
- 页面模拟：A4 纸边距视觉效果（通过 padding 实现）
- 输出：单一 HTML 文件，背景灰色（模拟纸张效果）

**双栏分页模式（two-column）**：
- 适用场景：打印输出、PDF 导出
- 特点：每页独立容器，双栏布局，页眉页脚
- 页面控制：使用 `@page` CSS 规则和 `page-break-after`
- 输出：多页结构，每页背景白色，页间间隔 10mm

### 输入 Markdown 样例
参见 `references/sample.md`，包含：
- 主标题（`# 标题`）
- 副标题（`## 副标题`）
- 作者/单位（`**作者：**` / `**单位：**`）
- 摘要/关键词（`**摘要：**` / `**关键词：**`）
- 章节标题（`## 一、` / `## 二、`）
- 正文段落（自动缩进 2em）
- 独立引文（`> 引文内容`）
- 脚注（`[^1]` 引用和 `[^1]:` 定义）

### 错误处理
- **无效模式**：退出码 1，输出 "supported modes: single, two-column"
- **文件不存在**：退出码 1，输出 "ERROR: 输入文件不存在"
- **模板缺失**：退出码 1，输出 "ERROR: 模板文件不存在"

---

## 验证命令清单

排版完成后，运行以下命令进行机器验证（均应返回退出码 0）：

```bash
VALIDATOR="/Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/validate_layout.py"

# 校验单栏模板（18/18 规则）
python3 "$VALIDATOR" \
  "/Users/jikunren/.config/opencode/skills/历史研究格式排版/assets/template-single-column.html"

# 校验双栏模板（18/18 规则）
python3 "$VALIDATOR" \
  "/Users/jikunren/.config/opencode/skills/历史研究格式排版/assets/template-two-column.html"

# 校验用户生成的输出文件
python3 "$VALIDATOR" 输出文件.html
```

校验规则 18 条分布：
- **边距**（4条）：上 3.3cm / 下 2.7cm / 左 2.4cm / 右 2.3cm
- **字号**（5条）：正文 12pt / 大标题 26pt / 二级标题 16pt / 脚注 10.5pt / 摘要 12pt
- **行距**（2条）：正文 17.9pt / 脚注 14.5pt
- **字体**（2条）：Times New Roman + @font-face / SimSun/STSong
- **PAS 斜体**（4条）：ibid./et al. 斜体 / 文章标题不误用斜体 / NEEDS_REVIEW 标记检测 / 船名规则注册
- **版芯**（1条）：36 字宽（16cm）

---

## 脚注每页编号兼容性说明

### 当前实现
- 使用 CSS `counter-reset: footnote` 在每个 `.page` 容器上，**每页脚注序号从 1 重新开始**
- 纯 CSS 方案，无需 JavaScript，任意浏览器均可预览

### 已知限制
- **浏览器打印分页**：若依赖浏览器原生 `Ctrl+P` 打印，脚注序号可能不与视觉分页对齐（因浏览器自动分页逻辑与 `.page` div 无关）
- **推荐打印方案**：每页使用独立 `.page` div，确保视觉分页与逻辑分页一致；打印时浏览器应识别 `page-break-after: always`

### Paged.js 升级路径
模板内已保留 Paged.js 注释（`<!-- footnote reset fallback -->`），若需要精确分页，可参考：
```html
<!-- 解注以启用 Paged.js 精确分页（需联网） -->
<!-- <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script> -->
```

---

## 完整运行示例

### 示例 A：单栏连续（在线预览）

```bash
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/render.py \
  --mode single \
  --input /Users/jikunren/.config/opencode/skills/历史研究格式排版/references/sample.md \
  --output /tmp/preview-single.html

# 校验输出
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/validate_layout.py \
  /tmp/preview-single.html
# 期望：退出码 0，18/18 PASS
```

### 示例 B：双栏分页（PDF 打印）

```bash
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/render.py \
  --mode two-column \
  --input /Users/jikunren/.config/opencode/skills/历史研究格式排版/references/sample.md \
  --output /tmp/preview-two-column.html

# 校验输出
python3 /Users/jikunren/.config/opencode/skills/历史研究格式排版/scripts/validate_layout.py \
  /tmp/preview-two-column.html
# 期望：退出码 0，18/18 PASS
```

---

## 文件目录

```
历史研究格式排版/
├── SKILL.md                              本文件（Skill 使用说明）
├── assets/
│   ├── template-single-column.html       单栏连续模板
│   └── template-two-column.html          双栏分页模板
├── references/
│   ├── style-mapping.md                  排版规格映射表
│   ├── italic-rules-pas.md               PAS 斜体规则（斜体/正体适用范围）
│   ├── footnote-strategy.md              脚注每页编号技术方案
│   └── sample.md                         最小样本（测试用）
└── scripts/
    ├── render.py                          渲染入口（--mode single/two-column）
    └── validate_layout.py                 自动化校验脚本（18 条规则，机器可执行）
```
