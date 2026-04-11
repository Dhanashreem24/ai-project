import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

from network import DriverBehaviorModel
from dataset import DriverDataset, get_transforms

import os


def train_model(dataset_root, epochs=10, batch_size=32, lr=0.001):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # Dataset folder
    train_dir = os.path.join(dataset_root, "train")

    if not os.path.exists(train_dir):
        print("ERROR: train folder not found:", train_dir)
        return

    # Load full dataset
    full_dataset = DriverDataset(train_dir, transform=get_transforms(train=True))

    dataset_size = len(full_dataset)

    if dataset_size == 0:
        print("Dataset is empty. Check dataset path.")
        return

    print("Total Images Loaded:", dataset_size)

    classes = full_dataset.classes
    print("Classes:", classes)

    # Split dataset
    train_size = int(0.7 * dataset_size)
    val_size = int(0.15 * dataset_size)
    test_size = dataset_size - train_size - val_size

    train_dataset, val_dataset, test_dataset = random_split(
        full_dataset,
        [train_size, val_size, test_size]
    )

    print("Train samples:", len(train_dataset))
    print("Val samples:", len(val_dataset))
    print("Test samples:", len(test_dataset))

    # DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # Model
    model = DriverBehaviorModel(num_classes=len(classes)).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_acc = 0

    # Training Loop
    for epoch in range(epochs):

        model.train()
        running_loss = 0

        for images, labels in train_loader:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)

        # Validation
        model.eval()
        correct = 0

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                _, preds = torch.max(outputs, 1)

                correct += torch.sum(preds == labels).item()

        val_acc = correct / len(val_dataset)

        print(
            f"Epoch {epoch+1}/{epochs} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Val Accuracy: {val_acc:.4f}"
        )

        # Save best model
        if val_acc > best_acc:

            best_acc = val_acc
            torch.save(model.state_dict(), "best_model.pth")
            print("Saved best model")

    # Testing
    print("\nTesting best model...")

    model.load_state_dict(torch.load("best_model.pth"))
    model.eval()

    correct = 0

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            correct += torch.sum(preds == labels).item()

    test_acc = correct / len(test_dataset)

    print("\nFinal Test Accuracy:", test_acc)


if __name__ == "__main__":

    # CHANGE THIS PATH
    DATASET_ROOT = r"D:\Downloads\ai_project\ai_project\backend\model\dataset"

    train_model(
        dataset_root=DATASET_ROOT,
        epochs=10,
        batch_size=32,
        lr=0.001
    )
    # import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, random_split

# from network import DriverBehaviorModel
# from dataset import DriverDataset, get_transforms

# import os


# def train_model(dataset_root, epochs=10, batch_size=32, lr=0.001):

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print("Using device:", device)

#     train_dir = os.path.join(dataset_root, "train")
#     test_dir = os.path.join(dataset_root, "test")

#     train_dataset = DriverDataset(train_dir, transform=get_transforms(train=True))
#     test_dataset = DriverDataset(test_dir, transform=get_transforms(train=False))

#     classes = train_dataset.classes
#     print("Classes:", classes)

#     val_size = int(0.2 * len(train_dataset))
#     train_size = len(train_dataset) - val_size

#     train_subset, val_subset = random_split(train_dataset, [train_size, val_size])

#     train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
#     val_loader = DataLoader(val_subset, batch_size=batch_size)
#     test_loader = DataLoader(test_dataset, batch_size=batch_size)

#     model = DriverBehaviorModel(num_classes=len(classes)).to(device)

#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model.parameters(), lr=lr)

#     best_acc = 0

#     for epoch in range(epochs):

#         model.train()
#         running_loss = 0

#         for images, labels in train_loader:

#             images = images.to(device)
#             labels = labels.to(device)

#             optimizer.zero_grad()

#             outputs = model(images)
#             loss = criterion(outputs, labels)

#             loss.backward()
#             optimizer.step()

#             running_loss += loss.item()

#         print(f"Epoch {epoch+1}/{epochs} Train Loss: {running_loss/len(train_loader):.4f}")

#         model.eval()
#         correct = 0

#         with torch.no_grad():
#             for images, labels in val_loader:

#                 images = images.to(device)
#                 labels = labels.to(device)

#                 outputs = model(images)
#                 _, preds = torch.max(outputs, 1)

#                 correct += torch.sum(preds == labels)

#         val_acc = correct.double() / len(val_subset)

#         print("Validation Accuracy:", val_acc.item())

#         if val_acc > best_acc:
#             best_acc = val_acc
#             torch.save(model.state_dict(), "best_model.pth")
#             print("Saved best model")

#     print("\nTesting best model...")

#     model.load_state_dict(torch.load("best_model.pth"))
#     model.eval()

#     correct = 0

#     with torch.no_grad():
#         for images, labels in test_loader:

#             images = images.to(device)
#             labels = labels.to(device)

#             outputs = model(images)
#             _, preds = torch.max(outputs, 1)

#             correct += torch.sum(preds == labels)

#     test_acc = correct / len(test_dataset)

#     print("Final Test Accuracy:", test_acc.item())


# if __name__ == "__main__":

#     DATASET_ROOT = r"D:\Downloads\ai_project\ai_project\backend\model\dataset"

#     train_model(DATASET_ROOT)