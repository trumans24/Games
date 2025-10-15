from itertools import product
from typing import Self, List

card_value_dict = {
    'skullking':17,
    'pirate': 16,
    'mermaid': 15,
}
class Card(str):
    color: str
    number: int

    def __new__(cls, value: str) -> Self:
        obj = str.__new__(cls, value)
        color, *number = obj.split('-')
        number = ''.join(number)
        obj.color = color
        obj.number = int(number) if number else (card_value_dict[color] if color in card_value_dict else 0)
        return obj

    def __init__(self, *args, **kwargs) -> None:
        self.color = self.color
        self.number = self.number


colors = 'black', 'yellow', 'green', 'purple'
numbers = tuple(range(14,0, -1))
winning_special = ['skullking'] + ['pirate']*5 + ['mermaid']*2 + ['tigress']
winning_special = [Card(card) for card in winning_special]
lossing_special = ['pass']*5+ ['white_whale'] + ['kraken'] + ['tigress']
lossing_special = [Card(card) for card in lossing_special]

special = winning_special + lossing_special
special.remove(Card('tigress'))
deck = special + ['-'.join([color, str(number)]) for color, number in product(colors, numbers)]
deck = [Card(card) for card in deck]
available_cards = ['skullking', 'pirate', 'mermaid', 'tigress'] + ['-'.join([color, str(number)]) for color, number in product(colors, numbers)] + ['pass', 'white_whale', 'kraken']
available_cards = [Card(card) for card in available_cards]
deckDict = dict(zip(available_cards, range(len(available_cards))))


# num2card = {0: 'skullking-',1: 'pirate-',2: 'mermaid-',3: 'tigress-',4: 'black-14',5: 'black-13',6: 'black-12',7: 'black-11',8: 'black-10',9: 'black-9',10: 'black-8',11: 'black-7',12: 'black-6',13: 'black-5',14: 'black-4',15: 'black-3',16: 'black-2',17: 'black-1',18: 'yellow-14',19: 'yellow-13',20: 'yellow-12',21: 'yellow-11',22: 'yellow-10',23: 'yellow-9',24: 'yellow-8',25: 'yellow-7',26: 'yellow-6',27: 'yellow-5',28: 'yellow-4',29: 'yellow-3',30: 'yellow-2',31: 'yellow-1',32: 'green-14',33: 'green-13',34: 'green-12',35: 'green-11',36: 'green-10',37: 'green-9',38: 'green-8',39: 'green-7',40: 'green-6',41: 'green-5',42: 'green-4',43: 'green-3',44: 'green-2',45: 'green-1',46: 'purple-14',47: 'purple-13',48: 'purple-12',49: 'purple-11',50: 'purple-10',51: 'purple-9',52: 'purple-8',53: 'purple-7',54: 'purple-6',55: 'purple-5',56: 'purple-4',57: 'purple-3',58: 'purple-2',59: 'purple-1',60: 'pass-',61: 'white_whale-',62: 'kraken-',63: 'mermaid- (2)',64: 'pirate- (2)',65: 'pirate- (3)',66: 'pirate- (4)',67: 'pirate- (5)'}

# cv2_transform = transforms.Compose([
#         transforms.ToTensor(),
#         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#     ])
# model = torch.load(r'C:\Users\truma\Projects\Games\model.pt',map_location=torch.device('cpu'))
# _ = model.eval()
# def identify_card(show=False, blur=True):
#     vid = cv2.VideoCapture(0)
#     while(True): 
#         ret, frame = vid.read()
#         top_left = (200, 200)
#         bottom_right = (424, 424)
#         torch_img = cv2_transform(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]])
#         out = model(torch_img.unsqueeze(0)).softmax(-1)
#         index = out.argmax().item()
#         card = num2card[index]
#         confidence = out[0][index]
#         cv2.rectangle(frame,top_left, bottom_right, 255, 2)
#         show_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         if blur:
#             show_img = cv2.blur(show_img, (20, 20))
#         if show:
#             cv2.imshow('frame', show_img)
#             cv2.setWindowTitle('frame', f'Prediction: {card}, confidence: {confidence}, counter: {0}')
#         if confidence > 0.9:
#             cv2.waitKey(10)
#             break
#         if cv2.waitKey(1) & 0xFF == ord('q'): 
#             break
#     cv2.waitKey(10)
#     vid.release()
#     cv2.waitKey(10)
#     cv2.destroyAllWindows()
#     cv2.waitKey(10)
#     return card.split()[0]

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# def cards2vect(number_of_players, cards):
#     card_vector = torch.zeros(len(deckDict))
#     for card in cards:
#         card_vector[deckDict[card]] += 1.0
#     return torch.concat([torch.tensor([number_of_players]), card_vector])

# def vect2cards(vect):
#     return [available_cards[i] for i, card in enumerate(vect) if card > 0]

# def state2cards(state):
#   flat_state = state.squeeze()
#   number_of_players = flat_state[0]
#   a = flat_state[1:len(flat_state)//2]
#   b = flat_state[len(flat_state)//2+1:]
#   cards = vect2cards(a)
#   hand = vect2cards(b)
#   return number_of_players.item(), cards, hand

