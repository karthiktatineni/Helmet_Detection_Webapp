import os
from pathlib import Path
import modal

# 1. Define the Modal Image
# Modal 1.0 syntax: Use add_local_dir directly on the image
image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install("libgl1-mesa-glx", "libglib2.0-0") 
    .pip_install(
        "fastapi==0.115.0",
        "uvicorn[standard]==0.30.0",
        "python-multipart==0.0.9",
        "sqlalchemy==2.0.35",
        "aiosqlite==0.20.0",
        "loguru==0.7.2",
        "pydantic-settings==2.5.2",
        "yagmail==0.15.293",
        "ultralytics==8.3.8",
        "opencv-python-headless==4.10.0.84",
        "numpy==1.26.4",
        "pillow==10.4.0",
    )
    .add_local_dir("./backend", remote_path="/root/backend")
)

# 2. Define the Modal App
app = modal.App("helmet-detection-api")

# 3. Define Volumes for persistent storage
model_volume = modal.Volume.from_name("helmet-models", create_if_missing=True)
data_volume = modal.Volume.from_name("helmet-data", create_if_missing=True)

@app.function(
    image=image,
    gpu="T4",
    volumes={
        "/models": model_volume,
        "/data": data_volume,
    },
    env={
        # Override paths to point to Volume mounts
        "YOLO_COCO_CFG": "/models/yolov3model/yolov3.cfg",
        "YOLO_COCO_WEIGHTS": "/models/yolov3model/yolov3.weights",
        "YOLO_COCO_LABELS": "/models/yolov3model/yolov3-labels",
        "YOLO_HELMET_CFG": "/models/helmet/yolov3-obj.cfg",
        "YOLO_HELMET_WEIGHTS": "/models/helmet/yolov3-obj_2400.weights",
        "CNN_PLATE_JSON": "/models/plate/model.json",
        "CNN_PLATE_WEIGHTS": "/models/plate/model_weights.h5",
        "CNN_PLATE_LABELS": "/models/plate/labels.txt",
        
        "DATABASE_URL": "sqlite+aiosqlite:////data/helmet_detection.db",
        "UPLOAD_DIR": "/data/uploads",
        "OUTPUT_DIR": "/data/outputs",
        
        "SENDER_EMAIL": "karthiktatineni34@gmail.com",
        "SENDER_PASSWORD": "biol nikq lzlk qftx",
        "RECEIVER_EMAIL": "22951a0472@iare.ac.in",
        "ENABLE_EMAIL_ALERTS": "true",
        
        "APP_DEBUG": "false",
    },
    scaledown_window=300,
    timeout=600,
)
@modal.asgi_app()
def fastapi_app():
    import sys
    import os
    
    # Ensure the backend code is in the python path
    sys.path.append("/root")
    
    # Symlink data and models to /root so relative paths in code work
    try:
        if not os.path.exists("/root/data"):
            os.symlink("/data", "/root/data")
        if not os.path.exists("/root/models"):
            os.symlink("/models", "/root/models")
    except Exception:
        pass

    # Create necessary directories in the Volume if they don't exist
    for d in ["/data/uploads/videos", "/data/outputs/results", "/data/outputs/violations"]:
        os.makedirs(d, exist_ok=True)
    
    # Import and return your existing FastAPI app
    from backend.main import app as web_app
    return web_app
