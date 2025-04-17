from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os

survey_bp = Blueprint('survey', __name__)

# 보조 함수: 흡연 점수 계산
def get_smoking_score(smoking_now, smoking_past, smoking_amount, max_smoking_amount=30.0, max_score_now=0.5, past_smoker_score=0.75):
    score = 0.0
    if smoking_now == 'yes':
        ratio = min(smoking_amount / max_smoking_amount, 1.0)
        score += ratio * max_score_now
    if smoking_past == 'yes':
        score += past_smoker_score
    return score

# 보조 함수: 음주 점수 계산
def get_drinking_score(alcohol, drinking_amount, max_drinking_amount=3.0, max_score=1.0):
    if alcohol != 'yes':
        return 0.0
    ratio = min(drinking_amount / max_drinking_amount, 1.0)
    return ratio * max_score

# 보조 함수: 나이 점수 계산
def get_age_score(age):
    age = int(age)
    if age < 40:
        return 0.25
    elif age < 50:
        return 0.5
    elif age < 60:
        return 1.0
    elif age < 70:
        return 1.5
    else:
        return 2.0

# 보조 함수: 직업 점수 계산 (위암에만 적용)
def get_job_score(occupation):
    job_scores = {
        '무직': 0.5,
        '기타': 0.25,
        '주부': 0.5,
        '자유업': 0.25,
        '회사원': 0.25,
        '전문직': 0.1,
        '교사': 0.1,
        '학생': 0.1,
        '군인': 0.1,
    }
    return job_scores.get(occupation, 0.1)

# 신장암에 대한 직업 점수 계산 (신장암 직업 점수 반영)
def get_kidney_cancer_job_score(occupation):
    job_scores = {
        '무직': 0.5,
        '기타': 0.5,
        '주부': 0.5,
        '자유업': 0.5,
        '회사원': 0.5,
        '전문직': 0.25,
        '교사': 0.25,
        '학생': 0.25,
        '군인': 0.25,
    }
    return job_scores.get(occupation, 0.25)

# 암별 점수 계산 함수
def calculate_stomach_cancer_score(gender, alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount, diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += get_smoking_score(smoking_now, smoking_past, smoking_amount)
    score += get_drinking_score(alcohol, drinking_amount)
    if diabetes == 'yes': score += 0.25
    if hypertension == 'yes': score += 0.1
    if heart_disease == 'yes': score += 0.75
    if cancer_history == 'yes': score += 0.25
    score += get_age_score(age)
    score += get_job_score(occupation)
    return min(score, 7.0)

def calculate_kidney_cancer_score(gender, alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount, diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += get_smoking_score(smoking_now, smoking_past, smoking_amount)
    score += get_drinking_score(alcohol, drinking_amount)
    if diabetes == 'yes': score += 0.5
    if hypertension == 'yes': score += 1
    if heart_disease == 'yes': score += 0.25
    if cancer_history == 'yes': score += 0.25
    score += get_age_score(age)
    score += get_kidney_cancer_job_score(occupation)  # 직업에 의한 점수 추가
    return min(score, 7.0)

def calculate_lung_cancer_score(gender, smoking_now, smoking_past, smoking_amount, heart_disease, age):
    score = 0.0
    score += get_smoking_score(smoking_now, smoking_past, smoking_amount)
    if heart_disease == 'yes': score += 0.25
    score += get_age_score(age)
    return min(score, 7.0)

def calculate_colorectal_cancer_score(gender, alcohol, drinking_amount, diabetes, hypertension, cancer_history, age):
    score = 0.0
    score += get_drinking_score(alcohol, drinking_amount)
    if diabetes == 'yes': score += 1.0
    if hypertension == 'yes': score += 1.0
    if cancer_history == 'yes': score += 0.5
    score += get_age_score(age)
    return min(score, 7.0)

# 그래프 생성 함수
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

# 설문 라우트
@survey_bp.route('/survey', methods=["GET", "POST"])
def survey_form():
    if request.method == "POST":
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        occupation = request.form['occupation']
        diabetes = request.form['diabetes']
        alcohol = request.form['alcohol']
        cancer_history = request.form.get('cancer')
        smoking_now = request.form['smoking_now']
        smoking_past = request.form['smoking_past']
        heart_disease = request.form['heart_disease']
        hypertension = request.form['hypertension']
        smoking_amount = float(request.form['smoking_amount'])
        drinking_amount = float(request.form['drinking_amount'])

        # 점수 계산
        stomach_score = calculate_stomach_cancer_score(gender, alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount, diabetes, hypertension, heart_disease, cancer_history, age, occupation)
        kidney_score = calculate_kidney_cancer_score(gender, alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount, diabetes, hypertension, heart_disease, cancer_history, age, occupation)  # 신장암 직업 점수 반영
        lung_score = calculate_lung_cancer_score(gender, smoking_now, smoking_past, smoking_amount, heart_disease, age)
        colorec_score = calculate_colorectal_cancer_score(gender, alcohol, drinking_amount, diabetes, hypertension, cancer_history, age)

        # 그래프 생성
        create_risk_graph(stomach_score, lung_score, kidney_score, colorec_score)

        # 결과 렌더링
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
