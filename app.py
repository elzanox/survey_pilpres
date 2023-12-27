from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Inisialisasi koneksi MQTT
mqtt_broker = "218.234.97.77"
mqtt_port = 1883
mqtt_topic = "survey"

# Inisialisasi nilai awal
count_1 = 0
count_2 = 0
count_3 = 0
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        mqtt_client.subscribe(mqtt_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    global count_1, count_2, count_3
    received_payload = message.payload.decode("utf-8")
    try:
        payload_json = json.loads(received_payload)
        count_1 = payload_json.get("count_1", count_1)
        count_2 = payload_json.get("count_2", count_2)
        count_3 = payload_json.get("count_3", count_3)
        print(f"Received JSON payload: {payload_json}")

        # Mengirim pembaruan nilai ke semua klien WebSocket
        socketio.emit('update', {'c1': count_1, 'c2': count_2, 'c3': count_3}, namespace='/survey')
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Konfigurasi koneksi MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.subscribe(mqtt_topic)
mqtt_client.loop_start()
mqtt_client.enable_logger()


# Membuat route untuk halaman utama
@app.route('/')
def home():
    return 'Hello, ini adalah halaman utama!'

# Membuat route untuk halaman survey
@app.route('/survey')
def survey():
    return render_template('survey_socketio.html', c1=count_1, c2=count_2, c3=count_3)

# Membuat event handler untuk koneksi WebSocket
@socketio.on('connect', namespace='/survey')
def handle_connect():
    print('Client connected')
    # Mengirim nilai awal ke klien WebSocket saat terhubung
    socketio.emit('update', {'c1': count_1, 'c2': count_2, 'c3': count_3}, namespace='/survey')

if __name__ == '__main__':
    # Menjalankan aplikasi dengan SocketIO
     socketio.run(app, host='0.0.0.0', port=80, debug=True)
