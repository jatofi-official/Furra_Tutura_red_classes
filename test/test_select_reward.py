from __future__ import annotations
import unittest

from typing import List, Optional
from terra_futura.simple_types import GridPosition, Resource
from terra_futura.interfaces import InterfaceCard, Effect, InterfaceGrid
from terra_futura.select_reward import SelectReward

class CardFake(InterfaceCard):
    def __init__(self, can_put: bool = True, index: int = 0) -> None:
        # Attributes
        self.resources: List[Resource] = []
        self.pollutionSpacesL: int = 0

        self.index = index

        # Multiplicity 0..1 — may be None or an Effect instance
        self.upperEffect: Optional[Effect] = None
        self.lowerEffect: Optional[Effect] = None

        self.can_put_resources_result = can_put
        self.resources_put: List[Resource] = []


    def canPutResources(self, resources: List[Resource]) -> bool:
        return self.can_put_resources_result

    def putResources(self, resources: List[Resource]) -> None:
        self.resources_put.extend(resources)
        
    def isActive(self) -> bool:
        return True

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
        return False
    def state(self) -> str:
        return '{"state": "card"}'

class GridFake(InterfaceGrid):
    def getCard(self, coordinate: GridPosition)-> Optional[InterfaceCard]:
        return None

    def canPutCard(self, coordinate: GridPosition)-> bool:
        return True
    
    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> None:
        pass

    def canBeActivated(self, coordinate: GridPosition)-> bool:
        return False
        
    def setActivated(self, coordinate: GridPosition) -> None:
        ...

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        ...
        
    def endTurn(self) -> None:
        ...

    def state(self) -> str:
        return ""


class TestSelectReward(unittest.TestCase):
    def setUp(self) -> None:
        self.playerId = 1
        self.rewardList = [Resource.YELLOW, Resource.RED, Resource.YELLOW]
        self.mockCard = CardFake(can_put=True)



    def test_reward_not_set(self) -> None:
        selectReward = SelectReward() 
        # Nothing set
        self.assertEqual("Reward not set", selectReward.state())
    
    def test_no_player(self) -> None:
        selectReward = SelectReward()
        # Should raise error
        with self.assertRaises(ValueError):
            selectReward.player

    def test_successful_resource_transfer(self) -> None:
        selectReward = SelectReward()
        # Set rewards
        selectReward.setReward(self.playerId, self.mockCard, self.rewardList)
        
        # Select one YELLOW
        selectReward.selectReward(Resource.YELLOW)
        
        # Check selection was updated (one YELLOW removed)
        self.assertEqual(selectReward._selection, [Resource.RED, Resource.YELLOW])
        
        # Check card received the resource
        self.assertEqual(self.mockCard.resources_put, [Resource.YELLOW])

    def test_cannot_select_unavailable_resource(self) -> None:
        selectReward = SelectReward()

        # Test that an unavailable resource cannot be selected
        selectReward.setReward(self.playerId, self.mockCard, [Resource.RED])
        
        # Check canSelectReward for the unavailable resource
        self.assertFalse(selectReward.canSelectReward(Resource.GREEN))
        
        # Check selectReward raises an error
        with self.assertRaisesRegex(ValueError, "Invalid resources for selection"):
            selectReward.selectReward(Resource.GREEN)

    def test_selection_blocked_by_card(self) -> None:
        blocked_card = CardFake(can_put=False)
        selectReward = SelectReward()
        selectReward.setReward(self.playerId, blocked_card, self.rewardList)
        
        # canSelectReward should be False
        self.assertFalse(selectReward.canSelectReward(Resource.YELLOW))
        
        # Should raise error
        with self.assertRaisesRegex(ValueError, "Invalid resources for selection"):
            selectReward.selectReward(Resource.YELLOW)

    def test_all_rewards_selected_empty_selection(self) -> None:
        selectReward = SelectReward()

        selectReward.setReward(self.playerId, self.mockCard, self.rewardList)
        
        # Select all three resources
        selectReward.selectReward(Resource.YELLOW) 
        selectReward.selectReward(Resource.RED)    
        selectReward.selectReward(Resource.YELLOW) 
        
        # Check selection is now empty
        self.assertEqual(selectReward._selection, [])
        self.assertEqual(selectReward.state(), "Player: 1; Resources: []")
        
        # Cannot select anything afterwards
        self.assertFalse(selectReward.canSelectReward(Resource.RED))