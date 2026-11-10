import sys
import time
import random
from tasks import proses_pembayaran, kirim_notifikasi, broadcast_promo

def jalankan_single_demo():
    print("=== [DEMO 1]: Pengujian 3 Skema Penanganan Pesan ===")
    
    print("\n[1] Pelanggan checkout (Testing TOPIC - routing_key='pesanan.pembayaran')...")
    t1 = proses_pembayaran.delay("ORDER-101", 150000)
    print(f"    -> Task dikirim ke broker (ID: {t1.id})")
    
    print("\n[2] Status pesanan berubah (Testing WILDCARD - routing_key='pesanan.update_status')...")
    t2 = kirim_notifikasi.delay("Pesanan ORDER-101 sedang dipacking oleh gudang!")
    print(f"    -> Task dikirim ke broker (ID: {t2.id})")
    
    print("\n[3] Siaran promo flash sale (Testing FAN-OUT - exchange='toko_fanout')...")
    t3 = broadcast_promo.delay("FLASH SALE! Diskon hingga 70% hanya hari ini!")
    print(f"    -> Task dikirim ke broker (ID: {t3.id})")
    print("\n=== SEMUA TASK DEMO 1 TELAH MASUK KE ANTRIAN BROKER ===\n")

def generate_batch_orders(jumlah=5):
    print(f"=== [DEMO 2]: Pembangkit Data Masukan (Input Generator {jumlah} Transaksi) ===")
    status_list = ["pembayaran diterima", "sedang dipacking", "diserahkan ke kurir", "dalam pengiriman"]
    
    for i in range(1, jumlah + 1):
        order_id = f"ORDER-{random.randint(100, 999)}"
        nominal = random.randint(25, 500) * 1000
        status = random.choice(status_list)
        
        print(f"[{i}/{jumlah}] Generate data: {order_id} (Rp{nominal:,}) & status '{status}'")
        proses_pembayaran.delay(order_id, nominal)
        kirim_notifikasi.delay(f"Pesanan {order_id}: {status}")
        time.sleep(0.3)
    
    print("\n=== SEMUA DATA INPUT GENERATOR BERHASIL DIKIRIM KE BROKER ===\n")

if __name__ == "__main__":
    jalankan_single_demo()
    
    # Mode Batch Generator
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        generate_batch_orders(5)
    elif sys.stdin.isatty():
        try:
            pilihan = input("Jalankan Input Generator Batch (5 transaksi acak)? (y/n) [y]: ").strip().lower()
            if pilihan in ("", "y", "yes"):
                generate_batch_orders(5)
        except (EOFError, KeyboardInterrupt):
            pass
