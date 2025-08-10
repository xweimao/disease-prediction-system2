from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_babel import gettext, ngettext

main_bp = Blueprint('main', __name__)

# 疾病分类配置
DISEASE_CATEGORIES = {
    'cancer': {
        'name_zh': '癌症',
        'name_en': 'Cancer',
        'diseases': [
            {'id': 'lung_cancer', 'name_zh': '肺癌', 'name_en': 'Lung Cancer'},
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

@main_bp.route('/')
def index():
    """主页"""
    return render_template('index.html', disease_categories=DISEASE_CATEGORIES)

@main_bp.route('/set_language/<language>')
def set_language(language):
    """设置语言"""
    session['language'] = language
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """联系页面"""
    return render_template('contact.html')

@main_bp.route('/disease/<disease_id>')
def disease_info(disease_id):
    """疾病信息页面"""
    # 查找疾病信息
    disease_info = None
    category_info = None
    
    for category_id, category in DISEASE_CATEGORIES.items():
        for disease in category['diseases']:
            if disease['id'] == disease_id:
                disease_info = disease
                category_info = category
                break
        if disease_info:
            break
    
    if not disease_info:
        return render_template('404.html'), 404
    
    return render_template('disease_info.html', 
                         disease=disease_info, 
                         category=category_info,
                         disease_id=disease_id)
