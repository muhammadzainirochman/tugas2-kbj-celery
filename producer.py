from tasks import proses_pembayaran, kirim_notifikasi, broadcast_promo

if __name__ == "__main__":
    print("=== SISTEM TOKO ONLINE DIMULAI ===\n")
    
    print("[1] Pelanggan checkout (Testing TOPIC)...")
    task_1 = proses_pembayaran.delay("ORDER-001", 150000)
    
    print("[2] Status berubah (Testing WILDCARD)...")
    task_2 = kirim_notifikasi.delay("Pesanan ORDER-001 sedang dipacking!")
    
    print("[3] Flash Sale (Testing FAN-OUT)...")
    task_3 = broadcast_promo.delay("Diskon 50% untuk semua Sepatu!")

    print("\n=== SEMUA PROSES TELAH DIKIRIM KE BROKER ===")