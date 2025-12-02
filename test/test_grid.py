from __future__ import annotations
import unittest

from typing import List, Optional
from terra_futura.simple_types import GridPosition, Resource
from terra_futura.interfaces import InterfaceCard, Effect
from terra_futura.grid import Grid

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


class TestGrid(unittest.TestCase):
    def setUp(self) ->None:
        ...
        
    def test_empty_grid(self) -> None:
        grid = Grid()

        self.assertEqual("Empty grid", grid.state())

    def test_starting_card_in_middle(self) -> None:
        grid = Grid()

        card = CardFake(0)

        # Position is not in middle
        grid.putCard(GridPosition(2,2),card)

        print(grid.state())
        
        # Position 0, 0 should be taken
        self.assertFalse(grid.canPutCard(GridPosition(0,0)))
    

    def test_can_put_card(self) -> None:
        grid = Grid()

        card = CardFake(0)


        grid.putCard(GridPosition(0,0),card)

        self.assertFalse(grid.canPutCard(GridPosition(0,0)))
        self.assertTrue(grid.canPutCard(GridPosition(1,1)))

        grid.putCard(GridPosition(-2, -2),card)

        # should not put card outside of boundary
        self.assertFalse(grid.canPutCard(GridPosition(1,1)))


    def test_two_cards(self) -> None:
        grid = Grid()

        card1 = CardFake(1)
        card2 = CardFake(2)


        grid.putCard(GridPosition(0,0),card1)
        grid.putCard(GridPosition(2,2),card2)

        self.assertEqual(""" [C]  [ ]  [ ] \n [ ]  [ ]  [ ] \n [ ]  [ ]  [C] """, grid.state())
        self.assertFalse(grid.canPutCard(GridPosition(0,0)))
        self.assertEqual(card1.index, grid.getCard(GridPosition(0,0)).index)
        self.assertNotEqual(card1.index, grid.getCard(GridPosition(2,2)).index)
    
    def test_activation_pattern(self) ->None:
        grid = Grid()

        card1 = CardFake(1)
        card2 = CardFake(2)
        card3 = CardFake(3)
        card4 = CardFake(4)


        grid.putCard(GridPosition(0,0),card1)
        grid.putCard(GridPosition(2,2),card2)
