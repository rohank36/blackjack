from enum import Enum
from dataclasses import dataclass
from typing import List
import random

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

class Deck:
    def __init__(self):
        self.deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        assert len(self.deck) == DECK_SIZE, f"Deck is incorrect size: {len(self.deck)}"
        self.shuffle()

    def get_deck(self) -> tuple[Card, ...]:
        return tuple(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

class Hand:
    def __init__(self):
        self.hand:List[Card] = []

    def draw(self, n:int):
        pass

    def get_sum(self):
        pass       

class Game:
    def __init__(self):
        self.dealer = Hand()
        self.player = Hand()
        self.deck = Deck()

    def deal(self,n=2):
        self.dealer.draw(n)
        self.player.draw(n)

    def get_env():
        pass

    def get_obs():
        pass

    def get_actions():
        pass


#print(f"{Rank.JACK.name} {Rank.JACK.value} {Rank.JACK.value[1]}")