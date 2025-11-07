import torch
import torch.nn as nn
import torch.optim as optim

import lightning as L
from random import choice, randint

from torchvision import models
from torchvision.datasets import FakeData
from torchvision.transforms.v2 import Compose, Resize, ToImage, ToDtype


fake_images = FakeData(100, (3, 224, 224))

class RandomBackground(nn.Module):
    def forward(self, img):
        background = choice(fake_images)[0]
        x, y = randint(0, background.width-img.width//2), randint(0, background.height-img.height//2)
        background.paste(img, (x, y))
        return background


add_background = Compose([
    Resize((224 * 3 // 4, 224 // 2)),
    RandomBackground(),
    ToImage(),
    ToDtype(torch.float32, scale=True),
])

class lightningClassifier(L.LightningModule):
    def __init__(self, num_classes=52) -> None:
        super().__init__()
        resnet_model = models.resnet18(weights='IMAGENET1K_V1')
        num_ftrs = resnet_model.fc.in_features
        resnet_model.fc = nn.Linear(num_ftrs, num_classes)
        self.model = resnet_model

    def training_step(self, batch, batch_idx):
        x, y = batch
        z = self.model(x)
        loss = nn.functional.cross_entropy(z, y)
        return loss
    
    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
