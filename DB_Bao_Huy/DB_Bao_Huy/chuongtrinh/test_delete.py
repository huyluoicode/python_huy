from common.delete_danhmuc import delete_danhmuc

try:
    id_xoa = int(input("Nhập ID danh mục cần xóa: "))
    delete_danhmuc(id_xoa)
except ValueError:
    print("⚠️ ID phải là số nguyên!")
