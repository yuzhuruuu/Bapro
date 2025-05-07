menu = {
    "Fried Chicken": 12000,
    "Burger King": 25000,
    "French Fries": 15000,
    "Spageti": 30000,
    "Jasmin Tea": 7000,
    "Coca-Cola": 12000,
    "Matcha": 15000,
}

total_bayar = 0  
pesanan = []  


while True:
    nama_menu = input("Masukkan nama menu (atau 'selesai' untuk keluar): ").title()
    if nama_menu.lower() == 'selesai':
        break

    if nama_menu in menu:
        try:
            jumlah = int(input(f"Masukkan jumlah untuk {nama_menu}: "))
            harga_total = menu[nama_menu] * jumlah
            total_bayar += harga_total
            pesanan.append((nama_menu, jumlah, harga_total))
        except ValueError:
            print("Masukkan jumlah dalam angka yang benar.")
    else:
        print("Menu tidak ditemukan. Silakan pilih menu yang tersedia.")

for item in pesanan:
    nama_menu, jumlah, harga = item
    print(f"{nama_menu:<20} {jumlah:<9} {harga:>10,}")

print("================================================")
print("                   YSR STORE")
print("         Jl. Raya Bantarsari No. 122")
print("           Telp. (+62) 876544323457")
print("================================================")
print("         No. Transaksi: 000022446635")
print("================================================")
print(f"{'Menu':<20} {'Jumlah':<9} {'Harga':>10}")
print("------------------------------------------------")

print("------------------------------------------------")
print(f"{'Total Bayar':<29} {total_bayar:>10,}")

while True:
    try:
        pembayaran = int(input("Masukkan jumlah pembayaran: "))
        if pembayaran >= total_bayar:
            kembalian = pembayaran - total_bayar
            print(f"Kembalian: {kembalian:,}")
            break
        else:
            print("Uang yang dibayarkan kurang.")
    except ValueError:
        print("Masukkan jumlah pembayaran dalam angka.")

print("========================")
print("Terima kasih telah berbelanja di YSR STORE!")
