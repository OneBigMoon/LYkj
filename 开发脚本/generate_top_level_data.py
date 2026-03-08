#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按照行业TOP标准生成大量真实数据
"""

import random
from datetime import datetime, timedelta

# 真实的中文姓名库
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗', '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹', '彭', '曾', '肖', '田', '董', '袁', '潘', '于', '蒋', '蔡', '余', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈']
GIVEN_NAMES = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞', '平', '刚', '桂英', '建华', '文', '辉', '力', '华', '鹏', '飞', '宇', '晨', '阳', '雪', '梅', '婷', '欣', '瑶', '萍', '红', '玲', '慧', '琳', '颖', '莉', '佳', '思', '雨', '晴', '悦']

def generate_name():
    """生成真实的中文姓名"""
    surname = random.choice(SURNAMES)
    given_name = random.choice(GIVEN_NAMES)
    return f"{surname}{given_name}"

def generate_username(name):
    """根据姓名生成用户名"""
    pinyin_map = {
        '王': 'wang', '李': 'li', '张': 'zhang', '刘': 'liu', '陈': 'chen',
        '杨': 'yang', '黄': 'huang', '赵': 'zhao', '周': 'zhou', '吴': 'wu'
    }
    surname = name[0]
    pinyin = pinyin_map.get(surname, 'user')
    return f"{pinyin}{random.randint(100, 999)}"

def generate_ip():
    """生成IP地址"""
    return f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_time_ago():
    """生成时间描述"""
    minutes = random.randint(1, 480)
    if minutes < 60:
        return f"{minutes}分钟前"
    else:
        hours = minutes // 60
        return f"{hours}小时前"

# 生成20个额外用户数据
print("=== 生成用户数据 ===\n")
roles = ['模型工程师', '数据分析师', '标注员', '审计员', '产品经理', '运维工程师']
departments = ['AI研发部', '数据部', '安全部', '产品部', '运维部']
statuses = [('🟢 在线', 'status-running'), ('🟡 离线', 'status-queued')]

for i in range(20):
    name = generate_name()
    username = generate_username(name)
    role = random.choice(roles)
    dept = random.choice(departments)
    status, status_class = random.choice(statuses)
    time_ago = generate_time_ago()
    ip = generate_ip()
    emp_id = f"{chr(65 + random.randint(0, 5))}{random.randint(100, 999):03d}"
    
    role_class = 'status-running' if '工程师' in role else 'status-completed' if '分析师' in role or '经理' in role else 'status-queued'
    
    print(f"""                  <tr>
                    <td>👤 {username}</td>
                    <td>{name}<br><span style="font-size: 11px; color: #64748B;">{emp_id}</span></td>
                    <td><span class="status-badge {role_class}">{role}</span></td>
                    <td>{dept}</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td>{time_ago}<br><span style="font-size: 11px; color: #64748B;">{ip}</span></td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">编辑</button></td>
                  </tr>""")

print("\n=== 生成训练任务数据 ===\n")

# 训练任务模板
industries = ['金融', '电商', '政务', '医疗', '教育', '客服', '保险', '物流', '制造', '零售']
model_types = ['ASR', 'NLU', 'TTS', '意图识别', '实体识别', '情感分析', '对话管理', '知识图谱']
versions = ['V1.0', 'V1.5', 'V2.0', 'V2.1', 'V2.5', 'V3.0']
train_types = ['全量训练', '增量训练', '微调', '蒸馏', '迁移学习']

for i in range(30):
    industry = random.choice(industries)
    model_type = random.choice(model_types)
    version = random.choice(versions)
    train_type = random.choice(train_types)
    
    task_name = f"{industry}-{model_type}-{version}-{train_type}"
    task_id = f"TASK-{random.randint(10000, 99999)}"
    
    # 随机状态
    status_choice = random.random()
    if status_choice < 0.3:  # 30% 运行中
        status = '运行中'
        status_color = '#10B981'
        status_bg = 'rgba(16, 185, 129, 0.1)'
        epoch_current = random.randint(10, 45)
        epoch_total = 50
        loss = round(random.uniform(0.01, 0.05), 4)
        acc = round(random.uniform(92, 98), 1)
        progress = int((epoch_current / epoch_total) * 100)
        remaining = f"{random.randint(1, 5)}h {random.randint(0, 59)}m"
        
        print(f"""                <div style="background: {status_bg}; border-left: 3px solid {status_color}; padding: 16px; border-radius: 6px; margin-bottom: 12px;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 600; color: {status_color};">🟢 {status} | {task_name}</span>
                    <span style="font-size: 12px; color: #94A3B8;">{task_id}</span>
                  </div>
                  <div class="progress-bar" style="margin: 12px 0;">
                    <div class="progress-fill" style="width: {progress}%;"></div>
                  </div>
                  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; font-size: 12px; margin-bottom: 12px;">
                    <div>📊 Epoch: {epoch_current}/{epoch_total}</div>
                    <div>📉 Loss: {loss}</div>
                    <div>🎯 Acc: {acc}%</div>
                    <div>⏱️ 剩余: {remaining}</div>
                  </div>
                  <div style="display: flex; gap: 8px;">
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">查看详情</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">TensorBoard</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">暂停</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">停止</button>
                  </div>
                </div>""")
    
    elif status_choice < 0.5:  # 20% 排队中
        status = '排队中'
        status_color = '#F59E0B'
        status_bg = 'rgba(245, 158, 11, 0.1)'
        queue_pos = random.randint(1, 10)
        gpu_count = random.choice([4, 8, 16])
        memory = random.choice([64, 128, 256])
        duration = random.randint(3, 12)
        wait_time = random.randint(10, 120)
        
        print(f"""                <div style="background: {status_bg}; border-left: 3px solid {status_color}; padding: 16px; border-radius: 6px; margin-bottom: 12px;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 600; color: {status_color};">🟡 {status} | {task_name}</span>
                    <span style="font-size: 12px; color: #94A3B8;">队列: 第{queue_pos}位</span>
                  </div>
                  <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                    💻 需求资源: GPU×{gpu_count} | 内存: {memory}GB | 预计时长: {duration}小时 | 预计等待: {wait_time}分钟
                  </div>
                  <div style="display: flex; gap: 8px;">
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">查看详情</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">调整优先级</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">取消</button>
                  </div>
                </div>""")
    
    else:  # 50% 已完成
        status = '已完成'
        status_color = '#3B82F6'
        status_bg = 'rgba(59, 130, 246, 0.1)'
        loss = round(random.uniform(0.01, 0.03), 4)
        acc = round(random.uniform(95, 99), 1)
        f1 = round(random.uniform(0.94, 0.99), 3)
        duration = f"{random.randint(2, 8)}h {random.randint(0, 59)}m"
        acc_improve = round(random.uniform(0.5, 3.0), 1)
        latency_improve = random.randint(5, 25)
        
        print(f"""                <div style="background: {status_bg}; border-left: 3px solid {status_color}; padding: 16px; border-radius: 6px; margin-bottom: 12px;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 600; color: {status_color};">✅ {status} | {task_name}</span>
                    <span style="font-size: 12px; color: #94A3B8;">{task_id}</span>
                  </div>
                  <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                    📊 最终指标: Loss: {loss} | Acc: {acc}% | F1: {f1} | 用时: {duration}
                  </div>
                  <div style="font-size: 12px; color: #10B981; margin-bottom: 8px;">
                    🎯 性能提升: Acc ↑{acc_improve}% | 响应时间 ↓{latency_improve}%
                  </div>
                  <div style="display: flex; gap: 8px;">
                    <button class="btn btn-primary" style="font-size: 11px; padding: 4px 8px;">注册模型</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">查看报告</button>
                    <button class="btn" style="font-size: 11px; padding: 4px 8px;">重新训练</button>
                  </div>
                </div>""")

print("\n数据生成完成！")
print("请将生成的HTML代码复制到对应的页面中。")
