from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import numpy as np


import pandas as pd
import os
import matplotlib.pyplot as plt

survey_result_bp = Blueprint('survey_result', __name__)



# MySQL 연결 함수
def connect_to_mysql():
    try:
        conn = pymysql.connect(
            host="127.0.0.1", 
            user="humanda5",  
            password="human", 
            database="mini1",  
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("MySQL connected successfully.")
        return conn
    except Exception as e:
        print("MySQL connection error:", e)
        return None





# 설문 결과 처리 및 데이터베이스 저장
@survey_result_bp.route('/survey_result', methods=['GET', 'POST'])
def survey_result():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        occupation = request.form.get('occupation')
        diabetes = request.form.get('diabetes')
        alcohol = request.form.get('alcohol')
        cancer = request.form.get('cancer')
        smoking_now = request.form.get('smoking_now')
        smoking_past = request.form.get('smoking_past')
        hypertension = request.form.get('hypertension')
        heart_disease = request.form.get('heart_disease')

        # 데이터베이스 연결
        conn = connect_to_mysql()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # 설문 결과를 데이터베이스에 INSERT
                    insert_query = """
                        INSERT INTO survey_result 
                        (name, gender, age, occupation, diabetes, alcohol, cancer, smoking_now, smoking_past, hypertension, heart_disease)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (name, gender, age, occupation, diabetes, alcohol, cancer, smoking_now, smoking_past, hypertension, heart_disease))
                    conn.commit()
                    print("Data inserted successfully.")
            except Exception as e:
                print("Error inserting data:", e)
                conn.rollback()  # 오류 발생 시 롤백
            finally:
                conn.close()
        else:
            print("Failed to connect to MySQL.")

        # 위험도 계산
        risk_score = calculate_cancer_risk(gender, age, alcohol, smoking_now,
                                           smoking_past, hypertension, diabetes, heart_disease)
        risk_percent = int(risk_score * 100)

        return render_template('survey_result/survey_result.html', 
                            name=name, gender=gender, age=age,
                            occupation=occupation, diabetes=diabetes, alcohol=alcohol,
                            cancer=cancer, smoking_now=smoking_now, smoking_past=smoking_past,
                            hypertension=hypertension, heart_disease=heart_disease, kidney_risk=risk_percent)    # GET 요청 처리 (설문 결과를 입력하지 않은 경우)
    return render_template("survey_result.html")


# 위험도 계산 함수
def calculate_cancer_risk(gender, age, alcohol, smoking_now, smoking_past,
                          hypertension, diabetes, heart_disease):
    risk_score = 0.1
    if smoking_now == 'yes':
        risk_score += 0.2
    if smoking_past == 'yes':
        risk_score += 0.1
    if alcohol == 'yes':
        risk_score += 0.1
    if hypertension == 'yes':
        risk_score += 0.05
    if diabetes == 'yes':
        risk_score += 0.05
    if heart_disease == 'yes':
        risk_score += 0.05
    try:
        age = int(age)
        risk_score += min(age, 100) * 0.002
    except:
        pass
    if gender == 'male':
        risk_score += 0.05

    return min(risk_score, 1.0)  # 최대 1.0 (100%) 넘지 않게


# 설문 결과 기반으로 위험도 그래프를 생성하는 함수
def create_risk_graph(risk_data):
    # 그래프 데이터 (위험도를 계산한 결과, 예시)
    diseases = ['간암', '폐암', '신장암', '대장암']
    risk_percentages = [55, 70, risk_data, 90]  # 예시로 위험도 퍼센트를 넣음

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    bars = plt.bar(diseases, risk_percentages, color=['red', 'orange', 'blue', 'green'])

    # 그래프 제목 및 레이블
    plt.title('설문 결과에 따른 위험도')
    plt.xlabel('질병 종류')
    plt.ylabel('위험도 (%)')
    
    # 막대 위에 위험도 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 3, f'{yval}%', ha='center', va='bottom')

    # 이미지 파일로 저장
    img_path = os.path.join('static', 'images', 'risk_graph.png')
    plt.savefig(img_path)
    plt.close()



# 설문 결과 처리 후 위험도 그래프 생성
def survey_result():
    if request.method == 'POST':
        # 설문 결과 입력
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        occupation = request.form.get('occupation')
        diabetes = request.form.get('diabetes')
        alcohol = request.form.get('alcohol')
        cancer = request.form.get('cancer')
        smoking_now = request.form.get('smoking_now')
        smoking_past = request.form.get('smoking_past')
        hypertension = request.form.get('hypertension')
        heart_disease = request.form.get('heart_disease')

        # 데이터베이스에 저장 코드 (생략)

        # 위험도 계산
        risk_score = calculate_cancer_risk(gender, age, alcohol, smoking_now,
                                           smoking_past, hypertension, diabetes, heart_disease)
        risk_percent = int(risk_score * 100)

        # 위험도 그래프 생성
        create_risk_graph(risk_percent)

        return render_template('survey_result/survey_result.html', 
                            name=name, gender=gender, age=age,
                            occupation=occupation, diabetes=diabetes, alcohol=alcohol,
                            cancer=cancer, smoking_now=smoking_now, smoking_past=smoking_past,
                            hypertension=hypertension, heart_disease=heart_disease, kidney_risk=risk_percent)
    return render_template("survey_result.html")