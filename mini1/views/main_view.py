from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
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
