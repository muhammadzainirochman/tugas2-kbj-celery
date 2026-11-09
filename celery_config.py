from kombu import Exchange, Queue

broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

exchange_pesanan = Exchange('toko_topic', type='topic')
exchange_pengumuman = Exchange('toko_fanout', type='fanout')

task_queues = (
    Queue('queue_pembayaran', exchange_pesanan, routing_key='pesanan.pembayaran'),
    Queue('queue_notifikasi', exchange_pesanan, routing_key='pesanan.*'),
    Queue('queue_promo_hp', exchange_pengumuman),
    Queue('queue_promo_web', exchange_pengumuman),
)

task_routes = {
    'tasks.proses_pembayaran': {'queue': 'queue_pembayaran', 'routing_key': 'pesanan.pembayaran'},
    'tasks.kirim_notifikasi': {'queue': 'queue_notifikasi', 'routing_key': 'pesanan.update_status'},
    'tasks.broadcast_promo': {'exchange': 'toko_fanout', 'routing_key': 'bebas'},
}