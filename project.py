import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

class AplikasiKasir:
    def __init__(self, root):
        self.root = root
        self.root.title("Bowl&Bite - Restaurant")
        self.root.geometry("1200x700")
        
        # Tambahkan inisialisasi kategori_aktif
        self.kategori_aktif = "Semua"
        
        # Konfigurasi warna (menggunakan hijau tua)
        self.colors = {
            "primary": "#1B4D3E",    # Hijau tua untuk header
            "secondary": "#2D6A4F", # Hijau tua lebih muda untuk tombol
            "bg_light": "#F0F7F4",  # Putih keabu-abuan untuk background
            "text_dark": "#2F2F2F",  # Hitam untuk teks
            "success": "#3F826D",    # Hijau untuk total
            "card_bg": "#FFFFFF"     # Putih untuk card menu
        }
        
        # Mengatur warna background utama
        self.root.configure(bg=self.colors["bg_light"])
        
        # Data menu dengan gambar dan opsi
        self.menu = {
            "Makanan": {
                "Mie Level": {"harga": 15000, "gambar": "mie_goreng.png", "opsi": {"level": ["1", "2", "3", "4", "5"]}},
                "Chicken Ricebowl": {"harga": 25000, "gambar": "ricebowl.png", "opsi": {"saus": ["BBQ", "Sambal Matah", "Blackpepper"]}}
            },
            "Minuman": {
                "Teh": {"harga": 5000, "gambar": "es_teh.png", "opsi": {"tipe": ["Es", "Hangat"]}},
                "Jeruk": {"harga": 6000, "gambar": "es_jeruk.png", "opsi": {"tipe": ["Es", "Hangat"]}},
                "Lemon Tea": {"harga": 8000, "gambar": "lemon_tea.png"},
                "Leci Tea": {"harga": 8000, "gambar": "leci_tea.png"},
                "Air Mineral": {"harga": 3000, "gambar": "air_mineral.png"}
            },
            "Cemilan": {
                "Siomay": {"harga": 15000, "gambar": "siomay.png"},
                "Udang Keju": {"harga": 20000, "gambar": "udang_keju.png"},
                "Sushi": {"harga": 25000, "gambar": "sushi.png"},
                "Pangsit Goreng": {"harga": 12000, "gambar": "pangsit.png"}
            }
        }

        # Variabel untuk menyimpan pesanan
        self.pesanan = {}
        self.setup_styles()
        self.buat_gui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style untuk frame kategori
        style.configure("Category.TFrame", background=self.colors["bg_light"])
        
        # Style untuk tombol kategori
        style.configure("Category.TButton",
                      font=("Helvetica", 10),
                      background=self.colors["primary"],
                      foreground="white")
        
        # Style untuk card menu
        style.configure("MenuCard.TFrame",
                      background=self.colors["card_bg"],
                      relief="flat",
                      padding=5)
        
        # Style untuk label menu
        style.configure("Menu.TLabel",
                      font=("Helvetica", 12),
                      background=self.colors["card_bg"])
        
        # Style untuk label harga
        style.configure("Price.TLabel",
                      font=("Helvetica", 12, "bold"),
                      foreground=self.colors["primary"],
                      background=self.colors["card_bg"])

        # Style untuk tombol tambah
        style.configure("Custom.TButton",
                      padding=5,
                      font=("Helvetica", 10))

    def tampilkan_menu(self):
        # Membersihkan frame menu
        for widget in self.menu_grid.winfo_children():
            widget.destroy()

        # Menampilkan menu dalam grid 3x2
        row = 0
        col = 0
        
        for kategori, items in self.menu.items():
            if self.kategori_aktif != "Semua" and kategori != self.kategori_aktif:
                continue
                
            for nama, detail in items.items():
                # Frame untuk setiap menu
                card = ttk.Frame(self.menu_grid, style="MenuCard.TFrame")
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Coba load gambar
                try:
                    img = Image.open(f"Image/{detail['gambar']}")
                    img = img.resize((180, 180), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    label = ttk.Label(card, image=photo, background=self.colors["card_bg"])
                    label.image = photo
                    label.pack(pady=(5,2))
                except:
                    canvas = tk.Canvas(card, width=180, height=180, bg="gray")
                    canvas.create_text(90, 90, text=nama, fill="white")
                    canvas.pack(pady=(5,2))

                # Nama menu
                ttk.Label(card, text=nama, 
                         style="Menu.TLabel").pack(pady=2)

                # Harga
                ttk.Label(card, text=f"Rp {detail['harga']:,}", 
                         style="Price.TLabel").pack(pady=2)

                # Opsi tambahan jika ada
                if "opsi" in detail:
                    for opsi_nama, opsi_values in detail["opsi"].items():
                        frame = ttk.Frame(card, style="MenuCard.TFrame")
                        frame.pack(pady=2)
                        ttk.Label(frame, text=f"{opsi_nama}: ", 
                                 style="Menu.TLabel").pack(side="left")
                        combo = ttk.Combobox(frame, values=opsi_values, width=10)
                        combo.set(opsi_values[0])
                        combo.pack(side="left")

                # Tombol tambah
                ttk.Button(card, text="+ Tambah", 
                          command=lambda n=nama, k=kategori: self.tambah_ke_pesanan(n, k),
                          style="Custom.TButton").pack(pady=5)

                # Update grid
                col += 1
                if col > 2:
                    col = 0
                    row += 1

    def filter_menu(self, kategori):
        self.kategori_aktif = kategori
        for widget in self.menu_grid.winfo_children():
            widget.destroy()
        self.tampilkan_menu()

    def tambah_ke_pesanan(self, nama_menu, kategori):
        detail = self.menu[kategori][nama_menu]
        harga = detail["harga"]
        
        # Dapatkan opsi yang dipilih
        opsi_str = ""
        opsi_dict = {}
        if "opsi" in detail:
            for widget in self.menu_grid.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame) and nama_menu in [label["text"] for label in child.winfo_children() if isinstance(label, ttk.Label)]:
                        for frame in child.winfo_children():
                            if isinstance(frame, ttk.Frame):
                                for combo in frame.winfo_children():
                                    if isinstance(combo, ttk.Combobox):
                                        opsi_name = frame.winfo_children()[0]["text"].strip(":")
                                        opsi_value = combo.get()
                                        opsi_dict[opsi_name] = opsi_value

            # Buat string opsi terurut
            opsi_items = []
            for key in sorted(opsi_dict.keys()):
                opsi_items.append(f"{key}: {opsi_dict[key]}")
            opsi_str = ", ".join(opsi_items)

        # Buat kunci unik untuk pesanan dengan opsi
        pesanan_key = f"{nama_menu} ({opsi_str})" if opsi_str else nama_menu

        # Update pesanan
        if pesanan_key in self.pesanan:
            self.pesanan[pesanan_key]["jumlah"] += 1
        else:
            self.pesanan[pesanan_key] = {
                "harga": harga,
                "jumlah": 1,
                "opsi": opsi_str
            }

        # Update tabel
        self.update_tabel_pesanan()
        self.update_total()

    def update_tabel_pesanan(self):
        # Hapus semua item di tabel
        for item in self.tabel_pesanan.get_children():
            self.tabel_pesanan.delete(item)

        # Tambahkan pesanan ke tabel
        for nama, detail in self.pesanan.items():
            total = detail["harga"] * detail["jumlah"]
            self.tabel_pesanan.insert("", "end", 
                                    values=(nama, detail["opsi"], 
                                           detail["jumlah"], f"Rp {total:,}"))

    def update_total(self):
        total = sum(detail["harga"] * detail["jumlah"] 
                   for detail in self.pesanan.values())
        self.total_label.config(text=f"Total: Rp {total:,}")

    def proses_pembayaran(self):
        if not self.pesanan:
            messagebox.showwarning("Peringatan", "Belum ada pesanan yang dibuat!")
            return
            
        total = sum(detail["harga"] * detail["jumlah"] 
                   for detail in self.pesanan.values())
        
        # Generate dan tampilkan struk
        struk = self.generate_struk(total)
        messagebox.showinfo("Struk Pembayaran", struk)
        
        # Reset pesanan
        self.pesanan = {}
        self.update_tabel_pesanan()
        self.update_total()
        messagebox.showinfo("Sukses", "Pembayaran berhasil!")

    def generate_struk(self, total):
        struk = []
        struk.append("===== BOWL&BITE =====")
        struk.append("Jl. Restaurant No. 123")
        struk.append("Telp: (021) 123-4567")
        struk.append("-" * 30)
        struk.append(f"Tanggal: {datetime.now().strftime('%Y-%m-%d')}")
        struk.append(f"Waktu : {datetime.now().strftime('%H:%M:%S')}")
        struk.append("-" * 30)
        struk.append("Detail Pesanan:")
        
        for nama, detail in self.pesanan.items():
            subtotal = detail["harga"] * detail["jumlah"]
            struk.append(f"\n{nama}")
            if detail["opsi"]:
                struk.append(f"({detail['opsi']})")
            struk.append(f"  {detail['jumlah']} x Rp {detail['harga']:,}")
            struk.append(f"  Subtotal: Rp {subtotal:,}")
        
        struk.append("\n" + "-" * 30)
        struk.append(f"Total: Rp {total:,}")
        struk.append("-" * 30)
        struk.append("Terima kasih atas kunjungan Anda!")
        struk.append("Selamat menikmati hidangan kami")
        return "\n".join(struk)

    def buat_gui(self):
        # Frame utama dibagi menjadi dua bagian
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        # Frame kiri untuk menu (70% width)
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(side="left", fill="both", expand=True)
    
        # Frame kategori di atas menu
        kategori_frame = ttk.Frame(menu_frame, style="Category.TFrame")
        kategori_frame.pack(fill="x", pady=(0, 10))
    
        # Tombol-tombol kategori
        kategori = ["Semua", "Makanan", "Minuman", "Cemilan"]
        for kat in kategori:
            ttk.Button(kategori_frame, text=kat,
                      command=lambda k=kat: self.filter_menu(k),
                      style="Category.TButton").pack(side="left", padx=5)
    
        # Canvas dan scrollbar untuk menu
        canvas = tk.Canvas(menu_frame)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        self.menu_grid = ttk.Frame(canvas)
    
        # Konfigurasi scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
    
        # Buat window di dalam canvas untuk menu_grid
        canvas_window = canvas.create_window((0, 0), window=self.menu_grid, anchor="nw")
    
        # Update scroll region saat ukuran frame berubah
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.menu_grid.bind("<Configure>", configure_scroll_region)
    
        # Update lebar window canvas saat canvas diubah ukurannya
        def configure_canvas_window(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", configure_canvas_window)
    
        self.tampilkan_menu()
    
        # Frame kanan untuk pesanan (30% width)
        pesanan_frame = ttk.Frame(main_frame, width=400)
        pesanan_frame.pack(side="right", fill="both", padx=(10, 0))
        pesanan_frame.pack_propagate(False)
    
        # Label Pesanan
        ttk.Label(pesanan_frame, text="Pesanan", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)
    
        # Tabel pesanan
        columns = ("Menu", "Opsi", "Jumlah", "Total")
        self.tabel_pesanan = ttk.Treeview(pesanan_frame, columns=columns, 
                                         show="headings", height=10)
        for col in columns:
            self.tabel_pesanan.heading(col, text=col)
            self.tabel_pesanan.column(col, width=95)
        self.tabel_pesanan.pack(fill="x", padx=5, pady=5)
    
        # Total
        self.total_label = ttk.Label(pesanan_frame, 
                                   text="Total: Rp 0", 
                                   font=("Helvetica", 14, "bold"),
                                   foreground=self.colors["success"])
        self.total_label.pack(pady=10)
    
        # Tombol Proses
        ttk.Button(pesanan_frame, text="Proses Pembayaran", 
                  command=self.proses_pembayaran,
                  style="Custom.TButton").pack(pady=5, fill="x", padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiKasir(root)
    root.mainloop()