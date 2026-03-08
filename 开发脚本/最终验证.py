#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证 - 确保没有基础错误
"""

import re

print("=" * 80)
print("最终验证检查...")
print("=" * 80)

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
warnings = []

# ==================== 1. 检查关键函数 ====================
print("\n1. 检查关键函数...")

critical_functions = [
    'openModal', 'closeModal', 'showNotification',
    'showLoading', 'hideLoading', 'sortTable',
    'initPagination', 'renderPagination', 'changePage',
    'changePageSize', 'applyPagination', 'refreshAuditData'
]

for func in critical_functions:
    if f'function {func}' in content:
        print(f"  ✓ {func}")
    else:
        errors.append(f"缺少关键函数: {func}")
        print(f"  ❌ {func}")

# ==================== 2. 检查所有14个页面 ====================
print("\n2. 检查所有14个页面...")

pages = {
    'dashboard': '智能指挥中心',
    'user-management': '账号权限管理',
    'model-factory': 'AI模型工厂',
    'experiment': '实验跟踪',
    'knowledge-graph': '知识图谱',
    'trace': '链路追踪',
    'model-monitor': '模型监控',
    'data-governance': '数据治理',
    'labeling': '智能标注',
    'intervention': '人工干预',
    'audit': '审计中心',
    'flow': '流程编排',
    'chat': '对话模拟',
    'config': '系统配置'
}

for page_id, page_name in pages.items():
    if f"'{page_id}':" in content or f"{page_id}:" in content:
        print(f"  ✓ {page_id} ({page_name})")
    else:
        errors.append(f"页面缺失: {page_id}")
        print(f"  ❌ {page_id} ({page_name})")

# ==================== 3. 检查模态框 ====================
print("\n3. 检查模态框...")

modal_count = content.count('id="modalOverlay"')
if modal_count == 1:
    print(f"  ✓ modalOverlay: 1个（正确）")
else:
    errors.append(f"modalOverlay数量错误: {modal_count}个")
    print(f"  ❌ modalOverlay: {modal_count}个")

# 检查closeModal调用
close_modal_count = content.count('closeModal()')
if close_modal_count > 0:
    print(f"  ✓ closeModal()调用: {close_modal_count}次")
else:
    errors.append("没有closeModal()调用")
    print(f"  ❌ closeModal()调用: 0次")

# 检查是否还有错误的Modal.close()
modal_close_count = content.count('Modal.close()')
if modal_close_count == 0:
    print(f"  ✓ Modal.close()调用: 0次（正确）")
else:
    errors.append(f"仍有错误的Modal.close()调用: {modal_close_count}次")
    print(f"  ❌ Modal.close()调用: {modal_close_count}次（应该为0）")

# ==================== 4. 检查事件监听 ====================
print("\n4. 检查事件监听...")

if "getElementById('modalOverlay').addEventListener" in content:
    print("  ✓ modalOverlay点击事件已绑定")
else:
    errors.append("modalOverlay点击事件未绑定")
    print("  ❌ modalOverlay点击事件未绑定")

if "e.key === 'Escape'" in content and "closeModal" in content:
    print("  ✓ ESC键关闭已绑定")
else:
    warnings.append("ESC键关闭可能未绑定")
    print("  ⚠️  ESC键关闭")

# ==================== 5. 检查流程编排器函数 ====================
print("\n5. 检查流程编排器函数...")

flow_functions = ['configureNode', 'deleteNode', 'saveNodeConfig']
for func in flow_functions:
    if f'window.{func}' in content:
        print(f"  ✓ window.{func}")
    else:
        errors.append(f"流程编排函数缺失: {func}")
        print(f"  ❌ window.{func}")

# ==================== 6. 检查表格功能 ====================
print("\n6. 检查表格功能...")

tables = ['auditTable', 'experimentTable', 'traceTable', 'interventionTable']
for table_id in tables:
    if f'id="{table_id}"' in content:
        print(f"  ✓ {table_id}")
    else:
        warnings.append(f"表格ID缺失: {table_id}")
        print(f"  ⚠️  {table_id}")

# ==================== 7. 检查数据量 ====================
print("\n7. 检查数据量...")

log_count = content.count('#LOG-')
exp_count = content.count('#EXP-')
wo_count = content.count('#WO-')
lbl_count = content.count('#LBL-')
ds_count = content.count('DS-')
flow_count = content.count('FLOW-')

print(f"  ✓ 审计日志: {log_count}条")
print(f"  ✓ 实验记录: {exp_count}条")
print(f"  ✓ 工单记录: {wo_count}条")
print(f"  ✓ 标注任务: {lbl_count}条")
print(f"  ✓ 数据源: {ds_count}条")
print(f"  ✓ 流程: {flow_count}条")

total_data = log_count + exp_count + wo_count + lbl_count + ds_count + flow_count
print(f"  ✓ 总数据量: {total_data}条")

if total_data < 400:
    warnings.append(f"数据量偏少: {total_data}条")

# ==================== 8. 检查CSS ====================
print("\n8. 检查关键CSS...")

critical_css = [
    '.modal-overlay', '.modal', '.pagination', 
    '.loading-overlay', '.sortable'
]

for css_class in critical_css:
    if f'{css_class} {{' in content or f'{css_class}{{' in content:
        print(f"  ✓ {css_class}")
    else:
        warnings.append(f"CSS类缺失: {css_class}")
        print(f"  ⚠️  {css_class}")

# ==================== 9. 检查重复ID ====================
print("\n9. 检查重复ID...")

from collections import Counter
id_pattern = r'id="([^"]+)"'
ids = re.findall(id_pattern, content)
id_counts = Counter(ids)
duplicate_ids = {id_name: count for id_name, count in id_counts.items() if count > 1}

if duplicate_ids:
    errors.append("发现重复ID:")
    for id_name, count in duplicate_ids.items():
        errors.append(f"  - {id_name}: {count}次")
        print(f"  ❌ 重复ID: {id_name} ({count}次)")
else:
    print("  ✓ 无重复ID")

# ==================== 10. 检查括号匹配 ====================
print("\n10. 检查括号匹配...")

open_parens = content.count('(')
close_parens = content.count(')')
if open_parens == close_parens:
    print(f"  ✓ 圆括号匹配: {open_parens}对")
else:
    errors.append(f"圆括号不匹配: ( {open_parens}次, ) {close_parens}次")
    print(f"  ❌ 圆括号: ( {open_parens}次, ) {close_parens}次")

open_braces = content.count('{')
close_braces = content.count('}')
if open_braces == close_braces:
    print(f"  ✓ 花括号匹配: {open_braces}对")
else:
    errors.append(f"花括号不匹配: {{ {open_braces}次, }} {close_braces}次")
    print(f"  ❌ 花括号: {{ {open_braces}次, }} {close_braces}次")

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("验证完成！")
print("=" * 80)

print(f"\n严重错误: {len(errors)}")
if errors:
    print("\n🔴 错误列表:")
    for error in errors:
        print(f"  {error}")

print(f"\n警告: {len(warnings)}")
if warnings:
    print("\n🟡 警告列表:")
    for warning in warnings:
        print(f"  {warning}")

# 最终评分
if not errors:
    if not warnings:
        score = 100
        status = "✅ 完美！无任何错误和警告"
    else:
        score = 98
        status = "✅ 优秀！无严重错误，仅有少量警告"
else:
    score = max(0, 100 - len(errors) * 10)
    status = "❌ 发现严重错误，需要修复"

print(f"\n{'=' * 80}")
print(f"最终评分: {score}/100")
print(f"状态: {status}")
print(f"{'=' * 80}")

print(f"\n文件大小: {len(content) / 1024:.1f} KB")
print(f"代码行数: {content.count(chr(10))} 行")

# 保存报告
with open('最终验证报告.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("最终验证报告\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"严重错误: {len(errors)}\n")
    if errors:
        f.write("\n错误列表:\n")
        for error in errors:
            f.write(f"  {error}\n")
    
    f.write(f"\n警告: {len(warnings)}\n")
    if warnings:
        f.write("\n警告列表:\n")
        for warning in warnings:
            f.write(f"  {warning}\n")
    
    f.write(f"\n最终评分: {score}/100\n")
    f.write(f"状态: {status}\n")

print("\n报告已保存到: 最终验证报告.txt")
