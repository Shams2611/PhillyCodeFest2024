from flask import Flask, jsonify, request, render_template, redirect, Response
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import ChatBot
import replicate

load_dotenv()

app = Flask(__name__, template_folder="../",static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default

@app.route("/")
def reroute():
    return redirect('/chatBot')

@app.route("/chatBot",methods = ['GET','POST'])
        
def botFunc():
    bot = ChatBot()
    output = ""
    if request.form.get("input") != None:
        output = bot.getOutput(request.form.get("input"))
    
    return render_template('/chatbot/chatbot.html',out=output)

if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)
    