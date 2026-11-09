# Tugas 2 KBJ: Job Queue & Message-Brokering (Celery & RabbitMQ)

**Mata Kuliah:** Komputasi Berbasis Jaringan (S2 Informatika, Universitas Negeri Surabaya)  
**Anggota Kelompok:**

1. Muhammad Zaini Rochman (26051905037)
2. Hendra Cahyo Setiawan (26051905039)

---

## 1. Deskripsi Proyek

Repositori ini berisi implementasi _Job Queue_ menggunakan arsitektur **Celery** dan **RabbitMQ** sebagai _message broker_. Proyek ini mensimulasikan proses latar belakang (_background processing_) pada sebuah **Sistem Toko Online Sederhana**.

Ketika pelanggan melakukan _checkout_, tugas-tugas berat (seperti verifikasi pembayaran ke API Bank atau mengirim email notifikasi) tidak diproses langsung yang dapat menyebabkan halaman web memuat lambat (sinkron), melainkan dilempar ke antrean (_broker_) untuk dikerjakan oleh _worker_ secara asinkron.

## 2. Eksplorasi Penanganan Pesan (Message Handling)

Proyek ini menguji tiga skema penanganan pesan pada AMQP/RabbitMQ yang dikonfigurasi melalui `celery_config.py`:

### A. Topic (Pencocokan Pasti / Spesifik)

- **Konsep:** Pesan dirutekan dari _exchange_ ke _queue_ berdasarkan kecocokan nama _routing key_ secara absolut.
- **Implementasi di Kode:** Task `proses_pembayaran` dikirim dengan _routing key_ `pesanan.pembayaran`. Broker HANYA meneruskannya ke `queue_pembayaran` karena _queue_ tersebut mengikat (_bind_) string yang sama persis.
- **Penggunaan:** Sangat cocok untuk tugas spesifik, seperti _worker_ khusus transaksi keuangan.

### B. Wildcard (Pencocokan Pola)

- **Konsep:** Variasi dari _Topic_, di mana _queue_ menggunakan karakter khusus (seperti `*` untuk satu kata) pada _routing key_ agar bisa menangkap beberapa jenis pesan sekaligus.
- **Implementasi di Kode:** Task `kirim_notifikasi` dikirim dengan _routing key_ `pesanan.update_status`. Pesan ini berhasil masuk ke `queue_notifikasi` karena antrean tersebut berlangganan pada pola `pesanan.*`.
- **Penggunaan:** Cocok untuk menangkap kelompok tugas yang sejenis, misalnya mengirim notifikasi untuk berbagai macam _event_ pesanan (pesanan.dikirim, pesanan.sampai, dsb).

### C. Fan-Out (Broadcast)

- **Konsep:** _Exchange_ mengabaikan _routing key_. Pesan akan digandakan dan dipancarkan ke **semua** _queue_ yang terhubung ke _exchange_ tersebut.
- **Implementasi di Kode:** Task `broadcast_promo` dilempar ke _exchange_ `toko_fanout`. Pesan ini otomatis diterima oleh `queue_promo_hp` dan `queue_promo_web` secara bersamaan.
- **Penggunaan:** Cocok untuk sistem siaran massal, seperti _push notification_ diskon _flash sale_ ke semua aplikasi pengguna secara serentak.

---

## 3. Langkah Menjalankan Proyek

**1. Persiapan Environment**

```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```
