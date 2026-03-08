#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除console.log调试代码
保留console.error
"""

import re

print("=" * 80)
print("开始移除console.log调试代码...")
print("=" * 80)

# 读取文件
with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 统计原有的console.log数量
original_count = len(re.findall(r'console\.log', content))
print(f"\n发现 {original_count} 处 console.log")

# 方案1: 注释掉console.log（保留代码，方便调试）
# content = re.sub(r'(\s*)console\.log\([^)]*\);', r'\1// console.log(...); // 已注释', content)

# 方案2: 完全删除console.log行（推荐用于评审）
content = re.sub(r'\s*console\.log\([^)]*\);\n', '', content)

# 统计删除后的console.log数量
remaining_count = len(re.findall(r'console\.log', content))
removed_count = original_count - remaining_count

print(f"已移除 {removed_count} 处 console.log")
print(f"剩余 {remaining_count} 处 console.log")

# 检查console.error（应该保留）
error_count = len(re.findall(r'console\.error', content))
print(f"保留 {error_count} 处 console.error")

# 保存文件
with open('ai-platform-complete.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 80)
print("✅ console.log移除完成！")
print("=" * 80)

# 显示文件大小变化
import os
file_size = os.path.getsize('ai-platform-complete.html')
print(f"\n文件大小: {file_size / 1024:.1f} KB")
