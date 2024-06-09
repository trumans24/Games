import torch
import torch.nn as nn
from random import choice, randint

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
    Resize((height * 3 // 4, width // 2)),
    RandomBackground(),
    ToImage(),
    ToDtype(torch.float32, scale=True),
])

cards_with_background = ImageFolder('data/playing_cards', transform=add_background)
n_classes = len(cards_with_background.classes)
n_repeat = 100
large_dataset = torch.utils.data.ConcatDataset([cards_with_background] * n_repeat)
train_loader = torch.utils.data.DataLoader(large_dataset, batch_size=n_classes, shuffle=True, num_workers=50)
val_loader = torch.utils.data.DataLoader(cards_with_background, batch_size=n_classes, shuffle=False, num_workers=50)

import lightning as L
import torch.optim as optim

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
        acc = (y == z.argmax(-1)).sum() / n_classes
        self.log("acc", acc, prog_bar=True)
        return acc
    
    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

model_ft = models.resnet18(weights='IMAGENET1K_V1')
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, len(cards_with_background.classes))

classifier = lightningClassifier(model_ft)

trainer = L.Trainer(max_epochs=10)
trainer.fit(model=classifier, train_dataloaders=train_loader, val_dataloaders=val_loader)