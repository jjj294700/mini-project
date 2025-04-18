from flask import Blueprint, render_template, request
from .survey_result import calculate_stomach_cancer_score, calculate_lung_cancer_score, calculate_kidney_cancer_score, calculate_colorectal_cancer_score
import matplotlib.pyplot as plt
import os

survey_bp = Blueprint('survey', __name__)

# 그래프 생성
def create_risk_graph(stomach, lung, kidney, colorec):
    diseases = ['위암', '폐암', '신장암', '대장암']
    scores = [stomach, lung, kidney, colorec]
    colors = ['red', 'orange', 'blue', 'green']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(diseases, scores, color=colors)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.1f}점', ha='center', va='bottom')

    img_path = os.path.join('static', 'images', 'risk_graph.png')
    plt.ylim(0, 7)
    plt.ylabel('위험 점수 (7점 만점)')
    plt.title('암 위험도 점수')
    plt.savefig(img_path)
    plt.close()

# 설문 처리 라우트
@survey_bp.route('/survey', methods=["GET", "POST"])
def survey_form():
    if request.method == "POST":
        # 설문 데이터 수집
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        occupation = request.form['occupation']
        diabetes = request.form['diabetes']
        alcohol = request.form['alcohol']
        cancer_history = request.form.get('cancer')  # get()을 사용하여 None 처리
        smoking_now = request.form['smoking_now']
        smoking_past = request.form['smoking_past']
        heart_disease = request.form['heart_disease']
        hypertension = request.form['hypertension']

        # smoking_amount와 drinking_amount를 float으로 변환하고, 값이 없을 경우 0으로 설정
        smoking_amount = float(request.form['smoking_amount']) if request.form['smoking_amount'] else 0.0
        drinking_amount = float(request.form['drinking_amount']) if request.form['drinking_amount'] else 0.0

        # 점수 계산
        stomach_score = calculate_stomach_cancer_score(
            alcohol, smoking_now, smoking_past, smoking_amount,
            drinking_amount, diabetes, hypertension, heart_disease,
            cancer_history, age, occupation
        )
        kidney_score = calculate_kidney_cancer_score(
            alcohol, smoking_now, smoking_past, smoking_amount,
            drinking_amount, diabetes, hypertension, heart_disease,
            cancer_history, age, occupation
        )
        lung_score = calculate_lung_cancer_score(
            smoking_now, smoking_past, smoking_amount, heart_disease, age
        )
        colorec_score = calculate_colorectal_cancer_score(
            alcohol, smoking_now, smoking_past, smoking_amount,
            drinking_amount, diabetes, hypertension, heart_disease,
            cancer_history, age, occupation
        )

        # 그래프 생성
        create_risk_graph(stomach_score, lung_score, kidney_score, colorec_score)

        # 결과 페이지 렌더링
        return render_template('survey_result/survey_result.html',
            name=name,
            gender=gender,
            age=age,
            occupation=occupation,
            diabetes=diabetes,
            alcohol=alcohol,
            cancer=cancer_history,
            smoking_now=smoking_now,
            smoking_past=smoking_past,
            heart_disease=heart_disease,
            hypertension=hypertension,
            smoking_amount=smoking_amount,
            drinking_amount=drinking_amount,
            stomach_risk=stomach_score,
            lung_risk=lung_score,
            kidney_risk=kidney_score,
            colorec_risk=colorec_score
        )

    return render_template('survey/survey_form.html')


