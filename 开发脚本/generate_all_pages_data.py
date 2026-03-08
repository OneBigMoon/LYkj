#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有页面生成行业TOP级别的大量真实数据
"""

import random
from datetime import datetime, timedelta

# 基础数据
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗']
GIVEN_NAMES = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超', '华', '鹏', '飞', '宇']
INDUSTRIES = ['金融', '电商', '政务', '医疗', '教育', '客服', '保险', '物流', '制造', '零售', '能源', '交通', '房产', '旅游', '媒体']
MODEL_TYPES = ['ASR', 'NLU', 'TTS', '意图识别', '实体识别', '情感分析', '对话管理', '知识图谱', '文本分类', '命名实体']
VERSIONS = ['V1.0', 'V1.5', 'V2.0', 'V2.1', 'V2.5', 'V3.0', 'V3.5', 'V4.0']
TRAIN_TYPES = ['全量训练', '增量训练', '微调', '蒸馏', '迁移学习', '联邦学习']

def generate_name():
    return f"{random.choice(SURNAMES)}{random.choice(GIVEN_NAMES)}"

def generate_ip():
    return f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_trace_id():
    chars = '0123456789abcdef'
    return ''.join(random.choice(chars) for _ in range(8)) + '-' + ''.join(random.choice(chars) for _ in range(4))

print("=" * 80)
print("生成审计中心数据 (100条)")
print("=" * 80)

operations = ['登录系统', '创建用户', '修改权限', '删除数据', '导出报表', '训练模型', '部署模型', '查看日志', '修改配置', '创建实验']
risk_levels = [('高风险', 'rgba(239, 68, 68, 0.2)', '#EF4444'), ('中风险', 'rgba(245, 158, 11, 0.2)', '#F59E0B'), ('低风险', 'rgba(59, 130, 246, 0.2)', '#3B82F6')]

for i in range(100):
    log_id = f"#LOG-{10000 + i}"
    user = generate_name()
    operation = random.choice(operations)
    risk, bg, color = random.choice(risk_levels)
    ip = generate_ip()
    
    hours_ago = random.randint(0, 72)
    minutes_ago = random.randint(0, 59)
    if hours_ago == 0:
        time_str = f"{minutes_ago}分钟前"
    else:
        time_str = f"{hours_ago}小时前"
    
    print(f"""                  <tr>
                    <td>{log_id}</td>
                    <td>{user}</td>
                    <td>{operation}</td>
                    <td><span class="status-badge" style="background: {bg}; color: {color}; border: 1px solid {color};">{risk}</span></td>
                    <td>{ip}</td>
                    <td>{time_str}</td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">详情</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成实验追踪数据 (50个)")
print("=" * 80)

for i in range(50):
    exp_id = f"#EXP-{2000 + i}"
    industry = random.choice(INDUSTRIES)
    model_type = random.choice(MODEL_TYPES)
    version = random.choice(VERSIONS)
    exp_name = f"{industry}-{model_type}-{version}-实验{i+1}"
    
    acc = round(random.uniform(92, 99), 1)
    loss = round(random.uniform(0.01, 0.08), 4)
    f1 = round(random.uniform(0.90, 0.99), 3)
    
    status_choice = random.random()
    if status_choice < 0.3:
        status = '运行中'
        status_class = 'status-running'
        epoch = f"{random.randint(10, 45)}/50"
    elif status_choice < 0.5:
        status = '排队中'
        status_class = 'status-queued'
        epoch = "0/50"
    else:
        status = '已完成'
        status_class = 'status-completed'
        epoch = "50/50"
    
    hours_ago = random.randint(1, 48)
    time_str = f"{hours_ago}小时前"
    
    print(f"""                  <tr>
                    <td>{exp_id}</td>
                    <td>{exp_name}</td>
                    <td>{model_type}</td>
                    <td>{acc}%</td>
                    <td>{loss}</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td>{time_str}</td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">详情</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成链路追踪数据 (100条)")
print("=" * 80)

services = [
    'API → ASR → NLU → Dialog → Response',
    'API → ASR → NLU → Dialog → RAG → Response',
    'API → TTS → Response',
    'API → ASR → Intent → Response',
    'API → NLU → Entity → Response',
    'API → ASR → NLU → Dialog → Knowledge → Response'
]

for i in range(100):
    trace_id = generate_trace_id()
    service = random.choice(services)
    duration = round(random.uniform(0.3, 3.0), 1)
    span_count = random.randint(8, 20)
    
    status_choice = random.random()
    if status_choice < 0.9:
        status = '✅ 成功'
        status_class = 'status-running'
    elif status_choice < 0.95:
        status = '❌ 失败'
        status_class = 'status-queued'
        service = service.replace('Response', '<span style="color: #EF4444;">Error</span>')
    else:
        status = '⏱️ 超时'
        status_class = 'status-queued'
        service = service.replace('Response', '<span style="color: #F59E0B;">Timeout</span>')
    
    minutes_ago = random.randint(0, 120)
    if minutes_ago < 60:
        time_str = f"{minutes_ago}分钟前"
    else:
        time_str = f"{minutes_ago // 60}小时前"
    
    print(f"""                  <tr>
                    <td style="font-family: monospace; font-size: 11px;">{trace_id}</td>
                    <td><div style="font-size: 11px;">{service}</div></td>
                    <td style="font-weight: 600;">{duration}s</td>
                    <td>{span_count}</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td style="font-size: 11px;">{time_str}</td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">详情</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成人工干预工单数据 (80个)")
print("=" * 80)

issue_types = ['模型准确率下降', '响应时间过长', '服务异常', '数据质量问题', '资源不足', '配置错误', '依赖服务故障', '性能瓶颈']
priorities = [('紧急', 'rgba(239, 68, 68, 0.2)', '#EF4444'), ('高', 'rgba(245, 158, 11, 0.2)', '#F59E0B'), ('中', 'rgba(59, 130, 246, 0.2)', '#3B82F6'), ('低', 'rgba(100, 116, 139, 0.2)', '#64748B')]
statuses = [('待处理', 'status-queued'), ('处理中', 'status-running'), ('已完成', 'status-completed')]

for i in range(80):
    ticket_id = f"#WO-{5000 + i}"
    issue = random.choice(issue_types)
    priority, pri_bg, pri_color = random.choice(priorities)
    status, status_class = random.choice(statuses)
    handler = generate_name() if status != '待处理' else '-'
    
    hours_ago = random.randint(1, 72)
    time_str = f"{hours_ago}小时前"
    
    print(f"""                  <tr>
                    <td>{ticket_id}</td>
                    <td>{issue}</td>
                    <td><span class="status-badge" style="background: {pri_bg}; color: {pri_color}; border: 1px solid {pri_color};">{priority}</span></td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td>{handler}</td>
                    <td>{time_str}</td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">处理</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成智能标注任务数据 (50个)")
print("=" * 80)

label_types = ['意图分类', '实体识别', '情感分析', '文本分类', '对话标注', '语音标注', '图像标注', '视频标注']

for i in range(50):
    task_id = f"#LBL-{3000 + i}"
    industry = random.choice(INDUSTRIES)
    label_type = random.choice(label_types)
    task_name = f"{industry}-{label_type}-批次{i+1}"
    
    total = random.randint(5000, 50000)
    completed = random.randint(int(total * 0.3), total)
    progress = int((completed / total) * 100)
    
    status_choice = random.random()
    if status_choice < 0.4:
        status = '进行中'
        status_class = 'status-running'
    elif status_choice < 0.6:
        status = '已完成'
        status_class = 'status-completed'
    else:
        status = '待审核'
        status_class = 'status-queued'
    
    quality = round(random.uniform(92, 99), 1)
    
    print(f"""                  <tr>
                    <td>{task_id}</td>
                    <td>{task_name}</td>
                    <td>{label_type}</td>
                    <td>{completed}/{total}</td>
                    <td><div class="progress-bar"><div class="progress-fill" style="width: {progress}%;"></div></div></td>
                    <td>{quality}%</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">详情</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成数据治理数据源 (40个)")
print("=" * 80)

db_types = ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'ClickHouse', 'HBase', 'Cassandra']
source_types = [('数据库', 'status-running'), ('API', 'status-completed'), ('文件', 'status-queued')]

for i in range(40):
    source_id = f"DS-{1000 + i}"
    source_type, type_class = random.choice(source_types)
    
    if source_type == '数据库':
        db_type = random.choice(db_types)
        source_name = f"{db_type}-{random.choice(INDUSTRIES)}-生产库"
    elif source_type == 'API':
        source_name = f"{random.choice(INDUSTRIES)}-数据接口-V{random.randint(1, 3)}"
    else:
        source_name = f"{random.choice(INDUSTRIES)}-数据文件-{random.randint(1, 100)}"
    
    size = random.choice(['128GB', '256GB', '512GB', '1TB', '2TB', '5TB'])
    records = f"{random.randint(10, 500)}万"
    quality = round(random.uniform(85, 99), 1)
    
    status_choice = random.random()
    if status_choice < 0.8:
        status = '正常'
        status_class = 'status-running'
    elif status_choice < 0.95:
        status = '异常'
        status_class = 'status-queued'
    else:
        status = '维护中'
        status_class = 'status-completed'
    
    print(f"""                  <tr>
                    <td>{source_id}</td>
                    <td>{source_name}</td>
                    <td><span class="status-badge {type_class}">{source_type}</span></td>
                    <td>{size}</td>
                    <td>{records}</td>
                    <td>{quality}%</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">详情</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("生成流程编排数据 (30个)")
print("=" * 80)

flow_types = ['训练流程', '推理流程', '数据处理', 'ETL流程', '模型评估', '自动部署']

for i in range(30):
    flow_id = f"FLOW-{100 + i}"
    industry = random.choice(INDUSTRIES)
    flow_type = random.choice(flow_types)
    flow_name = f"{industry}-{flow_type}-{i+1}"
    
    node_count = random.randint(5, 15)
    exec_count = random.randint(10, 1000)
    success_rate = round(random.uniform(90, 99.5), 1)
    
    status_choice = random.random()
    if status_choice < 0.7:
        status = '已发布'
        status_class = 'status-completed'
    elif status_choice < 0.9:
        status = '草稿'
        status_class = 'status-queued'
    else:
        status = '运行中'
        status_class = 'status-running'
    
    days_ago = random.randint(1, 30)
    time_str = f"{days_ago}天前"
    
    print(f"""                  <tr>
                    <td>{flow_id}</td>
                    <td>{flow_name}</td>
                    <td>{flow_type}</td>
                    <td>{node_count}</td>
                    <td>{exec_count}</td>
                    <td>{success_rate}%</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td>{time_str}</td>
                    <td><button class="btn" style="padding: 4px 8px; font-size: 11px;">编辑</button></td>
                  </tr>""")

print("\n" + "=" * 80)
print("数据生成完成！")
print("=" * 80)
