from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def insert_danhmuc(ten, slug, mo_ta=None, thu_tu=0, hien_thi=1):
    """
    Hàm thêm mới 1 danh mục vào bảng danhmuc.
    """
    conn = connect_mysql()
    if conn is None:
        print("❌ Không thể kết nối MySQL.")
        return False

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO danhmuc (ten, slug, mo_ta, thu_tu, hien_thi)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (ten, slug, mo_ta, thu_tu, hien_thi)
        cursor.execute(sql, values)
        conn.commit()
        print(f"✅ Đã thêm danh mục '{ten}' thành công! ID mới = {cursor.lastrowid}")
        return True

    except Error as e:
        print("❌ Lỗi khi thêm danh mục:", e)
        return False

    finally:
        cursor.close()
        conn.close()
