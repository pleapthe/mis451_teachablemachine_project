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
        img {
            max-width: 240px;
            margin-top: 10px;
            border-radius: 8px;
        }
    </style>
</head>
<body>

<div class="card">
    <h3>Teachable Machine Card Classification</h3>

    <button class="start" onclick="startWebcam()">▶ Start Webcam</button>
    <button class="stop" onclick="stopWebcam()">⏹ Stop</button>
    <button class="flip" onclick="toggleFlip()">🔄 Flip Camera</button>

    <hr>

    <input type="file" accept="image/*" onchange="handleImageUpload(event)">

    <div id="status">Status: Idle</div>

    <div id="webcam-container"></div>
    <img id="uploaded-image"/>
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

        labelContainer = document.getElementById("label-container");
        labelContainer.innerHTML = "";
        for (let i = 0; i < maxPredictions; i++) {
            labelContainer.appendChild(document.createElement("div"));
        }
    }

    async function startWebcam() {
        if (isRunning) return;

        document.getElementById("status").innerText = "Status: Loading model...";
        if (!model) await loadModel();

        webcam = new tmImage.Webcam(240, 240, flipCamera);
        await webcam.setup();
        await webcam.play();
        isRunning = true;

        document.getElementById("uploaded-image").style.display = "none";
        document.getElementById("webcam-container").innerHTML = "";
        document.getElementById("webcam-container").appendChild(webcam.canvas);

        document.getElementById("status").innerText = "Status: Webcam Running";
        window.requestAnimationFrame(loop);
    }

    function stopWebcam() {
        if (!isRunning) return;
        isRunning = false;
        webcam.stop();
        document.getElementById("status").innerText = "Status: Stopped";
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
        await predict(webcam.canvas);
        window.requestAnimationFrame(loop);
    }

    async function handleImageUpload(event) {
        if (!model) await loadModel();

        stopWebcam();

        const img = document.getElementById("uploaded-image");
        img.src = URL.createObjectURL(event.target.files[0]);
        img.style.display = "block";

        img.onload = async () => {
            document.getElementById("status").innerText = "Status: Image Uploaded";
            await predict(img);
        };
    }

    async function predict(image) {
        const prediction = await model.predict(image);

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
