from terra_futura.interfaces import InterfacePile, InterfaceCard
from typing import Optional, List, Protocol
import random
import time

class InterfaceShuffle(Protocol):
    # is necessary for testing randomness
    def shuffle(self, inputDeck: List[InterfaceCard]) -> List[InterfaceCard]:
        ...

class Shuffle(InterfaceShuffle):

    def __init__(self, seed: Optional[int]) -> None:
        # if there's a seed, set it
        if seed:
            self.randomGenerator  = random.Random(seed)
        else: # set seed to current time
            self.randomGenerator = random.Random(time.time())

    def shuffle(self, inputDeck: List[InterfaceCard]) -> List[InterfaceCard]:
        new = inputDeck.copy()

        self.randomGenerator.shuffle(new)

        return new


class Pile(InterfacePile):
    def __init__(self, allCards: List[InterfaceCard], shuffler: Optional[InterfaceShuffle]) -> None:
        self._hiddenCards: List[InterfaceCard]

        # If there's a shuffler, shuffle according to it
        self.shuffler: InterfaceShuffle


        if shuffler:
            self.shuffler = shuffler
        else:
            newShuffler = Shuffle(None)
            self.shuffler = newShuffler

        self._hiddenCards = self.shuffler.shuffle(allCards)    
            
        self._visibleCards: List[InterfaceCard] = []
        self._discardPile: List[InterfaceCard] = []

        #fill visible cards with random cards
        for _ in range(4):
            # This calls the implemented _getRandomCard
            card = self._getRandomCard()
            if card:
                 self._visibleCards.append(card)


    #private
        
    def _getRandomCard(self) -> Optional[InterfaceCard]:
        #if deck is empty
        if not self._hiddenCards:
            self._restoreDiscardPile

        # choose next card from _hiddenCards, pops it from list and returns it
        card = self._hiddenCards.pop()
        self._discardPile.append(card)

        return card
    
    def _restoreDiscardPile(self) -> None:
        self._hiddenCards.extend(self._discardPile)

        self._hiddenCards = self.shuffler.shuffle(self._hiddenCards)

        self._discardPile.clear()



    # public

    """Only gives the card information, does not change anything"""
    def getCard(self, index:int) ->Optional[InterfaceCard]:
        # Only get card if index is not out of range
        if index > 4 or index <1:
            return None
        
        return self._visibleCards[index-1]

    """Removes card from pile."""
    def takeCard(self, index: int) -> None:
        if index>=1 and index <=4:
            self._visibleCards.pop(index-1)

            card = self._getRandomCard()

            if card:
                self._visibleCards.insert(0,card)




    def removeLastCard(self) -> None:
        # Remove last card
        self._visibleCards.pop(-1)

        # get card
        card = self._getRandomCard()

        # If ther's a card
        if card:
            # inserts new card 
            self._visibleCards.insert(0,card)
        
    def state(self)-> str:
        if self._hiddenCards:
            return "There are " + str(len(self._hiddenCards)) + " hidden cards and " + str(len(self._visibleCards)) + " visible cards"
        return "Something went wrong"