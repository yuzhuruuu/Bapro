import tkinter as tk
from tkinter import ttk, messagebox

menu_items = {
    "Nasi Goreng": 15000,
    "Mie Ayam": 12000,
    "Ayam Geprek": 18000,
    "Es Teh": 5000,
    "Es Jeruk": 6000
}

class KasirApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Kasir UMKM")
        self.root.geometry("500x600")
        self.root.configure(bg="#f7f7f7")
        self.entries = {}

        title = tk.Label(root, text="Aplikasi Kasir UMKM", font=("Helvetica", 18, "bold"), bg="#f7f7f7")
        title.pack(pady=15)

        # Frame untuk menu input
        menu_frame = tk.Frame(root, bg="#f7f7f7")
        menu_frame.pack(pady=10)

        for item, price in menu_items.items():
            row = tk.Frame(menu_frame, bg="#f7f7f7")
            row.pack(fill="x", pady=5, padx=20)

            label = tk.Label(row, text=f"{item} (Rp{price})", font=("Helvetica", 12), width=25, anchor="w", bg="#f7f7f7")
            label.pack(side="left")

            qty_entry = ttk.Entry(row, width=5)
            qty_entry.insert(0, "0")
            qty_entry.pack(side="right")
            self.entries[item] = qty_entry

        # Tombol hitung
        calc_button = ttk.Button(root, text="Hitung Total", command=self.hitung_total)
        calc_button.pack(pady=20)

        # Output struk
        self.struk_label = tk.Label(root, text="Struk Pembayaran", font=("Helvetica", 14, "bold"), bg="#f7f7f7")
        self.struk_label.pack()

        self.struk_area = tk.Text(root, height=15, width=50, font=("Courier", 10))
        self.struk_area.pack(pady=10)

    def hitung_total(self):
        total = 0
        struk = "========= STRUK PEMBAYARAN =========\n"
        for item, entry in self.entries.items():
            try:
                qty = int(entry.get())
                if qty > 0:
                    harga = menu_items[item]
                    subtotal = harga * qty
                    total += subtotal
                    struk += f"{item:15} x{qty:<3} = Rp{subtotal:>6}\n" 
            except ValueError:
                messagebox.showerror("Input Error", f"Jumlah {item} harus angka")
                return
        struk += "------------------------------------\n"
        struk += f"TOTAL BAYAR:              Rp{total:>6}\n"
        struk += "===================================="
        self.struk_area.delete(1.0, tk.END)
        self.struk_area.insert(tk.END, struk)

if __name__ == "__main__":
    root = tk.Tk()
    app = KasirApp(root)
    root.mainloop()
