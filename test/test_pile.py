from __future__ import annotations
import unittest

from typing import List, Optional
from terra_futura.simple_types import GridPosition, Resource
from terra_futura.interfaces import InterfaceCard, Effect
from terra_futura.pile import Pile, Shuffle

class CardFake(InterfaceCard):
    def __init__(self, index: int) ->None:
        # Attributes
        self.resources: List[Resource] = []
        self.pollutionSpacesL: int = 0

        self.index = index

        # Multiplicity 0..1 — may be None or an Effect instance
        self.upperEffect: Optional[Effect] = None
        self.lowerEffect: Optional[Effect] = None

    # --- Interface methods ---
#not used
    def isActive(self) -> bool:
        return True

    def canPutResources(self, resources: List[Resource]) -> bool:
        return True

    def putResources(self, resources: List[Resource]) -> None:
        pass

    def canGetResources(self, resources: List[Resource]) -> bool:
        return True

    def getResources(self, resources: List[Resource]) -> None:
        pass

    def canPlacePollution(self, amount: int = 1) -> bool:
        return False

    def placePollution(self, amount: int = 1) -> None:
        pass


    def check(self, input: List[Resource], output: List[Resource], pollution: int) -> bool:
        return True

    def checkLower(self, input: List[Resource], output: List[Resource], pollution: int) -> bool:
        return True

    def hasAssistance(self) -> bool:
        return True

    def state(self) -> str:
        return str(self.index)


class TestPile(unittest.TestCase):
    def setUp(self) ->None:
        
        self.allCards:List[InterfaceCard] = []

        self.shufflerSetSeet = Shuffle(1)


        self.numCards = 20

        for i in range(self.numCards):
            card = CardFake(i)
            self.allCards.append(card)






    def test_visible_cards(self) ->None:
        pile = Pile(self.allCards,self.shufflerSetSeet)
        
        target = [4, 18, 2, 8]
        current = []

        for i in range(1,5):
            card = pile.getCard(i)
            if card is not None:
                current.append(int(card.state()))

        self.assertEqual(target, current)

    def test_visible_cards_after_removing(self) ->None:
        pile = Pile(self.allCards,self.shufflerSetSeet)
        
        target = [3, 4, 18, 2]
        current = []

        pile.removeLastCard()

        for i in range(1,5):
            card = pile.getCard(i)
            if card is not None:
                current.append(int(card.state()))

        self.assertEqual(target, current)


    def test_visible_cards_after_taking(self) ->None:
        pile = Pile(self.allCards,self.shufflerSetSeet)
        
        target = [3, 4, 18, 8]
        current = []

        pile.takeCard(3)

        for i in range(1,5):
            card = pile.getCard(i)
            if card is not None:
                current.append(int(card.state()))

        self.assertEqual(target, current)

    def test_discard_n_cards(self) -> None:
        pile = Pile(self.allCards,self.shufflerSetSeet)
        n = 10

        target = [3, 4, 18, 2]
        current = []

        for _ in range(n):
            pile.removeLastCard()

        hidden = len(pile._hiddenCards)
        discarded = len(pile._discardPile)
        visible = len(pile._visibleCards)



        for i in range(1,5):
            card = pile.getCard(i)
            if card is not None:
                current.append(int(card.state()))

        self.assertEqual(4, visible)
        self.assertEqual(self.numCards-n, discarded - visible)
        self.assertEqual(self.numCards-n-visible, hidden)
        self.assertEqual(self.numCards, hidden + discarded)

    def test_cycle_deck(self) -> None:
        pile = Pile(self.allCards,self.shufflerSetSeet)

        target = [0, 13, 14, 8]
        current = []

        for _ in range(17):
            pile.removeLastCard()

        hidden = len(pile._hiddenCards)
        discarded = len(pile._discardPile)
        visible = len(pile._visibleCards)
                

        for i in range(1,5):
            card = pile.getCard(i)
            if card is not None:
                current.append(int(card.state()))


        self.assertEqual(4, visible)
        self.assertEqual(target, current)