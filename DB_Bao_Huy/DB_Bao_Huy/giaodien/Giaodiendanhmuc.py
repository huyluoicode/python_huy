# giaodien/danhmuc_app.py (Pretty UI + Effects)
import re
import unicodedata
import tkinter as tk
from tkinter import messagebox

# ==== UI theme ====
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    USING_TTKBOOTSTRAP = True
except Exception:
    # Fallback: vẫn chạy với ttk thường nếu chưa cài ttkbootstrap
    import tkinter.ttk as tb
    USING_TTKBOOTSTRAP = False

from ketnoidb.ketnoi_mysql import connect_mysql  # dùng hàm kết nối có sẵn


# -------------------- Tiện ích --------------------
def slugify(s: str) -> str:
    """Tạo slug không dấu từ tên."""
    s = unicodedata.normalize("NFD", s)
    s = s.encode("ascii", "ignore").decode("utf-8")
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", s).strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s[:180]


# -------------------- Ứng dụng --------------------
class DanhMucApp:
    def __init__(self):
        # Cửa sổ với theme hiện đại
        if USING_TTKBOOTSTRAP:
            self.root = tb.Window(themename="flatly")  # gợi ý: cosmo / minty / flatly / litera
        else:
            self.root = tk.Tk()

        self.root.title("Quản lý Danh mục (Tkinter + MySQL)")
        self.root.geometry("980x600")
        self.root.minsize(900, 560)

        # Biến form
        self.var_id = tk.StringVar()
        self.var_ten = tk.StringVar()
        self.var_mota = tk.StringVar()
        self.var_hienthi = tk.IntVar(value=1)
        self.var_search = tk.StringVar()

        self._build_ui()
        self._style()
        self.load_data()

        self.root.mainloop()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 8}

        # Top bar: tìm kiếm
        topbar = tb.Frame(self.root)
        topbar.pack(fill="x", **pad)
        tb.Label(topbar, text="Tìm tên:").pack(side="left")
        ent_search = tb.Entry(topbar, textvariable=self.var_search, width=32)
        ent_search.pack(side="left", padx=(6, 12))
        ent_search.bind("<KeyRelease>", lambda e: self.load_data())

        # Khung form
        frm_form = tb.Labelframe(self.root, text="Thông tin danh mục")
        frm_form.pack(fill="x", **pad)

        r = 0
        tb.Label(frm_form, text="ID:").grid(row=r, column=0, padx=6, pady=6, sticky="w")
        tb.Entry(frm_form, textvariable=self.var_id, width=10, state="readonly")\
            .grid(row=r, column=1, padx=6, pady=6, sticky="w")

        tb.Label(frm_form, text="Tên danh mục:").grid(row=r, column=2, padx=6, pady=6, sticky="e")
        self.ent_ten = tb.Entry(frm_form, textvariable=self.var_ten, width=42)
        self.ent_ten.grid(row=r, column=3, padx=6, pady=6, sticky="w")

        r += 1
        tb.Label(frm_form, text="Mô tả:").grid(row=r, column=0, padx=6, pady=6, sticky="w")
        self.ent_mota = tb.Entry(frm_form, textvariable=self.var_mota, width=70)
        self.ent_mota.grid(row=r, column=1, columnspan=3, padx=6, pady=6, sticky="we")

        r += 1
        self.chk_hienthi = tb.Checkbutton(frm_form, text="Hiển thị", variable=self.var_hienthi)
        self.chk_hienthi.grid(row=r, column=0, padx=6, pady=6, sticky="w")

        frm_form.columnconfigure(3, weight=1)

        # Nút
        frm_btns = tb.Frame(self.root)
        frm_btns.pack(fill="x", padx=12, pady=(0, 8))
        tb.Button(frm_btns, text="➕ Thêm", command=self.add_item,
                  bootstyle=(SUCCESS if USING_TTKBOOTSTRAP else None)).pack(side="left", padx=6)
        tb.Button(frm_btns, text="✏️ Sửa", command=self.update_item,
                  bootstyle=(WARNING if USING_TTKBOOTSTRAP else None)).pack(side="left", padx=6)
        tb.Button(frm_btns, text="🗑️ Xóa", command=self.delete_item,
                  bootstyle=(DANGER if USING_TTKBOOTSTRAP else None)).pack(side="left", padx=6)
        tb.Button(frm_btns, text="🧹 Xóa form", command=self.clear_form,
                  bootstyle=(SECONDARY if USING_TTKBOOTSTRAP else None)).pack(side="left", padx=6)
        tb.Button(frm_btns, text="🔄 Tải lại", command=self.load_data,
                  bootstyle=(INFO if USING_TTKBOOTSTRAP else None)).pack(side="left", padx=6)

        # Bảng
        frm_table = tb.Frame(self.root)
        frm_table.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        cols = ("id", "ten", "slug", "mo_ta", "hien_thi")
        self.tree = tb.Treeview(frm_table, columns=cols, show="headings", selectmode="browse")
        headers = {
            "id": "ID", "ten": "Tên danh mục", "slug": "Slug", "mo_ta": "Mô tả", "hien_thi": "Hiển thị"
        }
        for c in cols:
            self.tree.heading(c, text=headers[c], command=lambda col=c: self._sort_by(col, False))

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("ten", width=240)
        self.tree.column("slug", width=260)
        self.tree.column("mo_ta", width=300)
        self.tree.column("hien_thi", width=90, anchor="center")

        vsb = tb.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        hsb = tb.Scrollbar(frm_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="we")

        frm_table.rowconfigure(0, weight=1)
        frm_table.columnconfigure(0, weight=1)

        # chọn dòng -> điền form
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        # Thanh trạng thái
        self.status = tb.Label(self.root, text="Sẵn sàng", anchor="w")
        self.status.pack(fill="x", padx=12, pady=(0, 8))

    # ---------- Style ----------
    def _style(self):
        style = tb.Style() if USING_TTKBOOTSTRAP else tb.Style()
        try:
            style.configure(".", font=("Segoe UI", 10))
            style.configure("Treeview", rowheight=28)
        except Exception:
            pass

        # Zebra rows (sọc)
        self.tree.tag_configure("oddrow", background="#f8fafc")   # slate-50
        self.tree.tag_configure("evenrow", background="#eef2f7")  # light slate

    # ---------- DB helpers ----------
    def query(self, sql, params=None, fetch=False):
        conn = connect_mysql()
        if not conn:
            messagebox.showerror("Lỗi", "Không kết nối được MySQL.")
            return None
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return cur.rowcount
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi SQL", str(e))
            return None
        finally:
            conn.close()

    # ---------- Sort ----------
    def _sort_by(self, col, descending):
        data = [(self._coerce_sort(self.tree.set(k, col)), k) for k in self.tree.get_children("")]
        data.sort(reverse=descending)
        for idx, item in enumerate(data):
            self.tree.move(item[1], "", idx)
            # refresh zebra sau sort
            self.tree.item(item[1], tags=("oddrow" if idx % 2 else "evenrow",))
        self.tree.heading(col, command=lambda: self._sort_by(col, not descending))

    @staticmethod
    def _coerce_sort(val):
        v = str(val).replace(",", "")
        return int(v) if v.isdigit() else v

    # ---------- Actions ----------
    def load_data(self):
        key = self.var_search.get().strip()
        like = f"%{key}%"
        rows = self.query(
            "SELECT id, ten, slug, mo_ta, hien_thi FROM danhmuc "
            "WHERE %s = '' OR ten LIKE %s "
            "ORDER BY id ASC",
            (key, like),
            fetch=True,
        )
        if rows is None:
            return
        # clear
        for i in self.tree.get_children():
            self.tree.delete(i)
        # insert (zebra)
        for idx, r in enumerate(rows):
            id_, ten, slug, mo_ta, hien_thi = r
            tag = "oddrow" if idx % 2 else "evenrow"
            self.tree.insert(
                "", "end",
                values=(id_, ten, slug, mo_ta, "Có" if hien_thi else "Không"),
                tags=(tag,)
            )
        self.status.config(text=f"Đang hiển thị {len(rows)} danh mục")

    def clear_form(self):
        self.var_id.set("")
        self.var_ten.set("")
        self.var_mota.set("")
        self.var_hienthi.set(1)
        self.ent_ten.focus()
        self.status.config(text="Đã xóa dữ liệu form")

    def on_select_row(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        id_, ten, slug, mo_ta, hien_thi = self.tree.item(sel[0], "values")
        self.var_id.set(id_)
        self.var_ten.set(ten)
        self.var_mota.set(mo_ta)
        self.var_hienthi.set(1 if hien_thi == "Có" else 0)

    def add_item(self):
        ten = self.var_ten.get().strip()
        if not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Tên danh mục.")
            return
        mo_ta = self.var_mota.get().strip() or None
        hien_thi = int(self.var_hienthi.get())
        slug = slugify(ten)

        rowcount = self.query(
            "INSERT INTO danhmuc (ten, slug, mo_ta, hien_thi) VALUES (%s, %s, %s, %s)",
            (ten, slug, mo_ta, hien_thi),
        )
        if rowcount:
            messagebox.showinfo("Thành công", f"Đã thêm danh mục: {ten}")
            self.clear_form()
            self.load_data()

    def update_item(self):
        if not self.var_id.get():
            messagebox.showwarning("Chưa chọn", "Hãy chọn một dòng để sửa.")
            return
        try:
            id_ = int(self.var_id.get())
        except ValueError:
            messagebox.showwarning("Lỗi", "ID không hợp lệ.")
            return

        ten = self.var_ten.get().strip()
        if not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Tên danh mục.")
            return
        mo_ta = self.var_mota.get().strip() or None
        hien_thi = int(self.var_hienthi.get())
        slug = slugify(ten)

        rowcount = self.query(
            "UPDATE danhmuc SET ten=%s, slug=%s, mo_ta=%s, hien_thi=%s WHERE id=%s",
            (ten, slug, mo_ta, hien_thi, id_),
        )
        if rowcount is not None:
            if rowcount > 0:
                messagebox.showinfo("Thành công", f"Đã cập nhật danh mục ID {id_}.")
                self.load_data()
            else:
                messagebox.showwarning("Không thay đổi", "Không có bản ghi nào được cập nhật.")

    def delete_item(self):
        if not self.var_id.get():
            messagebox.showwarning("Chưa chọn", "Hãy chọn một dòng để xóa.")
            return
        try:
            id_ = int(self.var_id.get())
        except ValueError:
            messagebox.showwarning("Lỗi", "ID không hợp lệ.")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn chắc muốn xóa danh mục ID {id_}?"):
            return

        rowcount = self.query("DELETE FROM danhmuc WHERE id=%s", (id_,))
        if rowcount is not None:
            if rowcount > 0:
                messagebox.showinfo("Thành công", f"Đã xóa danh mục ID {id_}.")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", "ID không tồn tại.")


# -------------------- Chạy app --------------------
if __name__ == "__main__":
    DanhMucApp()
