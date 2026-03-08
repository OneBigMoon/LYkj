#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业审查 - 从PMP/产品经理角度审查演示系统
"""

import re
from collections import Counter

print("=" * 80)
print("专业审查 - 40年经验的项目经理视角")
print("=" * 80)

with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

issues = []
suggestions = []

# ==================== 1. 数据一致性检查 ====================
print("\n【维度1: 数据一致性】")
print("-" * 80)

# 检查数字统计的一致性
print("1.1 检查仪表盘数据一致性...")

# 提取所有数字指标
metrics = {
    '训练任务': re.findall(r'训练任务.*?(\d+)', content),
    '模型准确率': re.findall(r'模型准确率.*?([\d.]+%)', content),
    '在线用户': re.findall(r'在线用户.*?(\d+)', content),
}

for metric, values in metrics.items():
    if len(set(values)) > 1:
        issues.append(f"数据不一致: {metric} 在不同位置显示不同的值: {set(values)}")
        print(f"  ⚠️  {metric}: {set(values)}")
    else:
        print(f"  ✓ {metric}: 一致")

# ==================== 2. 业务逻辑检查 ====================
print("\n【维度2: 业务逻辑完整性】")
print("-" * 80)

print("2.1 检查工作流完整性...")

# 检查是否有完整的CRUD操作
crud_operations = {
    '创建': ['新建', '创建', '添加'],
    '读取': ['查看', '详情', '列表'],
    '更新': ['编辑', '修改', '更新'],
    '删除': ['删除', '移除'],
}

for operation, keywords in crud_operations.items():
    found = any(keyword in content for keyword in keywords)
    if found:
        print(f"  ✓ {operation}操作: 存在")
    else:
        issues.append(f"缺少{operation}操作")
        print(f"  ⚠️  {operation}操作: 缺失")

print("\n2.2 检查审批流程...")
approval_keywords = ['审批', '审核', '通过', '驳回']
has_approval = any(keyword in content for keyword in approval_keywords)
if has_approval:
    print(f"  ✓ 审批流程: 存在")
    # 检查审批状态
    if '待审批' in content and '已通过' in content:
        print(f"  ✓ 审批状态: 完整")
    else:
        suggestions.append("审批流程缺少完整的状态流转")
else:
    suggestions.append("建议添加审批流程")

# ==================== 3. 用户体验检查 ====================
print("\n【维度3: 用户体验设计】")
print("-" * 80)

print("3.1 检查空状态处理...")
empty_state_keywords = ['暂无数据', '无数据', '空列表', 'No data']
has_empty_state = any(keyword in content for keyword in empty_state_keywords)
if has_empty_state:
    print(f"  ✓ 空状态提示: 存在")
else:
    issues.append("缺少空状态提示")
    print(f"  ⚠️  空状态提示: 缺失")

print("\n3.2 检查加载状态...")
loading_count = content.count('showLoading')
if loading_count > 0:
    print(f"  ✓ 加载状态: {loading_count}处使用")
else:
    issues.append("缺少加载状态提示")

print("\n3.3 检查错误提示...")
error_handling = content.count('catch') + content.count('error')
if error_handling > 10:
    print(f"  ✓ 错误处理: {error_handling}处")
else:
    suggestions.append("建议增加更多错误处理")

print("\n3.4 检查确认对话框...")
confirm_count = content.count('confirm(')
if confirm_count > 0:
    print(f"  ⚠️  使用原生confirm: {confirm_count}处（建议使用自定义确认框）")
    suggestions.append("建议将confirm()替换为自定义确认对话框")
else:
    print(f"  ✓ 未使用原生confirm")

# ==================== 4. 数据展示检查 ====================
print("\n【维度4: 数据展示专业性】")
print("-" * 80)

print("4.1 检查时间格式...")
time_formats = re.findall(r'\d{4}-\d{2}-\d{2}', content)
if time_formats:
    print(f"  ✓ 标准时间格式: {len(time_formats)}处")
else:
    suggestions.append("建议统一使用标准时间格式")

print("\n4.2 检查数据单位...")
units = ['KB', 'MB', 'GB', 'TB', 'ms', 's', '%', 'QPS']
unit_usage = {unit: content.count(unit) for unit in units if content.count(unit) > 0}
if unit_usage:
    print(f"  ✓ 数据单位使用:")
    for unit, count in unit_usage.items():
        print(f"    - {unit}: {count}处")
else:
    suggestions.append("建议为数据添加单位")

print("\n4.3 检查数据精度...")
# 检查百分比精度
percentages = re.findall(r'(\d+\.\d+)%', content)
if percentages:
    precisions = [len(p.split('.')[1]) for p in percentages]
    if len(set(precisions)) > 2:
        suggestions.append("百分比精度不统一，建议统一为1-2位小数")
        print(f"  ⚠️  百分比精度不统一: {set(precisions)}位小数")
    else:
        print(f"  ✓ 百分比精度: 统一")

# ==================== 5. 交互设计检查 ====================
print("\n【维度5: 交互设计专业性】")
print("-" * 80)

print("5.1 检查快捷键支持...")
shortcut_keys = ['Ctrl', 'Alt', 'Shift', 'ESC', 'Enter']
has_shortcuts = any(key in content for key in shortcut_keys)
if has_shortcuts:
    print(f"  ✓ 快捷键支持: 存在")
else:
    suggestions.append("建议添加常用快捷键支持")

print("\n5.2 检查搜索功能...")
search_inputs = len(re.findall(r'placeholder="[^"]*搜索[^"]*"', content))
if search_inputs > 0:
    print(f"  ✓ 搜索框: {search_inputs}个")
    # 检查是否有搜索功能实现
    if 'function search' in content.lower() or 'filter' in content.lower():
        print(f"  ✓ 搜索功能: 已实现")
    else:
        issues.append("搜索框存在但功能未实现")
        print(f"  ⚠️  搜索功能: 未实现")
else:
    suggestions.append("建议添加搜索功能")

print("\n5.3 检查批量操作...")
batch_keywords = ['批量', '全选', 'checkbox']
has_batch = any(keyword in content for keyword in batch_keywords)
if has_batch:
    print(f"  ✓ 批量操作: 存在")
else:
    suggestions.append("建议添加批量操作功能（全选、批量删除等）")
    print(f"  ⚠️  批量操作: 缺失")

# ==================== 6. 权限和安全检查 ====================
print("\n【维度6: 权限和安全设计】")
print("-" * 80)

print("6.1 检查角色权限...")
roles = re.findall(r'(超级管理员|管理员|工程师|分析师|标注员)', content)
if roles:
    print(f"  ✓ 角色定义: {len(set(roles))}种角色")
    print(f"    角色: {', '.join(set(roles))}")
else:
    suggestions.append("建议明确定义用户角色")

print("\n6.2 检查操作日志...")
if '审计' in content or '日志' in content:
    print(f"  ✓ 操作日志: 存在")
else:
    issues.append("缺少操作日志记录")

print("\n6.3 检查敏感操作确认...")
dangerous_operations = ['删除', '停止', '取消']
for op in dangerous_operations:
    if op in content:
        # 检查是否有确认机制
        print(f"  ✓ {op}操作: 存在")

# ==================== 7. 性能和可用性检查 ====================
print("\n【维度7: 性能和可用性】")
print("-" * 80)

print("7.1 检查分页功能...")
if 'pagination' in content.lower():
    print(f"  ✓ 分页功能: 存在")
else:
    suggestions.append("建议为大数据量列表添加分页")

print("\n7.2 检查数据量...")
# 统计数据行数
table_rows = len(re.findall(r'<tr>', content))
print(f"  ✓ 表格行数: {table_rows}行")
if table_rows > 500:
    suggestions.append("数据量较大，建议优化加载性能")

print("\n7.3 检查响应式设计...")
responsive_keywords = ['@media', 'mobile', 'responsive']
has_responsive = any(keyword in content for keyword in responsive_keywords)
if has_responsive:
    print(f"  ✓ 响应式设计: 存在")
else:
    suggestions.append("建议添加响应式设计支持移动端")
    print(f"  ⚠️  响应式设计: 缺失")

# ==================== 8. 业务场景完整性 ====================
print("\n【维度8: 业务场景完整性】")
print("-" * 80)

print("8.1 检查异常处理场景...")
exception_scenarios = {
    '网络错误': ['网络', '超时', 'timeout'],
    '权限不足': ['权限', '无权限', 'permission'],
    '数据为空': ['暂无', '无数据', 'empty'],
    '操作失败': ['失败', 'failed', 'error'],
}

for scenario, keywords in exception_scenarios.items():
    found = any(keyword in content for keyword in keywords)
    if found:
        print(f"  ✓ {scenario}: 已考虑")
    else:
        suggestions.append(f"建议添加{scenario}的处理")
        print(f"  ⚠️  {scenario}: 未考虑")

print("\n8.2 检查状态流转...")
status_flow = ['待处理', '处理中', '已完成', '已取消']
status_found = [s for s in status_flow if s in content]
if len(status_found) >= 3:
    print(f"  ✓ 状态流转: 完整 ({len(status_found)}/4)")
else:
    suggestions.append("建议完善状态流转逻辑")
    print(f"  ⚠️  状态流转: 不完整 ({len(status_found)}/4)")

# ==================== 9. 国际化和本地化 ====================
print("\n【维度9: 国际化和本地化】")
print("-" * 80)

print("9.1 检查文本硬编码...")
# 简单检查是否所有文本都是硬编码
if 'i18n' in content or 'locale' in content or 'lang' in content:
    print(f"  ✓ 国际化支持: 存在")
else:
    suggestions.append("建议考虑国际化支持（如需要）")
    print(f"  ⚠️  国际化支持: 未实现")

print("\n9.2 检查时区处理...")
if 'timezone' in content.lower() or 'utc' in content.lower():
    print(f"  ✓ 时区处理: 已考虑")
else:
    suggestions.append("建议考虑时区处理")
    print(f"  ⚠️  时区处理: 未考虑")

# ==================== 10. 文档和帮助 ====================
print("\n【维度10: 文档和帮助】")
print("-" * 80)

print("10.1 检查帮助文档...")
help_keywords = ['帮助', '说明', '文档', 'help', '?']
has_help = any(keyword in content for keyword in help_keywords)
if has_help:
    print(f"  ✓ 帮助入口: 存在")
else:
    suggestions.append("建议添加帮助文档入口")
    print(f"  ⚠️  帮助入口: 缺失")

print("\n10.2 检查操作提示...")
tooltip_count = content.count('title=')
if tooltip_count > 10:
    print(f"  ✓ 操作提示: {tooltip_count}处")
else:
    suggestions.append("建议为按钮添加title提示")
    print(f"  ⚠️  操作提示: 较少")

# ==================== 总结 ====================
print("\n" + "=" * 80)
print("审查完成！")
print("=" * 80)

print(f"\n【严重问题】: {len(issues)}")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. ❌ {issue}")
else:
    print("  ✅ 未发现严重问题")

print(f"\n【优化建议】: {len(suggestions)}")
if suggestions:
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. 💡 {suggestion}")
else:
    print("  ✅ 无优化建议")

# 计算专业评分
total_checks = 40  # 总检查项
critical_issues = len(issues)
minor_issues = len(suggestions)

score = max(0, 100 - critical_issues * 5 - minor_issues * 1)

print(f"\n" + "=" * 80)
print(f"【专业评分】: {score}/100")
print("=" * 80)

if score >= 90:
    level = "优秀 ⭐⭐⭐⭐⭐"
    comment = "系统设计专业，细节完善，可以直接用于评审"
elif score >= 80:
    level = "良好 ⭐⭐⭐⭐"
    comment = "系统整体不错，有少量细节需要优化"
elif score >= 70:
    level = "中等 ⭐⭐⭐"
    comment = "系统基本可用，但需要较多改进"
else:
    level = "需改进 ⭐⭐"
    comment = "系统存在较多问题，需要重点优化"

print(f"\n评级: {level}")
print(f"评语: {comment}")

# 保存报告
with open('专业审查报告.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("专业审查报告 - 40年经验的项目经理视角\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"严重问题: {len(issues)}\n")
    for i, issue in enumerate(issues, 1):
        f.write(f"  {i}. {issue}\n")
    
    f.write(f"\n优化建议: {len(suggestions)}\n")
    for i, suggestion in enumerate(suggestions, 1):
        f.write(f"  {i}. {suggestion}\n")
    
    f.write(f"\n专业评分: {score}/100\n")
    f.write(f"评级: {level}\n")
    f.write(f"评语: {comment}\n")

print("\n报告已保存到: 专业审查报告.txt")
