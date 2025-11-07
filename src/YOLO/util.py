from PIL import Image
from torch import randint as randi, uint8, zeros_like
from random import choice, randint
from pathlib import Path
from torch.nn import Module
from torchvision.transforms.functional import to_pil_image, pil_to_tensor
from torchvision.transforms.v2 import Compose, RandomResize, ColorJitter, RandomRotation, RandomPerspective, RandomResizedCrop, Resize


def fake_image(height, width, channel=3, PIL=True):
    if PIL:
        return to_pil_image(randi(0, 255, (channel, height, width), dtype=uint8))
    return randi(0, 255, (channel, height, width), dtype=uint8)

class CombineImages(Module):
    def forward(self, imgs):
        background = fake_image(224, 224)
        for img in imgs:
            x = randint(0, background.width - img.width)
            y = randint(0, background.height - img.height)
            background.paste(img, (x, y))
        return background

class CombineCards(Module):
    def forward(self, samples):
        background = fake_image(224, 224)
        labels = []
        for img, label in samples:
            x = randint(0, background.width - img.width)
            y = randint(0, background.height - img.height)
            cx = (x + img.width // 2) / background.width
            cy = (y + img.height // 2) / background.height
            labels.append(f'{label} {cx} {cy} {img.width / background.width} {img.height / background.height}')  # class cx cy width height
            background.paste(img, (x, y))
        return background, '\n'.join(labels)

class AddBackground(Module):
    def __init__(self, source, size=640, PIL=True) -> None:
        super().__init__()
        self.width = size
        self.height = size
        self.PIL = PIL
        self.background = RandomBackground(source)

    def forward(self, samples):
        background = pil_to_tensor(self.background())
        labels = []
        for img, label in samples:
            height, width = img.height, img.width
            x = randint(0, self.width-width)
            y = randint(0, self.height-height)
            img = pil_to_tensor(img)
            mask = zeros_like(background)
            mask[:, y:y+height, x:x+width] = img
            background[:, (mask >  0).any(0)] = 0
            background = mask | background
            cx = (x + width // 2) / self.width
            cy = (y + height // 2) / self.height
            labels.append(f'{label} {cx} {cy} {width / self.width} {height / self.height}')  # class cx cy width height
        if self.PIL:
            return to_pil_image(background), '\n'.join(labels)
        return background, '\n'.join(labels)
    
class AddBackground_v3(Module):
    def __init__(self, width=640, height=640, PIL=True) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.PIL = PIL
        self.card_transform = Compose([
            RandomResize(50, 224),
            ColorJitter(brightness=(0.5, 1.0), contrast=(0.5, 1.0)),
            RandomRotation(30, expand=True),
            RandomPerspective(0.3),
        ])

    def forward(self, samples, background):
        background = pil_to_tensor(background) #(self.height, self.width, PIL=False)
        labels = []
        for img, label in samples:
            img = self.card_transform(img)
            height, width = img.height, img.width
            x = randint(0, self.width-width)
            y = randint(0, self.height-height)
            img = pil_to_tensor(img)
            mask = zeros_like(background)
            mask[:, y:y+height, x:x+width] = img
            background[:, (mask >  0).any(0)] = 0
            background = mask | background
            cx = (x + width // 2) / self.width
            cy = (y + height // 2) / self.height
            labels.append(f'{label} {cx} {cy} {width / self.width} {height / self.height}')  # class cx cy width height
        if self.PIL:
            return to_pil_image(background), '\n'.join(labels)
        return background, '\n'.join(labels)

def read_root(root, size=None, labels=None):
    if size is not None:
        resize = Resize(size)
    imgs = []
    for path in root.glob('**/*.jpg'):
        with open(path, "rb") as f:
            img = Image.open(f)
            if size is not None:
                img = resize(img)
            if labels is not None:
                imgs.append(((img.convert("RGB")), labels.index(path.stem)))
            else:
                imgs.append(img.convert("RGB"))
    return imgs


class RandomBackground(Module):
    def __init__(self, source, size=640, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.files = list(Path(source).glob('*.jpg'))
        self.crop = RandomResizedCrop(size)
    
    def forward(self):
        path = choice(self.files)
        with open(path, "rb") as f:
            img = Image.open(f)
            return self.crop(img.convert("RGB"))