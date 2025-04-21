from flask import Flask
from .views import main_bp, auth_bp, survey_result_bp, survey_bp  # views 폴더 내의 블루프린트들을 한 번에 임포트

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '12345'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(survey_result_bp)
    app.register_blueprint(survey_bp, url_prefix='/survey')  # '/survey' 경로로 블루프린트 등록

    return app