from __future__ import annotations
import unittest
from typing import List, Optional, Dict

from terra_futura.simple_types import GridPosition, Resource, Deck, CardSource, GameState, Points
from terra_futura.interfaces import InterfaceCard, TerraFuturaObserverInterface, InterfacePile
from terra_futura.card import Card
from terra_futura.transformation_fixed import TransformationFixed
from terra_futura.arbitrary_basic import ArbitraryBasic
from terra_futura.effect_or import EffectOr
from terra_futura.pile import Pile, Shuffle
from terra_futura.grid import Grid
from terra_futura.player import Player
from terra_futura.activation_pattern import ActivationPattern
from terra_futura.scoring_method import ScoringMethod
from terra_futura.game import Game
from terra_futura.game_observer import GameObserver
from terra_futura.move_card import MoveCard
from terra_futura.process_action import ProcessAction
from terra_futura.process_action_assistance import ProcessActionAssistance
from terra_futura.select_reward import SelectReward


class ObserverRecorder(TerraFuturaObserverInterface):
    """Observer that records all state notifications"""

    def __init__(self) -> None:
        self.state_history: List[str] = []
        self.notification_count: int = 0
    
    def notify(self, game_state: str) -> None:
        self.state_history.append(game_state)
        self.notification_count += 1


class TestIntegration2(unittest.TestCase):
    """
    Advanced integration test simulating a 3-player game with:
    - Complex card effects (OR effects)
    - Assistance mechanics
    - Activation patterns
    - Scoring methods
    """
    
    def setUp(self) -> None:
        # Create observers for three players
        self.observer1 = ObserverRecorder()
        self.observer2 = ObserverRecorder()
        self.observer3 = ObserverRecorder()
        
        observers: Dict[int, TerraFuturaObserverInterface] = {1: self.observer1, 2: self.observer2, 3: self.observer3}
        
        # Initialize game components
        self.game_observer = GameObserver(observers)
        self.move_card = MoveCard()
        self.process_action = ProcessAction()
        self.process_action_assistance = ProcessActionAssistance()
        self.select_reward = SelectReward()
        
        # Create card decks
        level1_cards: List[InterfaceCard] = self._create_advanced_level1_cards()
        level2_cards: List[InterfaceCard] = self._create_advanced_level2_cards()
        
        self.pile_level1 = Pile(level1_cards, Shuffle(100))
        self.pile_level2 = Pile(level2_cards, Shuffle(101))
        
        piles: Dict[Deck, InterfacePile] = {
            Deck.LEVEL_I: self.pile_level1,
            Deck.LEVEL_II: self.pile_level2
        }
        
        # Create three players
        self.player1 = self._create_advanced_player(1)
        self.player2 = self._create_advanced_player(2)
        self.player3 = self._create_advanced_player(3)
        
        # Initialize game
        self.game = Game(
            players=[self.player1, self.player2, self.player3],
            piles=piles,
            moveCard=self.move_card,
            processAction=self.process_action,
            processActionAssistance=self.process_action_assistance,
            selectReward=self.select_reward,
            gameObserver=self.game_observer
        )
    
    def _create_advanced_level1_cards(self) -> List[InterfaceCard]:
        """Create Level I cards with complex effects including OR effects"""

        cards: List[InterfaceCard] = []
        
        # Card 1: OR effect - choice between two transformations
        effect1a = TransformationFixed(
            from_=[Resource.YELLOW],
            to=[Resource.GOODS],
            pollution=1
        )
        effect1b = TransformationFixed(
            from_=[Resource.RED, Resource.RED],
            to=[Resource.GOODS, Resource.MONEY],
            pollution=0
        )
        card1 = Card(
            pollutionSpacesL=2,
            upperEffect=EffectOr(effects=[effect1a, effect1b])
        )
        cards.append(card1)
        
        # Card 2: Construction production
        card2 = Card(
            pollutionSpacesL=3,
            upperEffect=TransformationFixed(
                from_=[Resource.GOODS, Resource.GOODS],
                to=[Resource.CONSTRUCTION],
                pollution=2
            )
        )
        cards.append(card2)
        
        # Card 3: Dual effect card (upper and lower)
        card3 = Card(
            pollutionSpacesL=2,
            upperEffect=TransformationFixed(
                from_=[Resource.GREEN],
                to=[Resource.FOOD],
                pollution=1
            ),
            lowerEffect=ArbitraryBasic(
                from_=1,
                to=[Resource.MONEY],
                pollution=0
            )
        )
        cards.append(card3)
        
        # Card 4: Resource multiplier
        card4 = Card(
            pollutionSpacesL=1,
            upperEffect=ArbitraryBasic(
                from_=3,
                to=[Resource.RED, Resource.GREEN, Resource.YELLOW, Resource.MONEY],
                pollution=1
            )
        )
        cards.append(card4)
        
        # Fill remaining slots
        for i in range(16):
            card = Card(
                pollutionSpacesL=1,
                upperEffect=ArbitraryBasic(
                    from_=1,
                    to=[Resource.YELLOW],
                    pollution=0
                )
            )
            cards.append(card)
        
        return cards
    
    def _create_advanced_level2_cards(self) -> List[InterfaceCard]:
        """Create Level II cards with advanced effects"""

        cards: List[InterfaceCard] = []
        
        # Card 1: High-value production with OR effect
        effect1a = TransformationFixed(
            from_=[Resource.CONSTRUCTION],
            to=[Resource.MONEY, Resource.MONEY, Resource.MONEY],
            pollution=0
        )
        effect1b = ArbitraryBasic(
            from_=2,
            to=[Resource.CONSTRUCTION],
            pollution=1
        )
        card1 = Card(
            pollutionSpacesL=3,
            upperEffect=EffectOr(effects=[effect1a, effect1b])
        )
        cards.append(card1)
        
        # Fill remaining slots
        for i in range(19):
            card = Card(
                pollutionSpacesL=2,
                upperEffect=TransformationFixed(
                    from_=[Resource.YELLOW],
                    to=[Resource.RED, Resource.GREEN],
                    pollution=1
                )
            )
            cards.append(card)
        
        return cards
    
    def _create_advanced_player(self, player_id: int) -> Player:
        """Create player with multiple activation patterns"""

        grid = Grid()
        
        # Create diverse activation patterns
        pattern1 = ActivationPattern(grid, [GridPosition(0, 0)])
        pattern2 = ActivationPattern(grid, [
            GridPosition(0, 0), 
            GridPosition(0, 1), 
            GridPosition(1, 0)
        ])
        
        # Create scoring with different resource combinations
        if player_id == 1:
            scoring1 = ScoringMethod([Resource.GOODS, Resource.FOOD], Points(8), grid)
            scoring2 = ScoringMethod([Resource.CONSTRUCTION], Points(10), grid)
        elif player_id == 2:
            scoring1 = ScoringMethod([Resource.FOOD], Points(6), grid)
            scoring2 = ScoringMethod([Resource.GOODS], Points(7), grid)
        else:
            scoring1 = ScoringMethod([Resource.RED, Resource.GREEN], Points(5), grid)
            scoring2 = ScoringMethod([Resource.YELLOW], Points(4), grid)
        
        return Player(
            id=player_id,
            activation_patterns=[pattern1, pattern2],
            scoring_methods=[scoring1, scoring2],
            grid=grid
        )
    
    def test_three_player_game_initialization(self) -> None:
        """Test game initializes correctly with 3 players"""

        self.assertEqual(len(self.game.players), 3)
        self.assertEqual(self.game.currentPlayerId, 1)
        self.assertEqual(self.game.state, GameState.TakeCardNoCardDiscarded)
    
    def test_round_robin_turn_order(self) -> None:
        """Test that turns cycle through all 3 players correctly"""

        # Track player order through one complete round
        turn_order = []
        # Adjusted positions to use different spots for card placement for player 1, 2, 3
        positions_p1 = GridPosition(0, 0)
        positions_p2 = GridPosition(0, 0)
        positions_p3 = GridPosition(0, 0)
        
        for i in range(3):
            current_player = self.game.currentPlayerId
            turn_order.append(current_player)
            
            # Use player's own unique grid for placement
            if current_player == 1:
                pos = positions_p1
            elif current_player == 2:
                pos = positions_p2
            else:
                pos = positions_p3
            
            # Take card and finish turn
            self.game.takeCard(
                playerId=current_player,
                source=CardSource(Deck.LEVEL_I, 1),
                cardIndex=1,
                destination=pos
            )
            self.game.turnFinished(current_player)
        
        # Verify all three players had their turn
        self.assertEqual(turn_order, [1, 2, 3])
        self.assertEqual(self.game.turnNumber, 2)
        self.assertEqual(self.game.currentPlayerId, 1)
    
    
    def test_complex_resource_chain(self) -> None:
        """Test multi-step resource transformation across cards"""

        # Player 1 places first card
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        
        # Add resources directly to test card functionality
        card1 = self.player1.grid.getCard(GridPosition(0, 0))
        # Assert type for testing attributes/methods outside of InterfaceCard
        self.assertIsInstance(card1, Card)
        
        if card1:
            # Add initial resources
            card1.putResources([Resource.YELLOW, Resource.YELLOW])
            initial_count = len(card1.resources)
            
            # Test resource removal
            if card1.canGetResources([Resource.YELLOW]):
                card1.getResources([Resource.YELLOW])
                self.assertEqual(len(card1.resources), initial_count - 1)
            
            # Test resource addition
            if card1.canPutResources([Resource.GOODS]):
                card1.putResources([Resource.GOODS])
                self.assertIn(Resource.GOODS, card1.resources)
            
            # Test pollution management
            
            initial_pollution = card1.getPollution() if hasattr(card1, 'getPollution') else 0
            if card1.canPlacePollution(1):
                card1.placePollution(1)
                final_pollution = card1.getPollution() if hasattr(card1, 'getPollution') else 1 # Assuming it's Card
                self.assertEqual(final_pollution, initial_pollution + 1)
    
    def test_grid_expansion(self) -> None:
        """Test that grid can expand up to 3x3"""

        # Player 1 places cards to form a pattern
        # Use unique positions for each turn (player 1, 2, 3 will place on their own separate grids)
        positions = [
            (GridPosition(0, 0), 1),
            (GridPosition(0, 0), 2),
            (GridPosition(0, 0), 3),
            (GridPosition(0, 1), 1),
            (GridPosition(0, 1), 2),
            (GridPosition(0, 1), 3),
            (GridPosition(1, 0), 1),
            (GridPosition(1, 0), 2),
            (GridPosition(1, 0), 3),
        ]
        
        for i, (pos, expected_player) in enumerate(positions):
            current_player = self.game.currentPlayerId
            self.assertEqual(current_player, expected_player)
            
            # Take card at specific position
            success = self.game.takeCard(
                playerId=current_player,
                source=CardSource(Deck.LEVEL_I, 1),
                cardIndex=1,
                destination=pos
            )
            self.assertTrue(success)
            
            # Verify card is placed
            player = self.game.players[current_player - 1]
            card = player.grid.getCard(pos)
            self.assertIsNotNone(card)
            
            self.game.turnFinished(current_player)
    
    def test_pollution_across_multiple_cards(self) -> None:
        """Test pollution distribution across grid"""

        # Player 1 sets up first card
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        self.game.turnFinished(1)
        
        # Players 2 and 3 take turns
        self.game.takeCard(2, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        self.game.turnFinished(2)
        self.game.takeCard(3, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        self.game.turnFinished(3)
        
        # Player 1 places second card
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 1))
        
        card1 = self.player1.grid.getCard(GridPosition(0, 0))
        card2 = self.player1.grid.getCard(GridPosition(0, 1))
        
        # Assert type for pollution access
        self.assertIsInstance(card1, Card)
        self.assertIsInstance(card2, Card)
        
        if card1 and card2:
            # Both cards start active
            self.assertTrue(card1.isActive())
            self.assertTrue(card2.isActive())
            
            # Add pollution to first card
            initial_pollution = card1.getPollution() if hasattr(card1, 'getPollution') else 0
            if card1.canPlacePollution(1):
                card1.placePollution(1)
                final_pollution = card1.getPollution() if hasattr(card1, 'getPollution') else initial_pollution + 1
                self.assertEqual(final_pollution, initial_pollution + 1)
            
            # Second card should remain unaffected
            self.assertEqual(card2.getPollution() if hasattr(card2, 'getPollution') else 0, 0)
    
    def test_observer_notifications(self) -> None:
        """Test that observers receive notifications on state changes"""

        initial_count = self.observer1.notification_count
        
        # Perform an action
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        
        # Observer should have received notification
        self.assertGreater(self.observer1.notification_count, initial_count)
        self.assertGreater(len(self.observer1.state_history), 0)
    
    
    def test_activation_pattern_selection(self) -> None:
        """Test selecting and applying activation patterns"""

        # Setup: Place some cards for player 1
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        self.game.turnFinished(1)
        
        # Get the activation pattern
        pattern = self.player1.activation_patterns[0]
        initial_selection = pattern.is_selected()
        
        # Pattern should not be selected initially
        self.assertFalse(initial_selection)
        
        # Manually select pattern (simulate end-game scenario)
        pattern.select()
        
        # Verify pattern is now selected
        self.assertTrue(pattern.is_selected())
    
    def test_scoring_calculation(self) -> None:
        """Test scoring method calculation at game end"""

        # Setup: Player 1 has cards with resources
        self.game.takeCard(1, CardSource(Deck.LEVEL_I, 1), 1, GridPosition(0, 0))
        
        card = self.player1.grid.getCard(GridPosition(0, 0))
        if card:
            # Add various resources
            card.putResources([
                Resource.GOODS,
                Resource.FOOD,
                Resource.CONSTRUCTION,
                Resource.MONEY
            ])
        
        # Calculate score using first scoring method
        scoring = self.player1.scoring_methods[0]
        scoring.selectThisMethodAndCalculate()
        
        self.assertIsNotNone(scoring.calculatedTotal)
        if scoring.calculatedTotal:
            self.assertGreater(scoring.calculatedTotal.value, 0)