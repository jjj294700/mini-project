from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from ..db import memeber_util  # member_util에서 정의한 함수들 사용

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        
        # 이메일 중복 확인
        existing_user = memeber_util.select_member_by_email(email)
        if existing_user:
            flash('이미 사용 중인 이메일입니다.', 'danger')
            return redirect(url_for('auth.register'))
        
        # 회원가입 처리
        memeber_util.insert_member(email, password, username)
        flash('회원가입 성공! 로그인 해주세요.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = memeber_util.select_member_by_email(email)
        
        if user and check_password_hash(user[1], password):  # 비밀번호 확인
            session['user_id'] = user[0]  # 세션에 사용자 ID 저장
            flash('로그인 성공!', 'success')
            return redirect(url_for('main.home'))  # 로그인 후 홈으로 리디렉션
        else:
            flash('이메일 또는 비밀번호가 잘못되었습니다.', 'danger')
    
    return render_template("auth/login.html")