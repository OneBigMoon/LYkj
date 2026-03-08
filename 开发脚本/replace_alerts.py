#!/usr/bin/env python3
import re

# 读取文件
with open('ai-platform-complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义替换规则
replacements = [
    # 简单的alert替换
    (r"alert\('([^']+)'\);", lambda m: f"showNotification('{m.group(1)}', 'info');"),
    (r'alert\("([^"]+)"\);', lambda m: f'showNotification("{m.group(1)}", \'info\');'),
    
    # 带变量的alert
    (r"alert\('([^']*)'  \+ ([^)]+)\);", lambda m: f"showNotification('{m.group(1)}' + {m.group(2)}, 'info');"),
    (r"alert\(([^)]+) \+ '([^']*)'\);", lambda m: f"showNotification({m.group(1)} + '{m.group(2)}', 'info');"),
]

# 手动替换特定的alert
specific_replacements = {
    "alert('重新训练')": "showNotification('✅ 已创建新的训练任务', 'success')",
    "alert('新建实验功能')": "showNotification('📝 新建实验', 'info')",
    "alert('请选择要对比的实验')": "showNotification('📊 请选择要对比的实验', 'info')",
    "alert('工单已分配给处理人员')": "showNotification('✅ 工单已分配给处理人员', 'success')",
    "alert('审批通过')": "showNotification('✅ 审批通过', 'success')",
    "alert('服务器重启中...')": "showNotification('🔄 服务器重启中...', 'warning')",
    "alert('扩容申请已提交')": "showNotification('✅ 扩容申请已提交', 'success')",
    "alert('数据清理任务已创建')": "showNotification('✅ 数据清理任务已创建', 'success')",
    "alert('查看任务详情')": "showNotification('📄 查看任务详情', 'info')",
    "alert('正在生成截图...')": "showNotification('📷 正在生成截图...', 'info')",
    "alert('流程已保存')": "showNotification('✅ 流程已保存', 'success')",
    "alert('流程开始运行...')": "showNotification('🚀 流程开始运行...', 'info')",
    "alert('正在导出对话记录...')": "showNotification('📥 正在导出对话记录...', 'info')",
    "alert('配置已重置为默认值')": "showNotification('✅ 配置已重置为默认值', 'success')",
    "alert('配置保存成功!')": "showNotification('✅ 配置保存成功!', 'success')",
    "alert('新建实体功能')": "showNotification('➕ 新建实体', 'info')",
}

# 执行特定替换
for old, new in specific_replacements.items():
    content = content.replace(old, new)

# 保存文件
with open('ai-platform-complete.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("替换完成!")
