import csv
import json
import paho.mqtt.client as mqtt
import time
# Ganti 'nama_file.csv' dengan nama file CSV yang ingin Anda baca
csv_comment_path = "comments.csv"  # Ganti dengan path file CSV yang sesuai
csv_gift_path = "gifts.csv"  # Ganti dengan path file CSV yang sesuai

def baca_csv_gift(nama_file):
    count_gifts = {"Coffee": 0, "Rose": 0, "Orange Juice": 0}  # Set ulang ke keadaan awal
    
    with open(nama_file, 'r') as file_csv:
        pembaca_csv = csv.DictReader(file_csv)
        
        total_jumlah = 0  # Inisialisasi total jumlah
        
        for baris in pembaca_csv:
            # Mendapatkan nilai kolom 'count' dan 'gift' dari setiap baris
            jumlah = int(baris['count'])
            gift = baris['gift']
            
            # Menambahkan jumlah ke dalam dictionary sesuai dengan item hadiah
            if gift in count_gifts:
                count_gifts[gift] += jumlah
            total_jumlah += jumlah
    
    # Menghitung persentase setiap item hadiah berdasarkan total jumlah
    percentages = {gift: round(count / total_jumlah * 100, 2) for gift, count in count_gifts.items()}
    
    # Menampilkan hasil di konsol
    print(percentages)
    
    # Mengirim hasil ke broker MQTT
    publish_mqtt(json.dumps(percentages))

def baca_csv_comment(nama_file):
    count_comments = {"1": 0, "2": 0, "3": 0}  # Set ulang ke keadaan awal
    
    with open(nama_file, 'r') as file_csv:
        pembaca_csv = csv.DictReader(file_csv)
        total_jumlah = 0
        for baris in pembaca_csv:
            # Mendapatkan nilai kolom 'comment' dari setiap baris
            comment = baris['comment']
            
            # Menentukan kategori berdasarkan isi komentar
            if '1' in comment or '01' in comment:
                count_comments["1"] += 1
            elif '2' in comment or '02' in comment:
                count_comments["2"] += 1
            elif '3' in comment or '03' in comment:
                count_comments["3"] += 1
                
            total_jumlah += 1

    # Menghitung persentase setiap item hadiah berdasarkan total jumlah
    percentages = {gift: round(count / total_jumlah * 100, 2) for gift, count in count_comments.items()}
    # Menampilkan hasil di konsol
    print(percentages)
    
    # Mengirim hasil ke broker MQTT
    publish_mqtt(json.dumps(percentages))


def publish_mqtt(message):
    # Konfigurasi broker MQTT
    broker_address = "218.235.216.37"
    port = 1883
    topic = "survey"
    
    # Inisialisasi client MQTT
    client = mqtt.Client()
    
    # Koneksi ke broker
    client.connect(broker_address, port=port)
    
    # Publish pesan ke topik
    client.publish(topic, message)
    
    # Tutup koneksi
    client.disconnect()

if __name__ == "__main__":
    
    
    try:
        while True:
            baca_csv_gift(csv_gift_path)
            baca_csv_comment(csv_comment_path)
            time.sleep(1)  # Menunggu 1 detik sebelum membaca lagi
    except FileNotFoundError:
        print(f"File {csv_gift_path} tidak ditemukan.")
        print(f"File {csv_comment_path} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
