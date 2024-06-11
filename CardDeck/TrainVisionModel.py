from util import add_background, lightningClassifier
from torch.nn import Linear
from lightning import Trainer
from torchvision.models import resnet18
from torch.utils.data import DataLoader, ConcatDataset
from torchvision.datasets import ImageFolder

cards_with_background = ImageFolder('data/playing_cards', transform=add_background)
n_classes = len(cards_with_background.classes)
n_repeat = 100
large_dataset = ConcatDataset([cards_with_background] * n_repeat)
train_loader = DataLoader(large_dataset, batch_size=n_classes, shuffle=True, num_workers=50)
val_loader = DataLoader(cards_with_background, batch_size=n_classes, shuffle=False, num_workers=50)

model_ft = resnet18(weights='IMAGENET1K_V1')
num_ftrs = model_ft.fc.in_features
model_ft.fc = Linear(num_ftrs, len(cards_with_background.classes))

classifier = lightningClassifier(model_ft)

trainer = Trainer(max_epochs=10)
trainer.fit(model=classifier, train_dataloaders=train_loader, val_dataloaders=val_loader)