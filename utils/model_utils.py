"""
Model architecture, weight loading, and Grad-CAM utilities for the
DeepFake Face Detector.

IMPORTANT: This architecture must stay byte-for-byte identical to the one
used during training in Kaggle, or `load_state_dict` will fail (or worse,
silently load into the wrong layers).
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

IMG_SIZE = 128
CLASSES = ["fake", "real"]
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


class DeepfakeCNN(nn.Module):
    """Same architecture as the Kaggle training notebook (Cell 6)."""

    def __init__(self, num_classes: int = 2):
        super().__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2),
        )

        fc_input_size = 256 * (IMG_SIZE // 16) * (IMG_SIZE // 16)

        self.fc_layers = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(fc_input_size, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x


def get_transform():
    return transforms.Compose(
        [
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def load_model(model_path: str, device: torch.device) -> DeepfakeCNN:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model weights not found at: {model_path}")

    model = DeepfakeCNN(num_classes=2)
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def preprocess_image(pil_image: Image.Image, device: torch.device):
    pil_image = pil_image.convert("RGB")
    tensor = get_transform()(pil_image).unsqueeze(0).to(device)
    return tensor


@torch.no_grad()
def predict(model: DeepfakeCNN, img_tensor: torch.Tensor):
    outputs = model(img_tensor)
    probs = F.softmax(outputs, dim=1).cpu().numpy()[0]
    pred_idx = int(np.argmax(probs))
    return {
        "label": CLASSES[pred_idx],
        "confidence": float(probs[pred_idx]),
        "fake_prob": float(probs[0]),
        "real_prob": float(probs[1]),
    }


class GradCAM:
    """
    Minimal Grad-CAM implementation targeting the last conv block
    (index 12 in `conv_layers`, the final Conv2d before the last MaxPool).
    Lets the UI show *where* the model is looking, which is genuinely
    useful for a deepfake demo since it visually justifies the verdict.
    """

    def __init__(self, model: DeepfakeCNN):
        self.model = model
        self.gradients = None
        self.activations = None
        # Last Conv2d layer in the conv stack
        target_layer = self.model.conv_layers[12]
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, inp, out):
        self.activations = out.detach()

    def _save_gradient(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()

    def generate(self, img_tensor: torch.Tensor, class_idx: int) -> np.ndarray:
        self.model.zero_grad()
        output = self.model(img_tensor)
        score = output[0, class_idx]
        score.backward()

        gradients = self.gradients[0]          # (C, H, W)
        activations = self.activations[0]      # (C, H, W)
        weights = gradients.mean(dim=(1, 2))   # (C,)

        cam = torch.zeros(activations.shape[1:], dtype=torch.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i]

        cam = F.relu(cam)
        cam -= cam.min()
        if cam.max() > 0:
            cam /= cam.max()
        return cam.numpy()
