from flask import Flask
from .views.main_view import main_bp 
from .views.auth_view import auth_bp 
from .views.survey_result import survey_result_bp


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '12345'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(survey_result_bp)

    return app