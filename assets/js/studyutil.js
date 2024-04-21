let isRunning = false;
let timerDuration = 25 * 60; // 25 minutes
let totalDuration = timerDuration;
let timerId;
let completedSessions = 0;
const circumference = 2 * Math.PI * 60; // Circle circumference for larger progress bar

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        timerId = setInterval(() => {
            if (timerDuration > 0) {
                timerDuration--;
                updateDisplay();
            } else {
                completedSessions++;
                document.getElementById('completedSessions').textContent = completedSessions;
                resetTimer();
                alert('Time is up!');
            }
        }, 1000);
    }
}

function pauseTimer() {
    if (isRunning) {
        clearInterval(timerId);
        isRunning = false;
    }
}

function resetTimer() {
    clearInterval(timerId);
    timerDuration = 25 * 60; // reset to 25 minutes
    isRunning = false;
    updateDisplay();
}

function updateDisplay() {
    let minutes = Math.floor(timerDuration / 60);
    let seconds = timerDuration % 60;
    document.getElementById('timer').textContent = `${padTime(minutes)}:${padTime(seconds)}`;
    updateProgress(timerDuration);
}

function padTime(time) {
    return time.toString().padStart(2, '0');
}

function updateProgress(timeLeft) {
    const progress = (1 - timeLeft / totalDuration) * circumference;
    document.getElementById('progress').style.strokeDashoffset = circumference - progress;
}

var alerted = false;
var camera_on = false;
const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const canvasContext = canvasElement.getContext('2d');

function ResetAlert() {
    alerted = false;
}

// Access the user's camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        videoElement.srcObject = stream;
        startCapturingImages();
        camera_on = true;
    })
    .catch(function (error) {
        console.log('Error accessing camera:', error);
        camera_on = false;
    });

function startCapturingImages() {
    setInterval(function () {
        if (!isRunning)
            return;

        // Capture an image from the video stream
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

        // Convert the captured image to a Blob
        canvasElement.toBlob(function (blob) {
            // Create a FormData object to send the image
            const formData = new FormData();
            formData.append('image', blob, 'image.png');

            // Send the image to the Flask backend
            fetch('/upload-image', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {

                    //document.getElementById("num").textContent = data.count;
                    if (data.isTired) {
                        document.getElementById("tired").textContent = "You seem Tired";
                        if (!alerted) {
                            alert("You seem tired. Maybe you should take a break");
                            alerted = true;
                        }
                    }
                })
                .catch(error => {
                    console.log('Error uploading image:', error);
                });
        }, 'image/png');
    }, 1000); // Capture an image every 1000 milliseconds (1 second)
}