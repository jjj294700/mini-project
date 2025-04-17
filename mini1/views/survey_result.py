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
                                           smoking_past, hypertension, diabetes, heart_disease, occupation)
        risk_percent = int(risk_score * 100)

     #   create_risk_graph(risk_percent)


        return render_template('survey_result/survey_result.html', 
                            name=name, gender=gender, age=age,
                            occupation=occupation, diabetes=diabetes, alcohol=alcohol,
                            cancer=cancer, smoking_now=smoking_now, smoking_past=smoking_past,
                            hypertension=hypertension, heart_disease=heart_disease, kidney_risk=risk_percent)
    
    return render_template("survey_result/survey_result.html")



#위험도 계산
def calculate_cancer_risk(gender, age, alcohol, smoking_now, smoking_past,
                          hypertension, diabetes, heart_disease, occupation):
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

    occupation_risk = {
        '무직': 0.5,
        '회사원': 0.5,
        '기타': 0.5,
        '자유업': 0.5,
        '주부': 0.5,
        '전문직': 0.25,
        '교사': 0.25,
        '학생': 0.25,
        '군인': 0.25
    }
    if occupation in occupation_risk:
        risk_score += occupation_risk[occupation]
    else:
        risk_score += 0.5 
    return min(risk_score, 1.0)


