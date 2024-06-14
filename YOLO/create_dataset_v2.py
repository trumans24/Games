"""
python create_dataset_v2.py /home/trumanss/CodeProject/Games/data/playing_cards -d dataset/object_detection_v2/ --train 10000 --val 3000
"""
import argparse
from tqdm import trange
from util import AddBackground
from random import choice, randint
from pathlib import Path
from torch.nn import Module
from torchvision.datasets import ImageFolder, FakeData
from torchvision.transforms.v2 import Resize, Compose, RandomResize, ColorJitter, RandomRotation, RandomPerspective

# Initialize parser
parser = argparse.ArgumentParser(prog='test', description='Testing functionality of argparse', epilog='I am exploring argparse and I need to understand what is happening')
parser.add_argument('source', help="Specify the root of the directory with images of cards and which must follow pytorch's convention for ImageFolder.")
parser.add_argument('-b', '--background', default='../data/sample_images', help="Specify the root of the directory random background images can be found.")
parser.add_argument('-d', '--destination', default='dataset/object_detection/', help="Specify the root of the directory where the dataset should be saved.")
parser.add_argument('--train', type=int, default=100, help="Specify how many sample to make for the training dataset")
parser.add_argument('--val', type=int, default=10, help="Specify how many sample to make for the validation dataset")
parser.add_argument('--test', type=int, default=0, help="Specify how many sample to make for the testing dataset")

# Read arguments from command line
args = parser.parse_args()

card_transform = Compose([
    RandomResize(50, 112),
    ColorJitter(brightness=(0.5, 1.0), contrast=(0.5, 1.0)),
    RandomRotation(30, expand=True),
    RandomPerspective(0.3),
])

cards = ImageFolder(args.source, transform=card_transform)
dst = Path(args.destination)

resize = Resize(112)
combine_cards = AddBackground(args.background)

for group in [g for g in ['train', 'val', 'test'] if vars(args)[g] > 0]:
    images_dir = dst / 'images' / group
    labels_dir = dst / 'labels' / group
    
    if not images_dir.is_dir():
        images_dir.mkdir(parents=True)
    if not labels_dir.is_dir():
        labels_dir.mkdir(parents=True)

    for i in trange(vars(args)[group]):
        card_sample = []
        num_cards = randint(1, 3)
        for _ in range(num_cards):
            img, label = choice(cards)
            img = resize(img)
            card_sample.append((img, label))
        img, label = combine_cards(card_sample)
        img_file = images_dir / f'img{str(i).rjust(9, '0')}.jpg'
        label_file = labels_dir / f'img{str(i).rjust(9, '0')}.txt'
        img.save(img_file, "JPEG")
        img.close()
        with open(label_file, 'w') as f:
            f.write(label)

import yaml

if args.test:
    data = {
        'path':f'../{dst.relative_to(dst.parents[1])}',
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': dict(zip(range(len(cards.classes)), cards.classes))
        }
else:
    data = {
        'path':f'../{dst.relative_to(dst.parents[1])}',
        'train': 'images/train',
        'val': 'images/val',
        'names': dict(zip(range(len(cards.classes)), cards.classes))
        }
    
with open(dst/'data.yaml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)