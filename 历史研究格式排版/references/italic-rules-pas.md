# PAS 斜体规则文档 (Italic Rules for Physical & Applied Sciences)

## 概述

本文档基于 *The Chicago Manual of Style* (17th ed.) 第7章和 Physical & Applied Sciences (PAS) 引注规范，规定学术论文中何时使用斜体（italic）、何时使用正体（roman），以及边界情形的处理策略。

**核心原则**:
- ✅ 斜体用于**作品标题**、**未归化外语术语**、**特定专有名词**
- ❌ 正体用于**文章标题**（使用引号）、**已英语化外来词**、**机构名/地名/人名**
- ⚠️ 低置信度情形必须标记 `<!-- NEEDS_REVIEW: italic -->`，由人工审核

---

## 第一部分：INCLUDE（应使用斜体）

以下类型必须使用斜体（`<i>` 或 `<em>`）：

### 1. 独立出版著作（书名） 📘

**规则**: 所有独立出版的书籍、专著、学位论文使用斜体。

**示例**:
```html
<i>The Structure of Scientific Revolutions</i>
<i>Origin of Species</i>
<i>A Brief History of Time</i>
```

**参考**: CMS 8.166

---

### 2. 期刊名、报纸名 📘

**规则**: 期刊全称、报纸名称使用斜体（不包括文章标题）。

**示例**:
```html
<i>Nature</i>
<i>Science</i>
<i>The New York Times</i>
<i>Physical Review Letters</i>
```

**注意**: 文章标题使用引号，不斜体：
```html
"Dark matter evidence in galaxy rotation curves," <i>Nature</i> 542 (2017): 123-128.
```

**参考**: CMS 14.198

---

### 3. 艺术品名与长篇史诗标题 📘

**规则**: 绘画、雕塑、长篇史诗、歌剧、交响乐作品使用斜体。

**示例**:
```html
<i>Mona Lisa</i>
<i>The Thinker</i>
<i>Iliad</i>
<i>The Magic Flute</i>
```

**参考**: CMS 8.193

---

### 4. 出版文集标题 📘

**规则**: 已出版的论文集、会议论文集名称使用斜体。

**示例**:
```html
<i>Proceedings of the 2023 IEEE Conference on Computer Vision</i>
<i>Advances in Neural Information Processing Systems</i>
```

**参考**: CMS 14.176

---

### 5. 未归化外语术语（首次出现时） 📘

**规则**: 首次出现的外语术语（尚未英语化）使用斜体，之后可改正体。

**示例**:
```html
<!-- 首次出现 -->
The concept of <i>Weltanschauung</i> (worldview) is central to this theory.

<!-- 再次出现（可选正体） -->
This Weltanschauung influenced later philosophers.
```

**已归化词（正体）**:
```html
<!-- 已英语化，不斜体 -->
The Gestapo arrested him in 1943.
Renaissance art flourished in Italy.
```

**参考**: CMS 7.53

---

### 6. 法律案件名 📘

**规则**: 法律案件名称使用斜体（但 "v." 正体）。

**示例**:
```html
<i>Brown</i> v. <i>Board of Education</i>
<i>Roe</i> v. <i>Wade</i>
```

**参考**: CMS 14.281

---

### 7. 船名 📘

**规则**: 船只名称使用斜体（但 HMS、USS 等前缀正体）。

**示例**:
```html
HMS <i>Victory</i>
USS <i>Enterprise</i>
<i>Titanic</i>
```

**参考**: CMS 8.116

---

### 8. 固定缩写：`ibid.`、`et al.` 📘

**规则**: 拉丁语缩写在引注中使用斜体。

**示例**:
```html
<i>ibid.</i>, p. 45.
Smith <i>et al.</i> (2023) demonstrated...
```

**参考**: CMS 14.34, 15.26

---

## 第二部分：EXCLUDE（应使用正体，不可斜体）

以下类型**禁止使用斜体**，必须使用正体（roman）：

### 1. 文章标题与章节标题 📘

**规则**: 期刊文章、书籍章节标题使用引号（quotation marks），不斜体。

**示例**:
```html
<!-- ✅ 正确：引号 + 正体 -->
"The role of dark matter in galaxy formation," <i>Nature</i> 542 (2017): 123.

<!-- ❌ 错误：斜体 -->
<i>The role of dark matter in galaxy formation</i>, Nature 542 (2017): 123.
```

**参考**: CMS 14.177

---

### 2. 未出版档案与手稿描述 📘

**规则**: 档案馆藏、未出版手稿的描述性文字使用正体。

**示例**:
```html
<!-- ✅ 正确：正体 -->
Letter from Einstein to Bohr, 1935, Albert Einstein Archives, Hebrew University, Jerusalem.

<!-- ❌ 错误：斜体 -->
<i>Letter from Einstein to Bohr, 1935</i>, Albert Einstein Archives...
```

**参考**: CMS 14.221

---

### 3. 机构名称 📘

**规则**: 大学、研究所、公司名称使用正体。

**示例**:
```html
<!-- ✅ 正确：正体 -->
Massachusetts Institute of Technology
National Institutes of Health
Max Planck Institute for Physics

<!-- ❌ 错误：斜体 -->
<i>Massachusetts Institute of Technology</i>
```

**参考**: CMS 8.66

---

### 4. 地名 📘

**规则**: 所有地理名称（国家、城市、地区）使用正体。

**示例**:
```html
<!-- ✅ 正确：正体 -->
Beijing, China
Silicon Valley
The Alps

<!-- ❌ 错误：斜体 -->
<i>Beijing</i>, China
```

---

### 5. 人名 📘

**规则**: 所有人名使用正体（无论语言）。

**示例**:
```html
<!-- ✅ 正确：正体 -->
Albert Einstein
Marie Curie
李四光

<!-- ❌ 错误：斜体 -->
<i>Albert Einstein</i>
```

---

### 6. 已英语化外来词 📘

**规则**: 已进入英语日常用语的外来词使用正体（不需斜体）。

**已英语化词典（正体）**:

| 外来词 | 来源 | 说明 |
|--------|------|------|
| Gestapo | 德语 | 已英语化，正体 |
| Renaissance | 法语 | 已英语化，正体 |
| karate | 日语 | 已英语化，正体 |
| sushi | 日语 | 已英语化，正体 |
| plaza | 西班牙语 | 已英语化，正体 |

**未归化词（斜体）**:

| 外来词 | 来源 | 说明 |
|--------|------|------|
| *Weltanschauung* | 德语 | 未归化，需斜体 |
| *Sturm und Drang* | 德语 | 未归化，需斜体 |
| *realpolitik* | 德语 | 未归化，需斜体（首次） |

**判断标准**:
1. 查询 *Merriam-Webster* 或 *Oxford English Dictionary*
2. 若词条存在且无斜体标注 → 正体
3. 若词条不存在或标注为 "foreign term" → 斜体

**参考**: CMS 7.53

---

## 第三部分：EDGE CASES（边界情形与低置信度处理）

### 情形1：首次出现外语词的处理

**规则**:
- 首次出现：使用斜体 + 括号注释英文释义
- 之后重复：可改正体（若已在文中定义）

**示例**:
```html
<!-- 首次 -->
The concept of <i>Bildung</i> (self-cultivation) is central to German philosophy.

<!-- 再次（可选正体） -->
Humboldt's notion of Bildung influenced modern education.
```

**实施策略**:
- AI 检测首次出现时标记 `<i>`
- 低置信度时标记 `<!-- NEEDS_REVIEW: italic; first occurrence of 'Bildung' -->`

---

### 情形2：已归化 vs 未归化判断

**高置信度情形（无需标记）**:

| 词汇 | 判断 | 原因 |
|------|------|------|
| Gestapo | 正体 | 已收录 *Merriam-Webster* |
| Renaissance | 正体 | 已收录 *Merriam-Webster* |
| sushi | 正体 | 已收录 *Merriam-Webster* |

**低置信度情形（需标记 NEEDS_REVIEW）**:

| 词汇 | 处理 | 原因 |
|------|------|------|
| realpolitik | `<i>realpolitik</i><!-- NEEDS_REVIEW: italic; check if naturalized -->` | 部分词典正体，部分斜体 |
| Zeitgeist | `<i>Zeitgeist</i><!-- NEEDS_REVIEW: italic; check if naturalized -->` | 使用频率高但仍有争议 |
| gesundheit | `gesundheit<!-- NEEDS_REVIEW: italic; colloquial usage -->` | 口语化但非正式收录 |

---

### 情形3：文集中的文章标题

**规则**:
- 文集标题（出版）→ 斜体
- 文集中的单篇文章 → 引号 + 正体

**示例**:
```html
<!-- ✅ 正确 -->
"Dark matter constraints from gravitational lensing," in <i>Proceedings of the 2023 APS Meeting</i>, ed. John Smith (New York: APS Press, 2023), 45-67.

<!-- ❌ 错误 -->
<i>Dark matter constraints from gravitational lensing</i>, in <i>Proceedings of the 2023 APS Meeting</i>...
```

---

### 情形4：软件/数据库名称

**规则**:
- 商业软件（如 Microsoft Word）→ 正体
- 开源项目（GitHub 仓库名）→ 正体 + 等宽字体（`code`）

**示例**:
```html
<!-- 商业软件 -->
Data were analyzed using MATLAB R2023a.

<!-- 开源项目 -->
We used the <code>scipy</code> library for statistical analysis.
```

**参考**: CMS 8.197（计算机程序名正体）

---

### 情形5：学位论文（已发表 vs 未发表）

**规则**:
- 已出版（如 ProQuest）→ 斜体
- 未出版（仅存档）→ 引号 + 正体

**示例**:
```html
<!-- 已出版 -->
John Smith, <i>The Role of Dark Matter in Galaxy Formation</i> (PhD diss., MIT, 2020), ProQuest (28012345).

<!-- 未出版 -->
Jane Doe, "Quantum entanglement in superconducting qubits" (PhD diss., Stanford University, 2023).
```

**参考**: CMS 14.218

---

## 低置信度标记规范

当 AI 无法确定是否使用斜体时，必须使用以下格式标记：

```html
<!-- 格式 -->
<element><!-- NEEDS_REVIEW: italic; <reason> --></element>

<!-- 示例1：外来词归化不确定 -->
<i>realpolitik</i><!-- NEEDS_REVIEW: italic; check if naturalized in Merriam-Webster -->

<!-- 示例2：文集 vs 期刊不确定 -->
<i>Proceedings of CVPR 2023</i><!-- NEEDS_REVIEW: italic; verify if published as book or journal -->

<!-- 示例3：首次出现判断不确定 -->
<i>Bildung</i><!-- NEEDS_REVIEW: italic; first occurrence, check if already defined earlier -->
```

**人工审核流程**:
1. 搜索 HTML 中所有 `NEEDS_REVIEW: italic`
2. 查询权威来源（CMS、*Merriam-Webster*、期刊规范）
3. 移除注释，确认使用 `<i>` 或 `<span>`（正体）

---

## 例外词典（快速查询）

### 正体词（已英语化，无需斜体）

| 词汇 | 来源 | 依据 |
|------|------|------|
| Gestapo | 德语 | *Merriam-Webster* 正体 |
| Renaissance | 法语 | *Merriam-Webster* 正体 |
| karate | 日语 | *Merriam-Webster* 正体 |
| sushi | 日语 | *Merriam-Webster* 正体 |
| plaza | 西班牙语 | *Merriam-Webster* 正体 |

### 斜体词（未归化，需斜体）

| 词汇 | 来源 | 依据 |
|------|------|------|
| *Weltanschauung* | 德语 | CMS 7.53（首次需斜体） |
| *Sturm und Drang* | 德语 | CMS 7.53（未归化） |
| *realpolitik* | 德语 | *Merriam-Webster* 标为斜体 |
| *schadenfreude* | 德语 | 首次需斜体，之后可正体 |

---

## 实施检查清单

生成 HTML 后，必须验证：

### 必检项

- [ ] 所有书名使用 `<i>` 斜体
- [ ] 所有期刊名使用 `<i>` 斜体
- [ ] 所有文章标题使用引号（`"..."`）+ 正体
- [ ] 机构名/地名/人名全部正体
- [ ] 已英语化外来词（Gestapo, Renaissance 等）正体
- [ ] 未归化外来词（*Weltanschauung* 等）斜体
- [ ] 法律案件名使用 `<i>` 斜体（v. 正体）
- [ ] 船名使用 `<i>` 斜体
- [ ] `ibid.` 和 `et al.` 使用 `<i>` 斜体

### 低置信度检查

- [ ] 搜索所有 `<!-- NEEDS_REVIEW: italic -->`
- [ ] 对每条标记进行人工审核
- [ ] 查询权威来源（CMS/*Merriam-Webster*/期刊规范）
- [ ] 移除注释，确认最终格式

---

## 参考来源

- *The Chicago Manual of Style*, 17th ed. (University of Chicago Press, 2017), Chapter 7 & 14.
- *Merriam-Webster's Collegiate Dictionary*, 11th ed.
- *Oxford English Dictionary* (OED Online)
- PAS (Physical & Applied Sciences) 引注规范

---

## 版本历史

- **v1.0** (2026-02-23): 初始版本，基于 CMS 第17版和 PAS 规范
