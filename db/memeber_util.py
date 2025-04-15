import pymysql

def insert_member(email, passwd, username):
    try:
        conn = pymysql.connect(
        host="localhost",
        user="humanda5",
        password="human",
        database="mini1"
        )
        cursor = conn.cursor()

        sql = "isert into member (email, passwd, username) values(%s,%s,%s)"
        cursor.execute(sql, (email, passwd, username))
        conn.commit()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()






def select_member_by_email(email):
    row = None
    try:
        conn = pymysql.connect(host="localhost", 
                               database='demoweb', 
                               user='humanda5', 
                               password='humanda5')
        
        cursor = conn.cursor()

        sql = """select email, passwd, username, usertype, regdate 
                 from member
                 where email = %s and deleted = FALSE"""
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
    except Exception as e:
        print('데이터 저장 실패', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return row