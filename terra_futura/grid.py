from terra_futura.interfaces import InterfaceGrid, InterfaceCard
from typing import Optional, List, Dict, Set
from terra_futura.simple_types import *

class Grid (InterfaceGrid):
    def __init__(self) ->None:

        self.gridSize = 3

        self._activationPattern: List[GridPosition] = []
        self._recentlyActivated: Set[GridPosition] = set()
        self._positions: Dict[GridPosition, InterfaceCard] = {}

    
    def getCard(self, coordinate: GridPosition)-> Optional[InterfaceCard]:
        # Return card if exists
        if coordinate in self._positions.keys():
            return self._positions[coordinate]
        
        return None

    def canPutCard(self, coordinate: GridPosition)-> bool:
        # First card can always be placed
        if self._positions.keys() == []:
            return True
        
        # Position occupied
        if coordinate in self._positions.keys():
            return False
        
        # get all x positions and y positions
        xPos = [position.x for position in self._positions.keys()]
        yPos = [position.y for position in self._positions.keys()]

        xPos.append(coordinate.x)
        yPos.append(coordinate.y)

        width = max(xPos) - min(xPos) + 1
        height = max(yPos) - min(yPos) + 1

        #check if grid would change its max size
        if width > self.gridSize or height > self.gridSize:
            return False
        
        return True
    
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
        # I don't understand reason why putCard can return boolean but setActivated cannot,
        # when it works the same principle. Unfortunately it is not possible at this moment
        # to change all interfaces so I have to raise an error...
        if not self.canBeActivated(coordinate):
            raise ValueError("Unable to activate on position")
        
        self._recentlyActivated.add(coordinate)

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        # Set pattern
        self._activationPattern = pattern
        # Clear recently activated cards
        self.endTurn()
        
    def endTurn(self) -> None:
        # Clear recently activated cards
        self._recentlyActivated.clear()

    def state(self) -> str:
        if not self._positions.keys():
            return "Empty grid"


        return ""