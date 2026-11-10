# Tugas 2 KBJ: Job Queue & Message-Brokering (Celery & RabbitMQ)

**Mata Kuliah:** Komputasi Berbasis Jaringan (S2 Informatika, Universitas Negeri Surabaya)  
**Anggota Kelompok:**
1. Muhammad Zaini Rochman (26051905037)
2. Hendra Cahyo Setiawan (26051905039)

---

## 1. Deskripsi Proyek

Repositori ini berisi implementasi _Job Queue_ menggunakan arsitektur **Celery** dan **RabbitMQ** sebagai _message broker_. Proyek ini mensimulasikan proses latar belakang (_background processing_) pada sebuah **Sistem Toko Online Sederhana**.

Ketika pelanggan melakukan _checkout_, tugas-tugas berat (seperti verifikasi pembayaran ke API Bank atau mengirim email notifikasi) tidak diproses langsung yang dapat menyebabkan halaman web memuat lambat (sinkron), melainkan dilempar ke antrean (_broker_) untuk dikerjakan oleh _worker_ secara asinkron.

---

## 2. Eksplorasi Penanganan Pesan (Message Handling)

Proyek ini menguji tiga skema penanganan pesan pada AMQP/RabbitMQ yang dikonfigurasi melalui `celery_config.py`:

### A. Topic (Pencocokan Pasti / Spesifik)
- **Konsep:** Pesan dirutekan dari _exchange_ ke _queue_ berdasarkan kecocokan nama _routing key_ secara absolut.
- **Implementasi di Kode:** Task `proses_pembayaran` dikirim ke exchange `toko_topic` dengan _routing key_ `pesanan.pembayaran`. Broker HANYA meneruskannya ke `queue_pembayaran` karena antrean tersebut mengikat (_bind_) string yang sama persis.
- **Penggunaan:** Sangat cocok untuk tugas spesifik, seperti _worker_ khusus transaksi keuangan.

### B. Wildcard (Pencocokan Pola)
- **Konsep:** Variasi dari _Topic_, di mana _queue_ menggunakan karakter khusus (seperti `*` untuk satu kata) pada _routing key_ agar bisa menangkap beberapa jenis pesan sekaligus.
- **Implementasi di Kode:** Task `kirim_notifikasi` dikirim ke exchange `toko_topic` dengan _routing key_ `pesanan.update_status`. Pesan ini berhasil masuk ke `queue_notifikasi` karena antrean tersebut berlangganan pada pola `pesanan.*`.
- **Penggunaan:** Cocok untuk menangkap kelompok tugas yang sejenis, misalnya mengirim notifikasi untuk berbagai macam _event_ pesanan (pesanan.dikirim, pesanan.sampai, dsb).

### C. Fan-Out (Broadcast)
- **Konsep:** _Exchange_ mengabaikan _routing key_. Pesan akan digandakan dan dipancarkan ke **semua** _queue_ yang terhubung ke _exchange_ tersebut.
- **Implementasi di Kode:** Task `broadcast_promo` dilempar ke exchange `toko_fanout`. Pesan ini otomatis diterima oleh `queue_promo_hp` dan `queue_promo_web` secara bersamaan.
- **Penggunaan:** Cocok untuk sistem siaran massal, seperti _push notification_ diskon _flash sale_ ke semua aplikasi pengguna secara serentak.

---

## 3. Langkah Menjalankan Proyek

### 1. Persiapan Environment
Pastikan dependensi telah terpasang di virtual environment:
```bash
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```

### 2. Menjalankan Message Broker (RabbitMQ)
Jalankan RabbitMQ menggunakan Docker:
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
> RabbitMQ Web Dashboard dapat diakses di `http://localhost:15672` (User: `guest`, Password: `guest`).

### 3. Menjalankan Celery Worker
Buka terminal baru dan aktifkan worker untuk mendengarkan antrean:

**Opsi A (Worker Global - mendengarkan semua antrean):**
```bash
source myvenv/bin/activate
celery -A tasks worker --loglevel=INFO
```

**Opsi B (Multi-Worker per Antrean / Spesifik Queue):**
```bash
# Terminal 1 - Worker Pembayaran (Topic)
celery -A tasks worker -Q queue_pembayaran -l INFO -n worker_pay@%h

# Terminal 2 - Worker Notifikasi (Wildcard)
celery -A tasks worker -Q queue_notifikasi -l INFO -n worker_notif@%h

# Terminal 3 - Worker Promo (Fanout)
celery -A tasks worker -Q queue_promo_hp,queue_promo_web -l INFO -n worker_promo@%h
```

### 4. Menjalankan Dashboard Monitoring Flower (Opsional)
Untuk melihat monitoring real-time antrean dan worker di browser:
```bash
source myvenv/bin/activate
celery -A tasks flower --port=5555
```
Akses di browser: `http://localhost:5555`.

### 5. Menjalankan Producer (Pembangkit Data Masukan)
Buka terminal lain dan kirimkan tugas ke broker:
```bash
source myvenv/bin/activate
python producer.py
```

