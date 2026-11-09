from celery import Celery
import time

app = Celery('toko_worker')
app.config_from_object('celery_config')

@app.task
def proses_pembayaran(order_id, nominal):
    print(f"\n[WORKER - TOPIC] Memproses pembayaran {order_id} sebesar Rp{nominal}...")
    time.sleep(3)
    print(f"[WORKER - TOPIC] Pembayaran {order_id} LUNAS.")
    return {"status": "lunas", "order_id": order_id}

@app.task
def kirim_notifikasi(pesan):
    print(f"\n[WORKER - WILDCARD] Mengirim Email: '{pesan}'")
    return True

@app.task
def broadcast_promo(pesan_promo):
    print(f"\n[WORKER - FAN-OUT] Notifikasi Promo Muncul: '{pesan_promo}'")
    return True