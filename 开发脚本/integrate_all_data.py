#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集成脚本 - 将生成的大量数据集成到主HTML文件中
"""

import re

print("=" * 80)
print("开始数据集成...")
print("=" * 80)

# 读取文件
with open('all_pages_data.html', 'r', encoding='utf-8') as f:
    data_lines = f.readlines()

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    main_content = f.read()

# 提取数据段的函数
def extract_rows(lines, start_idx, end_idx):
    """提取指定范围内的所有<tr>行"""
    rows = []
    in_tr = False
    current_tr = []
    
    for i in range(start_idx, end_idx):
        line = lines[i]
        if '<tr>' in line:
            in_tr = True
            current_tr = [line]
        elif in_tr:
            current_tr.append(line)
            if '</tr>' in line:
                rows.append(''.join(current_tr))
                in_tr = False
                current_tr = []
    
    return ''.join(rows)

# 找到各个数据段的起止行号
sections = {
    '审计中心': (4, 904),  # 行号从grep结果得出
    '实验追踪': (909, 1408),
    '链路追踪': (1413, 2312),
    '人工干预': (2317, 3036),
    '智能标注': (3041, 3540),
    '数据治理': (3545, 3944),
    '流程编排': (3949, 4278)
}

# 提取所有数据
extracted_data = {}
for name, (start, end) in sections.items():
    print(f"\n提取{name}数据 (行 {start}-{end})...")
    data = extract_rows(data_lines, start, end)
    row_count = data.count('<tr>')
    extracted_data[name] = data
    print(f"  ✓ 提取了 {row_count} 条数据")

print("\n" + "=" * 80)
print("数据提取完成！")
print("=" * 80)

# 现在需要在主HTML文件中找到对应的tbody并替换
# 策略：找到每个页面的render函数中的<tbody>...</tbody>，替换其中的内容

def replace_tbody_in_page(content, page_marker, new_rows):
    """在指定页面的tbody中替换数据"""
    # 找到页面的render函数
    page_pattern = f"'{page_marker}':\\s*{{\\s*render\\(\\)\\s*{{\\s*return\\s*`"
    match = re.search(page_pattern, content)
    
    if not match:
        print(f"  ✗ 未找到页面: {page_marker}")
        return content
    
    # 从这个位置开始查找<tbody>
    start_pos = match.end()
    
    # 找到这个页面render函数中的第一个<tbody>...</tbody>
    tbody_pattern = r'<tbody>(.*?)</tbody>'
    tbody_match = re.search(tbody_pattern, content[start_pos:start_pos+50000], re.DOTALL)
    
    if not tbody_match:
        print(f"  ✗ 未找到tbody: {page_marker}")
        return content
    
    # 计算实际位置
    tbody_start = start_pos + tbody_match.start()
    tbody_end = start_pos + tbody_match.end()
    
    # 替换tbody内容
    new_tbody = f'<tbody>\n{new_rows}                </tbody>'
    new_content = content[:tbody_start] + new_tbody + content[tbody_end:]
    
    return new_content

# 定义页面标识和对应的数据
page_mappings = {
    'audit': '审计中心',
    'experiment': '实验追踪',
    'trace': '链路追踪',
    'intervention': '人工干预',
    'labeling': '智能标注',
    'data-governance': '数据治理',
    'flow': '流程编排'
}

print("\n" + "=" * 80)
print("开始集成数据到主HTML文件...")
print("=" * 80)

updated_content = main_content

for page_id, data_name in page_mappings.items():
    print(f"\n集成 {data_name} 到页面 '{page_id}'...")
    if data_name in extracted_data:
        updated_content = replace_tbody_in_page(updated_content, page_id, extracted_data[data_name])
        print(f"  ✓ 完成")
    else:
        print(f"  ✗ 数据不存在")

# 保存更新后的文件
output_file = 'ai-platform-complete-with-data.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("\n" + "=" * 80)
print(f"数据集成完成！")
print(f"新文件已保存为: {output_file}")
print("=" * 80)

# 统计信息
print("\n数据统计:")
for name, data in extracted_data.items():
    count = data.count('<tr>')
    print(f"  {name}: {count} 条")

print(f"\n总计: {sum(data.count('<tr>') for data in extracted_data.values())} 条数据")
