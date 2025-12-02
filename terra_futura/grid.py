from terra_futura.interfaces import InterfaceGrid, InterfaceCard
from typing import Optional, List, Dict, Set
from terra_futura.simple_types import *

class Grid (InterfaceGrid):
    def __init__(self) ->None:

        self._activationPattern: List[GridPosition] = []
        self._recentlyActivated: Set[GridPosition] = set()
        self._positions: Dict[GridPosition, InterfaceCard] = {}

    
    def getCard(self, coordinate: GridPosition)-> Optional[InterfaceCard]:
        # Return card if exists
        if coordinate in self._positions.keys():
            return self._positions[coordinate]
        
        return None

    def canPutCard(self, coordinate: GridPosition)-> bool:
        return False

    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> bool:
        # If cannot put card return false (final check)
        if not self.canPutCard(coordinate):
            return False
        
        # Put card on position
        self._positions[coordinate] = card

        return True

    def canBeActivated(self, coordinate: GridPosition)-> bool:
        # if card was recently activated return false
        if coordinate in self._recentlyActivated:
            return False
        # if card can be activated return True
        if coordinate in self._positions.keys() and coordinate in self._activationPattern:
            return True
        
        # default case
        return False
        
    def setActivated(self, coordinate: GridPosition) -> None:
        ...

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        # Set pattern
        self._activationPattern = pattern
        # Clear recently activated cards
        self.endTurn()
        
    def endTurn(self) -> None:
        # Clear recently activated cards
        self._recentlyActivated.clear()

    def state(self) -> str:
        return ""