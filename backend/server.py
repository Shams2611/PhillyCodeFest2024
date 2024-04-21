from flask import Flask, jsonify, request, render_template,redirect
from flask_cors import CORS
from drowsy_detection_code.faceSentiment import DrowsyDetection

app = Flask(__name__, template_folder="../",static_url_path="/", static_folder="../")
CORS(app)  # Enable CORS for all routes by default
dd = DrowsyDetection()
@app.route("/reroute")
def reroute():
    dd.reset()
    return redirect('/camera')


@app.route("/")
def serve_index():
    """ Serves the index.html file on the default server route """
    return app.send_static_file("index.html")

@app.route("/camera")
def serve_camera():
    dd.reset()
    return render_template("/study_planner.html")
    #return app.send_static_file("backend/testing/camera.html")

@app.route('/upload-image', methods=['POST'])
def upload_image():
    image = request.files['image']

    # BytesIO
    # data = image.stream
    
    # Raw bytes
    data = image.stream.read()
    dd.faceSentiBytesSrc(data)
    # print(dir(image))
    
    return jsonify({'message': 'Image uploaded successfully','count':dd.getCount(),'isTired':(dd.getCount()>=6)})


if __name__ == "__main__":
    # Replace with your desired host and port
    app.run(host="0.0.0.0", port=5000)
    