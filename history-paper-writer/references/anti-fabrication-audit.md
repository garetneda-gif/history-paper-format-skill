# 引文防造假审计清单 (Anti-Fabrication Audit Checklist)

## 1. 核心原则
每一条引注必须经过三要素验证，确保史实准确、来源真实。严禁任何形式的文献造假或过度推导。

---

## 2. 三要素验证 (Mandatory Fields)

每一条引文在进入初稿前，必须在审计记录中登记以下三个字段：

| 字段名称 (Field) | 要求说明 (Requirements) | 示例 (Example) |
| :--- | :--- | :--- |
| **source_path** | 引用来源文件的**绝对路径**或明确的数据库定位。 | `/Users/jikunren/Documents/Archives/NARA_RG59_Box1032.pdf` |
| **page_locator** | 准确的**页码、段落或章节**定位。古籍需注a/b面或栏位。 | 第461页下栏 |
| **quote_snippet** | 来源文件中的**原始文字片段**。用于比对引文是否变形。 | “惠施多方，其书五车。” |

---

## 3. 审计操作流程 (Audit Workflow)

1. **录入期**：在提取史料时，立即记录 `source_path` 和 `page_locator`。
2. **校验期**：撰写引文时，对照 `quote_snippet` 确认引注文字的一致性。
3. **终审期**：全稿完成后，抽查 20% 的引注，通过 `source_path` 重新定位原始文本，验证 `page_locator` 的准确性。

---

## 4. 严禁行为 (Redlines)
- **禁止**：使用没有具体页码或定位信息的引注（如仅标注书名）。
- **禁止**：在转引文献时伪造成直接引用原始文献。
- **禁止**：修改 `quote_snippet` 中的文字以适应论点（除必要的删节外，删节需加省略号）。
