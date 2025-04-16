from flask import Blueprint, render_template, request
from . import db

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/survey', methods=["GET", "POST"])
def survey_form():
    if request.method == "POST":
        # 폼 데이터 받기
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        occupation = request.form['occupation']
        diabetes = request.form['diabetes']
        alcohol = request.form['alcohol']
        cancer_history = request.form['cancer_history']
        smoking_now = request.form['smoking_now']
        smoking_past = request.form['smoking_past']
        hypertension = request.form['hypertension']
        heart_disease = request.form['heart_disease']
        comments = request.form['comments']

