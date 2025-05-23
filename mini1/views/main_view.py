from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    user_id = session.get('user_id')
    if user_id:
        # 사용자 정보가 있으면 보여주기 (예: user_id)
        return render_template("page_modules/base.html", user_id=user_id)
    return render_template('page_modules/base.html')

@main_bp.route("/kidney_cancer")
def kidney_cancer_info():
    return render_template('page_modules/kidney_cancer.html')

@main_bp.route("/lung_cancer")
def lung_cancer_info():
    return render_template('page_modules/lung_cancer.html')

@main_bp.route("/stomach_cancer")
def stomach_cancer():
    return render_template('page_modules/stomach_cancer.html')

@main_bp.route("/colorectal_cancer")
def colorectal_cancer():
    return render_template('page_modules/colorectal_cancer.html')

@main_bp.route("/survey")
def survey():
    return render_template('page_modules/survey.html')

@main_bp.route("/login")
def login():
    return render_template('auth/login.html')

@main_bp.route("/register")
def register():

    return render_template('auth/register.html')
