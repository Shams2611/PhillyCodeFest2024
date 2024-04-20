from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default

@app.route("/")
def serve_index():
    """ Serves the index.html file on the default server route """
    return app.send_static_file("index.html")

if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)