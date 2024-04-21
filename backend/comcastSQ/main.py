from flask import Flask, jsonify, request, render_template, redirect, Response
from flask_cors import CORS
from dotenv import load_dotenv
import replicate

load_dotenv()

app = Flask(__name__, template_folder="../",static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default

@app.route("/")
def reroute():
    return render_template("/comcastSQ/comcastTest.html")

if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)
    