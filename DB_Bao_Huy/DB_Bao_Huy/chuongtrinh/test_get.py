from common.get_danhmuc import get_all_danhmuc

while True:
    get_all_danhmuc()

    tiep = input("\nBạn có muốn xem lại danh sách (y/n)? ").strip().lower()
    if tiep != "y":
        print("👋 Kết thúc xem danh mục.")
        break
