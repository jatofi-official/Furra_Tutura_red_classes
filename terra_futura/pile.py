from terra_futura.interfaces import InterfacePile, InterfaceCard
from typing import Optional, List
import random

class Pile(InterfacePile):
    def __init__(self, allCards: List[InterfaceCard]) -> None:
        pass

        self._hiddenCards: List[InterfaceCard] = allCards
        self._visibleCards: List[InterfaceCard] = []

        #fill visible cards with random cards
        for _ in range(4):
            # This calls the implemented getRandomCard
            card = self.getRandomCard()
            if card:
                 self._visibleCards.append(card)
        
    def getRandomCard(self) -> Optional[InterfaceCard]:
        #if deck is empty
        if not self._hiddenCards:
            return None

        # choose random card from _hiddenCards, pops it from list and returns it
        index = random.randrange(len(self._hiddenCards))
        card = self._hiddenCards.pop(index)

        return card

    """Only gives the card information, does not change anything"""
    def getCard(self, index:int) ->Optional[InterfaceCard]:
        # Only get card if index is not out of range
        if index > 4 or index <1:
            return None
        
        return self._visibleCards[index-1]

    """Removes card from grid."""
    def takeCard(self, index: int) -> None:
        ...



    def removeLastCard(self) -> None:
        # Remove last card
        self._visibleCards.pop(-1)

        # get card
        card = self.getRandomCard()


        
        # If ther's a card
        if card:
            
            # inserts new card 
            self._visibleCards.insert(0,card)
        
    def state(self)-> str:
        if self._hiddenCards:
            return "There are " + str(len(self._hiddenCards)) + " hidden cards and " + str(len(self._visibleCards)) + " visible cards"
        return "Something went wrong"