import os
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms


# -------------------------------------------------
# Image Transformations (for MobileNet / ResNet)
# -------------------------------------------------

def get_transforms(train=True):
    if train:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    return transform


# -------------------------------------------------
# Driver Distracted Dataset Loader
# -------------------------------------------------

class DriverDataset(Dataset):

    def __init__(self, root_dir, transform=None):

        self.root_dir = root_dir
        self.transform = transform

        # State Farm dataset classes
        self.classes = [
            "c0", "c1", "c2", "c3", "c4",
            "c5", "c6", "c7", "c8", "c9"
        ]

        # Class labels mapping
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}

        self.image_paths = []
        self.labels = []

        # Scan dataset folders
        for cls_name in self.classes:

            class_folder = os.path.join(self.root_dir, cls_name)

            if not os.path.exists(class_folder):
                continue

            for img_file in os.listdir(class_folder):

                if img_file.lower().endswith((".jpg", ".jpeg", ".png")):

                    img_path = os.path.join(class_folder, img_file)

                    self.image_paths.append(img_path)
                    self.labels.append(self.class_to_idx[cls_name])

        print(f"Total Images Loaded: {len(self.image_paths)}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):

        img_path = self.image_paths[index]
        label = self.labels[index]

        # Load image
        image = Image.open(img_path).convert("RGB")

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.long)