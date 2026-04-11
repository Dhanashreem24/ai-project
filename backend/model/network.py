import torch.nn as nn
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights


class DriverBehaviorModel(nn.Module):

    def __init__(self, num_classes=10, pretrained=True):
        super(DriverBehaviorModel, self).__init__()

        weights = MobileNet_V2_Weights.DEFAULT if pretrained else None
        self.model = mobilenet_v2(weights=weights)

        in_features = self.model.classifier[1].in_features

        self.model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)