import pymysql
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 해시 처리

def insert_member(email, passwd, username):

    if passwd is None or passwd == "":
        raise ValueError("Password cannot be None or empty")

    try:
        conn = pymysql.connect(
            host="localhost",
            user="humanda5",
            password="humanda5",
            database="mini1"
        )
        cursor = conn.cursor()

        # 비밀번호 해시 처리
        hashed_password = generate_password_hash(passwd)
        
        sql = "INSERT INTO member (email, passwd, username) VALUES (%s, %s, %s)"
        cursor.execute(sql, (email, hashed_password, username))
        conn.commit()

    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:  # cursor가 None이 아니면 닫기
            cursor.close()
        if conn:  # conn이 None이 아니면 닫기
            conn.close()


def select_member_by_email(email):
    row = None
    cursor = None  # cursor를 미리 정의하여 finally에서 참조 가능하도록 설정
    conn = None  # conn도 미리 정의

    try:
        conn = pymysql.connect(
            host="localhost",
            database='mini1',
            user='humanda5',
            password='humanda5'
        )
        cursor = conn.cursor()

        sql = """SELECT email, passwd, username 
                 FROM member
                 WHERE email = %s"""
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
    except Exception as e:
        print('데이터 조회 실패', e)
    finally:
        if cursor:  # cursor가 None이 아니면 닫기
            cursor.close()
        if conn:  # conn이 None이 아니면 닫기
            conn.close()

    return row
