from .simple_types import Resource
from .interfaces import InterfaceSelectReward, InterfaceCard
from typing import List, Optional

class SelectReward(InterfaceSelectReward):

    def __init__(self) -> None:
        self._player: Optional[int] = None           
        self._selection: List[Resource] = []         
        self._card: Optional[InterfaceCard] = None   

    @property
    def player(self) -> int:
        if self._player is None:
            raise ValueError("Empty player")
        
        return self._player
    
    def setReward(self, player: int, card: InterfaceCard, reward: List[Resource]) -> None:
        # Copy from arguments
        self._player = player
        self._card = card
        self._selection = reward.copy()
    
    def canSelectReward(self, resource: Resource) -> bool:
        # Player and card have to exist
        if self._player is None or self._card is None:
            return False

        if not self._card.canPutResources([resource]):
            return False

        # Resources have to be in selection
        if resource not in self._selection:
            return False
        
        # all in order
        return True


    def selectReward(self, resource: Resource) -> None:
        # If cannot select reward raise error
        if not self.canSelectReward(resource):
            raise ValueError("Invalid resources for selection")
        
        # Remove resource from selection
        self._selection.remove(resource)
        
        # Put resources on card is card exists
        if self._card is not None:
            self._card.putResources([resource])

    def state(self)-> str:
        if not self._player:
            return "Reward not set"
        return "Player: " + str(self._player) + "; Resources: " + str(self._selection)