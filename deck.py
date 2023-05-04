import random

suits = ["spades", "hearts", "diamonds", "clubs"]
suits_rank = {"spades":0, "hearts":1, "diamonds":2, "clubs":3}
faces = ["A", "K", "Q", "J", "10", "9", "8", "7"]
all_trump = {"J":20, "9":14, "A":11, "10":10, "K":4, "Q":3, "8":0, "7":-1}
no_trump = {"A":11, "10":10, "K":4, "Q":3, "J":2, "9":0, "8":-1, "7":-2}


class Card():
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return self.suit + " " + self.face
    
    def __lt__(self, other):
        if no_trump[self.face] < no_trump[other.face]:
            return True
        if no_trump[self.face] == no_trump[other.face]:
            if suits_rank[self.suit] > suits_rank[other.suit]:
                return True
        return False
    
    def __eq__(self, other):
        if self.suit == other.suit and self.face == other.face:
            return True
        return False
    
    
class Deck(list):
    def __init__(self):
        super().__init__()
        [[self.append(Card(s, f)) for f in faces] for s in suits]
        
    def shuffle(self):
        random.shuffle(self)

    def deal(self, number_of_cards, player):
        for _ in range(number_of_cards):   
            player.cards.append(self.pop(0))
                   

def sort(cards, contract):
    if contract == "face":
        for i in range(len(cards) - 1):
            for j in range(len(cards) - i - 1):
                if faces.index(cards[j].face) > faces.index(cards[j + 1].face):
                    cards[j], cards[j + 1] = cards[j + 1], cards[j]
        return
    for i in range(len(cards) - 1):
        for j in range(len(cards) - i - 1):
            if cards[j].suit != contract and cards[j + 1].suit != contract:
                if suits_rank[cards[j].suit] > suits_rank[cards[j + 1].suit]:
                    cards[j], cards[j + 1] = cards[j + 1], cards[j]
            if cards[j].suit != contract and cards[j + 1].suit == contract:
                cards[j], cards[j + 1] = cards[j + 1], cards[j]
            if suits_rank[cards[j].suit] == suits_rank[cards[j + 1].suit]:
                if contract == "all_trump":
                    if all_trump[cards[j].face] < all_trump[cards[j + 1].face]:
                        cards[j], cards[j + 1] = cards[j + 1], cards[j]
                elif contract == "no_trump":
                    if no_trump[cards[j].face] < no_trump[cards[j + 1].face]:
                        cards[j], cards[j + 1] = cards[j + 1], cards[j]
                else:
                    if cards[j].suit == contract:
                        if all_trump[cards[j].face] < all_trump[cards[j + 1].face]:
                            cards[j], cards[j + 1] = cards[j + 1], cards[j]
                    else:
                        if no_trump[cards[j].face] < no_trump[cards[j + 1].face]:
                            cards[j], cards[j + 1] = cards[j + 1], cards[j]

def cut(cards):
        cards_to_cut = random.randint(3, 29)
        for _ in range(cards_to_cut):
            card_to_cut = cards[0]
            cards.pop(0)
            cards.append(card_to_cut)
