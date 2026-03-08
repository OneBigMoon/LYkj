#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际功能测试 - 检查真正的问题
"""

import re

print("=" * 80)
print("实际功能测试...")
print("=" * 80)

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
warnings = []

# ==================== 1. 检查关键函数是否存在 ====================
print("\n1. 检查关键函数...")

critical_functions = {
    'openModal': r'function openModal',
    'closeModal': r'function closeModal',
    'showNotification': r'function showNotification',
    'showLoading': r'function showLoading',
    'hideLoading': r'function hideLoading',
    'sortTable': r'function sortTable',
    'initPagination': r'function initPagination',
    'renderPagination': r'function renderPagination',
    'changePage': r'function changePage',
    'changePageSize': r'function changePageSize',
    'applyPagination': r'function applyPagination',
    'refreshAuditData': r'function refreshAuditData',
}

for func_name, pattern in critical_functions.items():
    if re.search(pattern, content):
        print(f"  ✓ {func_name}")
    else:
        errors.append(f"缺少关键函数: {func_name}")
        print(f"  ❌ {func_name}")

# ==================== 2. 检查页面定义 ====================
print("\n2. 检查页面定义...")

pages = [
    'dashboard', 'users', 'model-factory', 'experiment', 
    'knowledge', 'trace', 'monitor', 'data-governance',
    'labeling', 'intervention', 'audit', 'flow', 'chat', 'config'
]

for page in pages:
    pattern = f"'{page}':\\s*{{\\s*render"
    if re.search(pattern, content):
        print(f"  ✓ {page}")
    else:
        warnings.append(f"页面可能缺失: {page}")
        print(f"  ⚠️  {page}")

# ==================== 3. 检查表格ID ====================
print("\n3. 检查表格ID...")

expected_tables = ['auditTable', 'experimentTable', 'traceTable', 'interventionTable']
for table_id in expected_tables:
    if f'id="{table_id}"' in content:
        print(f"  ✓ {table_id}")
    else:
        warnings.append(f"表格ID缺失: {table_id}")
        print(f"  ⚠️  {table_id}")

# ==================== 4. 检查模态框 ====================
print("\n4. 检查模态框...")

modal_count = content.count('id="modalOverlay"')
if modal_count == 1:
    print(f"  ✓ modalOverlay: 1个（正确）")
elif modal_count == 0:
    errors.append("modalOverlay不存在")
    print(f"  ❌ modalOverlay: 0个")
else:
    errors.append(f"modalOverlay重复: {modal_count}个")
    print(f"  ❌ modalOverlay: {modal_count}个（重复）")

# ==================== 5. 检查事件绑定 ====================
print("\n5. 检查事件绑定...")

# 检查modalOverlay的事件监听
if "getElementById('modalOverlay').addEventListener" in content:
    print("  ✓ modalOverlay事件监听已绑定")
else:
    errors.append("modalOverlay事件监听未绑定")
    print("  ❌ modalOverlay事件监听未绑定")

# 检查ESC键监听
if "e.key === 'Escape'" in content and "closeModal" in content:
    print("  ✓ ESC键关闭模态框已绑定")
else:
    warnings.append("ESC键关闭模态框可能未绑定")
    print("  ⚠️  ESC键关闭模态框")

# ==================== 6. 检查CSS ====================
print("\n6. 检查CSS...")

critical_css = [
    '.modal-overlay', '.modal', '.modal-header', '.modal-body', '.modal-footer',
    '.pagination', '.loading-overlay', '.sortable', '.sort-icon'
]

for css_class in critical_css:
    if f'{css_class} {{' in content or f'{css_class}{{' in content:
        print(f"  ✓ {css_class}")
    else:
        warnings.append(f"CSS类可能缺失: {css_class}")
        print(f"  ⚠️  {css_class}")

# ==================== 7. 检查数据 ====================
print("\n7. 检查数据...")

# 检查是否有大量数据
log_count = content.count('#LOG-')
exp_count = content.count('#EXP-')
wo_count = content.count('#WO-')

print(f"  ✓ 审计日志: {log_count}条")
print(f"  ✓ 实验记录: {exp_count}条")
print(f"  ✓ 工单记录: {wo_count}条")

if log_count < 50:
    warnings.append(f"审计日志数据较少: {log_count}条")
if exp_count < 30:
    warnings.append(f"实验记录数据较少: {exp_count}条")

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)

print(f"\n严重错误: {len(errors)}")
if errors:
    for error in errors:
        print(f"  ❌ {error}")

print(f"\n警告: {len(warnings)}")
if warnings:
    for warning in warnings[:10]:
        print(f"  ⚠️  {warning}")

if not errors:
    print("\n✅ 未发现严重错误！所有关键功能都存在。")
    if warnings:
        print("⚠️  有一些警告，但不影响核心功能。")
else:
    print("\n❌ 发现严重错误，需要立即修复！")

print(f"\n文件大小: {len(content) / 1024:.1f} KB")
print(f"代码行数: {content.count(chr(10))} 行")
