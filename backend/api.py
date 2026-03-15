import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import logging
from pydantic import BaseModel

app = FastAPI(title="AI-BASED FAKE IMAGE AND VIDEO DETECTOR")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress TF logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
tf.get_logger().setLevel("ERROR")

# Load our detection model safely
MODEL_PATH = "deepfake_detector.h5"

fake_model = None

@app.on_event("startup")
async def load_model_on_startup():
    global fake_model
    if os.path.exists(MODEL_PATH):
        try:
            fake_model = load_model(MODEL_PATH)
            logger.info("Deepfake Detection model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    else:
        logger.warning(f"Model file '{MODEL_PATH}' not found. Please train/download it first.")

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    global fake_model

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image file"}

    # Mock response if model is not yet compiled
    if fake_model is None:
        # Simulate logic while waiting for the user to train deepfake_detector.h5
        import random
        # Just random fake/real response to allow UI testing even if backend has no .h5 file yet
        is_fake = random.choice([True, False])
        confidence = round(random.uniform(85, 99.9), 1)
        return {
            "type": "image",
            "is_fake": is_fake,
            "confidence": confidence,
            "message": "⚠️ DEEPFAKE DETECTED" if is_fake else "✅ AUTHENTIC MEDIA",
            "analysis": "Simulated CNN output since no .h5 model found."
        }

    # Real inference
    img_resized = cv2.resize(img, (128, 128))
    img_scaled = img_resized / 255.0
    img_reshaped = np.reshape(img_scaled, (1, 128, 128, 3))

    prediction = fake_model.predict(img_reshaped, verbose=0)
    conf = float(prediction[0][0]) * 100

    is_fake = prediction > 0.5
    final_conf = conf if is_fake else (100 - conf)

    return {
        "type": "image",
        "is_fake": bool(is_fake),
        "confidence": round(final_conf, 1),
        "message": "⚠️ SYNTHETIC (DEEPFAKE)" if is_fake else "✅ AUTHENTIC",
        "analysis": "CNN prediction completed."
    }


@app.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)):
    global fake_model
    
    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    if fake_model is None:
        import random
        os.remove(temp_path)
        fake_frames = random.randint(10, 50)
        real_frames = random.randint(10, 50)
        is_fake = fake_frames > real_frames
        return {
            "type": "video",
            "is_fake": is_fake,
            "confidence": round(random.uniform(88, 99.5), 1),
            "message": "⚠️ TAMPERED VIDEO DETECTED" if is_fake else "✅ AUTHENTIC VIDEO",
            "analysis": "Simulated CNN/RNN output since no .h5 model found.",
            "total_frames": fake_frames + real_frames,
            "fake_frames": fake_frames,
            "real_frames": real_frames
        }

    cap = cv2.VideoCapture(temp_path)
    frame_count = 0
    fake_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.resize(frame, (128, 128))
        img = img / 255.0
        img = np.reshape(img, (1, 128, 128, 3))

        pred = fake_model.predict(img, verbose=0)
        if pred > 0.5:
            fake_count += 1
        frame_count += 1

        # limit frames for API test
        if frame_count > 60:
            break

    cap.release()
    os.remove(temp_path)

    real_count = frame_count - fake_count
    is_fake = fake_count > real_count
    confidence = (fake_count / frame_count) * 100 if is_fake else (real_count / frame_count) * 100

    return {
        "type": "video",
        "is_fake": bool(is_fake),
        "confidence": round(confidence, 1),
        "total_frames": frame_count,
        "fake_frames": fake_count,
        "real_frames": real_count,
        "message": "⚠️ TAMPERED VIDEO DETECTED" if is_fake else "✅ AUTHENTIC VIDEO",
        "analysis": "CNN/RNN frame analysis completed."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
