from ketnoidb.ketnoi_mysql import connect_mysql
from mysql.connector import Error

def update_danhmuc(id_danhmuc: int, ten_moi: str = None, mo_ta_moi: str = None, hien_thi: int | None = None):
    """
    Hàm cập nhật danh mục theo ID.
    Các tham số nào không truyền vào (None) thì sẽ giữ nguyên.
    """

    conn = connect_mysql()
    if conn is None:
        print("❌ Không thể kết nối MySQL.")
        return False

    try:
        cursor = conn.cursor()

        # Tạo danh sách cập nhật động (chỉ cập nhật trường được truyền vào)
        fields = []
        values = []

        if ten_moi is not None:
            fields.append("ten = %s")
            values.append(ten_moi)
        if mo_ta_moi is not None:
            fields.append("mo_ta = %s")
            values.append(mo_ta_moi)
        if hien_thi is not None:
            fields.append("hien_thi = %s")
            values.append(hien_thi)

        if not fields:
            print("⚠️ Không có dữ liệu nào để cập nhật!")
            return False

        # Ghép câu lệnh SQL
        sql = f"UPDATE danhmuc SET {', '.join(fields)} WHERE id = %s"
        values.append(id_danhmuc)

        cursor.execute(sql, tuple(values))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã cập nhật danh mục ID = {id_danhmuc} thành công!")
            return True
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {id_danhmuc}.")
            return False

    except Error as e:
        print("❌ Lỗi khi cập nhật danh mục:", e)
        return False

    finally:
        cursor.close()
        conn.close()
