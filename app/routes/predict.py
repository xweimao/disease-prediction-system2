from flask import Blueprint, request, jsonify, render_template, session
from flask_babel import gettext as _
import numpy as np
import os
import json
from datetime import datetime

predict_bp = Blueprint('predict', __name__)

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
    }
    # 可以继续添加其他疾病模型...
}

def calculate_risk_score(disease_id, factors):
    """计算疾病风险评分"""
    # 这里使用简化的风险计算模型
    # 在实际应用中，这里应该调用训练好的机器学习模型

    if disease_id == 'lung_cancer':
        return calculate_lung_cancer_risk(factors)
    elif disease_id == 'diabetes':
        return calculate_diabetes_risk(factors)
    else:
        # 默认风险计算
        return calculate_default_risk(factors)

def calculate_lung_cancer_risk(factors):
    """肺癌风险计算"""
    risk_score = 0

    # 年龄因子
    age = factors.get('age', 0)
    if age > 60:
        risk_score += 30
    elif age > 45:
        risk_score += 20
    elif age > 30:
        risk_score += 10

    # 吸烟因子
    smoking_years = factors.get('smoking_years', 0)
    smoking_amount = factors.get('smoking_amount', 0)
    smoking_index = smoking_years * smoking_amount / 20  # 包年

    if smoking_index > 30:
        risk_score += 40
    elif smoking_index > 20:
        risk_score += 30
    elif smoking_index > 10:
        risk_score += 20
    elif smoking_index > 0:
        risk_score += 10

    # 家族史
    if factors.get('family_history', 0) == 1:
        risk_score += 15

    # 职业暴露
    if factors.get('occupational_exposure', 0) == 1:
        risk_score += 10

    # 性别因子
    if factors.get('gender', 0) == 1:  # 男性
        risk_score += 5

    return min(risk_score, 100)  # 最大100分

def calculate_diabetes_risk(factors):
    """糖尿病风险计算"""
    risk_score = 0

    # 年龄因子
    age = factors.get('age', 0)
    if age > 65:
        risk_score += 25
    elif age > 45:
        risk_score += 15
    elif age > 35:
        risk_score += 10

    # BMI因子
    bmi = factors.get('bmi', 0)
    if bmi > 30:
        risk_score += 25
    elif bmi > 25:
        risk_score += 15
    elif bmi > 23:
        risk_score += 10

    # 腰围因子
    waist = factors.get('waist_circumference', 0)
    if waist > 90:  # 简化处理，实际应该区分性别
        risk_score += 15
    elif waist > 85:
        risk_score += 10

    # 血压因子
    sbp = factors.get('systolic_bp', 0)
    if sbp > 140:
        risk_score += 15
    elif sbp > 130:
        risk_score += 10

    # 家族史
    if factors.get('family_history', 0) == 1:
        risk_score += 20

    # 体力活动
    activity = factors.get('physical_activity', 1)
    if activity == 0:  # 低
        risk_score += 10
    elif activity == 2:  # 高
        risk_score -= 5

    return min(max(risk_score, 0), 100)  # 0-100分

def calculate_default_risk(factors):
    """默认风险计算（用于其他疾病）"""
    # 简化的通用风险计算
    age = factors.get('age', 0)
    family_history = factors.get('family_history', 0)

    risk_score = (age - 20) * 0.5 + family_history * 20
    return min(max(risk_score, 0), 100)

@predict_bp.route('/disease/<disease_id>')
def predict_disease(disease_id):
    """疾病预测页面"""
    if disease_id not in DISEASE_MODELS:
        return render_template('404.html'), 404

    disease_info = DISEASE_MODELS[disease_id]
    return render_template('predict_form.html',
                         disease_id=disease_id,
                         disease_info=disease_info)

@predict_bp.route('/api/predict/<disease_id>', methods=['POST'])
def api_predict(disease_id):
    """疾病预测API"""
    try:
        if disease_id not in DISEASE_MODELS:
            return jsonify({'error': _('Disease not found')}), 404

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'error': _('Invalid request data')}), 400

        factors = data.get('factors', {})
        if not factors:
            return jsonify({'error': _('Missing risk factors')}), 400

        # 计算风险评分
        risk_score = calculate_risk_score(disease_id, factors)

        # 确定风险等级
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

        # 生成建议
        recommendations = generate_recommendations(disease_id, risk_level, factors)

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
        return jsonify({'error': f'{_("Prediction failed")}: {str(e)}'}), 500

def generate_recommendations(disease_id, risk_level, factors):
    """生成健康建议"""
    recommendations = {
        'zh': [],
        'en': []
    }

    if disease_id == 'lung_cancer':
        if factors.get('smoking_years', 0) > 0:
            recommendations['zh'].append('强烈建议戒烟，这是降低肺癌风险最重要的措施')
            recommendations['en'].append('Strongly recommend quitting smoking, which is the most important measure to reduce lung cancer risk')

        if risk_level == 'high':
            recommendations['zh'].append('建议每年进行胸部CT筛查')
            recommendations['en'].append('Recommend annual chest CT screening')

        recommendations['zh'].append('避免二手烟和空气污染')
        recommendations['en'].append('Avoid secondhand smoke and air pollution')

    elif disease_id == 'diabetes':
        if factors.get('bmi', 0) > 25:
            recommendations['zh'].append('建议控制体重，保持健康的BMI')
            recommendations['en'].append('Recommend weight control and maintaining healthy BMI')

        if factors.get('physical_activity', 1) == 0:
            recommendations['zh'].append('增加体力活动，每周至少150分钟中等强度运动')
            recommendations['en'].append('Increase physical activity, at least 150 minutes of moderate exercise per week')

        recommendations['zh'].append('保持健康饮食，限制糖分和精制碳水化合物摄入')
        recommendations['en'].append('Maintain a healthy diet, limit sugar and refined carbohydrate intake')

    # 通用建议
    recommendations['zh'].append('定期体检，及时发现和处理健康问题')
    recommendations['en'].append('Regular health checkups to detect and address health issues early')

    if risk_level == 'high':
        recommendations['zh'].append('建议咨询专科医生，制定个性化的预防方案')
        recommendations['en'].append('Recommend consulting specialists for personalized prevention plans')

    return recommendations

@predict_bp.route('/api/diseases')
def api_diseases():
    """获取所有疾病列表API"""
    return jsonify({
        'diseases': DISEASE_MODELS,
        'status': 'success'
    })

@predict_bp.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': _('Service is running normally'),
        'timestamp': datetime.now().isoformat()
    })
