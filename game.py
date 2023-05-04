import deck
from player import Player
from deck import sort
from deck import cut
from deck import no_trump
from deck import all_trump
from deck import suits_rank
from deck import faces
from deck import suits

trump_rank = {"pass":0, "clubs":1, "diamonds":2, "hearts":3, "spades":4, "no_trump":5, "all_trump":6}
    
class Game():
    def __init__(self, players):
        self.players = players
        self.score_team0 = 0       
        self.score_team1 = 0        
        self.playing_deck = deck.Deck()
        self.playing_deck.shuffle()
        self.first_deal = 1
        self.hanging_points = 0
        
        self.current_score_team0 = 0
        self.current_score_team1 = 0
        self.contract = "pass"   
        self.double = 0   
        self.trump_committed = players[0]
        self.team0_declarations = [[],[],[],[],[]]
        self.team1_declarations = [[],[],[],[],[]]
        self.last_taken = self.players[0]


    def choosing_first(self):
        for p in self.players:
            self.playing_deck.deal(1, p)
            print(p.name + ": " + p.cards[0].face + " " + p.cards[0].suit)
        max = self.players[0].cards[0]
        dealer = self.players[0]
        for i in range(1, 4):
            if no_trump[self.players[i].cards[0].face] > no_trump[max.face]:
                max = self.players[i].cards[0]
                dealer = self.players[i]
            elif no_trump[self.players[i].cards[0].face] == no_trump[max.face] and suits_rank[self.players[i].cards[0].suit] < suits_rank[max.suit]:
                max = self.players[i].cards[0]
                dealer = self.players[i]
        print('\n')
        print("Dealer is: " + dealer.name + "\n")
        while self.players[3] != dealer:
            self.players.append(self.players.pop(0))
        for p in self.players:
            self.playing_deck.extend(p.cards)
            p.cards.clear()

    def dealing(self):
        if not self.first_deal:
            self.players.append(self.players.pop(0))
        if self.first_deal:
            self.choosing_first()
            self.first_deal = 0
        cut(self.playing_deck)
        first_player = self.players[0]
        for p in self.players:
            self.playing_deck.deal(3, p)
        for p in self.players:
            self.playing_deck.deal(2, p)
            sort(p.cards, "no_trump")
            if p.robot == False:
                print("Your cards: ")
                print(p.cards)
                print('\n')
        self.choosing_trump()
        while self.players[0] != first_player:
            self.players.append(self.players.pop(0))
        if self.contract != "pass":
            print("-" * 182)
            for p in self.players:
                self.playing_deck.deal(3, p)
                sort(p.cards, self.contract)
                if p.robot == False:
                    print("Your cards: ")
                    print(p.cards)
        else:
            for p in self.players:
                self.playing_deck.extend(p.cards)
                p.cards.clear()
            self.dealing()

    def choosing_trump(self):
        current_trump = "pass"
        decision = "pass"
        count_of_pass = 0
        while True:
            if current_trump == "all_trump" and self.double == 2:
                break
            if count_of_pass == 4 and current_trump == "pass":
                break
            if count_of_pass == 3 and current_trump != "pass":
                break 
            for p in self.players:
                if p.robot == False:
                    decision = input()
                    if decision != "double" and decision != "re-double":
                        while decision != "pass" and trump_rank[decision] < trump_rank[current_trump]:
                            decision = input()
                    while decision == "double" or decision =="re-double" and current_trump == "pass":
                        decision = input()
                else:
                    decision = "pass"
                    if p.count_face("J") > 2:
                        decision = "all_trump"       
                    elif p.count_face("J") > 1 and p.count_face("9") > 1:
                        if p.from_one_suit(["J", "9"]) != None:
                            decision = "all_trump"
                    elif p.from_one_suit(["9", "A", "10"]) != None and p.count_face("J") > 1:
                        decision = "all_trump"                 
                    elif p.from_one_suit(["9", "10", "K"]) != None and p.count_face("J") > 1:
                        decision = "all_trump"               
                    elif p.count_face("A") > 2:                      
                        decision = "no_trump"           
                    elif p.count_face("A") > 1 and p.count_face("10") > 1:
                        if p.from_one_suit(["A", "10"]) != None:                           
                            decision = "no_trump"
                    elif p.count_face("A") > 1 and p.from_one_suit(["10", "K", "Q"]) != None:                        
                        decision = "no_trump"                            
                    elif p.count_face("A") > 1 and p.from_one_suit(["A", "10", "K"]) != None and p.from_one_suit(["A", "10", "K", "J"]) == None:                        
                        decision = "no_trump"                       
                    elif p.from_one_suit(["J", "9", "A"]) != None:
                        suit = p.from_one_suit(["J", "9", "A"])
                        decision = suit                        
                    elif p.from_one_suit(["J", "9", "10"]) != None:
                        suit = p.from_one_suit(["J", "9", "10"])                        
                        decision = suit                          
                    elif p.from_one_suit(["9", "A", "10", "K"]) != None and p.count_face("A") > 1:
                        suit = p.from_one_suit(["9", "A", "10", "K"])                       
                        decision = suit                           
                    elif p.from_one_suit(["J", "9"]) != None and p.count_face("A") > 1:
                        suit = p.from_one_suit(["J", "9"])
                        if p.count_suit(suit) > 2:                            
                            decision = suit                                
                    elif p.from_one_suit(["J", "10"]) != None and p.count_face("A") > 1:
                        suit = p.from_one_suit(["J", "10"])
                        if p.count_suit(suit) > 2:                            
                            decision = suit                                
                    elif p.from_one_suit(["J", "9"]) != None:
                        suit = p.from_one_suit(["J", "9"])
                        if p.count_suit(suit) > 3:                        
                            decision = suit                              
                    else:
                        decision = "pass"
                
                if trump_rank[current_trump] > trump_rank[decision]:
                    decision = "pass"    
                if current_trump == decision and decision != "pass" and self.trump_committed.team != p.team and self.double == 0:
                    decision = "double"
                if current_trump == decision and decision != "pass" and self.trump_committed.team == p.team and self.double == 1:
                    decision = "re-double"
                print(p.name + ": " + decision)
                                      
                if decision == "pass":
                    count_of_pass += 1
                    if count_of_pass == 3 and current_trump != "pass":
                        break
                    if count_of_pass == 4 and current_trump == "pass":
                        break
                elif decision == "double":
                    self.double = 1
                    count_of_pass = 0
                elif decision == "re-double":
                    self.double = 2
                    count_of_pass = 0
                    if current_trump == "all_trump" and self.double == 2:
                        break
                else:
                    count_of_pass = 0
                    current_trump = decision
                    self.trump_committed = p
                    self.double = 0
            
            self.contract = current_trump
            print("Contract: " + self.contract + "\n")  
            

    def declarations(self):
        for i in range(5):
            self.team0_declarations[i].clear()
            self.team1_declarations[i].clear()
        if self.contract == "no_trump":
            return
        for p in self.players:
            p.declarations(self.contract)       
        for p in self.players:
            if p.team == "team0":
                self.team0_declarations[0].extend(p.carre)
                self.team0_declarations[1].extend(p.quinte)
                self.team0_declarations[2].extend(p.quarte)
                self.team0_declarations[3].extend(p.tierce)
                self.team0_declarations[4].extend(p.belote)
            else:
                self.team1_declarations[0].extend(p.carre)
                self.team1_declarations[1].extend(p.quinte)
                self.team1_declarations[2].extend(p.quarte)
                self.team1_declarations[3].extend(p.tierce)
                self.team1_declarations[4].extend(p.belote)
        for i in range(5):
            sort(self.team0_declarations[i], "face")
            sort(self.team1_declarations[i], "face")
        for j in range(4):
            if len(self.team0_declarations[j]) == 0 and len(self.team1_declarations[j]) > 0:
                for i in range(4):
                    self.team0_declarations[i].clear()
            elif len(self.team0_declarations[j]) > 0 and len(self.team1_declarations[j]) == 0:
                for i in range(4):
                    self.team1_declarations[i].clear()
            elif len(self.team0_declarations[j]) > 0 and len(self.team1_declarations[j]) > 0:
                if faces.index(self.team0_declarations[j][0].face) > faces.index(self.team1_declarations[j][0].face):
                    for i in range(4):
                        self.team0_declarations[i].clear()
                elif faces.index(self.team0_declarations[j][0].face) < faces.index(self.team1_declarations[j][0].face):
                    for i in range(4):
                        self.team1_declarations[i].clear()
                else:
                    if trump_rank[self.team0_declarations[j][0].suit] > trump_rank[self.team1_declarations[j][0].suit]:
                        for i in range(4):
                            self.team1_declarations[i].clear()
                    else:
                        for i in range(4):
                            self.team0_declarations[i].clear()

        print("\n" + "carre: quinte: quarte: tierce: belote:")
        print("Team0:")
        print(self.team0_declarations)
        print("Team1:")
        print(self.team1_declarations)
        print("\n")
    
    def choosing_winner(self, cards):
        winning_suit = []
        index = 0
        for card in cards:
            if card.suit == cards[0].suit:
                winning_suit.append(card)
        if self.contract == "all_trump":
            sort(winning_suit, "all_trump")
            index = cards.index(winning_suit[0])
        elif self.contract == "no_trump":
            sort(winning_suit, "no_trump")
            index = cards.index(winning_suit[0])
        else:
            if winning_suit[0].suit == self.contract:
                sort(winning_suit, "all_trump")
                index = cards.index(winning_suit[0])
            else:
                trumps = []
                for card in cards:
                    if card.suit == self.contract:
                        trumps.append(card)
                if len(trumps) == 0:
                    sort(winning_suit, "no_trump")
                    index = cards.index(winning_suit[0])
                else:
                    sort(trumps, "all_trump")
                    index = cards.index(trumps[0])
        return index

    def score_calculation(self):
        self.current_score_team0 = 0
        self.current_score_team1 = 0
        for i in range(3, 5):      
            for declaration in self.team0_declarations[i]:                
                self.current_score_team0 += 20
        for declaration in self.team0_declarations[2]:      
            self.current_score_team0 += 50
        for declaration in self.team0_declarations[1]:      
            self.current_score_team0 += 100
        for declaration in self.team0_declarations[0]:
            if declaration == "J":
                self.current_score_team0 += 200
            elif declaration == "9":
                self.current_score_team0 += 150
            elif declaration == "A" or declaration == "10" or declaration == "K" or declaration == "Q":
                self.current_score_team0 += 100
        for i in range(3, 5):      
            for declaration in self.team1_declarations[i]:                
                self.current_score_team1 += 20
        for declaration in self.team1_declarations[2]:      
            self.current_score_team1 += 50
        for declaration in self.team1_declarations[1]:      
            self.current_score_team1 += 100
        for declaration in self.team1_declarations[0]:
            if declaration == "J":
                self.current_score_team1 += 200
            elif declaration == "9":
                self.current_score_team1 += 150
            elif declaration == "A" or declaration == "10" or declaration == "K" or declaration == "Q":
                self.current_score_team1 += 100
        for p in self.players:
            p.clear()
        if len(self.players[0].taken_cards) + len(self.players[2].taken_cards) == 0:           
            if self.players[0].team == "team0":
                if self.contract == "all_trump":
                    self.current_score_team1 += 350
                if self.contract =="no_trump":
                    self.current_score_team1 += 440
                else:
                    self.current_score_team1 += 250
            else:
                if self.contract == "all_trump":
                    self.current_score_team0 += 350
                if self.contract =="no_trump":
                    self.current_score_team0 += 440
                else:
                    self.current_score_team0 += 250
        elif len(self.players[1].taken_cards) + len(self.players[3].taken_cards) == 0:
            if self.players[1].team == "team0":
                if self.contract == "all_trump":
                    self.current_score_team1 += 350
                if self.contract =="no_trump":
                    self.current_score_team1 += 440
                else:
                    self.current_score_team1 += 250
            else:
                if self.contract == "all_trump":
                    self.current_score_team0 += 350
                if self.contract =="no_trump":
                    self.current_score_team0 += 440
                else:
                    self.current_score_team0 += 250
        else:  
            for p in self.players:
                
                score_player = 0
                if p == self.last_taken:
                    score_player += 10
                for card in p.taken_cards:                   
                    if self.contract == "all_trump":
                        if all_trump[card.face] > 0:
                            score_player += all_trump[card.face]
                    elif self.contract == "no_trump":
                        if no_trump[card.face] > 0:
                            score_player += no_trump[card.face]
                    else:
                        if card.suit == self.contract:
                            if all_trump[card.face] > 0:
                                score_player += all_trump[card.face]
                        else:
                            if no_trump[card.face] > 0:
                                score_player += no_trump[card.face]
                if self.contract == "no_trump":
                    score_player *= 2
                if p.team == "team0":
                    self.current_score_team0 += score_player
                else:
                    self.current_score_team1 += score_player
        for p in self.players:
            self.playing_deck.extend(p.taken_cards)
            p.taken_cards = []
        if self.trump_committed.team == "team0":
            if self.current_score_team0 > self.current_score_team1:
                self.score_team0 += self.current_score_team0
                self.score_team0 += self.hanging_points
                self.hanging_points = 0
                self.score_team1 += self.current_score_team1               
            elif self.current_score_team0 < self.current_score_team1:
                self.score_team1 += self.current_score_team1
                self.score_team1 += self.current_score_team0
                self.score_team1 += self.hanging_points
                self.hanging_points = 0
            else:
                self.score_team1 += self.current_score_team1
                self.hanging_points = self.current_score_team0
        else:
            if self.current_score_team0 < self.current_score_team1:
                self.score_team0 += self.current_score_team0
                self.score_team1 += self.current_score_team1
                self.score_team1 += self.hanging_points
                self.hanging_points = 0
            elif self.current_score_team0 > self.current_score_team1:
                self.score_team0 += self.current_score_team1
                self.score_team0 += self.current_score_team0
                self.score_team0 += self.hanging_points
                self.hanging_points = 0
            else:
                self.score_team0 += self.current_score_team0
                self.hanging_points = self.current_score_team1
        print("Team0: " + str(self.current_score_team0))
        print("Team1: " + str(self.current_score_team1))

    def acting(self):
        while self.score_team0 < 1510 and self.score_team1 < 1510:
            print("*" * 182)
            self.dealing() 
            self.declarations()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            played_cards = []
            past_cards = []
            while self.players[0].cards:
                for p in self.players:
                    p.trow_card(self.contract, played_cards, self.trump_committed, past_cards)
                    print(p.name + ": " + played_cards[-1].face + " " + played_cards[-1].suit)
                past_cards.extend(played_cards)
                winner = self.choosing_winner(played_cards)  
                print(players[winner].name + " takes cards!" + "\n")             
                self.players[winner].taken_cards.extend(played_cards)                
                played_cards = []
                if len(self.players[0].cards) == 0:
                    self.last_taken = self.players[winner] 
                for _ in range(winner):
                    self.players.append(self.players.pop(0))              
            self.score_calculation()
            print("*" * 182)
            print("Team0: " + str(self.score_team0))
            print("Team1: " + str(self.score_team1))
    
    
    


    
p0 = Player("player1", False, "team0")
p1 = Player("player2", True, "team1")
p2 = Player("player3", True, "team0")
p3 = Player("player4", True, "team1")

players = [p0, p1, p2, p3]
g = Game(players)

g.acting()
