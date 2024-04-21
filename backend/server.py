from flask import Flask, jsonify, request, render_template, redirect, Response, session
from flask_cors import CORS
from drowsy_detection_code.faceSentiment import DrowsyDetection
from chatbot.bot import ChatBot
from dotenv import load_dotenv
from os import urandom
from playsound import playsound
import multiprocessing
import time

load_dotenv()

app = Flask(__name__, template_folder="../", static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default

dd = DrowsyDetection()
chatbot = ChatBot()

app.secret_key = urandom(32)

@app.route("/reset", methods=["POST"])
def reroute():
    session["tired_count"] = 0
    return Response(status=200)


@app.route("/")
def serve_index():
    """Serves the index.html file on the default server route"""
    return app.send_static_file("index.html")


@app.route("/study_planner")
def serve_camera():
    session["tired_count"] = 0
    return render_template("/study_planner.html")
    # return app.send_static_file("backend/testing/camera.html")


@app.route("/upload-image", methods=["POST"])
def upload_image():
    image = request.files["image"]

    if "tired_count" not in session:
        session["tired_count"] = 0

    # Raw bytes
    if session["tired_count"]==6:
        p = multiprocessing.Process(target=playsound, args=('PhillyCodeFest2024/backend/audio_test/608088__funwithsound__horn-14-leslie-125.mp3',))
        p.start()
        time.sleep(3)
        p.terminate()
    data = image.stream.read()
    if dd.faceSentiBytesSrc(data) == 1:
        was_tired = True
        session["tired_count"] += 1
    else:
        was_tired = False
    
    print(repr(session["tired_count"]))
    return jsonify(
        {
            "message": "Image uploaded successfully",
            "count": session["tired_count"],
            "drowsyDetected": was_tired,
            "isTired": session["tired_count"] >= 6,
        }
    )

@app.route("/testchat", methods=["GET", "POST"])
def chatbot_server():
    if request.method == "POST":
        try:
            data = request.get_json()
            user_input = data["input"]
        except Exception as e:
            print("Error caught:", e)
            return jsonify({"message": "failed to parse input"}), 400

        output = chatbot.getOutput(user_input)
        return jsonify({"response": output})
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405
        # return app.send_static_file("chatbot.html")


if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)
