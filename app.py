from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import socket
import time

app = Flask(__name__, static_folder='.')
CORS(app)

# Update these paths to match your container paths
PIPER_PATH = "/app/piper/piper/piper"
MODELS = {
    "nepali": "/app/piper/piper/models/nepali/ne_NP-google-medium.onnx",
    "english": "/app/piper/piper/models/english/en_US-amy-medium.onnx"
}

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text")
    model_key = data.get("model")

    model_path = MODELS.get(model_key)
    if not model_path:
        return jsonify({"error": "Invalid model"}), 400

    try:
        subprocess.run("pkill -f 'aplay -r 22050' || true", shell=True)
        time.sleep(1)
        cmd = f"echo '{text}' | {PIPER_PATH} --model {model_path} --output-raw | aplay -r 22050 -f S16_LE -t raw -"
        subprocess.run(cmd, shell=True, check=True)
        return jsonify({"status": "success"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Add this to serve other static files if needed
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)
####################################### LAN CODES ######################
def get_lan_ip():
    """Get the LAN IP address of the server"""
    try:
        #CREATE A DUMMY SOCKET TO GET THE IP
        s = socker.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return request.host.split(':')[0]

@app.route('/get_server_ip')
def get_server_ip():
    return jsonify({"ip": get_lan_ip()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
