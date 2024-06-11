from torch import randint as randi, uint8
from random import choice, randint
from torch.nn import Module
from torchvision.datasets import FakeData
from torchvision.transforms.functional import to_pil_image

class CombineImages(Module):
    def forward(self, imgs):
        background = to_pil_image(randi(0, 255, (3, 224, 224), dtype=uint8))
        for img in imgs:
            x = randint(0, background.width - img.width)
            y = randint(0, background.height - img.height)
            background.paste(img, (x, y))
        return background

class CombineCards(Module):
    def forward(self, samples):
        background = to_pil_image(randi(0, 255, (3, 224, 224), dtype=uint8))
        labels = []
        for img, label in samples:
            x = randint(0, background.width - img.width)
            y = randint(0, background.height - img.height)
            cx = (x + img.width // 2) / background.width
            cy = (y + img.height // 2) / background.height
            labels.append(f'{label} {cx} {cy} {img.width / background.width} {img.height / background.height}')  # class cx cy width height
            background.paste(img, (x, y))
        return background, '\n'.join(labels)
