import time
import json
import paho.mqtt.client as mqtt
import random

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Koneksi ke broker MQTT berhasil")
    else:
        print(f"Gagal terkoneksi ke broker MQTT. Kode: {rc}")

def kirim_mqtt_data(client):
    # Ganti topik dengan topik MQTT yang sesuai
    topik = 'survey'
    c1 = random.randint(0, 100)
    c2 = random.randint(0, 100)
    c3 = random.randint(0, 100)
    
    # Ganti data_json dengan data JSON yang ingin Anda kirim
    data_json = {"count_1": c1, "count_2": c2, "count_3": c3}

    # Mengirim data JSON sebagai pesan MQTT
    client.publish(topik, json.dumps(data_json))
    print(f'Data berhasil dikirim ke topik {topik}')

if __name__ == "__main__":
    # Ganti broker dan port sesuai dengan broker MQTT yang Anda gunakan
    broker = "218.234.49.151"
    port = 1883

    client = mqtt.Client()
    client.on_connect = on_connect

    # Hubungkan ke broker
    client.connect(broker, port, 60)

    # Loop untuk mengirim data setiap 2 detik
    while True:
        client.loop_start()
        kirim_mqtt_data(client)
        time.sleep(0.5)
        client.loop_stop()
