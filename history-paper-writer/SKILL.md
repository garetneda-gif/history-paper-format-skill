---
name: history-paper-writer
description: 历史学学术论文写作技能。用户提供论文大纲和 NotebookLM 链接（已上传参考文献PDF），按《历史研究》引注规范输出投稿级DOCX论文。每条引用必须可追溯至 NotebookLM 文献来源，禁止虚构文献。触发词：写论文、学术论文、历史研究、引注规范、论文写作。
---

# 历史学术论文写作

## 触发条件

当用户满足以下**全部**条件时激活本技能：
- 明确要求写一篇**历史学**学术论文
- 提供了 NotebookLM 笔记本链接（已预先上传参考文献PDF）
- 提供了论文大纲（outline.md / outline.txt，或在对话中直接给出）

## 输入契约

| 必需项 | 说明 |
|--------|------|
| NotebookLM URL | `https://notebooklm.google.com/notebook/...`，用户已上传所有参考文献PDF |
| 论文大纲 | outline.md / outline.txt，或对话中直接提供 |
| 论文元信息 | 题目、作者姓名 |

> **不再需要本地文献目录**。所有参考文献由用户预先上传至 NotebookLM，Claude 通过 MCP 工具查询。

论文目录结构（仅输出文件）：

```
{论文目录}/
├── outline.md               ← 用户大纲（可选，也可对话提供）
├── citation_claims.json     ← 引注审计数据（自动生成）
├── audit_report.json        ← 审计报告（自动生成）
└── {论文题目}.docx          ← 最终输出（自动生成）
```

## 输出契约

最终 `.docx` 文件包含：
1. **封面**：题目（1号宋体）、作者（小2号仿宋）
2. **中文摘要**：摘要标识（小4号黑体）+ 内容（小4号仿宋）
3. **中文关键词**：关键词标识（小4号黑体）+ 词组（小4号仿宋）
4. **英文摘要**：Abstract 标识 + 内容
5. **英文关键词**：Keywords 标识 + 词组
6. **正文**：小4号宋体，行距17.9磅，首行缩进2字符
7. **脚注**：5号楷体，行距14.5磅，圈号①②③，每页重新编号
8. **参考文献**：完整引用列表

页面设置：上3.3cm / 下2.7cm / 左2.4cm / 右2.3cm，每页36字×35行。

---

## 工作流程

### 阶段1：初始化与 NotebookLM 接入

**步骤 1：认证检查**

调用 `mcp__notebooklm__get_health` 确认认证状态：
- `authenticated: true` → 继续
- `authenticated: false` → 提示用户运行 `mcp__notebooklm__setup_auth`（会弹出浏览器手动登录）
- 触达免费账户 50 次/日配额时，调用 `mcp__notebooklm__re_auth` 切换账号

**步骤 2：笔记本注册**

调用 `mcp__notebooklm__list_notebooks` 检查用户提供的 NotebookLM URL 是否已在库中：
- 已存在 → 记录其 `notebook_id`，后续查询优先使用 `notebook_id`（比 URL 稳定）
- 不存在 → 先用 `notebook_url` 发起首次查询，获取内容后再用 `mcp__notebooklm__add_notebook` 将其加入库

> 整篇论文写作期间使用固定 `session_id`（如 `paper_论文题目`），以保持跨问题的上下文连贯性。

**步骤 3：文献概览查询**

调用 `mcp__notebooklm__ask_question`：

```
参数:
  question: "请列出本笔记本中所有已上传的文献，包括每篇文献的完整标题、作者、年份和类型（专著/期刊/档案等）。"
  notebook_id: {已注册的 notebook_id}   # 或 notebook_url（首次）
  session_id: "paper_{论文题目}"
```

记录返回的文献列表，作为后续写作的**可用来源范围**。

**⚠️ follow-up 强制要求**：每次 `ask_question` 响应末尾含有提示"Is that ALL you need to know?"。在回复用户之前，必须评估回答是否完整；若有缺口，**立即追问**，直到信息完全满足需求再继续。

**步骤 4：章节覆盖度探测**

对大纲中每个一级标题，分别调用 `mcp__notebooklm__ask_question`（**复用同一 session_id**）：

```
question: "本笔记本中有哪些文献支持关于[章节主题]的论述？请列出相关文献及其关键论点。"
```

**步骤 5：汇总与用户确认**

告知用户：
- 文献充足的章节
- 文献不足或缺失的章节（提示用户补充上传相关文献到 NotebookLM）

**等待用户确认**：若存在文献缺口，用户选择补充上传后重试步骤3，或继续（标注待补充处）

### 阶段2：详细写作计划

1. 基于大纲和文献概览，制定详细写作计划：
   - 每章标题、预计字数
   - 每章拟引用的核心文献（来自 NotebookLM 概览结果）
   - 论证逻辑链：论点 → 史料 → 分析
2. 将写作计划呈现给用户确认
3. 用户确认后进入逐章写作

### 阶段3：逐章写作

对每一章执行以下循环：

1. **史料查询**：在撰写每个论点前，先向 NotebookLM 查询支撑史料：

   ```
   问题："关于[具体论点/事件/人物]，请提供笔记本中的原始史料引文，
         包含：来源文献名称、作者、相关原文段落。"
   ```

   - 若 NotebookLM 返回「文献中未找到相关内容」→ 不得编造，必须标注「此处需补充文献」
   - 若 NotebookLM 返回有来源的内容 → 以该内容为基础写作

2. **撰写正文**：
   - 所有事实性陈述必须附带脚注
   - 脚注内容来自 NotebookLM 查询结果中的文献信息
   - 独立引文（超过3行的直接引用）使用楷体、左右各缩进2字符

3. **同步记录引注审计数据**：
   每插入一条脚注，必须在内部审计记录中登记：

   ```json
   {
     "claim": "正文中的事实性陈述",
     "notebooklm_source": "NotebookLM 返回的来源文献（含标题、作者）",
     "page_locator": "页码（若 NotebookLM 提供）或'见原文'",
     "quote_snippet": "NotebookLM 返回的原始文字片段（用于比对）"
   }
   ```

   **规则**：
   - `notebooklm_source`：必须非空，来自 NotebookLM 的实际回答
   - `quote_snippet`：必须是 NotebookLM 返回的原始文字，不得自行编造
   - `page_locator`：若 NotebookLM 未提供页码，如实标注"页码待核"，不得编造数字

4. **脚注格式**严格遵循 `references/citation-standard-history-research.md`：
   - 中文著作：`责任者：《题名》，出版地：出版者，年份，第X页。`
   - 古籍刻本：`责任者：《题名》卷X，版本，第X页a。`
   - 古籍点校本：`责任者：《题名》，点校者，出版地：出版者，年份，第X页。`
   - 期刊：`责任者：《题名》，《期刊名》年份第X期。`
   - 英文专著：`Author, *Title*, Place: Publisher, Year, p.X.`
   - 日文专著：`責任者：『題名』、出版地：出版者、年份、第X頁。`
   - 再次引用同一文献：简化为 `责任者：《书名》，第X页。`
   - 转引：先标原始出处，再标"转引自"及转引文献信息

   完整格式模板见 `references/citation-standard-history-research.md`。

5. **呈现给用户确认**，用户可要求修改后再继续下一章

### 阶段4：全文组装与引注审计

1. 组装全部章节为完整论文
2. 生成中文摘要和关键词（可向 NotebookLM 查询："请基于以下内容要点，提供核心论述的概括"）
3. 将中文摘要翻译为英文，检查术语一致性
4. 将全文引注数据保存为 `{论文目录}/citation_claims.json`
5. 运行引注审计：

```bash
python3 {skill_dir}/scripts/citation_audit.py \
  --input "{论文目录}/citation_claims.json" \
  --report "{论文目录}/audit_report.json"
```

6. **审计结果处理**：
   - 若 `status: "PASS"` → 继续生成DOCX
   - 若 `status: "FAIL"` → 逐一检查 violations 列表：
     - `MISSING_SOURCE`：`notebooklm_source` 为空 → 必须重新向 NotebookLM 查询
     - `MISSING_SNIPPET`：`quote_snippet` 为空 → 必须重新向 NotebookLM 查询
     - `UNCONFIRMED_PAGE`：页码为"页码待核"且未标注 → 保留标注，用户知情
   - **审计未通过前不允许生成最终DOCX**

### 阶段5：DOCX 生成

1. 将完整论文内容整理为 JSON 格式：

```json
{
  "title": "论文标题",
  "author": "作者姓名",
  "abstract_cn": "中文摘要...",
  "abstract_en": "English abstract...",
  "keywords_cn": ["关键词1", "关键词2"],
  "keywords_en": ["keyword1", "keyword2"],
  "chapters": [
    {
      "title": "第一章 引言",
      "content": "正文内容（脚注标记用①②③）...",
      "footnotes": [
        {"index": 1, "text": "脚注引用内容..."}
      ]
    }
  ],
  "references": ["参考文献1完整条目", "参考文献2完整条目"]
}
```

2. 运行 DOCX 生成脚本：

```bash
node {skill_dir}/scripts/generate_docx.cjs \
  --input "{论文目录}/paper_content.json" \
  --output "{论文目录}/output_raw.docx"
```

3. 解包 DOCX 为 XML：

```bash
python3 ~/.claude/skills/docx/ooxml/scripts/unpack.py \
  "{论文目录}/output_raw.docx" \
  "{论文目录}/docx_unpacked"
```

4. 注入脚注属性（圈号编号 + 每页重排）：

```bash
python3 {skill_dir}/scripts/postprocess_footnotes.py \
  --dir "{论文目录}/docx_unpacked"
```

5. 重新打包为最终 DOCX：

```bash
python3 {skill_dir}/scripts/pack_simple.py \
  "{论文目录}/docx_unpacked" \
  "{论文目录}/{论文题目}.docx"
```

6. 清理中间文件（`output_raw.docx`、`docx_unpacked/`、`paper_content.json`）

### 阶段6：交付

1. 告知用户最终文件位置：`{论文目录}/{论文题目}.docx`
2. 提供审计摘要：总引用数、通过数、NotebookLM 来源分布
3. 提供写作统计：总字数、章节数、脚注数
4. 列出所有「页码待核」标注，提醒用户手动核实

---

## NotebookLM MCP 工具参考

> 来源：[PleasePrompto/notebooklm-mcp — docs/tools.md](https://github.com/PleasePrompto/notebooklm-mcp/blob/main/docs/tools.md)

### 核心工具（Core）

| 工具 | 参数 | 用途 |
|------|------|------|
| `mcp__notebooklm__ask_question` | `question`（必填）, `session_id`（可选）, `notebook_id`（可选）, `notebook_url`（可选）, `show_browser`（可选） | 向 NotebookLM 提问，返回有文献来源的回答 + follow-up 提示 |
| `mcp__notebooklm__get_health` | 无 | 检查认证状态、活跃会话数、配置信息 |
| `mcp__notebooklm__setup_auth` | 无 | 打开浏览器进行首次 Google 登录（浏览器必须可见） |
| `mcp__notebooklm__re_auth` | 无 | 切换 Google 账号或重新认证；触达免费账户 50 次/日配额时使用；会关闭所有会话并清除认证数据 |
| `mcp__notebooklm__list_sessions` | 无 | 查看当前活跃的浏览器会话 |
| `mcp__notebooklm__close_session` | `session_id` | 关闭指定会话 |
| `mcp__notebooklm__reset_session` | `session_id` | 重置会话对话历史（保留 session_id） |

### 笔记本库管理

| 工具 | 说明 |
|------|------|
| `mcp__notebooklm__add_notebook` | 安全的对话式添加，写入前需确认；必须提供 `url`、`name`、`description`、`topics` |
| `mcp__notebooklm__list_notebooks` | 返回库中每个笔记本的 id、name、topics、URL、元数据 |
| `mcp__notebooklm__get_notebook` | 通过 `id` 获取单个笔记本详情 |
| `mcp__notebooklm__select_notebook` | 设置默认活跃笔记本（后续 ask_question 无需指定 notebook_id） |
| `mcp__notebooklm__update_notebook` | 修改元数据字段 |
| `mcp__notebooklm__remove_notebook` | 从库中移除条目（不删除 NotebookLM 中的原始笔记本） |
| `mcp__notebooklm__search_notebooks` | 按 name/description/topics/tags 搜索库 |
| `mcp__notebooklm__get_library_stats` | 返回总数、使用统计等汇总信息 |

### Resources（只读）

| URI | 内容 |
|-----|------|
| `notebooklm://library` | 完整库的 JSON：活跃笔记本、统计、所有条目 |
| `notebooklm://library/{id}` | 特定笔记本的元数据（`{id}` 支持自动补全） |

### ask_question 使用规范

```
参数组合（三选一）:
  ① notebook_id   → 库中已注册的笔记本（推荐，稳定）
  ② notebook_url  → 临时查询未注册的笔记本
  ③ 两者均不填    → 使用 select_notebook 设置的默认笔记本

session_id 规则:
  - 同一篇论文的所有查询使用固定 session_id（如 paper_论文题目）
  - session_id 保持跨问题上下文连贯，免费账户最多 10 个并发 session
  - 15 分钟无活动后自动关闭
```

### Follow-up 强制规则（来自官方文档）

> **"Every `ask_question` response ends with a reminder that nudges your agent to keep asking until the user's task is fully addressed."**

**执行要求**：
1. 收到 ask_question 回答后，**先停下来分析**，对照原始需求判断信息是否完整
2. 若回答缺少具体来源、引文或页码 → **立即追问**，不得直接写作
3. 若回答含"文献中未找到" → 记录为文献缺口，**不得编造**
4. 完全满足需求后，再综合所有回答开始写作

### 史料查询模板

| 场景 | 查询模板 |
|------|---------|
| 文献概览 | "请列出本笔记本中所有已上传的文献，包括完整标题、作者、年份和类型。" |
| 章节覆盖 | "本笔记本中有哪些文献支持关于[主题]的论述？列出文献及关键论点。" |
| 史料查询 | "关于[具体事件/人物/现象]，请提供原始史料引文，包含来源文献名和相关文字。" |
| 直接引文 | "请从[文献名]中找出关于[主题]的原文段落，原文引用，标注大致位置。" |
| 论点核实 | "笔记本中是否有证据支持这一论断：[论断内容]？请提供具体文献依据。" |
| 追问来源 | "你刚才提到的[论断]出自哪篇文献？请给出作者和书名。" |

---

## 反虚构规则（红线）

以下行为**绝对禁止**：

1. **虚构文献**：引用 NotebookLM 未返回的文献（含标题、作者）
2. **虚构页码**：编造页码；NotebookLM 未提供页码时标"页码待核"
3. **篡改引文**：修改 NotebookLM 返回的原文（删节需加省略号）
4. **凭记忆引用**：未经 NotebookLM 查询直接写入事实性陈述
5. **无证据论断**：正文中写入无 NotebookLM 文献支撑的事实
6. **绕过审计**：在审计未通过的情况下生成最终文档

若当前文献不足以支撑某个论点：
- **正确做法**：标注"此处需补充文献（建议上传XXX相关文献到 NotebookLM）"
- **错误做法**：编造一条看似合理的引用

---

## 脚本 CLI 参考

### citation_audit.py — 引注审计

```bash
python3 citation_audit.py --input <引注JSON> --report <报告JSON>
```

- `--input`：包含 `citations` 数组的 JSON 文件
- `--report`：审计报告输出路径
- 退出码：0 = 全部通过，1 = 存在违规
- 违规类型：`MISSING_SOURCE`、`MISSING_SNIPPET`、`MISSING_FIELD`

每条引注审计字段：

```json
{
  "claim": "正文中的事实性陈述（必填）",
  "notebooklm_source": "NotebookLM 返回的文献来源（必填，不得为空）",
  "page_locator": "页码或'页码待核'（必填）",
  "quote_snippet": "NotebookLM 原始文字片段（必填，不得为空）"
}
```

### generate_docx.cjs — DOCX 生成

```bash
node generate_docx.cjs --input <论文JSON> --output <DOCX路径>
```

- `--input`：包含完整论文结构的 JSON 文件
- `--output`：输出 DOCX 文件路径
- JSON 必需字段：`title`、`author`、`abstract_cn`、`abstract_en`、`keywords_cn`、`keywords_en`、`chapters`、`references`
- 每章 `chapters[].content` 中用圈号①②③标记脚注位置
- 每章 `chapters[].footnotes[]` 对应脚注内容

### postprocess_footnotes.py — 脚注后处理

```bash
python3 postprocess_footnotes.py --dir <解包后的DOCX目录>
```

- `--dir`：unpack.py 解包后的 DOCX 目录
- 注入 `numRestart="eachPage"`（每页重新编号）
- 注入 `numFmt="decimalEnclosedCircle"`（圈号①②③）
- 限制：Unicode 圈号最多到⑳（20），超过 20 条/页回退为阿拉伯数字

### pack_simple.py — OOXML 回包

```bash
python3 pack_simple.py <解包目录> <输出DOCX路径>
```

- 将修改后的 XML 重新打包为 DOCX
- 兼容 Python 3.9+

---

## 依赖技能

本技能执行时需加载以下技能：

| 技能 | 用途 | 何时使用 |
|------|------|----------|
| `notebooklm` (MCP) | 查询文献内容、获取史料 | 全流程核心工具 |
| `docx` | OOXML 解包/回包工具链 | 阶段5（DOCX生成后处理） |

---

## 引注格式速查

详细模板见 `references/citation-standard-history-research.md`，以下为常用类型：

| 类型 | 格式 |
|------|------|
| 著作 | 作者：《书名》，出版地：出版社，年份，第X页。 |
| 析出文献 | 作者：《篇名》，《文集名》第X册，出版地：出版社，年份，第X页。 |
| 古籍刻本 | 作者：《书名》卷X，版本，第X页a。 |
| 古籍点校本 | 作者：《书名》，点校者，出版地：出版社，年份，第X页。 |
| 古籍影印本 | 作者：《书名》卷X，出版地：出版社，年份影印本，册，第X页下栏。 |
| 期刊 | 作者：《篇名》，《期刊名》年份第X期。 |
| 报纸 | 作者：《篇名》，《报纸名》年月日，第X版。 |
| 档案 | 《文件名》，日期，档案号，藏所。 |
| 转引 | 原作者：《原题》，原版本，原页码，转引自 转引者：《转引题》，版本，页码。 |
| 英文专著 | Author, *Title*, Place: Publisher, Year, p.X. |
| 英文期刊 | Author, "Title," *Journal*, Vol.X, No.X, Year, pp.X-X. |
| 日文专著 | 責任者：『題名』、出版地：出版者、年份、第X頁。 |
| 再次引用 | 作者：《书名》，第X页。 |
