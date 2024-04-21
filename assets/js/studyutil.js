let isRunning = false;
let timerDuration = 25 * 60; // 25 minutes
let totalDuration = timerDuration;
let timerId;
let completedSessions = 0;
const circumference = 2 * Math.PI * 60; // Circle circumference for larger progress bar

const progressCircle = document.getElementById('progress');
let timeLeft = totalDuration;

function updateDrowsyDetectionStatus() {
    if (isRunning) {
        document.getElementById("drowsyStatus").textContent = "Drowsiness detection Active"
    } else {
        document.getElementById("drowsyStatus").textContent = "Drowsiness detection Inactive"
    }
}

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        updateDrowsyDetectionStatus()
        timerId = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateDisplay();
                updateProgress(timeLeft);
            } else {
                alert('Time is up!');
                resetTimer();
            }
        }, 1000);
    }
}

function pauseTimer() {
    if (isRunning) {
        updateDrowsyDetectionStatus()
        clearInterval(timerId);
        isRunning = false;
    }
}

function resetTimer() {
    clearInterval(timerId);
    timeLeft = totalDuration;
    isRunning = false;
    updateDrowsyDetectionStatus()
    updateDisplay();
    updateProgress(timeLeft); // Reset the progress circle to full
}

function updateDisplay() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    document.getElementById('timer').textContent = `${padTime(minutes)}:${padTime(seconds)}`;
}

function padTime(time) {
    return time.toString().padStart(2, '0');
}

function updateProgress(timeLeft) {
    const progress = (1 - timeLeft / totalDuration) * (2 * Math.PI * 60); // Updated to use the actual circumference
    progressCircle.style.strokeDashoffset = 471 - progress; // Make sure this aligns with your SVG's circumference
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
                    if (data.drowsyDetected) {
                        document.getElementById("tired").textContent = "You seem tired...";
                    } else {
                        document.getElementById("tired").textContent = "Looking good!";
                    }

                    //document.getElementById("num").textContent = data.count;
                    if (data.isTired && !alerted) {
                        alert("You seem tired. Maybe you should take a break");
                        alerted = true;
                    }
                })
                .catch(error => {
                    console.log('Error uploading image:', error);
                });
        }, 'image/png');
    }, 1000); // Capture an image every 1000 milliseconds (1 second)
}