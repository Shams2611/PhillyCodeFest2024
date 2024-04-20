from flask import Flask, jsonify, request
from flask_cors import CORS
from drowsy_detection_code import *

app = Flask(__name__, static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default

@app.route("/")
def serve_index():
    """ Serves the index.html file on the default server route """
    return app.send_static_file("index.html")

@app.route("/camera")
def serve_camera():
    return app.send_static_file("backend/testing/camera.html")

@app.route('/upload-image', methods=['POST'])
def upload_image():
    image = request.files['image']

    # BytesIO
    # data = image.stream

    # Raw bytes
    data = image.stream.read()
    print(dir(image))
    return jsonify({'message': 'Image uploaded successfully'})

if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)