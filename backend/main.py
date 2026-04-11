from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random
import os
import sys

# Add model to path explicitly to avoid import issues
sys.path.append(os.path.join(os.path.dirname(__file__), "model"))
from inference import DriverBehaviorInference

app = FastAPI(title="Driver Behavior API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Inference
inference_engine = DriverBehaviorInference('model/best_model.pth')

global_status = {
    "behavior": "Awaiting System Feed",
    "confidence": 0.0,
    "alert": False,
    "message": ""
}

class FrameData(BaseModel):
    image_b64: str

@app.get("/")
def get_root():
    return {"status": "Backend is running with PyTorch Inference"}

@app.post("/api/predict")
async def predict_frame(data: FrameData):
    global global_status
    result = inference_engine.predict_from_base64(data.image_b64)
    
    # Update global tracking state
    global_status = {
        "behavior": result["behavior"],
        "confidence": result["confidence"],
        "alert": result["alert"],
        "message": "DISTRACTION DETECTED" if result["alert"] else "Clear"
    }
    return global_status

@app.get("/api/status")
def get_status():
    return global_status

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
