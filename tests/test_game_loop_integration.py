"""Integration tests for the game loop skeleton.

These tests verify that:
- GameEngine can run in player mode and step on player actions
- GameEngine can run in headless mode and advance ticks
- ActionHandler integrates with WorldState
- The game loop properly advances world ticks and applies actions
"""

import logging

from src.entities.entity import Entity, Position
from src.game.action_handler import ActionHandler
from src.game.game_engine import GameEngine, GameMode
from src.simulation.npc_ai import Action
from src.world.world_state import WorldState


class TestGameLoopIntegration:
    """Integration tests demonstrating the complete game loop."""

    def test_player_mode_with_move_action(self):
        """Test player mode with a move action applied via ActionHandler.
        
        Demonstrates the full flow:
        1. Create world with entity
        2. Create GameEngine in player mode
        3. Create ActionHandler
        4. Apply a move action
        5. Step the game engine
        6. Verify entity moved and world ticked
        """
        # Setup world with entity
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="player", position=pos)
        world.add_entity(entity)

        # Create game engine in player mode
        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Create and apply a move action
        target = Position(x=5, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)
        handler.handle_action(action, "player")

        # Step the game engine
        engine.step(action=action)

        # Verify results
        assert entity.position.x == 1
        assert entity.position.y == 1
        assert world.time == 1

    def test_player_mode_multiple_actions(self):
        """Test player mode with multiple move actions over several steps."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="arena")
        entity = Entity(id="hero", position=pos)
        world.add_entity(entity)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        target = Position(x=3, y=0, location_id="arena")
        action = Action(action_type="move", target_position=target)

        # Move entity toward target over multiple steps
        for i in range(3):
            handler.handle_action(action, "hero")
            engine.step(action=action)

        # Verify entity reached target and time advanced
        assert entity.position.x == 3
        assert entity.position.y == 0
        assert world.time == 3

    def test_player_mode_attack_action(self):
        """Test player mode with an attack action."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="battle")
        pos2 = Position(x=2, y=2, location_id="battle")
        hero = Entity(id="hero", position=pos1)
        enemy = Entity(id="goblin", position=pos2)
        world.add_entity(hero)
        world.add_entity(enemy)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Create and apply attack action
        action = Action(action_type="attack", target_entity_id="goblin")
        result = handler.handle_action(action, "hero")
        engine.step(action=action)

        # Verify attack was processed and time advanced
        assert result is True
        assert world.time == 1

    def test_headless_mode_advances_ticks(self):
        """Test headless mode automatically advances world ticks.
        
        Demonstrates autonomous simulation without player input.
        """
        world = WorldState()
        pos = Position(x=0, y=0, location_id="world")
        entity = Entity(id="npc", position=pos)
        world.add_entity(entity)

        engine = GameEngine(world=world, mode=GameMode.HEADLESS)

        # Run headless simulation
        final_time = engine.run_headless(ticks=50)

        # Verify simulation advanced time
        assert final_time == 50
        assert world.time == 50
        assert world.get_entity("npc") is entity

    def test_headless_mode_with_npc_actions(self):
        """Test headless mode with NPC actions being processed."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="dungeon")
        npc = Entity(id="guard", position=pos)
        world.add_entity(npc)

        engine = GameEngine(world=world, mode=GameMode.HEADLESS)
        handler = ActionHandler(world=world)

        # Simulate NPCs taking actions during headless ticks
        target = Position(x=10, y=0, location_id="dungeon")
        action = Action(action_type="move", target_position=target)

        # Run some ticks
        engine.run_headless(ticks=5)

        # Apply NPC action
        handler.handle_action(action, "guard")

        # Run more ticks
        engine.run_headless(ticks=5)

        # Verify NPC moved and time advanced
        assert npc.position.x == 1
        assert world.time == 10

    def test_mode_switching(self):
        """Test switching between player and headless modes."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="player", position=pos)
        world.add_entity(entity)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Player mode: advance 3 steps
        action = Action(action_type="move", target_position=Position(x=10, y=0, location_id="test"))
        for _ in range(3):
            handler.handle_action(action, "player")
            engine.step(action=action)

        assert world.time == 3
        assert entity.position.x == 3

        # Switch to headless mode and run simulation
        engine.set_mode(GameMode.HEADLESS)
        engine.run_headless(ticks=10)

        assert world.time == 13

        # Back to player mode
        engine.set_mode(GameMode.PLAYER)
        handler.handle_action(action, "player")
        engine.step(action=action)

        assert world.time == 14
        assert entity.position.x == 4

    def test_multiple_entities_with_actions(self):
        """Test game loop with multiple entities performing actions."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="arena")
        pos2 = Position(x=10, y=10, location_id="arena")
        pos3 = Position(x=5, y=5, location_id="arena")
        
        hero = Entity(id="hero", position=pos1)
        npc1 = Entity(id="npc1", position=pos2)
        npc2 = Entity(id="npc2", position=pos3)
        
        world.add_entity(hero)
        world.add_entity(npc1)
        world.add_entity(npc2)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Hero moves toward center
        hero_action = Action(action_type="move", target_position=Position(x=5, y=5, location_id="arena"))
        handler.handle_action(hero_action, "hero")

        # NPC1 moves toward center
        npc1_action = Action(action_type="move", target_position=Position(x=5, y=5, location_id="arena"))
        handler.handle_action(npc1_action, "npc1")

        # NPC2 stays idle
        npc2_action = Action(action_type="idle")
        handler.handle_action(npc2_action, "npc2")

        # Advance game
        engine.step()

        # Verify all entities and time
        assert hero.position.x == 1
        assert hero.position.y == 1
        assert npc1.position.x == 9
        assert npc1.position.y == 9
        assert npc2.position.x == 5  # Idle, no movement
        assert npc2.position.y == 5
        assert world.time == 1

    def test_game_loop_logs_correctly(self, caplog):
        """Test that game loop components log their actions correctly."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos)
        world.add_entity(entity)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        action = Action(action_type="move", target_position=Position(x=1, y=1, location_id="test"))

        with caplog.at_level(logging.DEBUG):
            handler.handle_action(action, "test_entity")
            engine.step(action=action)

        # Check for expected log messages
        assert "moved from (0, 0) to (1, 1)" in caplog.text
        assert "Game step completed" in caplog.text

    def test_acceptance_criteria_player_mode(self):
        """Acceptance test: GameEngine can run in player mode (step on player action)."""
        world = WorldState()
        pos = Position(x=5, y=5, location_id="start")
        player = Entity(id="player_char", position=pos)
        world.add_entity(player)

        # Create engine in player mode
        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Player action: move
        move_action = Action(action_type="move", target_position=Position(x=10, y=10, location_id="start"))
        handler.handle_action(move_action, "player_char")
        time1 = engine.step(action=move_action)

        assert time1 == 1
        assert player.position.x == 6
        assert player.position.y == 6

        # Another player action: attack
        enemy_pos = Position(x=7, y=7, location_id="start")
        enemy = Entity(id="enemy", position=enemy_pos)
        world.add_entity(enemy)
        
        attack_action = Action(action_type="attack", target_entity_id="enemy")
        handler.handle_action(attack_action, "player_char")
        time2 = engine.step(action=attack_action)

        assert time2 == 2

    def test_acceptance_criteria_headless_mode(self):
        """Acceptance test: GameEngine can run in headless mode (advance ticks)."""
        world = WorldState()
        
        # Create engine in headless mode
        engine = GameEngine(world=world, mode=GameMode.HEADLESS)

        # Run headless simulation
        initial_time = engine.get_current_time()
        assert initial_time == 0

        final_time = engine.run_headless(ticks=100)
        
        assert final_time == 100
        assert world.time == 100

    def test_acceptance_criteria_action_handler_integration(self):
        """Acceptance test: ActionHandler integrates with WorldState for move and attack."""
        world = WorldState()
        
        # Setup entities
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=5, y=0, location_id="test")
        entity1 = Entity(id="entity1", position=pos1)
        entity2 = Entity(id="entity2", position=pos2)
        world.add_entity(entity1)
        world.add_entity(entity2)

        handler = ActionHandler(world=world)

        # Test move action
        move_action = Action(action_type="move", target_position=Position(x=10, y=0, location_id="test"))
        result_move = handler.handle_action(move_action, "entity1")
        
        assert result_move is True
        assert entity1.position.x == 1

        # Test attack action
        attack_action = Action(action_type="attack", target_entity_id="entity2")
        result_attack = handler.handle_action(attack_action, "entity1")
        
        assert result_attack is True

    def test_acceptance_criteria_world_tick_advancement(self):
        """Acceptance test: Game loop advances world ticks and applies move action."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="world")
        entity = Entity(id="test_entity", position=pos, properties={"name": "Test"})
        world.add_entity(entity)

        engine = GameEngine(world=world, mode=GameMode.PLAYER)
        handler = ActionHandler(world=world)

        # Initial state
        assert world.time == 0
        assert entity.position.x == 0

        # Apply move action and step
        move_action = Action(action_type="move", target_position=Position(x=5, y=5, location_id="world"))
        handler.handle_action(move_action, "test_entity")
        engine.step(action=move_action)

        # Verify world tick advanced and move was applied
        assert world.time == 1
        assert entity.position.x == 1
        assert entity.position.y == 1

        # Apply another move and step
        handler.handle_action(move_action, "test_entity")
        engine.step(action=move_action)

        # Verify continued advancement
        assert world.time == 2
        assert entity.position.x == 2
        assert entity.position.y == 2
