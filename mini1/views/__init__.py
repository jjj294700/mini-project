from .main_view import main_bp
from .auth_view import auth_bp
from .survey_result import survey_result_bp
from .survey import survey_bp  # survey.py의 블루프린트 임포트

__all__ = ['main_bp', 'auth_bp', 'survey_result_bp', 'survey_bp']