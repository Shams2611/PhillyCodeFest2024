from flask import Flask, jsonify, request, render_template, redirect, Response, session, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from os import urandom,listdir
from playsound import playsound




load_dotenv()

app = Flask(__name__, template_folder="./", static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default
audio_path = 'PhillyCodeFest2024/backend/audio_test/608088__funwithsound__horn-14-leslie-125.mp3'
app.secret_key = urandom(32)

@app.route("/")
def index():
    return render_template("audiotest.html")

#original function made by jlacson on GitHub
@app.route('/play')
def play():
    playsound(audio_path)
    return render_template("audiotest.html")

if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)
