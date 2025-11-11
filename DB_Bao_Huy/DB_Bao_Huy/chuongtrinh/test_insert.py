from common.insertdanhmuc import insert_danhmuc

while True:
    ten = input("Nhập vào tên danh mục: ").strip()
    mota = input("Nhập vào mô tả: ").strip() or None

    insert_danhmuc(ten, mota)   # hàm của bạn tự tạo slug từ tên

    con = input("Tiếp tục (y), thoát (phím bất kỳ): ").strip().lower()
    if con != "y":
        break
