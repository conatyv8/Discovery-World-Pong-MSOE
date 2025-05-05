# connect.py
# This program connects to the MQTT broker, subscribes to human and AI paddle positions,
# and game state updates, then sends the relevant data to a connected Raspberry Pi over TCP.

import socket
import datetime
import json
import threading
import paho.mqtt.client as mqtt
import uuid
import sys
# --- Logging utility ---
def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()

# --- TCP Server Config ---
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5006       # Port to listen on

# --- MQTT Subscriber Class ---
class PaddleMQTTSubscriber:
    def __init__(self, send_to_pi_callback):
        self.send_to_pi_callback = send_to_pi_callback
        client_id = "paddle-subscriber-" + str(uuid.uuid1())
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async("mqtt-broker", port=1883, keepalive=60)

    def on_connect(self, client, userdata, flags, rc):
        log("[MQTT] Connected with result code " + str(rc))
        client.subscribe("paddle1/position")  # Human paddle
        client.subscribe("paddle2/position")  # AI paddle
        client.subscribe("game/state")        # Game state (0, 1, 2) (waiting, ready, running)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload)
        log(f"[MQTT] Message on {topic}: {payload}")

        if topic == "paddle1/position":
            message = {"type": "human", "x": payload["position"]}
        elif topic == "paddle2/position":
            message = {"type": "ai", "x": payload["x"]}
        elif topic == "game/state":
            message = {"type": "state", "state": payload["position"]}
        else:
            return

        # Send data to Raspberry Pi
        self.send_to_pi_callback(message)

    def start(self):
        self.client.loop_start()

# --- Main TCP Server ---
def start_server():
    log(f"[SERVER] Starting TCP server on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        log("[SERVER] Socket bound successfully.")
        server_socket.listen()
        log("[SERVER] Listening for connections...")

        conn, addr = server_socket.accept()
        log(f"[SERVER] Connection established from {addr}")

        with conn:
            # Define how to send MQTT data to Raspberry Pi
            def send_to_pi(msg):
                try:
                    payload = json.dumps(msg).encode()
                    conn.sendall(payload)
                    log(f"[SENT TO PI]: {msg}")
                except Exception as e:
                    log(f"[ERROR sending to PI]: {e}")

            # Start MQTT in a background thread
            mqtt_subscriber = PaddleMQTTSubscriber(send_to_pi)
            mqtt_subscriber.start()

            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        log("[SERVER] Client disconnected.")
                        break
                    decoded = data.decode(errors="replace").strip()
                    log(f"[RECEIVED FROM PI]: {decoded}")
            except ConnectionResetError:
                log("[SERVER] Connection lost unexpectedly.")
            except Exception as e:
                log(f"[SERVER ERROR]: {e}")

if __name__ == "__main__":
    start_server()
