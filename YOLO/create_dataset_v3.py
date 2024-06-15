"""
python create_dataset_v3.py /home/trumanss/CodeProject/Games/data/playing_cards -d dataset/object_detection_v3/ --train 10000 --val 3000
"""
import argparse
from tqdm import trange
from util import AddBackground_v3, read_root
from random import choice, sample, randint
from pathlib import Path
from torch.nn import Module
from torchvision.datasets import ImageFolder, FakeData
from torchvision.transforms.v2 import Resize, Compose, RandomResize, ColorJitter, RandomRotation, RandomPerspective, RandomResizedCrop

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

card_classes = ImageFolder(r'../data/playing_cards').classes
cards = read_root(Path(args.source), size=224, labels=card_classes)
random_background = read_root(Path(args.background), size=640)
dst = Path(args.destination)

rcrop = RandomResizedCrop(640)
combine_cards = AddBackground_v3()

for group in [g for g in ['train', 'val', 'test'] if vars(args)[g] > 0]:
    images_dir = dst / 'images' / group
    labels_dir = dst / 'labels' / group
    
    if not images_dir.is_dir():
        images_dir.mkdir(parents=True)
    if not labels_dir.is_dir():
        labels_dir.mkdir(parents=True)

    for i in trange(vars(args)[group]):
        num_cards = randint(1, 3)
        card_sample = sample(cards, randint(1, 4))
        img, label = combine_cards(card_sample, rcrop(choice(random_background)))
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
        'names': dict(zip(range(len(card_classes)), card_classes))
        }
else:
    data = {
        'path':f'../{dst.relative_to(dst.parents[1])}',
        'train': 'images/train',
        'val': 'images/val',
        'names': dict(zip(range(len(card_classes)), card_classes))
        }
    
with open(dst/'data.yaml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)