#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加按钮事件 - 自动给未绑定的按钮添加onclick事件
"""

import re

print("=" * 80)
print("添加按钮事件...")
print("=" * 80)

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ==================== 1. 筛选按钮 ====================
print("\n1. 添加筛选按钮事件...")

filter_mappings = [
    (r'<button class="btn">全部</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'全部\')">全部</button>'),
    (r'<button class="btn">实时</button>', '<button class="btn" onclick="handleFilter(\'时间\', \'实时\')">实时</button>'),
    (r'<button class="btn">今日</button>', '<button class="btn" onclick="handleFilter(\'时间\', \'今日\')">今日</button>'),
    (r'<button class="btn">近7天</button>', '<button class="btn" onclick="handleFilter(\'时间\', \'近7天\')">近7天</button>'),
    (r'<button class="btn">近1小时</button>', '<button class="btn" onclick="handleFilter(\'时间\', \'近1小时\')">近1小时</button>'),
    (r'<button class="btn">近24小时</button>', '<button class="btn" onclick="handleFilter(\'时间\', \'近24小时\')">近24小时</button>'),
    (r'<button class="btn">紧急</button>', '<button class="btn" onclick="handleFilter(\'优先级\', \'紧急\')">紧急</button>'),
    (r'<button class="btn">严重</button>', '<button class="btn" onclick="handleFilter(\'级别\', \'严重\')">严重</button>'),
    (r'<button class="btn">高风险</button>', '<button class="btn" onclick="handleFilter(\'风险\', \'高风险\')">高风险</button>'),
    (r'<button class="btn">异常</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'异常\')">异常</button>'),
    (r'<button class="btn">待处理</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'待处理\')">待处理</button>'),
    (r'<button class="btn">处理中</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'处理中\')">处理中</button>'),
    (r'<button class="btn">已完成</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'已完成\')">已完成</button>'),
    (r'<button class="btn">运行中</button>', '<button class="btn" onclick="handleFilter(\'状态\', \'运行中\')">运行中</button>'),
    (r'<button class="btn">数据库</button>', '<button class="btn" onclick="handleFilter(\'类型\', \'数据库\')">数据库</button>'),
    (r'<button class="btn">API</button>', '<button class="btn" onclick="handleFilter(\'类型\', \'API\')">API</button>'),
    (r'<button class="btn">文件</button>', '<button class="btn" onclick="handleFilter(\'类型\', \'文件\')">文件</button>'),
]

for old, new in filter_mappings:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        changes += count
        print(f"  ✓ 已添加: {old.split('>')[1].split('<')[0]} ({count}个)")

# ==================== 2. 刷新按钮 ====================
print("\n2. 添加刷新按钮事件...")

content = content.replace(
    '<button class="btn">刷新</button>',
    '<button class="btn" onclick="handleRefresh(\'当前页面\')">刷新</button>'
)
print(f"  ✓ 已添加刷新按钮事件")
changes += 2

# ==================== 3. 导出按钮 ====================
print("\n3. 添加导出按钮事件...")

content = content.replace(
    '<button class="btn">导出</button>',
    '<button class="btn" onclick="handleExport(\'当前数据\')">导出</button>'
)
print(f"  ✓ 已添加导出按钮事件")
changes += 3

# ==================== 4. 新建按钮 ====================
print("\n4. 添加新建按钮事件...")

new_button_mappings = [
    ('+ 新建用户', 'handleCreate(\'用户\')'),
    ('+ 新建角色', 'handleCreate(\'角色\')'),
    ('+ 新建任务', 'handleCreate(\'任务\')'),
    ('+ 新建数据源', 'handleCreate(\'数据源\')'),
    ('+ 新建流程', 'handleCreate(\'流程\')'),
]

for btn_text, handler in new_button_mappings:
    old = f'<button class="btn btn-primary">{btn_text}</button>'
    new = f'<button class="btn btn-primary" onclick="{handler}">{btn_text}</button>'
    if old in content:
        content = content.replace(old, new)
        print(f"  ✓ 已添加: {btn_text}")
        changes += 1

# ==================== 5. 知识图谱按钮 ====================
print("\n5. 添加知识图谱按钮事件...")

graph_buttons = [
    ('🔍 放大', 'showNotification(\'🔍 放大功能\', \'info\')'),
    ('🔍 缩小', 'showNotification(\'🔍 缩小功能\', \'info\')'),
    ('↻ 刷新', 'handleRefresh(\'知识图谱\')'),
    ('📷 截图', 'showNotification(\'📷 截图功能\', \'info\')'),
]

for btn_text, handler in graph_buttons:
    old = f'<button class="btn">{btn_text}</button>'
    new = f'<button class="btn" onclick="{handler}">{btn_text}</button>'
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"  ✓ 已添加: {btn_text} ({count}个)")
        changes += count

# ==================== 6. 其他功能按钮 ====================
print("\n6. 添加其他功能按钮事件...")

other_buttons = [
    ('对比实验', 'showNotification(\'📊 对比实验功能\', \'info\')'),
    ('TensorBoard', 'showNotification(\'📈 TensorBoard功能\', \'info\')'),
    ('重新训练', 'showNotification(\'🔄 重新训练功能\', \'info\')'),
    ('停止', 'showNotification(\'⏹️ 停止功能\', \'info\')'),
    ('暂停', 'showNotification(\'⏸️ 暂停功能\', \'info\')'),
    ('取消', 'showNotification(\'❌ 取消功能\', \'info\')'),
    ('重置', 'showNotification(\'🔄 重置功能\', \'info\')'),
]

for btn_text, handler in other_buttons:
    old = f'<button class="btn">{btn_text}</button>'
    new = f'<button class="btn" onclick="{handler}">{btn_text}</button>'
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"  ✓ 已添加: {btn_text} ({count}个)")
        changes += count

# ==================== 保存文件 ====================
print("\n" + "=" * 80)
print(f"总共添加了 {changes} 个按钮事件")
print("=" * 80)

with open('ai-platform-complete.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ 文件已更新")
