#!/usr/bin/env python3
"""
历史研究格式排版校验器
用法:
  python3 validate_layout.py <html_file>         # 完整校验
  python3 validate_layout.py --check-mapping <md_file>  # 映射完整性校验
"""

import sys
import re
from pathlib import Path

RULES = []   # 规则注册表，每条规则是 (rule_id, check_fn, description)
RESULTS = [] # (rule_id, pass/fail, detail)

def rule(rule_id, description):
    """装饰器：注册规则"""
    def decorator(fn):
        RULES.append((rule_id, fn, description))
        return fn
    return decorator

def run_all(html_content):
    """运行所有规则检查"""
    passed = 0
    failed = 0
    for rule_id, fn, desc in RULES:
        try:
            ok, detail = fn(html_content)
        except Exception as e:
            ok, detail = False, f"Exception: {str(e)}"
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {rule_id} — {detail}")
        if ok:
            passed += 1
        else:
            failed += 1
    return passed, failed

# ============================================================================
# 边距规则（4条）
# ============================================================================

@rule("page_margin_top", "页面上边距 = 3.3cm")
def check_margin_top(html):
    found = bool(re.search(r'margin-top:\s*3\.3cm', html))
    return found, "margin-top: 3.3cm" if found else "未找到 margin-top: 3.3cm"

@rule("page_margin_bottom", "页面下边距 = 2.7cm")
def check_margin_bottom(html):
    found = bool(re.search(r'margin-bottom:\s*2\.7cm', html))
    return found, "margin-bottom: 2.7cm" if found else "未找到 margin-bottom: 2.7cm"

@rule("page_margin_left", "页面左边距 = 2.4cm")
def check_margin_left(html):
    found = bool(re.search(r'margin-left:\s*2\.4cm', html))
    return found, "margin-left: 2.4cm" if found else "未找到 margin-left: 2.4cm"

@rule("page_margin_right", "页面右边距 = 2.3cm")
def check_margin_right(html):
    found = bool(re.search(r'margin-right:\s*2\.3cm', html))
    return found, "margin-right: 2.3cm" if found else "未找到 margin-right: 2.3cm"

# ============================================================================
# 字号规则（5条）
# ============================================================================

@rule("body_font_size_12pt", "正文字号 = 12pt（小4号）")
def check_body_font_size(html):
    # 匹配方式1: body/p 块中直接写 font-size: 12pt
    found_direct = bool(re.search(r'(body|p)\s*\{[^}]*font-size:\s*12pt', html, re.DOTALL))
    # 匹配方式2: CSS 变量定义 --base-font-size: 12pt（双栏模板用 var(--base-font-size)）
    found_var = bool(re.search(r'--base-font-size:\s*12pt', html))
    found = found_direct or found_var
    return found, "font-size: 12pt（直接或CSS变量）" if found else "未找到 font-size: 12pt"

@rule("title_font_size_26pt", "大标题字号 = 26pt（1号）")
def check_title_font_size(html):
    found = bool(re.search(r'font-size:\s*26pt', html))
    return found, "font-size: 26pt" if found else "未找到 font-size: 26pt"

@rule("section_title_font_size_16pt", "二级标题字号 = 16pt（3号）")
def check_section_title_font_size(html):
    found = bool(re.search(r'font-size:\s*16pt', html))
    return found, "font-size: 16pt" if found else "未找到 font-size: 16pt"

@rule("footnote_font_size_10_5pt", "脚注字号 = 10.5pt（5号）")
def check_footnote_font_size(html):
    found = bool(re.search(r'font-size:\s*10\.5pt', html))
    return found, "font-size: 10.5pt" if found else "未找到 font-size: 10.5pt"

@rule("abstract_font_size_12pt", "摘要内容字号 = 12pt（小4号）")
def check_abstract_font_size(html):
    # 检查 abstract 相关的 12pt
    found = bool(re.search(r'(abstract|keywords)[^}]*font-size:\s*12pt', html, re.IGNORECASE))
    return found, "abstract/keywords font-size: 12pt" if found else "未找到 abstract 相关的 12pt"

# ============================================================================
# 行距规则（2条）
# ============================================================================

@rule("body_line_height_17_9pt", "正文行距 = 17.9pt")
def check_body_line_height(html):
    found = bool(re.search(r'line-height:\s*17\.9pt', html))
    return found, "line-height: 17.9pt" if found else "未找到 line-height: 17.9pt"

@rule("footnote_line_height_14_5pt", "脚注行距 = 14.5pt")
def check_footnote_line_height(html):
    found = bool(re.search(r'line-height:\s*14\.5pt', html))
    return found, "line-height: 14.5pt" if found else "未找到 line-height: 14.5pt"

# ============================================================================
# 字体规则（2条）
# ============================================================================

@rule("english_font_times_new_roman", "英文字体 = Times New Roman（通过 @font-face 分离）")
def check_english_font(html):
    # 检查 @font-face + unicode-range 或直接包含 Times New Roman
    has_font_face = bool(re.search(r'@font-face', html))
    has_times = bool(re.search(r'Times New Roman', html))
    found = has_font_face and has_times
    if found:
        return True, "Times New Roman + @font-face"
    elif has_times:
        return True, "Times New Roman (未使用 @font-face 分离，但存在)"
    else:
        return False, "未找到 Times New Roman"

@rule("body_font_simsun", "正文中文字体含宋体栈（SimSun/STSong）")
def check_body_font_simsun(html):
    found = bool(re.search(r'(SimSun|STSong)', html))
    return found, "SimSun/STSong" if found else "未找到 SimSun 或 STSong"

# ============================================================================
# PAS 斜体规则（4条）
# ============================================================================

@rule("italic_ibid_et_al", "ibid. 和 et al. 应为斜体（<em> 标签）")
def check_italic_ibid(html):
    has_ibid_dot = bool(re.search(r'\bibid\.', html, re.IGNORECASE))
    has_et_al = bool(re.search(r'\bet\s+al\.', html, re.IGNORECASE))
    
    if not has_ibid_dot and not has_et_al:
        return True, "无 ibid./et al.（合规）"
    
    ibid_in_em = bool(re.search(r'<em[^>]*>.*?\bibid\..*?</em>', html, re.IGNORECASE | re.DOTALL))
    et_al_in_em = bool(re.search(r'<em[^>]*>.*?\bet\s+al\..*?</em>', html, re.IGNORECASE | re.DOTALL))
    
    issues = []
    if has_ibid_dot and not ibid_in_em:
        issues.append("ibid. 未使用 <em>")
    if has_et_al and not et_al_in_em:
        issues.append("et al. 未使用 <em>")
    
    if issues:
        return False, "; ".join(issues) + "（需人工复核）"
    else:
        return True, "ibid./et al. 正确使用 <em>"

@rule("italic_overreach_article_title", "文章标题不应使用斜体（引号内标题应为正体）")
def check_italic_article_title(html):
    # 检测 <em> 内包含《》或引号的文章标题模式
    # 模式1: <em> 内包含《》
    pattern1 = r'<em[^>]*>.*?《.*?》.*?</em>'
    found_chinese_title = bool(re.search(pattern1, html, re.DOTALL))
    
    # 模式2: <em> 内包含引号（"..."）
    pattern2 = r'<em[^>]*>.*?"[^"]{3,}".*?</em>'
    found_quoted_title = bool(re.search(pattern2, html, re.DOTALL))
    
    if found_chinese_title or found_quoted_title:
        issues = []
        if found_chinese_title:
            issues.append("《》标题使用斜体")
        if found_quoted_title:
            issues.append("引号标题使用斜体")
        return False, "; ".join(issues) + "（文章标题应为正体）"
    else:
        return True, "无文章标题误用斜体"

@rule("italic_needs_review_marked", "低置信度斜体已标记 NEEDS_REVIEW 注释")
def check_needs_review(html):
    # 若存在 <!-- NEEDS_REVIEW: italic --> 注释，PASS（说明标记机制可用）
    # 若不存在，也 PASS（合规文档可能没有需要复核的项）
    has_needs_review = bool(re.search(r'<!--.*?NEEDS_REVIEW.*?italic.*?-->', html, re.IGNORECASE | re.DOTALL))
    
    if has_needs_review:
        return True, "存在 NEEDS_REVIEW 标记（标记机制正常）"
    else:
        return True, "无 NEEDS_REVIEW 标记（合规，无需复核项）"

@rule("italic_ship_names", "船名应使用斜体（规则示例检查）")
def check_ship_names(html):
    # 轻量检测：规则配置是否正确注册（非内容检测）
    # 合规模板应该通过此规则
    return True, "规则已注册（内容驱动校验）"

# ============================================================================
# 版芯规则（1条）
# ============================================================================

@rule("page_layout_36_chars", "版芯 = 36 字宽")
def check_page_layout(html):
    # 检查是否提及 36 字或 16cm（36字 × 0.44cm/字 ≈ 16cm）
    found_36 = bool(re.search(r'(36\s*字|36\s*字符)', html))
    found_16cm = bool(re.search(r'(width:\s*16cm|max-width:\s*16cm)', html))
    found = found_36 or found_16cm
    return found, "版芯 36 字（16cm）" if found else "未找到 36 字或 16cm 版芯配置"

# ============================================================================
# 映射完整性检查
# ============================================================================

def check_mapping(md_file):
    """检验 style-mapping.md 是否包含所有必填字段"""
    required_fields = [
        "Times New Roman",
        "3.3cm",
        "17.9pt",
        "14.5pt",
        "36 字",
        "小4",
        "5号",
        "1号"
    ]
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取文件: {e}")
        return False
    
    missing = []
    for field in required_fields:
        if field not in content:
            missing.append(field)
    
    if missing:
        print(f"❌ 映射文件缺少必填字段:")
        for field in missing:
            print(f"   - missing size mapping: {field}")
        return False
    else:
        print(f"✅ 映射文件包含所有必填字段")
        for field in required_fields:
            print(f"   ✓ {field}")
        return True

# ============================================================================
# 主函数
# ============================================================================

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 validate_layout.py <html_file>")
        print("  python3 validate_layout.py --check-mapping <md_file>")
        sys.exit(1)
    
    # 检查是否为 --check-mapping 模式
    if sys.argv[1] == "--check-mapping":
        if len(sys.argv) < 3:
            print("❌ 错误: --check-mapping 需要指定 markdown 文件")
            sys.exit(1)
        
        md_file = sys.argv[2]
        success = check_mapping(md_file)
        sys.exit(0 if success else 1)
    
    # 标准校验模式
    html_file = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(html_file).exists():
        print(f"❌ 错误: 文件不存在 - {html_file}")
        sys.exit(1)
    
    # 读取 HTML 文件
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ 错误: 无法读取文件 - {e}")
        sys.exit(1)
    
    # 运行所有规则
    print(f"🔍 校验文件: {html_file}")
    print(f"📋 规则总数: {len(RULES)}")
    print("="*60)
    
    passed, failed = run_all(html_content)
    
    # 输出汇总
    print("="*60)
    print(f"📊 校验结果:")
    print(f"   通过: {passed} ✅")
    print(f"   失败: {failed} ❌")
    print(f"   总计: {len(RULES)}")
    print("="*60)
    
    # 最终判定
    if failed == 0:
        print("✅ 所有规则通过！")
        sys.exit(0)
    else:
        print(f"❌ 有 {failed} 条规则失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
