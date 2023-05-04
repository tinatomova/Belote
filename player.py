faces = ["A", "K", "Q", "J", "10", "9", "8", "7"]
suits = ["spades", "hearts", "diamonds", "clubs"]
from deck import Card
all_trump = ["J", "9", "A", "10", "K", "Q", "8", "7"]
no_trump = ["A", "10", "K", "Q", "J", "9", "8", "7"]
from deck import sort
class Player():
    def __init__(self, name, robot, team):
        self.name = name
        self.robot = robot
        self.team = team

        self.cards = []
        self.taken_cards = []

        self.carre = []       
        self.quinte = []      
        self.quarte = []
        self.tierce = []
        self.belote = []

    def __repr__(self):
        return self.name
    
    def clear(self):
        self.carre.clear()
        self.quinte.clear()
        self.quarte.clear()
        self.tierce.clear()
        self.belote.clear()

    def from_one_suit(self, cards):
        count = 0
        for suit in suits:
            for c1 in cards:
                for c in self.cards:                
                    if c.face == c1 and c.suit == suit:
                        count += 1
            if count == len(cards):
                return suit
            count = 0
        return None

    def count_face(self, face):
        count = 0
        for c in self.cards:
            if c.face == face:
                count += 1
        return count
    
    def count_suit(self, suit):
        count = 0
        for c in self.cards:
            if c.suit == suit:
                count += 1
        return count
    
    def longest_suit(self):
        suits_count = [0, 0, 0, 0]
        for c in self.cards:
            i = suits.index(c.suit)
            suits_count[i] += 1
        max = suits_count[0]
        index = 0
        for i in range(1, 4):
            if suits_count[i] > max:
                max = suits_count[i]
                index = i
        return suits[index]
    
    def smallest(self, suit):
        for c in self.cards[::-1]:
            if c.suit == suit:
                return c.face
            
    def powerful(self, c, past_cards, contract):
        if contract == "all_trump":
            index = all_trump.index(c.face)
            for face in all_trump[:index]:
                if Card(c.suit, face) not in past_cards:
                    return False
            return True
        
    def suit_without(self, face):
        for suit in suits:
            if Card(suit, face) not in self.cards:
                return suit
        return None



    def trow_card(self, contract, played_cards, trump_committed, past_cards):
        if self.robot == True:
            #played_cards.append(self.cards.pop(0))
            if contract == "all_trump":
                if len(played_cards) == 0:
                    if trump_committed.team == self.team:
                        if len(self.cards) > 3:
                            suit = self.longest_suit()
                            for i in range(len(self.cards)):
                                if self.cards[i].face == "J" and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit) and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            for i in range(len(self.cards)):
                                if self.cards[i].face == "J":
                                    played_cards.append(self.cards.pop(i))
                                    return
                            for i in range(len(self.cards)):
                                if self.powerful(self.cards[i], past_cards, "all_trump") == True:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
                    else:
                        if len(self.cards) > 3:
                            suit = self.longest_suit()
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit) and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            for i in range(len(self.cards)):
                                if self.powerful(self.cards[i], past_cards, "all_trump") == True:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
                elif len(played_cards) == 1 or len(played_cards) == 2:
                    have_from_suit = False
                    for c in self.cards:
                        if c.suit == played_cards[0].suit:
                            have_from_suit = True
                    if have_from_suit:
                        for face in all_trump:
                            for i in range(len(self.cards)):
                                if self.cards[i].face == face and self.cards[i].suit == played_cards[0].suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                    else:
                        suit_to_play = self.suit_without("9")
                        if suit_to_play != None:
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit_to_play) and self.cards[i].suit == suit_to_play:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
                elif len(played_cards) == 3:
                    have_from_suit = False
                    for c in self.cards:
                        if c.suit == played_cards[0].suit:
                            have_from_suit = True
                    if have_from_suit:
                        for i in range(len(self.cards)):
                                if self.cards[i].face == "J" and self.cards[i].suit == played_cards[0].suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        for face in all_trump:
                            if Card(played_cards[0].suit, face) in self.cards:
                                played_cards.append(self.cards.pop(self.cards.index(Card(played_cards[0].suit, face))))
                                return
                    else:
                        suit_to_play = self.suit_without("9")
                        if suit_to_play != None:
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit_to_play) and self.cards[i].suit == suit_to_play:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
            if contract == "no_trump":
                if len(played_cards) == 0:
                    if trump_committed.team == self.team:
                        if len(self.cards) > 3:
                            suit = self.longest_suit()
                            for i in range(len(self.cards)):
                                if self.cards[i].face == "A" and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit) and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            for i in range(len(self.cards)):
                                if self.cards[i].face == "A":
                                    played_cards.append(self.cards.pop(i))
                                    return
                            for i in range(len(self.cards)):
                                if self.powerful(self.cards[i], past_cards, "no_trump") == True:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
                    else:
                        if len(self.cards) > 3:
                            suit = self.longest_suit()
                            for i in range(len(self.cards)):
                                if self.cards[i].face == self.smallest(suit) and self.cards[i].suit == suit:
                                    played_cards.append(self.cards.pop(i))
                                    return
                        else:
                            for i in range(len(self.cards)):
                                if self.powerful(self.cards[i], past_cards, "no_trump") == True:
                                    played_cards.append(self.cards.pop(i))
                                    return
                            played_cards.append(self.cards.pop(len(self.cards) - 1))
                            return
                elif len(played_cards) == 1 or len(played_cards) == 2:
                    played_cards.append(self.cards.pop(0))
                elif len(played_cards) == 3:
                    played_cards.append(self.cards.pop(0))
            else:
                played_cards.append(self.cards.pop(0))
        else:
            print("Choose card from 0 to " + str(len(self.cards) - 1) + ":")
            card_to_trow = input()
            played_cards.append(self.cards.pop(int(card_to_trow)))

    def declarations(self, contract):
        self.find_carre(contract)
        self.find_quinte(contract)
        if len(self.quinte) == 0:
            self.find_quarte(contract)
        self.find_tierce(contract)
        self.find_belote(contract)
    
    def find_carre(self, contract):
        carre = []
        for face in faces:              
            for suit in suits:
                in_cards = False
                for c in self.cards:
                    if c.face == face and c.suit == suit:
                        in_cards = True
                if in_cards == True:
                    carre.append(face)
                    if len(carre) == 4:
                        self.carre.append(face)
                        carre.clear()
                else:
                    carre.clear()
                    break

    def find_quinte(self, contract):
        q = []
        if contract == "all_trump":
            for suit in suits:
                if len(q) == 5:
                    break
                for i in range(4):
                    if len(q) == 5:
                        break
                    for j in range(i, i + 5):
                        in_cards = False
                        for c in self.cards:
                            if c.suit == suit and c.face == faces[j]:
                                in_cards = True
                        if in_cards == True:
                            q.append(Card(suit, faces[j]))
                            if len(q) == 5:
                                self.quinte.append(q[0])
                                break
                        else:
                            q.clear()
                            break
        else:
            suit = contract
            for i in range(4):
                if len(q) == 5:
                    break
                for j in range(i, i + 5):
                    in_cards = False
                    for c in self.cards:
                        if c.suit == suit and c.face == faces[j]:
                            in_cards = True
                    if in_cards == True:
                        q.append(Card(suit, faces[j]))
                        if len(q) == 5:
                            self.quinte.append(q[0])
                            break
                    else:
                        self.quinte.clear()
                        break
    
    def find_quarte(self, contract):
        q = []
        if contract == "all_trump":
            for suit in suits:    
                for i in range(5):                  
                    for j in range(i, i + 4):
                        in_cards = False
                        for c in self.cards:
                            if c.suit == suit and c.face == faces[j]:
                                in_cards = True
                                if len(self.carre) != 0 and self.carre[0] == c.face:
                                    in_cards = False
                        if in_cards:
                            q.append(Card(suit, faces[j]))
                        else:
                            q.clear()
                            break
                    if len(q) == 4:
                        self.quarte.append(q[0])
                        q.clear()
                        break
                if len(q) == 4:
                    self.quarte.append(q)
                    q.clear()
                    break
        else:
            suit = contract
            for i in range(5):                  
                for j in range(i, i + 4):
                    in_cards = False
                    for c in self.cards:
                        if c.suit == suit and c.face == faces[j]:
                            in_cards = True
                            if len(self.carre) != 0 and self.carre[0] == c.face:
                                in_cards = False
                    if in_cards:
                        q.append(Card(suit, faces[j]))
                    else:
                        q.clear()
                        break
                if len(q) == 4:
                    self.quarte.append(q[0])
                    q.clear()
                    break

    def find_tierce(self, contract):
        t = []  
        if contract == "all_trump":
            for suit in suits:                
                if len(self.quinte) > 0 and self.quinte[0].suit == suit:    
                    continue
                if len(self.quarte) > 0 and self.quarte[0].suit == suit:
                    if self.quarte[0].face == "A":
                        count = 0
                        for c in self.cards:
                            if c.face == "9" and c.suit == suit:
                                count += 1
                            if c.face == "8" and c.suit == suit:
                                count += 1
                            if c.face == "7" and c.suit == suit:
                                count += 1
                        if count == 3:
                            self.tierce.append(Card(suit, "9")) 
                            return
                        else:
                            continue
                    elif self.quarte[0].face == "10":
                        count = 0
                        for c in self.cards:
                            if c.face == "A" and c.suit == suit:
                                count += 1
                            if c.face == "K" and c.suit == suit:
                                count += 1
                            if c.face == "Q" and c.suit == suit:
                                count += 1
                        if count == 3:
                            self.tierce.append(Card(suit, "A")) 
                            return
                        else:
                            continue
                    else:
                        continue
                
                for i in range(6):  
                    if len(self.tierce) == 1 and self.tierce[0].suit == suit:
                        if self.tierce[0].face == "A":
                            i = 4
                        elif self.tierce[0].face == "K":
                            i = 5
                        else:
                            break
                    elif len(self.tierce) == 2:
                        break                        
                    for j in range(i, i + 3):      
                        in_cards = False
                        for c in self.cards:
                            if c.suit == suit and c.face == faces[j]:
                                in_cards = True
                                if len(self.carre) != 0 and self.carre[0] == c.face:
                                    in_cards = False
                        if in_cards:
                            t.append(Card(suit, faces[j]))
                            if len(t) == 3:   
                                self.tierce.append(t[0])
                                t.clear()                             
                        else:
                            t.clear()
                            break           
        else:
            suit = contract
            count = 0
            if len(self.quinte) > 0 and self.quinte[0].suit == suit:    
                return
            if len(self.quarte) > 0 and self.quarte[0].suit == suit:
                if self.quarte[0].face == "A":
                    for c in self.cards:
                        if c.face == "9" and c.suit == suit:
                            count += 1
                        if c.face == "8" and c.suit == suit:
                            count += 1
                        if c.face == "7" and c.suit == suit:
                            count += 1
                    if count == 3:
                        self.tierce.append(Card(suit, "9")) 
                        return
                elif self.quarte[0].face == "10":
                    for c in self.cards:
                        if c.face == "A" and c.suit == suit:
                            count += 1
                        if c.face == "K" and c.suit == suit:
                            count += 1
                        if c.face == "Q" and c.suit == suit:
                            count += 1
                    if count == 3:
                        self.tierce.append(Card(suit, "A")) 
                        return
                else:
                    return
            for i in range(6):  
                if len(self.tierce) == 1 and self.tierce[0].suit == suit:
                    if self.tierce[0].face == "A":
                        i = 4
                    elif self.tierce[0].face == "K":
                        i = 5
                    else:
                        break
                elif len(self.tierce) == 2:
                    return        
                for j in range(i, i + 3):      
                    in_cards = False
                    for c in self.cards:
                        if c.suit == suit and c.face == faces[j]:
                            in_cards = True
                            if len(self.carre) != 0 and self.carre[0] == c.face:
                                in_cards = False
                    if in_cards:
                        t.append(Card(suit, faces[j]))
                        if len(t) == 3:   
                            self.tierce.append(t[0])
                            t.clear()                             
                    else:
                        t.clear()
                        break         

    def find_belote(self, contract):
        if contract == "all_trump":
            for suit in suits:
                in_cardsK = False
                in_cardsQ = False
                for c in self.cards:
                    if c.suit == suit and c.face == "K":
                        in_cardsK = True
                    if c.suit == suit and c.face == "Q":
                        in_cardsQ = True
                if in_cardsQ and in_cardsK:
                    self.belote.append(Card(suit, "K"))            
        else:
            suit = contract
            in_cardsK = False
            in_cardsQ = False
            for c in self.cards:
                if c.suit == suit and c.face == "K":
                    in_cardsK = True
                if c.suit == suit and c.face == "Q":
                    in_cardsQ = True
            if in_cardsQ and in_cardsK:
                self.belote.append(Card(suit, "K"))   
        