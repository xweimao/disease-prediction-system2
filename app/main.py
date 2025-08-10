import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, get_locale
from routes.predict import predict_bp
from routes.main_routes import main_bp

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='static')

    # 配置
    app.config['SECRET_KEY'] = 'disease_prediction_secret_key_2024'
    app.config['LANGUAGES'] = {
        'en': 'English',
        'zh': '中文'
    }
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

    # 初始化Babel
    babel = Babel()
    babel.init_app(app)

    def get_locale():
        # 1. 如果URL中有语言参数，使用它
        if request.args.get('lang'):
            session['language'] = request.args.get('lang')
        # 2. 如果session中有语言设置，使用它
        if 'language' in session:
            return session['language']
        # 3. 否则使用浏览器语言偏好
        return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'zh'

    babel.localeselector(get_locale)

    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
