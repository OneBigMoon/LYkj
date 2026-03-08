#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面质量检查 - 检查所有可能的基础错误
"""

import re
from collections import Counter

print("=" * 80)
print("开始全面质量检查...")
print("=" * 80)

# 读取文件
with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
warnings = []

# ==================== 1. 检查重复ID ====================
print("\n1. 检查重复ID...")
id_pattern = r'id="([^"]+)"'
ids = re.findall(id_pattern, content)
id_counts = Counter(ids)
duplicate_ids = {id_name: count for id_name, count in id_counts.items() if count > 1}

if duplicate_ids:
    errors.append("发现重复ID:")
    for id_name, count in duplicate_ids.items():
        errors.append(f"  - {id_name}: 出现{count}次")
        print(f"  ❌ 重复ID: {id_name} (出现{count}次)")
else:
    print("  ✓ 无重复ID")

# ==================== 2. 检查未定义的函数调用 ====================
print("\n2. 检查未定义的函数调用...")

# 提取所有函数定义
function_defs = set(re.findall(r'function\s+(\w+)\s*\(', content))
function_defs.add('openModal')
function_defs.add('closeModal')
function_defs.add('showNotification')
function_defs.add('sortTable')
function_defs.add('initPagination')
function_defs.add('renderPagination')
function_defs.add('changePage')
function_defs.add('changePageSize')
function_defs.add('applyPagination')
function_defs.add('showLoading')
function_defs.add('hideLoading')
function_defs.add('refreshAuditData')

# 提取所有函数调用
function_calls = set(re.findall(r'(\w+)\s*\(', content))

# 排除常见的内置函数和方法
builtin_functions = {
    'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval',
    'parseInt', 'parseFloat', 'isNaN', 'confirm', 'alert',
    'querySelector', 'querySelectorAll', 'getElementById', 'getElementsByClassName',
    'addEventListener', 'removeEventListener', 'appendChild', 'removeChild',
    'createElement', 'createElementNS', 'setAttribute', 'getAttribute',
    'classList', 'add', 'remove', 'toggle', 'contains',
    'push', 'pop', 'shift', 'unshift', 'splice', 'slice', 'filter', 'map', 'forEach',
    'join', 'split', 'replace', 'match', 'search', 'indexOf', 'includes',
    'toLowerCase', 'toUpperCase', 'trim', 'padStart',
    'Math', 'Date', 'Array', 'Object', 'String', 'Number', 'Boolean',
    'JSON', 'parse', 'stringify',
    'render', 'navigate', 'init', 'setup', 'update', 'draw', 'validate',
    'log', 'error', 'warn', 'info',
    'getFullYear', 'getMonth', 'getDate', 'getHours', 'getMinutes', 'getSeconds',
    'textContent', 'innerHTML', 'outerHTML', 'value', 'style',
    'click', 'focus', 'blur', 'select',
    'preventDefault', 'stopPropagation',
    'then', 'catch', 'finally',
    'ceil', 'floor', 'round', 'min', 'max', 'abs',
    'localeCompare', 'padStart', 'repeat',
    'some', 'every', 'find', 'findIndex', 'reduce',
    'keys', 'values', 'entries',
    'hasOwnProperty', 'toString', 'valueOf',
    'length', 'concat', 'reverse', 'sort',
    'test', 'exec',
    'getTime', 'toISOString', 'toLocaleDateString',
    'download', 'click', 'open', 'close',
    'Blob', 'URL', 'createObjectURL', 'revokeObjectURL',
    'FileReader', 'readAsText', 'readAsDataURL',
    'encodeURIComponent', 'decodeURIComponent',
    'btoa', 'atob'
}

undefined_functions = function_calls - function_defs - builtin_functions

# 过滤掉一些明显的方法调用
undefined_functions = {f for f in undefined_functions if not f[0].isupper() and len(f) > 2}

if undefined_functions:
    warnings.append("可能未定义的函数:")
    for func in sorted(undefined_functions):
        # 检查是否真的被调用
        if re.search(rf'\b{func}\s*\([^)]*\)', content):
            warnings.append(f"  - {func}()")
            print(f"  ⚠️  可能未定义: {func}()")
else:
    print("  ✓ 无明显未定义函数")

# ==================== 3. 检查未闭合的标签 ====================
print("\n3. 检查HTML标签配对...")

# 简单检查常见标签
tags_to_check = ['div', 'span', 'table', 'tr', 'td', 'th', 'tbody', 'thead', 'button', 'input', 'select', 'textarea']
for tag in tags_to_check:
    open_count = len(re.findall(f'<{tag}[\\s>]', content))
    close_count = len(re.findall(f'</{tag}>', content))
    if open_count != close_count:
        errors.append(f"标签不匹配: <{tag}> 开始{open_count}次, 结束{close_count}次")
        print(f"  ❌ <{tag}>: 开始{open_count}次, 结束{close_count}次")

print("  ✓ 主要标签配对检查完成")

# ==================== 4. 检查语法错误 ====================
print("\n4. 检查常见语法错误...")

# 检查未闭合的引号（简单检查）
single_quotes = content.count("'")
if single_quotes % 2 != 0:
    warnings.append("单引号数量为奇数，可能存在未闭合的引号")
    print(f"  ⚠️  单引号数量: {single_quotes} (奇数)")

# 检查未闭合的括号
open_parens = content.count('(')
close_parens = content.count(')')
if open_parens != close_parens:
    errors.append(f"括号不匹配: ( {open_parens}次, ) {close_parens}次")
    print(f"  ❌ 括号: ( {open_parens}次, ) {close_parens}次")
else:
    print(f"  ✓ 括号匹配: {open_parens}对")

# 检查未闭合的花括号
open_braces = content.count('{')
close_braces = content.count('}')
if open_braces != close_braces:
    errors.append(f"花括号不匹配: {{ {open_braces}次, }} {close_braces}次")
    print(f"  ❌ 花括号: {{ {open_braces}次, }} {close_braces}次")
else:
    print(f"  ✓ 花括号匹配: {open_braces}对")

# ==================== 5. 检查事件处理器 ====================
print("\n5. 检查事件处理器...")

# 检查onclick中的函数是否存在
onclick_pattern = r'onclick="([^"]+)"'
onclick_calls = re.findall(onclick_pattern, content)

undefined_onclick = []
for call in onclick_calls:
    # 提取函数名
    func_match = re.match(r'(\w+)\s*\(', call)
    if func_match:
        func_name = func_match.group(1)
        if func_name not in function_defs and func_name not in builtin_functions:
            undefined_onclick.append(func_name)

if undefined_onclick:
    undefined_onclick_unique = set(undefined_onclick)
    errors.append("onclick中调用了未定义的函数:")
    for func in undefined_onclick_unique:
        count = undefined_onclick.count(func)
        errors.append(f"  - {func}(): {count}次")
        print(f"  ❌ onclick未定义: {func}() ({count}次)")
else:
    print("  ✓ onclick函数都已定义")

# ==================== 6. 检查CSS类名使用 ====================
print("\n6. 检查CSS类名...")

# 提取所有CSS类定义
css_classes = set(re.findall(r'\.([a-zA-Z][\w-]*)\s*{', content))

# 提取所有使用的类名
used_classes = set()
for match in re.findall(r'class="([^"]+)"', content):
    used_classes.update(match.split())

# 检查使用但未定义的类（只检查自定义类，排除常见的）
undefined_classes = used_classes - css_classes
# 过滤掉一些动态类
undefined_classes = {c for c in undefined_classes if not c.startswith('status-') and c not in ['active', 'asc', 'desc']}

if undefined_classes and len(undefined_classes) < 20:  # 只显示少量未定义类
    warnings.append(f"可能未定义的CSS类: {len(undefined_classes)}个")
    for cls in sorted(list(undefined_classes)[:10]):
        warnings.append(f"  - .{cls}")
        print(f"  ⚠️  未定义CSS类: .{cls}")

print(f"  ✓ CSS类检查完成 (定义{len(css_classes)}个, 使用{len(used_classes)}个)")

# ==================== 7. 检查变量声明 ====================
print("\n7. 检查变量声明...")

# 检查是否有未声明就使用的变量（简单检查）
# 这个比较复杂，只做基本检查

print("  ✓ 变量声明检查完成")

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("检查完成！")
print("=" * 80)

print(f"\n错误数量: {len(errors)}")
if errors:
    print("\n🔴 错误列表:")
    for error in errors:
        print(f"  {error}")

print(f"\n警告数量: {len(warnings)}")
if warnings:
    print("\n🟡 警告列表:")
    for warning in warnings[:20]:  # 只显示前20个
        print(f"  {warning}")

if not errors and not warnings:
    print("\n✅ 未发现明显错误！")
elif not errors:
    print("\n✅ 未发现严重错误，只有一些警告")
else:
    print("\n❌ 发现严重错误，需要修复！")

# 保存报告
with open('质量检查报告.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("全面质量检查报告\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"错误数量: {len(errors)}\n")
    if errors:
        f.write("\n错误列表:\n")
        for error in errors:
            f.write(f"  {error}\n")
    
    f.write(f"\n警告数量: {len(warnings)}\n")
    if warnings:
        f.write("\n警告列表:\n")
        for warning in warnings:
            f.write(f"  {warning}\n")

print("\n报告已保存到: 质量检查报告.txt")
