#!/usr/bin/env python
"""Demo script showing admin commands in headless mode.

This script demonstrates how admin commands can be used to inspect
and manipulate the game world during headless simulation.
"""

from src.admin import execute_command, get_registry
from src.entities.entity import Entity, Position
from src.game.game_engine import GameEngine, GameMode
from src.world.world_state import WorldState


def main():
    """Run admin commands demo."""
    print("=" * 60)
    print("Admin Commands Demo - Headless Mode")
    print("=" * 60)
    print()

    # Create a world state and add some entities
    world = WorldState()

    # Add a player entity
    player_pos = Position(x=10, y=10, location_id="hommlet")
    player = Entity(id="player", position=player_pos, properties={"hp": 50, "name": "Adventurer"})
    world.add_entity(player)

    # Add an NPC
    npc_pos = Position(x=15, y=20, location_id="hommlet")
    npc = Entity(id="npc_burne", position=npc_pos, properties={"hp": 20, "name": "Burne the Wizard"})
    world.add_entity(npc)

    print(f"Initial world time: {world.time} ticks")
    print(f"Entities: {', '.join(world.get_all_entity_ids())}")
    print()

    # List available commands
    registry = get_registry()
    print("Available admin commands:")
    for cmd in registry.list_commands():
        desc = registry.get_description(cmd)
        print(f"  - {cmd}: {desc}")
    print()

    # Demonstrate advance_time command
    print("1. Advancing time by 10 ticks...")
    result = execute_command("advance_time", world, ticks=10)
    print(f"   Result: {result.message}")
    print(f"   World time now: {world.time} ticks")
    print()

    # Demonstrate show_factions command
    print("2. Showing faction information...")
    result = execute_command("show_factions", world)
    print(f"   Result: {result.message}")
    print()

    # Demonstrate teleport command
    print("3. Teleporting player to temple...")
    result = execute_command("teleport", world, "player", "temple_level_1", 5, 8)
    print(f"   Result: {result.message}")
    retrieved_player = world.get_entity("player")
    print(f"   Player position: [{retrieved_player.position.x}, {retrieved_player.position.y}] in {retrieved_player.position.location_id}")
    print()

    # Demonstrate reveal_map command
    print("4. Revealing map areas...")
    result = execute_command("reveal_map", world, area="all")
    print(f"   Result: {result.message}")
    print()

    # Demonstrate integration with GameEngine
    print("5. Using admin commands with GameEngine headless mode...")
    engine = GameEngine(world=world, mode=GameMode.HEADLESS)
    print("   Running 50 ticks of headless simulation...")
    engine.run_headless(50)
    print(f"   Final world time: {world.time} ticks")
    print()

    # Advance time again to show accumulated changes
    print("6. Advancing time by 100 more ticks...")
    result = execute_command("advance_time", world, ticks=100)
    print(f"   Result: {result.message}")
    print(f"   Total world time: {world.time} ticks")
    print()

    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
