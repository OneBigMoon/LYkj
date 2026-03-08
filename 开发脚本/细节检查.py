#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
细节检查 - 检查所有未完善的功能
"""

import re

print("=" * 80)
print("细节检查...")
print("=" * 80)

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

issues = []

# ==================== 1. 检查未绑定事件的按钮 ====================
print("\n1. 检查未绑定事件的按钮...")

# 查找所有按钮
all_buttons = re.findall(r'<button[^>]*>(.*?)</button>', content, re.DOTALL)
buttons_with_onclick = re.findall(r'<button[^>]*onclick[^>]*>(.*?)</button>', content, re.DOTALL)

print(f"  总按钮数: {len(all_buttons)}")
print(f"  已绑定事件: {len(buttons_with_onclick)}")
print(f"  未绑定事件: {len(all_buttons) - len(buttons_with_onclick)}")

# 查找具体的未绑定按钮
unbound_buttons = []
for match in re.finditer(r'<button class="btn"(?!.*onclick).*?>(.*?)</button>', content):
    button_text = match.group(1).strip()
    if button_text and not button_text.startswith('<'):
        unbound_buttons.append(button_text)

if unbound_buttons:
    print(f"\n  未绑定事件的按钮（前20个）:")
    for btn in list(set(unbound_buttons))[:20]:
        print(f"    - {btn}")
    issues.append(f"有 {len(unbound_buttons)} 个按钮未绑定事件")

# ==================== 2. 检查筛选按钮 ====================
print("\n2. 检查筛选按钮...")

filter_buttons = ['全部', '实时', '今日', '近7天', '紧急', '严重', '高风险', '异常']
for btn_text in filter_buttons:
    pattern = f'<button class="btn">{btn_text}</button>'
    count = content.count(pattern)
    if count > 0:
        print(f"  ⚠️  筛选按钮未绑定: {btn_text} ({count}个)")

# ==================== 3. 检查刷新按钮 ====================
print("\n3. 检查刷新按钮...")

refresh_pattern = r'<button class="btn">刷新</button>'
refresh_count = len(re.findall(refresh_pattern, content))
if refresh_count > 0:
    print(f"  ⚠️  有 {refresh_count} 个刷新按钮未绑定事件")
    issues.append(f"{refresh_count} 个刷新按钮未绑定")

# ==================== 4. 检查导出按钮 ====================
print("\n4. 检查导出按钮...")

export_pattern = r'<button class="btn">导出</button>'
export_count = len(re.findall(export_pattern, content))
if export_count > 0:
    print(f"  ⚠️  有 {export_count} 个导出按钮未绑定事件")
    issues.append(f"{export_count} 个导出按钮未绑定")

# ==================== 5. 检查表格中的操作按钮 ====================
print("\n5. 检查表格中的操作按钮...")

table_button_patterns = [
    (r'<button class="btn"[^>]*>详情</button>', '详情'),
    (r'<button class="btn"[^>]*>编辑</button>', '编辑'),
    (r'<button class="btn"[^>]*>处理</button>', '处理'),
    (r'<button class="btn"[^>]*>查看</button>', '查看'),
    (r'<button class="btn"[^>]*>审批</button>', '审批'),
]

for pattern, name in table_button_patterns:
    matches = re.findall(pattern, content)
    unbound = [m for m in matches if 'onclick' not in m]
    if unbound:
        print(f"  ⚠️  {name}按钮: {len(unbound)} 个未绑定")

# ==================== 6. 检查输入框 ====================
print("\n6. 检查输入框...")

# 搜索框
search_inputs = re.findall(r'<input[^>]*placeholder="[^"]*搜索[^"]*"[^>]*>', content)
print(f"  搜索框数量: {len(search_inputs)}")

# 检查是否有搜索功能
if 'function search' not in content.lower() and 'function filter' not in content.lower():
    print(f"  ⚠️  没有搜索/筛选函数")
    issues.append("缺少搜索/筛选功能")

# ==================== 7. 检查下拉框 ====================
print("\n7. 检查下拉框...")

selects = re.findall(r'<select[^>]*id="([^"]*)"', content)
print(f"  下拉框数量: {len(selects)}")
for select_id in selects[:10]:
    print(f"    - {select_id}")

# ==================== 8. 检查模态框 ====================
print("\n8. 检查模态框...")

# 检查"新建"按钮
create_buttons = re.findall(r'<button[^>]*>\+\s*新建[^<]*</button>', content)
print(f"  新建按钮数量: {len(create_buttons)}")

unbound_create = [b for b in create_buttons if 'onclick' not in b]
if unbound_create:
    print(f"  ⚠️  {len(unbound_create)} 个新建按钮未绑定")
    issues.append(f"{len(unbound_create)} 个新建按钮未绑定")

# ==================== 9. 检查图表 ====================
print("\n9. 检查图表...")

# 检查是否有图表容器
chart_containers = re.findall(r'id="[^"]*[Cc]hart[^"]*"', content)
print(f"  图表容器数量: {len(chart_containers)}")

# ==================== 10. 检查链接 ====================
print("\n10. 检查链接...")

# 检查空链接
empty_links = re.findall(r'<a[^>]*href="#"[^>]*>', content)
print(f"  空链接数量: {len(empty_links)}")

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("检查完成！")
print("=" * 80)

print(f"\n发现的问题: {len(issues)}")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
else:
    print("  ✅ 未发现明显问题")

# 保存报告
with open('细节检查报告.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("细节检查报告\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"总按钮数: {len(all_buttons)}\n")
    f.write(f"已绑定事件: {len(buttons_with_onclick)}\n")
    f.write(f"未绑定事件: {len(all_buttons) - len(buttons_with_onclick)}\n\n")
    
    f.write(f"发现的问题: {len(issues)}\n")
    for i, issue in enumerate(issues, 1):
        f.write(f"  {i}. {issue}\n")

print("\n报告已保存到: 细节检查报告.txt")
