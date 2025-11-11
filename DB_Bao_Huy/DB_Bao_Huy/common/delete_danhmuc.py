from ketnoidb.ketnoi_mysql import connect_mysql
from mysql.connector import Error

def delete_danhmuc(id_danhmuc: int):
    """
    Hàm xóa danh mục theo ID.
    """
    conn = connect_mysql()
    if conn is None:
        print("❌ Không thể kết nối MySQL.")
        return False

    try:
        cursor = conn.cursor()
        sql = "DELETE FROM danhmuc WHERE id = %s"
        cursor.execute(sql, (id_danhmuc,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã xóa danh mục ID = {id_danhmuc} thành công!")
            return True
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {id_danhmuc}.")
            return False

    except Error as e:
        print("❌ Lỗi khi xóa danh mục:", e)
        return False

    finally:
        cursor.close()
        conn.close()
