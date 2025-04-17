from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

survey_result_bp = Blueprint('survey_result', __name__)

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

def calculate_cancer_risk(age, alcohol, smoking_now, smoking_past,
                          hypertension, diabetes, heart_disease, occupation):
    risk_score = 0

    # 각 위험 요소에 따라 점수를 더합니다.
    if smoking_now == 'yes':
        risk_score += 2
    if smoking_past == 'yes':
        risk_score += 1
    if alcohol == 'yes':
        risk_score += 1
    if hypertension == 'yes':
        risk_score += 0.5
    if diabetes == 'yes':
        risk_score += 0.5
    if heart_disease == 'yes':
        risk_score += 0.5

    # 직업에 따른 점수 추가
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

    # 나이에 따른 점수 추가
    if 0 <= age <= 20:
        risk_score += 0.25
    elif 20 < age <= 30:
        risk_score += 0.25
    elif 30 < age <= 40:
        risk_score += 0.25
    elif 40 < age <= 50:
        risk_score += 0.5
    elif 50 < age <= 60:
        risk_score += 1.0
    elif 60 < age <= 70:
        risk_score += 1.0
    else:
        risk_score += 1.0

    risk_percent = (risk_score / 7.0) * 100
    return risk_percent



@survey_result_bp.route('/survey_result', methods=['GET', 'POST'])
def survey_result():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = int(request.form.get('age'))  
        occupation = request.form.get('occupation')
        diabetes = request.form.get('diabetes')
        alcohol = request.form.get('alcohol')
        cancer = request.form.get('cancer')
        smoking_now = request.form.get('smoking_now')
        smoking_past = request.form.get('smoking_past')
        hypertension = request.form.get('hypertension')
        heart_disease = request.form.get('heart_disease')


        risk_score = calculate_cancer_risk(age, alcohol, smoking_now, smoking_past,
                                           hypertension, diabetes, heart_disease, occupation)
        risk_percent = int(risk_score) 


        conn = connect_to_mysql()
        if conn:
            try:
                with conn.cursor() as cursor:
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
                conn.rollback()
            finally:
                conn.close()
        else:
            print("Failed to connect to MySQL.")

        return render_template('survey_result/survey_result.html', 
                               name=name, gender=gender, age=age,
                               occupation=occupation, diabetes=diabetes, alcohol=alcohol,
                               cancer=cancer, smoking_now=smoking_now, smoking_past=smoking_past,
                               hypertension=hypertension, heart_disease=heart_disease, 
                               kidney_risk=risk_percent, kidney_score=risk_score)

    return render_template("survey_result/survey_result.html")