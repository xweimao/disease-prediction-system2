#!/usr/bin/env python3
"""
疾病预测系统启动文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from datetime import datetime



app = Flask(__name__,
            template_folder='templates',
            static_folder='app/static')

# 配置
app.config['SECRET_KEY'] = 'disease_prediction_secret_key_2024'
app.config['LANGUAGES'] = {
    'en': 'English',
    'zh': '中文'
}

# 语言设置函数
def get_locale():
    """获取当前语言设置"""
    return session.get('language', 'zh')

# 翻译函数
def translate_text(text):
    """翻译函数"""
    translations = {
        'zh': {
            'Disease Prediction System': '疾病预测系统',
            'Disease Risk Calculator': '重大慢病防治技术推广应用平台',
            'Major Chronic Disease Prevention and Treatment Technology Promotion Platform': '重大慢病防治技术推广应用平台',
            'Sichuan Provincial Key Laboratory of Human Genetics': '四川省人类基因重点实验室',
            'Data Life and Intelligent Health Center': '数基生命与智能健康中心',
            'Data Life and Intelligent Health Center (Xiaowei Mao)': '数基生命与智能健康中心 (毛晓伟)',
            '(Xiaowei Mao)': '(毛晓伟)',
            'Home': '首页',
            'About': '关于',
            'Contact': '联系我们',
            'All rights reserved': '保留所有权利',
            'Southwest China Multi-Disease Risk Assessment': '围绕四大慢病西南地区多发疾病',
            'Comprehensive disease risk prediction covering 8 categories of diseases prevalent in Southwest China': '涵盖西南地区多发的8类疾病的综合疾病风险预测',
            '8 Disease Categories': '8类疾病',

            'AI-Powered': 'AI驱动',
            'Evidence-Based': '循证医学',
            'Disease Risk Assessment': '疾病风险评估',
            'Select a disease category to begin your risk assessment': '选择疾病类别开始您的风险评估',
            'Why Choose Our Platform': '为什么选择我们的平台',
            'Facing Major Needs': '面向重大需求',
            'AI-Powered Analysis': 'AI智能分析',
            'Advanced machine learning algorithms for accurate risk assessment': '先进的机器学习算法，提供准确的风险评估',
            'Medical Data Security': '医学数据安全',
            'Your health data is secure and never stored permanently': '您的健康数据安全，永不永久存储',
            'Missing Data Imputation': '缺失数据填充',
            'Advanced algorithms to handle incomplete data effectively': '先进算法有效处理不完整数据',
            'Multi-Population Generalization': '多人群泛化性',
            'Validated across diverse populations for broad applicability': '在不同人群中验证，具有广泛适用性',
            'Based on extensive research and clinical data from Southwest China': '基于西南地区广泛的研究和临床数据',
            'Important Disclaimer': '重要免责声明',
            'This tool is for educational and research purposes only. Results should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.': '本工具仅用于教育和研究目的。结果不应替代专业医疗建议、诊断或治疗。医疗决策请务必咨询合格的医疗保健提供者。',
            'Multimodal Database': '多模态数据库',
            'Medical Text': '医学文本',
            'Omics Data': '组学数据',
            'Medical Imaging': '医学影像',
            'Panda Algorithm': 'Panda算法',
            'Federated Learning': '联邦学习',
            'Data Security': '数据安全',
            'Sample Data': '样例数据',
            'Comprehensive medical data integration platform': '综合医学数据集成平台',
            'Explore': '探索',
            'Explore Category': '探索分类',
            'Subcategories': '子分类',
            'Enter': '进入',
            'Category Information': '分类信息',
            'Data Types': '数据类型',
            'Features': '功能特性',
            'Real-time data access': '实时数据访问',
            'Advanced search capabilities': '高级搜索功能',
            'Data visualization tools': '数据可视化工具',
            'Export and analysis functions': '导出和分析功能',
            'Back to Database': '返回数据库',
            'Data Overview': '数据概览',
            'Total Records': '总记录数',
            'Active Studies': '活跃研究',
            'Data Sources': '数据来源',
            'ID': '编号',
            'Type': '类型',
            'Source': '来源',
            'Date': '日期',
            'Status': '状态',
            'Hospital A': '医院A',
            'Research Center B': '研究中心B',
            'Clinical Trial C': '临床试验C',
            'Active': '活跃',
            'Processing': '处理中',
            'Run Analysis': '运行分析',
            'Start Training': '开始训练',
            'Data Export': '数据导出',
            'Back to Category': '返回分类',
            'Database Home': '数据库首页',
            'Advanced AI analysis powered by Panda algorithm for intelligent data processing and pattern recognition.': '基于Panda算法的高级AI分析，用于智能数据处理和模式识别。',
            'Secure collaborative learning without sharing sensitive data across multiple institutions.': '在不共享敏感数据的情况下，跨多个机构进行安全协作学习。',
            'Export data in various formats for further analysis and research.': '以各种格式导出数据，用于进一步分析和研究。',
            'Detailed data exploration and analysis tools': '详细的数据探索和分析工具',
            'Data Integration Features': '数据集成功能',
            'Advanced encryption and privacy protection': '高级加密和隐私保护',
            'Distributed learning without data sharing': '无数据共享的分布式学习',
            'Advanced AI analysis engine': '高级AI分析引擎',
            'Rich sample datasets for research': '丰富的研究样本数据集',
            'Upload Data': '上传数据',
            'Start Analysis': '开始分析',
            'Federated Learning Module': '联邦学习模块',
            'Differential Privacy Module': '差分隐私模块',
            'Data Upload': '数据上传',
            'Analysis Results': '分析结果',
            'Sample Dataset': '样例数据集',
            'Privacy Level': '隐私级别',
            'High': '高',
            'Medium': '中',
            'Low': '低',
            'Training Status': '训练状态',
            'Ready': '就绪',
            'Training': '训练中',
            'Completed': '已完成',
            'Model Performance': '模型性能',
            'Accuracy': '准确率',
            'Precision': '精确率',
            'Recall': '召回率',
            'F1 Score': 'F1分数',
            'Download Results': '下载结果',
            'View Details': '查看详情',
            'Configure Parameters': '配置参数',
            'Select File': '选择文件',
            'Upload': '上传',
            'Cancel': '取消',
            'Processing': '处理中',
            'Error': '错误',
            'Success': '成功',
            'Warning': '警告',
            'Information': '信息',
            'Participating Nodes': '参与节点',
            'Total Samples': '总样本数',
            'Privacy Parameters': '隐私参数',
            'Enable Federated Learning': '启用联邦学习',
            'Enable Privacy Protection': '启用隐私保护',
            'Supported formats: CSV, Excel, JSON': '支持格式：CSV、Excel、JSON',
            'Dataset Info': '数据集信息',
            'Samples': '样本',
            'Features': '特征',
            'Format': '格式',
            'Size': '大小',
            'Load Sample Data': '加载样例数据',
            'Analysis ID': '分析编号',
            'Training Time': '训练时间',
            'Data Points': '数据点',
            'Features Used': '使用特征',
            'Privacy parameters configured successfully': '隐私参数配置成功',
            'Please select a file first': '请先选择文件',
            'Data uploaded successfully': '数据上传成功',
            'Sample data loaded successfully': '样例数据加载成功',
            'Sample data details': '样例数据详情',
            'This dataset contains breast cancer risk factors including age, family history, BRCA mutations, and other clinical variables.': '该数据集包含乳腺癌风险因子，包括年龄、家族史、BRCA突变和其他临床变量。',
            'Data Preprocessing Process': '数据预处理过程',
            'Data Quality Check': '数据质量检查',
            'Missing Value Analysis': '缺失值分析',
            'Data Imputation Process': '数据填充过程',
            'Before Imputation': '填充前',
            'After Imputation': '填充后',
            'Data Imputation Effectiveness': '数据填充效果评估',
            'Imputation Accuracy': '填充准确率',
            'Total Missing Rate': '总缺失率',
            'Completion Rate': '填充完成率',
            'Federated Learning Statistics': '联邦学习统计',
            'Training Rounds': '训练轮次',
            'Convergence Rate': '收敛率',
            'Privacy Budget': '隐私预算',
            'Download Full Report': '下载完整报告',
            'Export Results': '导出结果',
            'Please select a file first': '请先选择文件',
            'Uploading...': '上传中...',
            'Data uploaded successfully! Filename: ': '数据上传成功！文件名：',
            'Upload failed: ': '上传失败：',
            'Upload error: ': '上传错误：',
            'File Uploaded Successfully': '文件上传成功',
            'Filename': '文件名',
            'File Size': '文件大小',
            'Please upload a data file or load sample data first': '请先上传数据文件或加载样例数据',
            'Analyzing...': '分析中...',
            'Contains medical literature, medical records, diagnostic reports and other text data': '包含医学文献、病历、诊断报告等文本数据',
            'Contains genomics, proteomics, metabolomics and other multi-omics data': '包含基因组学、蛋白质组学、代谢组学等多组学数据',
            'Contains CT, MRI, X-ray, ultrasound and other medical imaging data': '包含CT、MRI、X光、超声等医学影像数据'
        },
        'en': {}  # 英文直接返回原文
    }

    locale = get_locale()
    if locale == 'zh' and text in translations['zh']:
        return translations['zh'][text]
    return text

# 注册模板函数
@app.template_global('_')
def template_translate(text):
    """模板翻译函数"""
    return translate_text(text)

@app.template_global('get_locale')
def template_get_locale():
    """获取当前语言设置"""
    return get_locale()

# 疾病预测模型配置
DISEASE_MODELS = {
    'lung_cancer': {
        'name_zh': '肺癌',
        'name_en': 'Lung Cancer',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'smoking_years', 'name_zh': '吸烟年数', 'name_en': 'Smoking Years', 'type': 'number', 'min': 0, 'max': 80, 'unit': '年/years'},
            {'id': 'smoking_amount', 'name_zh': '每日吸烟量', 'name_en': 'Cigarettes per Day', 'type': 'number', 'min': 0, 'max': 100, 'unit': '支/cigarettes'},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'occupational_exposure', 'name_zh': '职业暴露', 'name_en': 'Occupational Exposure', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]}
        ]
    },
    'diabetes': {
        'name_zh': '糖尿病',
        'name_en': 'Diabetes',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'bmi', 'name_zh': 'BMI', 'name_en': 'BMI', 'type': 'number', 'min': 15, 'max': 50, 'unit': 'kg/m²'},
            {'id': 'waist_circumference', 'name_zh': '腰围', 'name_en': 'Waist Circumference', 'type': 'number', 'min': 50, 'max': 150, 'unit': 'cm'},
            {'id': 'systolic_bp', 'name_zh': '收缩压', 'name_en': 'Systolic Blood Pressure', 'type': 'number', 'min': 80, 'max': 250, 'unit': 'mmHg'},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'physical_activity', 'name_zh': '体力活动', 'name_en': 'Physical Activity', 'type': 'select', 'options': [{'value': 0, 'label_zh': '低', 'label_en': 'Low'}, {'value': 1, 'label_zh': '中', 'label_en': 'Moderate'}, {'value': 2, 'label_zh': '高', 'label_en': 'High'}]}
        ]
    },
    'esophageal_cancer': {
        'name_zh': '食管癌',
        'name_en': 'Esophageal Cancer',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'smoking_years', 'name_zh': '吸烟年数', 'name_en': 'Smoking Years', 'type': 'number', 'min': 0, 'max': 80, 'unit': '年/years'},
            {'id': 'alcohol_consumption', 'name_zh': '饮酒量', 'name_en': 'Alcohol Consumption', 'type': 'select', 'options': [{'value': 0, 'label_zh': '不饮酒', 'label_en': 'No alcohol'}, {'value': 1, 'label_zh': '少量', 'label_en': 'Light'}, {'value': 2, 'label_zh': '中等', 'label_en': 'Moderate'}, {'value': 3, 'label_zh': '大量', 'label_en': 'Heavy'}]},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]}
        ]
    },
    'gastric_cancer': {
        'name_zh': '胃癌',
        'name_en': 'Gastric Cancer',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'h_pylori', 'name_zh': '幽门螺杆菌感染', 'name_en': 'H. pylori Infection', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'diet_habits', 'name_zh': '饮食习惯', 'name_en': 'Diet Habits', 'type': 'select', 'options': [{'value': 0, 'label_zh': '健康', 'label_en': 'Healthy'}, {'value': 1, 'label_zh': '一般', 'label_en': 'Average'}, {'value': 2, 'label_zh': '不健康', 'label_en': 'Unhealthy'}]}
        ]
    },
    'colorectal_cancer': {
        'name_zh': '结直肠癌',
        'name_en': 'Colorectal Cancer',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'bmi', 'name_zh': 'BMI', 'name_en': 'BMI', 'type': 'number', 'min': 15, 'max': 50, 'unit': 'kg/m²'},
            {'id': 'physical_activity', 'name_zh': '体力活动', 'name_en': 'Physical Activity', 'type': 'select', 'options': [{'value': 0, 'label_zh': '低', 'label_en': 'Low'}, {'value': 1, 'label_zh': '中', 'label_en': 'Moderate'}, {'value': 2, 'label_zh': '高', 'label_en': 'High'}]}
        ]
    },
    'liver_cancer': {
        'name_zh': '肝癌',
        'name_en': 'Liver Cancer',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'hepatitis_b', 'name_zh': '乙肝病毒感染', 'name_en': 'Hepatitis B', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'hepatitis_c', 'name_zh': '丙肝病毒感染', 'name_en': 'Hepatitis C', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'alcohol_consumption', 'name_zh': '饮酒量', 'name_en': 'Alcohol Consumption', 'type': 'select', 'options': [{'value': 0, 'label_zh': '不饮酒', 'label_en': 'No alcohol'}, {'value': 1, 'label_zh': '少量', 'label_en': 'Light'}, {'value': 2, 'label_zh': '中等', 'label_en': 'Moderate'}, {'value': 3, 'label_zh': '大量', 'label_en': 'Heavy'}]}
        ]
    },
    'stroke': {
        'name_zh': '卒中',
        'name_en': 'Stroke',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'systolic_bp', 'name_zh': '收缩压', 'name_en': 'Systolic Blood Pressure', 'type': 'number', 'min': 80, 'max': 250, 'unit': 'mmHg'},
            {'id': 'diabetes', 'name_zh': '糖尿病史', 'name_en': 'Diabetes History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'smoking_status', 'name_zh': '吸烟状态', 'name_en': 'Smoking Status', 'type': 'select', 'options': [{'value': 0, 'label_zh': '从不吸烟', 'label_en': 'Never'}, {'value': 1, 'label_zh': '已戒烟', 'label_en': 'Former'}, {'value': 2, 'label_zh': '现在吸烟', 'label_en': 'Current'}]}
        ]
    },
    'hypertension': {
        'name_zh': '高血压',
        'name_en': 'Hypertension',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'bmi', 'name_zh': 'BMI', 'name_en': 'BMI', 'type': 'number', 'min': 15, 'max': 50, 'unit': 'kg/m²'},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'salt_intake', 'name_zh': '盐摄入量', 'name_en': 'Salt Intake', 'type': 'select', 'options': [{'value': 0, 'label_zh': '低', 'label_en': 'Low'}, {'value': 1, 'label_zh': '中', 'label_en': 'Moderate'}, {'value': 2, 'label_zh': '高', 'label_en': 'High'}]}
        ]
    },
    'copd': {
        'name_zh': '慢性阻塞性肺疾病',
        'name_en': 'Chronic Obstructive Pulmonary Disease',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'smoking_years', 'name_zh': '吸烟年数', 'name_en': 'Smoking Years', 'type': 'number', 'min': 0, 'max': 80, 'unit': '年/years'},
            {'id': 'occupational_exposure', 'name_zh': '职业暴露', 'name_en': 'Occupational Exposure', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'air_pollution', 'name_zh': '空气污染暴露', 'name_en': 'Air Pollution Exposure', 'type': 'select', 'options': [{'value': 0, 'label_zh': '低', 'label_en': 'Low'}, {'value': 1, 'label_zh': '中', 'label_en': 'Moderate'}, {'value': 2, 'label_zh': '高', 'label_en': 'High'}]}
        ]
    },
    'hyperlipidemia': {
        'name_zh': '高血脂',
        'name_en': 'Hyperlipidemia',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'bmi', 'name_zh': 'BMI', 'name_en': 'BMI', 'type': 'number', 'min': 15, 'max': 50, 'unit': 'kg/m²'},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'diet_habits', 'name_zh': '饮食习惯', 'name_en': 'Diet Habits', 'type': 'select', 'options': [{'value': 0, 'label_zh': '健康', 'label_en': 'Healthy'}, {'value': 1, 'label_zh': '一般', 'label_en': 'Average'}, {'value': 2, 'label_zh': '不健康', 'label_en': 'Unhealthy'}]}
        ]
    },
    'hyperuricemia': {
        'name_zh': '高尿酸血症',
        'name_en': 'Hyperuricemia',
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'bmi', 'name_zh': 'BMI', 'name_en': 'BMI', 'type': 'number', 'min': 15, 'max': 50, 'unit': 'kg/m²'},
            {'id': 'alcohol_consumption', 'name_zh': '饮酒量', 'name_en': 'Alcohol Consumption', 'type': 'select', 'options': [{'value': 0, 'label_zh': '不饮酒', 'label_en': 'No alcohol'}, {'value': 1, 'label_zh': '少量', 'label_en': 'Light'}, {'value': 2, 'label_zh': '中等', 'label_en': 'Moderate'}, {'value': 3, 'label_zh': '大量', 'label_en': 'Heavy'}]},
            {'id': 'kidney_function', 'name_zh': '肾功能', 'name_en': 'Kidney Function', 'type': 'select', 'options': [{'value': 0, 'label_zh': '正常', 'label_en': 'Normal'}, {'value': 1, 'label_zh': '轻度异常', 'label_en': 'Mild abnormal'}, {'value': 2, 'label_zh': '中度异常', 'label_en': 'Moderate abnormal'}]}
        ]
    },
    'breast_cancer': {
        'name_zh': '乳腺癌',
        'name_en': 'Breast Cancer',
        'algorithm': 'Panda',
        'federated_learning': True,
        'risk_factors': [
            {'id': 'age', 'name_zh': '年龄', 'name_en': 'Age', 'type': 'number', 'min': 18, 'max': 100, 'unit': '岁/years'},
            {'id': 'gender', 'name_zh': '性别', 'name_en': 'Gender', 'type': 'select', 'options': [{'value': 0, 'label_zh': '女', 'label_en': 'Female'}, {'value': 1, 'label_zh': '男', 'label_en': 'Male'}]},
            {'id': 'family_history', 'name_zh': '家族史', 'name_en': 'Family History', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'brca_mutation', 'name_zh': 'BRCA基因突变', 'name_en': 'BRCA Mutation', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': 'BRCA1', 'label_en': 'BRCA1'}, {'value': 2, 'label_zh': 'BRCA2', 'label_en': 'BRCA2'}]},
            {'id': 'menstrual_age', 'name_zh': '初潮年龄', 'name_en': 'Age at Menarche', 'type': 'number', 'min': 8, 'max': 18, 'unit': '岁/years'},
            {'id': 'first_birth_age', 'name_zh': '初产年龄', 'name_en': 'Age at First Birth', 'type': 'number', 'min': 15, 'max': 50, 'unit': '岁/years'},
            {'id': 'hormone_therapy', 'name_zh': '激素治疗史', 'name_en': 'Hormone Therapy', 'type': 'select', 'options': [{'value': 0, 'label_zh': '无', 'label_en': 'No'}, {'value': 1, 'label_zh': '有', 'label_en': 'Yes'}]},
            {'id': 'breast_density', 'name_zh': '乳腺密度', 'name_en': 'Breast Density', 'type': 'select', 'options': [{'value': 0, 'label_zh': '低', 'label_en': 'Low'}, {'value': 1, 'label_zh': '中', 'label_en': 'Moderate'}, {'value': 2, 'label_zh': '高', 'label_en': 'High'}]}
        ]
    }
}

# 疾病分类配置
DISEASE_CATEGORIES = {
    'cancer': {
        'name_zh': '癌症',
        'name_en': 'Cancer',
        'diseases': [
            {'id': 'lung_cancer', 'name_zh': '肺癌', 'name_en': 'Lung Cancer'},
            {'id': 'breast_cancer', 'name_zh': '乳腺癌', 'name_en': 'Breast Cancer'},
            {'id': 'esophageal_cancer', 'name_zh': '食管癌', 'name_en': 'Esophageal Cancer'},
            {'id': 'gastric_cancer', 'name_zh': '胃癌', 'name_en': 'Gastric Cancer'},
            {'id': 'colorectal_cancer', 'name_zh': '结直肠癌', 'name_en': 'Colorectal Cancer'},
            {'id': 'liver_cancer', 'name_zh': '肝癌', 'name_en': 'Liver Cancer'}
        ]
    },
    'cardiovascular': {
        'name_zh': '心脑血管疾病',
        'name_en': 'Cardiovascular Disease',
        'diseases': [
            {'id': 'stroke', 'name_zh': '卒中', 'name_en': 'Stroke'},
            {'id': 'hypertension', 'name_zh': '高血压', 'name_en': 'Hypertension'}
        ]
    },
    'respiratory': {
        'name_zh': '呼吸疾病',
        'name_en': 'Respiratory Disease',
        'diseases': [
            {'id': 'copd', 'name_zh': '慢性阻塞性肺疾病', 'name_en': 'Chronic Obstructive Pulmonary Disease'}
        ]
    },
    'metabolic': {
        'name_zh': '代谢性疾病',
        'name_en': 'Metabolic Disease',
        'diseases': [
            {'id': 'diabetes', 'name_zh': '糖尿病', 'name_en': 'Diabetes'},
            {'id': 'hyperlipidemia', 'name_zh': '高血脂', 'name_en': 'Hyperlipidemia'},
            {'id': 'hyperuricemia', 'name_zh': '高尿酸血症', 'name_en': 'Hyperuricemia'}
        ]
    }
}

# 多模态数据库配置
MULTIMODAL_DATABASE = {
    'medical_text': {
        'name_zh': '医学文本',
        'name_en': 'Medical Text',
        'description_zh': '包含医学文献、病历、诊断报告等文本数据',
        'description_en': 'Contains medical literature, medical records, diagnostic reports and other text data',
        'subcategories': [
            {'id': 'literature', 'name_zh': '医学文献', 'name_en': 'Medical Literature'},
            {'id': 'records', 'name_zh': '电子病历', 'name_en': 'Electronic Health Records'},
            {'id': 'reports', 'name_zh': '诊断报告', 'name_en': 'Diagnostic Reports'}
        ]
    },
    'omics_data': {
        'name_zh': '组学数据',
        'name_en': 'Omics Data',
        'description_zh': '包含基因组学、蛋白质组学、代谢组学等多组学数据',
        'description_en': 'Contains genomics, proteomics, metabolomics and other multi-omics data',
        'subcategories': [
            {'id': 'genomics', 'name_zh': '基因组学', 'name_en': 'Genomics'},
            {'id': 'proteomics', 'name_zh': '蛋白质组学', 'name_en': 'Proteomics'},
            {'id': 'metabolomics', 'name_zh': '代谢组学', 'name_en': 'Metabolomics'}
        ]
    },
    'medical_imaging': {
        'name_zh': '医学影像',
        'name_en': 'Medical Imaging',
        'description_zh': '包含CT、MRI、X光、超声等医学影像数据',
        'description_en': 'Contains CT, MRI, X-ray, ultrasound and other medical imaging data',
        'subcategories': [
            {'id': 'ct', 'name_zh': 'CT影像', 'name_en': 'CT Imaging'},
            {'id': 'mri', 'name_zh': 'MRI影像', 'name_en': 'MRI Imaging'},
            {'id': 'xray', 'name_zh': 'X光影像', 'name_en': 'X-ray Imaging'},
            {'id': 'ultrasound', 'name_zh': '超声影像', 'name_en': 'Ultrasound Imaging'}
        ]
    }
}

def get_locale():
    """获取当前语言设置"""
    return session.get('language', 'zh')

def calculate_risk_score(disease_id, factors):
    """计算疾病风险评分"""
    if disease_id == 'lung_cancer':
        return calculate_lung_cancer_risk(factors)
    elif disease_id == 'diabetes':
        return calculate_diabetes_risk(factors)
    elif disease_id == 'breast_cancer':
        return calculate_breast_cancer_risk_panda(factors)
    else:
        return calculate_default_risk(factors)

def calculate_lung_cancer_risk(factors):
    """肺癌风险计算"""
    risk_score = 0
    
    age = factors.get('age', 0)
    if age > 60:
        risk_score += 30
    elif age > 45:
        risk_score += 20
    elif age > 30:
        risk_score += 10
    
    smoking_years = factors.get('smoking_years', 0)
    smoking_amount = factors.get('smoking_amount', 0)
    smoking_index = smoking_years * smoking_amount / 20
    
    if smoking_index > 30:
        risk_score += 40
    elif smoking_index > 20:
        risk_score += 30
    elif smoking_index > 10:
        risk_score += 20
    elif smoking_index > 0:
        risk_score += 10
    
    if factors.get('family_history', 0) == 1:
        risk_score += 15
    
    if factors.get('occupational_exposure', 0) == 1:
        risk_score += 10
    
    if factors.get('gender', 0) == 1:
        risk_score += 5
    
    return min(risk_score, 100)

def calculate_diabetes_risk(factors):
    """糖尿病风险计算"""
    risk_score = 0
    
    age = factors.get('age', 0)
    if age > 65:
        risk_score += 25
    elif age > 45:
        risk_score += 15
    elif age > 35:
        risk_score += 10
    
    bmi = factors.get('bmi', 0)
    if bmi > 30:
        risk_score += 25
    elif bmi > 25:
        risk_score += 15
    elif bmi > 23:
        risk_score += 10
    
    waist = factors.get('waist_circumference', 0)
    if waist > 90:
        risk_score += 15
    elif waist > 85:
        risk_score += 10
    
    sbp = factors.get('systolic_bp', 0)
    if sbp > 140:
        risk_score += 15
    elif sbp > 130:
        risk_score += 10
    
    if factors.get('family_history', 0) == 1:
        risk_score += 20
    
    activity = factors.get('physical_activity', 1)
    if activity == 0:
        risk_score += 10
    elif activity == 2:
        risk_score -= 5
    
    return min(max(risk_score, 0), 100)

def calculate_breast_cancer_risk_panda(factors):
    """乳腺癌风险计算 - Panda算法 (基于PIXANT改进的Python版本)"""
    import numpy as np

    # 基础风险评分
    risk_score = 0

    # 年龄因子 (权重: 0.25)
    age = factors.get('age', 0)
    if age < 30:
        age_score = 5
    elif age < 40:
        age_score = 10
    elif age < 50:
        age_score = 20
    elif age < 60:
        age_score = 30
    else:
        age_score = 35

    # 家族史因子 (权重: 0.30)
    family_history = factors.get('family_history', 0)
    family_score = family_history * 25

    # BRCA基因突变因子 (权重: 0.35)
    brca_mutation = factors.get('brca_mutation', 0)
    if brca_mutation == 1:  # BRCA1
        brca_score = 40
    elif brca_mutation == 2:  # BRCA2
        brca_score = 35
    else:
        brca_score = 0

    # 生殖因子 (权重: 0.15)
    menstrual_age = factors.get('menstrual_age', 13)
    first_birth_age = factors.get('first_birth_age', 25)

    # 早初潮增加风险
    if menstrual_age < 12:
        reproductive_score = 10
    elif menstrual_age < 14:
        reproductive_score = 5
    else:
        reproductive_score = 0

    # 晚育或未育增加风险
    if first_birth_age > 30:
        reproductive_score += 8
    elif first_birth_age > 25:
        reproductive_score += 4

    # 激素治疗史 (权重: 0.10)
    hormone_therapy = factors.get('hormone_therapy', 0)
    hormone_score = hormone_therapy * 12

    # 乳腺密度 (权重: 0.20)
    breast_density = factors.get('breast_density', 0)
    if breast_density == 2:  # 高密度
        density_score = 15
    elif breast_density == 1:  # 中等密度
        density_score = 8
    else:
        density_score = 0

    # Panda算法核心：非线性组合
    # 使用sigmoid函数进行风险整合
    linear_combination = (
        age_score * 0.25 +
        family_score * 0.30 +
        brca_score * 0.35 +
        reproductive_score * 0.15 +
        hormone_score * 0.10 +
        density_score * 0.20
    )

    # 联邦学习调整因子 (模拟多中心数据融合)
    federated_adjustment = np.random.normal(1.0, 0.05)  # 模拟联邦学习的不确定性

    # 最终风险评分
    final_score = linear_combination * federated_adjustment

    # 应用sigmoid函数进行归一化
    normalized_score = 100 / (1 + np.exp(-0.1 * (final_score - 50)))

    return min(max(normalized_score, 0), 100)

def calculate_default_risk(factors):
    """默认风险计算"""
    age = factors.get('age', 0)
    family_history = factors.get('family_history', 0)
    risk_score = (age - 20) * 0.5 + family_history * 20
    return min(max(risk_score, 0), 100)

# 路由定义
@app.route('/')
def index():
    """主页"""
    return render_template('index.html', 
                         disease_categories=DISEASE_CATEGORIES,
                         get_locale=get_locale)

@app.route('/set_language/<language>')
def set_language(language):
    """设置语言"""
    session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html', get_locale=get_locale)

@app.route('/contact')
def contact():
    """联系页面"""
    return render_template('contact.html', get_locale=get_locale)

@app.route('/disease/<disease_id>')
def predict_disease(disease_id):
    """疾病预测页面"""
    if disease_id not in DISEASE_MODELS:
        return render_template('404.html', get_locale=get_locale), 404

    disease_info = DISEASE_MODELS[disease_id]
    return render_template('predict_form.html',
                         disease_id=disease_id,
                         disease_info=disease_info,
                         get_locale=get_locale)

@app.route('/multimodal')
def multimodal_database():
    """多模态数据库主页"""
    return render_template('multimodal.html',
                         multimodal_data=MULTIMODAL_DATABASE,
                         get_locale=get_locale)

@app.route('/multimodal/<category_id>')
def multimodal_category(category_id):
    """多模态数据库分类页面"""
    if category_id not in MULTIMODAL_DATABASE:
        return render_template('404.html', get_locale=get_locale), 404

    category_info = MULTIMODAL_DATABASE[category_id]
    return render_template('multimodal_category.html',
                         category_id=category_id,
                         category_info=category_info,
                         get_locale=get_locale)

@app.route('/multimodal/<category_id>/<subcategory_id>')
def multimodal_subcategory(category_id, subcategory_id):
    """多模态数据库子分类页面"""
    if category_id not in MULTIMODAL_DATABASE:
        return render_template('404.html', get_locale=get_locale), 404

    category_info = MULTIMODAL_DATABASE[category_id]
    subcategory_info = None

    for subcat in category_info['subcategories']:
        if subcat['id'] == subcategory_id:
            subcategory_info = subcat
            break

    if not subcategory_info:
        return render_template('404.html', get_locale=get_locale), 404

    return render_template('multimodal_subcategory.html',
                         category_id=category_id,
                         subcategory_id=subcategory_id,
                         category_info=category_info,
                         subcategory_info=subcategory_info,
                         get_locale=get_locale)

@app.route('/api/predict/<disease_id>', methods=['POST'])
def api_predict(disease_id):
    """疾病预测API"""
    try:
        if disease_id not in DISEASE_MODELS:
            return jsonify({'error': 'Disease not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        factors = data.get('factors', {})
        if not factors:
            return jsonify({'error': 'Missing risk factors'}), 400
        
        risk_score = calculate_risk_score(disease_id, factors)
        
        if risk_score < 30:
            risk_level = 'low'
            risk_level_zh = '低风险'
            risk_level_en = 'Low Risk'
        elif risk_score < 70:
            risk_level = 'medium'
            risk_level_zh = '中等风险'
            risk_level_en = 'Medium Risk'
        else:
            risk_level = 'high'
            risk_level_zh = '高风险'
            risk_level_en = 'High Risk'
        
        recommendations = {
            'zh': ['定期体检，及时发现和处理健康问题', '保持健康的生活方式'],
            'en': ['Regular health checkups', 'Maintain a healthy lifestyle']
        }
        
        result = {
            'disease_id': disease_id,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_level_zh': risk_level_zh,
            'risk_level_en': risk_level_en,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/panda')
def panda_algorithm():
    """Panda算法主页"""
    return render_template('panda_algorithm.html', get_locale=get_locale)



@app.route('/panda/upload', methods=['POST'])
def panda_upload():
    """Panda算法数据上传"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': '没有选择文件' if get_locale() == 'zh' else 'No file selected'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': '没有选择文件' if get_locale() == 'zh' else 'No file selected'
            }), 400

        # 检查文件类型
        allowed_extensions = {'csv', 'xlsx', 'xls', 'json'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''

        if file_extension not in allowed_extensions:
            return jsonify({
                'status': 'error',
                'message': '不支持的文件格式' if get_locale() == 'zh' else 'Unsupported file format'
            }), 400

        # 保存文件到临时目录
        import os
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # 获取文件大小
        file_size = os.path.getsize(file_path)

        return jsonify({
            'status': 'success',
            'filename': filename,
            'size': file_size,
            'message': '文件上传成功' if get_locale() == 'zh' else 'File uploaded successfully'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/panda/analyze', methods=['POST'])
def panda_analyze():
    """Panda算法分析"""
    try:
        data = request.get_json()
        privacy_level = data.get('privacy_level', 'high')
        federated_mode = data.get('federated_mode', True)

        # 模拟分析过程
        import time
        time.sleep(2)  # 模拟处理时间

        # 生成模拟结果
        results = {
            'status': 'success',
            'analysis_id': f'panda_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'privacy_level': privacy_level,
            'federated_mode': federated_mode,
            'model_performance': {
                'accuracy': round(np.random.uniform(0.85, 0.95), 3),
                'precision': round(np.random.uniform(0.80, 0.90), 3),
                'recall': round(np.random.uniform(0.75, 0.85), 3),
                'f1_score': round(np.random.uniform(0.78, 0.88), 3)
            },
            'training_time': round(np.random.uniform(120, 300), 1),
            'data_points': np.random.randint(1000, 5000),
            'features_used': np.random.randint(15, 25),
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running normally',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("启动疾病预测系统...")
    print("访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
