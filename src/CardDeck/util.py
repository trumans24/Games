import torch
import torch.nn as nn
from random import choice, randint

import lightning as L
import torch.optim as optim

from torchvision import models
from torchvision.datasets import ImageFolder, FakeData
from torchvision.transforms.v2 import Compose, Resize, ToImage, ToDtype

channel = 3
width = 224
height = 224
fake_images = FakeData(1000, (channel, width, height))

class RandomBackground(torch.nn.Module):
    def forward(self, img):
        background = choice(fake_images)[0]
        x, y = randint(0, background.width-img.width//2), randint(0, background.height-img.height//2)
        background.paste(img, (x, y))
        return background


add_background = Compose([
    Resize(112),
    RandomBackground(),
    ToImage(),
    ToDtype(torch.float32, scale=True),
])

class lightningClassifier(L.LightningModule):
    def __init__(self, model) -> None:
        super().__init__()
        self.model = model

    def training_step(self, batch, batch_idx):
        x, y = batch
        z = self.model(x)
        loss = nn.functional.cross_entropy(z, y)
        # self.log("my_loss", loss, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        z = self.model(x)
        num_correct = (y == z.argmax(-1)).sum()
        self.log("num_correct", num_correct, prog_bar=True)
        return num_correct
    
    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
