import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Teachable Machine Image Model",
    layout="centered"
)

st.title("📷 Teachable Machine Image Classification")
st.caption("Real-time image classification using your webcam")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .card {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: inline-block;
        }
        button {
            padding: 8px 16px;
            margin: 6px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        .start { background-color: #22c55e; color: white; }
        .stop { background-color: #ef4444; color: white; }
        .flip { background-color: #3b82f6; color: white; }

        #status {
            margin-top: 10px;
            font-weight: bold;
        }
        #top-prediction {
            margin-top: 12px;
            font-size: 18px;
            color: #2563eb;
        }
    </style>
</head>
<body>

<div class="card">
    <h3>Teachable Machine Card Classification</h3>
    <h3>Description : Classify your cards in real-time: Paragon Student Card, National ID, & Vaccine Card.</h3>

    <button class="start" onclick="startWebcam()">▶ Start</button>
    <button class="stop" onclick="stopWebcam()">⏹ Stop</button>
    <button class="flip" onclick="toggleFlip()">🔄 Flip Camera</button>

    <div id="status">Status: Idle</div>

    <div id="webcam-container"></div>
    <div id="top-prediction"></div>
    <div id="label-container"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>

<script type="text/javascript">
    const URL = "https://teachablemachine.withgoogle.com/models/M8arciFtr/";

    let model, webcam, labelContainer, maxPredictions;
    let isRunning = false;
    let flipCamera = true;

    async function loadModel() {
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();
    }

    async function startWebcam() {
        if (isRunning) return;

        document.getElementById("status").innerText = "Status: Loading model...";
        if (!model) await loadModel();

        webcam = new tmImage.Webcam(240, 240, flipCamera);
        await webcam.setup();
        await webcam.play();
        isRunning = true;

        document.getElementById("webcam-container").innerHTML = "";
        document.getElementById("webcam-container").appendChild(webcam.canvas);

        labelContainer = document.getElementById("label-container");
        labelContainer.innerHTML = "";
        for (let i = 0; i < maxPredictions; i++) {
            labelContainer.appendChild(document.createElement("div"));
        }

        document.getElementById("status").innerText = "Status: Running";
        window.requestAnimationFrame(loop);
    }

    async function stopWebcam() {
        if (!isRunning) return;
        isRunning = false;
        webcam.stop();
        document.getElementById("status").innerText = "Status: Stopped";
        document.getElementById("top-prediction").innerText = "";
    }

    function toggleFlip() {
        flipCamera = !flipCamera;
        if (isRunning) {
            stopWebcam();
            startWebcam();
        }
    }

    async function loop() {
        if (!isRunning) return;
        webcam.update();
        await predict();
        window.requestAnimationFrame(loop);
    }

    async function predict() {
        const prediction = await model.predict(webcam.canvas);

        let topClass = "";
        let topProb = 0;

        for (let i = 0; i < maxPredictions; i++) {
            const prob = prediction[i].probability;
            const className = prediction[i].className;
            labelContainer.childNodes[i].innerHTML =
                className + ": " + prob.toFixed(2);

            if (prob > topProb) {
                topProb = prob;
                topClass = className;
            }
        }

        document.getElementById("top-prediction").innerText =
            "Top Prediction: " + topClass + " (" + topProb.toFixed(2) + ")";
    }
</script>

</body>
</html>
"""

components.html(html_code, height=650)

st.markdown(
    """
    **How to use:**
    - Click **Start** to enable webcam
    - Use **Flip Camera** for mirror correction
    - Click **Stop** to release the camera
    """
)
