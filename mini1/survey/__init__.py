from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request, redirect, url_for

from .survey import survey_bp

def create_app(): #FLask가 웹 앱 시작할떄 호출하는 자동함수 


    app = Flask(__name__)


    @app.route("/")
    def main():
        return render_template('page_modules/base.html')

    @app.route("/kidney_cancer")
    def kidney_cancer_info():
        return render_template('page_modules/kidney_cancer.html')

    @app.route("/lung_cancer")
    def lung_cancer_info():
        return render_template('page_modules/lung_cancer.html')

    @app.route("/liver_cancer")
    def liver_cancer():
        return render_template('page_modules/liver_cancer.html')
    
    @app.route("/colorectal_cancer")
    def colorectal_cancer():
        return render_template('page_modules/colorectal_cancer.html')

    @app.route("/survey")
    def survey():
        return render_template('page_modules/survey.html')



    @app.route('/survey_result', methods=['POST'])
    def survey_result():

        data = request.form  # 폼 데이터 가져오기
        print(data)  # 또는 데이터 처리 로직 추가
        return render_template('page_modules/survey_result.html')

    return app
