from enum import Enum
from dataclasses import dataclass
from typing import List, override
import random
from abc import ABC, abstractmethod

SEED = 27
DECK_SIZE = 52

class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"

class Rank(Enum):
    # access Rank value by Rank.<rank>.value[1] and Rank.ACE.value[1][x] for ACE.
    ACE = (1, [1, 11]) # game value can be 1 or 11
    TWO = (2, [2])
    THREE = (3, [3])
    FOUR = (4, [4])
    FIVE = (5, [5])
    SIX = (6, [6])
    SEVEN = (7, [7])
    EIGHT = (8, [8])
    NINE = (9, [9])
    TEN = (10, [10])
    JACK = (11, [10])
    QUEEN = (12, [10])
    KING = (13, [10])

@dataclass
class Card:
    suit: Suit
    rank: Rank
    def pretty(self)->str:
        return f"{self.rank.name} of {self.suit.value}"

class Deck:
    def __init__(self):
        self.deck = [Card(suit,rank) for suit in Suit for rank in Rank]
        self.discard_pile: List[Card] = []
        assert len(self.deck) == DECK_SIZE, f"Deck is incorrect size: {len(self.deck)}"
        self.shuffle()

    def get_deck(self) -> tuple[Card]:
        return tuple(self.deck)
    
    def draw(self,n:int) -> List[Card]:
        if len(self.deck) < n: 
            raise Exception(f"Want to draw {n} but deck only has {len(self.deck)} cards")
        drawn = []
        for _ in range(n):
            drawn.append(self.deck.pop())
        return drawn

    def discard(self,cards:List[Card]):
        self.discard_pile.extend(cards)

    def merge_discard_and_deck(self):
        self.deck.extend(self.discard_pile)

    def shuffle(self) -> None:
        random.shuffle(self.deck)

class Hand:
    def __init__(self):
        self.hand:List[Card] = []

    def show(self,is_dealer:bool) -> tuple[Card]:
        if is_dealer:
            return tuple(self.hand[:-1])
        return tuple(self.hand)

    def add_cards(self,cards:List[Card]) -> None:
        self.hand.extend(cards)

    def clear_hand(self)->None:
        self.hand.clear()

    def get_sum(self) -> int:
        total = 0
        aces = 0

        for card in self.hand:
            values = card.rank.value[1] 
            if card.rank == Rank.ACE:
                aces += 1
                total += 11 
            else:
                total += values[0] 

        while total > 21 and aces > 0:
            total -= 10  # turn one 11 into a 1
            aces -= 1

        return total       

class Player:
    def __init__(self):
        self.hand = Hand()

    def action(self) -> int:
        raise NotImplementedError
    
class Agent(Player):
    def __init__(self):
        super().__init__()

    @override
    def action(self) -> int:
        print("\nPlayer Action:")
        user_input = input(">")
        action = int(user_input.strip(">"))
        assert action==0 or action==1, "Invalid action"
        return action
    
class Dealer(Player):
    def __init__(self):
        super().__init__()

    @override
    def action(self) -> int:
        if self.hand.get_sum() <= 16:
            return 1 # hit
        return 0 # stand

class Game:
    def __init__(self,episodes:int=100,human_mode:bool=False):
        self.dealer = Dealer()
        self.player = Agent()
        self.deck = Deck()
        self.episodes = episodes
        self.human_mode = human_mode
        self.action_space = ["STAND","HIT"] # 0==stand, 1==hit
        self.game_over = False
        self.round_over = False
        self.points = {
            "PLAYER":0,
            "DEALER":0
        }
    
    def start(self) -> None:
        print("Starting Game...\n")
        for _ in range(self.episodes):
            while not self.game_over:
                self.deal()
                while not self.round_over:
                    print("Dealer:")
                    for card in self.dealer.hand.show(True):
                        print(card.pretty())

                    print("\nPlayer:")
                    for card in self.player.hand.show(False):
                        print(card.pretty())
                    print(f"Total: {self.player.hand.get_sum()}")

                    # decide on action
                    player_action = self.player.action()
                    print(f"Player: {self.action_space[player_action]}\n")

                    dealer_action = self.dealer.action()
                    print(f"Dealer: {self.action_space[dealer_action]}\n")

                    # check player sums
                    player_sum = self.player.hand.get_sum()
                    dealer_sum = self.dealer.hand.get_sum()

                    if player_sum > 21 or dealer_sum > 21:
                        if player_sum > 21 and dealer_sum <= 21:
                            self.points["DEALER"]+=1
                            print("DEALER wins\n")
                        elif dealer_sum > 21:
                            self.points["PLAYER"]+=1
                            print("PLAYER wins\n")
                        self.round_over = True
                        break

                self.deck.discard(self.player.hand.hand)
                self.deck.discard(self.dealer.hand.hand)
                self.player.hand.clear_hand()
                self.dealer.hand.clear_hand()
                
                self.round_over = False
                
                # check len of deck
                if len(self.deck.deck) < 5:
                    self.deck.merge_discard_and_deck()
                    self.deck.shuffle()

                print("\nContinue (y/n)")
                user_input = input(">")
                if user_input.strip(">") == "n":
                    self.game_over = True
                    break

            print(self.points)
            break 
                    
    def deal(self,n=2):
        self.dealer.hand.add_cards(self.deck.draw(n))
        self.player.hand.add_cards(self.deck.draw(n))

    def get_env():
        pass

    def get_obs():
        pass


if __name__ == "__main__":
    game = Game()
    game.start()