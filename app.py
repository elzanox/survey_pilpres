from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
# from gevent.pywsgi import WSGIServer
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import request
app = Flask(__name__)
socketio = SocketIO(app)

# Inisialisasi koneksi MQTT
mqtt_broker = "218.235.216.37"
mqtt_port = 1883
mqtt_topic = "survey"

# Inisialisasi nilai awal
count_1 = 0
count_2 = 0
count_3 = 0
gift_1 = 0
gift_2 = 0
gift_3 = 0
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        mqtt_client.subscribe(mqtt_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    global count_1, count_2, count_3, gift_1, gift_2, gift_3
    received_payload = message.payload.decode("utf-8")
    try:
        payload_json = json.loads(received_payload)
        count_1 = payload_json.get("1", count_1)
        count_2 = payload_json.get("2", count_2)
        count_3 = payload_json.get("3", count_3)
        gift_1 = payload_json.get("Coffee", gift_1)
        gift_2 = payload_json.get("Rose", gift_2)
        gift_3 = payload_json.get("Orange Juice", gift_3)
        print(f"Received JSON payload: {payload_json}")

        # Mengirim pembaruan nilai ke semua klien WebSocket
        socketio.emit('update', {'c1': gift_1, 'c2': gift_2, 'c3': gift_3}, namespace='/mini_games')
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
    return render_template('index.html')

@app.route('/comment')
def comment():
    return render_template('comment.html')

@app.route('/survey')
def survey():
    return render_template('survey.html', c1=count_1, c2=count_2, c3=count_3)

@app.route('/mini_games')
def mini_games():
    return render_template('mini_games.html', c1=gift_1, c2=gift_2, c3=gift_3)


# Global variable untuk menyimpan volume (nilai antara 0 dan 1)
current_volume = 1.0
@app.route('/music')
def music():
    return render_template('music.html',current_volume=current_volume)

@app.route('/set_volume/<float:volume>')
def set_volume(volume):
    global current_volume
    current_volume = volume
    return 'Volume set to {}'.format(volume)

# Membuat event handler untuk koneksi WebSocket
@socketio.on('connect', namespace='/mini_games')
def handle_connect():
    client_ip = request.remote_addr
    print(f'Client connected from IP: {client_ip}')
    # Mengirim nilai awal ke klien WebSocket saat terhubung
    socketio.emit('update', {'c1': gift_1, 'c2': gift_2, 'c3': gift_3}, namespace='/mini_games')
    
# Membuat event handler untuk koneksi WebSocket
@socketio.on('connect', namespace='/survey')
def handle_connect():
    client_ip = request.remote_addr
    print(f'Client connected from IP: {client_ip}')
    # Mengirim nilai awal ke klien WebSocket saat terhubung
    socketio.emit('update', {'c1': count_1, 'c2': count_2, 'c3': count_3}, namespace='/survey')
  
if __name__ == '__main__':
    # Menjalankan aplikasi dengan SocketIO menggunakan gevent-websocket handler
    # socketio.run(app, host='0.0.0.0', port=2024, debug=True, allow_unsafe_werkzeug=True, handler_class=WebSocketHandler)
    
    #  Use gevent.pywsgi to serve the Flask app
    # http_server = WSGIServer(('0.0.0.0', 2024), app)
    # print("Server running on http://0.0.0.0:2024/")
    # http_server.serve_forever()

    # Create a WSGIServer with WebSocketHandler
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 2024), app, handler_class=WebSocketHandler)

    # Start the server
    print("Running the server...")
    server.serve_forever()