from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
import pymysql

survey_result_bp = Blueprint('survey_result', __name__, url_prefix='/survey_result')

# MySQL 데이터베이스 연결 설정
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_user',
        password='your_password',
        database='cancer_risk_db',
        charset='utf8mb4'
    )

# 나이 점수 계산 (모든 암에 공통)
def calculate_age_score(age):
    try:
        age = int(age)
        if age < 40:
            return 0.25
        elif 40 <= age < 50:
            return 0.5
        elif 50 <= age < 60:
            return 1.0
        elif 60 <= age < 70:
            return 1.5
        else:
            return 2.0
    except:
        return 0.0

# 직업 점수 계산 (위암에만 적용)
def calculate_occupation_score(occupation):
    occupation_risk_map = {
        '무직': 0.5,
        '기타': 0.25,
        '주부': 0.5,
        '자유업': 0.25,
        '회사원': 0.25,
        '전문직': 0.1,
        '교사': 0.1,
        '학생': 0.1,
        '군인': 0.1
    }
    return occupation_risk_map.get(occupation, 0.1)

# 신장암 직업 점수 계산
def calculate_kidney_cancer_occupation_score(occupation):
    occupation_risk_map = {
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
    return occupation_risk_map.get(occupation, 0.25)

# 대장암 직업 점수 계산
def calculate_colorectal_cancer_occupation_score(occupation):
    occupation_risk_map = {
        '무직': 0.5,
        '기타': 0.5,
        '주부': 0.25,
        '자유업': 0.25,
        '회사원': 0.25,
        '전문직': 0.1,
        '교사': 0.1,
        '학생': 0.1,
        '군인': 0.1,
    }
    return occupation_risk_map.get(occupation, 0.1)

# 폐암 직업 점수 계산
def calculate_lung_cancer_occupation_score(occupation):
    occupation_risk_map = {
        '무직': 0.5,
        '기타': 0.5,
        '주부': 0.25,
        '자유업': 0.25,
        '회사원': 0.25,
        '전문직': 0.1,
        '교사': 0.1,
        '학생': 0.1,
        '군인': 0.1,
    }
    return occupation_risk_map.get(occupation, 0.1)

# 위험도 계산 함수들
def calculate_stomach_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                   diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += calculate_age_score(age)
    score += calculate_occupation_score(occupation)
    if smoking_now == 'yes':
        score += min(smoking_amount / 30.0, 1.0) * 0.5
    if smoking_past == 'yes':
        score += 0.75
    if alcohol == 'yes':
        score += min(drinking_amount / 3.0, 1.0)
    if diabetes == 'yes': score += 0.25
    if hypertension == 'yes': score += 1
    if heart_disease == 'yes': score += 0.75
    if cancer_history == 'yes': score += 0.25
    return min(score, 7.0)

def calculate_lung_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += calculate_age_score(age)
    if smoking_now == 'yes':
        score += min(smoking_amount / 30.0, 1.0) * 0.5
    if smoking_past == 'yes':
        score += 1.0
    if alcohol == 'yes':
        score += min(drinking_amount / 3.0, 1.0) * 1.0
    if diabetes == 'yes': score += 0.25
    if hypertension == 'yes': score += 1.0
    if heart_disease == 'yes': score += 0.25
    if cancer_history == 'yes': score += 0.5
    score += calculate_lung_cancer_occupation_score(occupation)
    return min(score, 7.0)

def calculate_colorectal_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                      diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += calculate_age_score(age)
    if smoking_now == 'yes':
        score += min(smoking_amount / 30.0, 1.0) * 0.5
    if smoking_past == 'yes':
        score += 1.0
    if alcohol == 'yes':
        score += min(drinking_amount / 3.0, 1.0) * 1.0
    if diabetes == 'yes': score += 0.25
    if hypertension == 'yes': score += 1.0
    if heart_disease == 'yes': score += 0.25
    if cancer_history == 'yes': score += 0.5
    score += calculate_colorectal_cancer_occupation_score(occupation)
    return min(score, 7.0)

def calculate_kidney_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                  diabetes, hypertension, heart_disease, cancer_history, age, occupation):
    score = 0.0
    score += calculate_age_score(age)
    if smoking_now == 'yes':
        score += min(smoking_amount / 30.0, 1.0) * 0.5
    if smoking_past == 'yes':
        score += 0.75
    if alcohol == 'yes':
        score += min(drinking_amount / 3.0, 1.0)
    if diabetes == 'yes': score += 0.5
    if hypertension == 'yes': score += 1
    if heart_disease == 'yes': score += 0.25
    if cancer_history == 'yes': score += 0.25
    score += calculate_kidney_cancer_occupation_score(occupation)
    return min(score, 7.0)

# 그래프 생성 함수
def create_risk_graph(stomach, lung, kidney, colorectal):
    diseases = ['위암', '폐암', '신장암', '대장암']
    scores = [stomach, lung, kidney, colorectal]
    colors = ['red', 'orange', 'blue', 'green']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(diseases, scores, color=colors)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.1f}점', ha='center', va='bottom')

    img_path = os.path.join('static', 'images', 'risk_graph.png')
    plt.ylim(0, 5)
    plt.ylabel('위험 점수 (4.5점 만점)')
    plt.title('암 위험도 점수')
    plt.savefig(img_path)
    plt.close()

# 설문 결과 처리 라우트
@survey_result_bp.route('/', methods=["GET", "POST"])
def survey_result_page():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        diabetes = request.form['diabetes']
        alcohol = request.form['alcohol']
        cancer_history = request.form.get('cancer')
        smoking_now = request.form['smoking_now']
        smoking_past = request.form['smoking_past']
        heart_disease = request.form['heart_disease']
        hypertension = request.form['hypertension']
        smoking_amount = float(request.form['smoking_amount'])
        drinking_amount = float(request.form['drinking_amount'])
        occupation = request.form['occupation']

        # 점수 계산
        stomach_score = calculate_stomach_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                                       diabetes, hypertension, heart_disease, cancer_history, age, occupation)
        lung_score = calculate_lung_cancer_score(smoking_now, smoking_past, smoking_amount, heart_disease, age, occupation)
        colorectal_score = calculate_colorectal_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                                             diabetes, hypertension, heart_disease, cancer_history, age, occupation)
        kidney_score = calculate_kidney_cancer_score(alcohol, smoking_now, smoking_past, smoking_amount, drinking_amount,
                                                     diabetes, hypertension, heart_disease, cancer_history, age, occupation)

        # MySQL에 저장
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(""" 
            INSERT INTO survey_results (
                name, age, diabetes, alcohol, cancer_history,
                smoking_now, smoking_past, hypertension, heart_disease,
                smoking_amount, drinking_amount, occupation,
                stomach_risk, lung_risk, colorectal_risk, kidney_risk
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name, age, diabetes, alcohol, cancer_history,
            smoking_now, smoking_past, hypertension, heart_disease,
            smoking_amount, drinking_amount, occupation,
            stomach_score, lung_score, colorectal_score, kidney_score
        ))
        connection.commit()
        cursor.close()
        connection.close()

        # 그래프 생성
        create_risk_graph(stomach_score, lung_score, kidney_score, colorectal_score)

    return render_template('survey/survey_form.html')

