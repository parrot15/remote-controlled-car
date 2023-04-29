from flask import Flask
from flask_cors import CORS
from parse_config_file import config
from flask_socketio import SocketIO
import socketio
from process_camera_imagery import process_frame, encode_frame

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
CORS(app)
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Connect to the Raspberry Pi web socket server
raspberry_pi_socket = socketio.Client()
raspberry_pi_socket.connect(config.get("Raspberry Pi", "url"))

@server_socket.on("car-movement")
def car_movement(direction):
    raspberry_pi_socket.emit("car-movement", direction)

@server_socket.on("camera-movement")
def camera_movement(direction):
    raspberry_pi_socket.emit("camera-movement", direction)

@raspberry_pi_socket.on("camera-imagery")
def camera_imagery(frame):
    processed = process_frame(frame)
    encoded = encode_frame(processed)
    server_socket.emit("camera-imagery", encoded)