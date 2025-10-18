import torch, torch.nn as nn, torchvision.transforms as T
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
from functools import lru_cache

class SimpleCV(nn.Module):
    def __init__(self, n_classes: int = 10):
        super().__init__()
        self.backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
        for p in self.backbone.parameters():
            p.requires_grad = False
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(in_features, n_classes)

    def forward(self, x):
        return self.backbone(x)

@lru_cache(maxsize=1)
def _preproc():
    return T.Compose([T.Resize((224,224)), T.ToTensor(), T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])])

def predict_image_category(img: Image.Image, labels=None):
    # NOTE: This is a stub using ImageNet weights; replace with fine-tuned weights for better accuracy.
    model = resnet18(weights=ResNet18_Weights.DEFAULT).eval()
    x = _preproc()(img).unsqueeze(0)
    with torch.no_grad():
        logits = model(x)
        idx = int(logits.argmax(dim=1).item())
    if labels and 0 <= idx < len(labels):
        return labels[idx]
    return f"imagenet_class_{idx}"
