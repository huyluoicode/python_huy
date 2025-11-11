import mysql.connector
from mysql.connector import Error

def connect_mysql():
    """Kết nối tới cơ sở dữ liệu qlythuoccaocap"""
    try:
        conn = mysql.connector.connect(
            host="localhost",      # hoặc 127.0.0.1
            port=3307,             # nếu bạn dùng XAMPP
            user="root",
            password="",           # điền mật khẩu MySQL nếu có
            database="qlythuoccaocap"
        )
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return conn
    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None
