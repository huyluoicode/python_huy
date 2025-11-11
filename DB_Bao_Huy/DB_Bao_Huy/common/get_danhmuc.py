from ketnoidb.ketnoi_mysql import connect_mysql
from mysql.connector import Error

def get_all_danhmuc():
    """
    Hàm lấy toàn bộ danh mục từ bảng danhmuc.
    Trả về danh sách các tuple (id, tên, slug, mô tả, hiển thị).
    """
    conn = connect_mysql()
    if conn is None:
        print("❌ Không thể kết nối MySQL.")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten, slug, mo_ta, hien_thi FROM danhmuc ORDER BY id ASC")
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ Không có danh mục nào trong cơ sở dữ liệu.")
        else:
            print(f"✅ Có {len(rows)} danh mục trong cơ sở dữ liệu:\n")
            for row in rows:
                id, ten, slug, mo_ta, hien_thi = row
                trang_thai = "Hiển thị" if hien_thi == 1 else "Ẩn"
                print(f"ID: {id} | Tên: {ten} | Slug: {slug} | Mô tả: {mo_ta} | {trang_thai}")

        return rows

    except Error as e:
        print("❌ Lỗi khi truy vấn danh mục:", e)
        return []

    finally:
        cursor.close()
        conn.close()
