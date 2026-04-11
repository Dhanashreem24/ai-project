import torch
from torchvision import transforms
from PIL import Image
import base64
import io
import os

from network import DriverBehaviorModel


CLASS_MAP = {
    0: "Safe Driving",
    1: "Texting Right",
    2: "Talking Phone Right",
    3: "Texting Left",
    4: "Talking Phone Left",
    5: "Operating Radio",
    6: "Drinking",
    7: "Reaching Behind",
    8: "Hair and Makeup",
    9: "Talking to Passenger"
}


class DriverBehaviorInference:

    def __init__(self, model_path="best_model.pth"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = DriverBehaviorModel(num_classes=10, pretrained=False)

        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            self.loaded = True
            print("Model loaded successfully")

        else:
            self.loaded = False
            print("Model weights not found")

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image):

        image = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(image)
            probs = torch.softmax(outputs, dim=1)

        confidence, pred = torch.max(probs, 1)

        class_idx = pred.item()

        return {
            "class_idx": class_idx,
            "behavior": CLASS_MAP[class_idx],
            "confidence": round(confidence.item(), 3),
            "alert": class_idx != 0
        }

    def predict_from_base64(self, b64_string):

        if ',' in b64_string:
            b64_string = b64_string.split(',')[1]

        image_bytes = base64.b64decode(b64_string)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        return self.predict(image)