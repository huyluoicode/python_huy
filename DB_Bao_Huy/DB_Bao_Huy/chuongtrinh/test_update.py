from common.update_danhmuc import update_danhmuc

while True:
    try:
        id_capnhat = int(input("Nhập ID danh mục cần cập nhật: "))
        ten_moi = input("Nhập tên mới (bỏ trống nếu giữ nguyên): ").strip() or None
        mo_ta_moi = input("Nhập mô tả mới (bỏ trống nếu giữ nguyên): ").strip() or None
        hien_thi_input = input("Hiển thị? (1: có, 0: không, Enter để giữ nguyên): ").strip()
        hien_thi = int(hien_thi_input) if hien_thi_input else None

        update_danhmuc(id_capnhat, ten_moi, mo_ta_moi, hien_thi)

    except ValueError:
        print("⚠️ ID hoặc giá trị nhập không hợp lệ!")

    tiep = input("Bạn có muốn tiếp tục cập nhật (y/n)? ").strip().lower()
    if tiep != "y":
        print("👋 Kết thúc chương trình cập nhật danh mục.")
        break
