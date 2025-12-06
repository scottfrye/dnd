# Save/Load Format Documentation

## Overview

The Temple of Elemental Evil roguelike uses a human-readable save file format to persist game state. Save files can be stored in either YAML (default) or JSON format, allowing for easy inspection, debugging, and manual editing if needed.

## File Naming Convention

Save files follow this naming pattern:
```
saves/
  ├── autosave.yaml          # Automatic save
  ├── quicksave.yaml         # Quick save (Ctrl+S)
  ├── slot_1.yaml           # Manual save slot 1
  ├── slot_2.yaml           # Manual save slot 2
  └── ...
```

## Save File Structure

### Top-Level Structure

```yaml
version: "1.0.0"              # Save file format version
game_version: "0.1.0"         # Game version
timestamp: "2024-12-06T12:30:45Z"
game_mode: "player"           # "player" or "headless"

world_state:
  time: 1000                  # Current game time in ticks
  locations: { ... }          # All location data
  entities: { ... }           # All entities (NPCs, monsters, items)
  factions: { ... }           # Faction data
  events: { ... }             # Event queue
  player: { ... }             # Player character data
```

### WorldState Schema

The `world_state` section contains all dynamic game state:

```yaml
world_state:
  time: <integer>             # Game time in ticks (1 tick = 1 round = 1 minute)
  
  locations:
    hommlet:
      id: "hommlet"
      name: "Village of Hommlet"
      type: "town"
      cleared: false
      last_visit: 950
      entities: [<entity_ids>]
      
    temple_level_1:
      id: "temple_level_1"
      name: "Temple of Elemental Evil - Level 1"
      type: "dungeon"
      cleared: false
      last_visit: null
      entities: [<entity_ids>]
  
  entities:
    <entity_id>:
      type: "npc" | "monster" | "player" | "item"
      # Type-specific data follows...
      
  factions:
    <faction_id>:
      id: <string>
      name: <string>
      power_level: <integer>
      relationships: { ... }
      members: [<entity_ids>]
      
  events:
    - tick: <integer>
      event_type: <string>
      data: { ... }
      
  player:
    entity_id: <string>
    party: [<entity_ids>]
```

### Entity Schema

Entities represent all characters, monsters, and items in the game:

```yaml
entities:
  char_001:
    id: "char_001"
    type: "player"
    name: "Adventurer"
    race: "human"
    class: "fighter"
    level: 3
    
    # Core AD&D stats
    abilities:
      strength: 16
      intelligence: 10
      wisdom: 12
      dexterity: 14
      constitution: 15
      charisma: 11
    
    # Derived stats
    hp: 24
    max_hp: 28
    ac: 4                     # Armor class
    thac0: 18                 # To-hit armor class 0
    
    # Position and status
    location: "hommlet"
    position: [10, 5]         # [x, y] coordinates
    alive: true
    
    # Inventory
    inventory:
      equipped:
        weapon: "item_longsword_001"
        armor: "item_chainmail_001"
        shield: "item_shield_001"
      backpack:
        - "item_potion_healing_001"
        - "item_rations_001"
    
    # Class-specific
    experience: 5000
    
    # Faction membership
    faction: null             # Most players are not in a faction
    
  npc_001:
    id: "npc_001"
    type: "npc"
    name: "Burne the Wizard"
    race: "human"
    class: "magic-user"
    level: 7
    
    abilities: { ... }
    hp: 20
    max_hp: 20
    ac: 8
    thac0: 18
    
    location: "hommlet"
    position: [15, 20]
    alive: true
    
    # NPC-specific
    ai_state: "patrol"
    faction: "hommlet_defenders"
    loyalty: 85
    spells_memorized:
      - "magic_missile"
      - "shield"
      - "fireball"
    
  monster_001:
    id: "monster_001"
    type: "monster"
    name: "Gnoll Warrior"
    monster_type: "gnoll"
    hit_dice: "2"
    
    abilities: { ... }
    hp: 12
    max_hp: 12
    ac: 5
    thac0: 19
    
    location: "temple_level_1"
    position: [5, 8]
    alive: true
    
    # Monster-specific
    ai_state: "guard"
    faction: "temple_guards"
    morale: 70
    treasure: ["item_gold_001"]
    
  item_longsword_001:
    id: "item_longsword_001"
    type: "item"
    name: "Longsword"
    item_type: "weapon"
    
    location: "char_001"      # In inventory
    position: null
    
    # Item-specific
    damage: "1d8"
    weight: 60                # In coins (10 coins = 1 pound)
    value: 15                 # In gold pieces
    magical: false
    properties: {}
```

### Faction Schema

Factions represent groups with shared goals and relationships:

```yaml
factions:
  hommlet_defenders:
    id: "hommlet_defenders"
    name: "Defenders of Hommlet"
    type: "good"
    power_level: 75           # 0-100 scale
    
    relationships:
      temple_of_fire: -80     # -100 to 100, negative = hostile
      temple_of_earth: -80
      temple_of_air: -80
      temple_of_water: -80
      nulb_bandits: -40
      
    members:
      - "npc_001"             # Burne
      - "npc_002"             # Rufus
      # ... more members
      
    territory:
      - "hommlet"
      
    goals:
      - type: "defend"
        target: "hommlet"
      - type: "patrol"
        area: "hommlet_roads"
        
  temple_of_fire:
    id: "temple_of_fire"
    name: "Cult of the Fire Temple"
    type: "evil"
    power_level: 60
    
    relationships:
      hommlet_defenders: -80
      temple_of_earth: -20    # Competing evil factions
      temple_of_air: -20
      temple_of_water: -20
      
    members:
      - "npc_fire_priest_001"
      # ... more members
      
    territory:
      - "temple_level_1"
      
    goals:
      - type: "recruit"
        rate: 1               # New recruit every N ticks
      - type: "expand"
        target: "temple_level_2"
```

### Event Queue Schema

The event queue schedules future events in the world:

```yaml
events:
  - tick: 1500
    event_type: "faction_recruitment"
    data:
      faction: "temple_of_fire"
      location: "temple_level_1"
      
  - tick: 2000
    event_type: "wandering_monster"
    data:
      location: "moathouse_ruins"
      monster_type: "giant_rat"
      count: 5
      
  - tick: 2500
    event_type: "faction_conflict"
    data:
      attacker: "temple_of_fire"
      defender: "hommlet_defenders"
      location: "hommlet_roads"
```

## Saving and Loading

### Saving

Use the save_manager module to save game state:

```python
from src.persistence.save_manager import save
from pathlib import Path

# Save to YAML (default)
save(world_state, "saves/slot_1.yaml")

# Save to JSON
save(world_state, "saves/slot_1.json", format="json")
```

### Loading

Load game state from a file:

```python
from src.persistence.save_manager import load

# Format auto-detected from file extension
world_state = load("saves/slot_1.yaml")
```

## Version Compatibility

### Save File Version History

- **1.0.0** (Current)
  - Initial save format
  - Full WorldState serialization
  - Support for YAML and JSON

### Version Migration

When loading save files from older versions:

1. The `version` field is checked
2. If version differs from current, migration is attempted
3. Migration functions transform old format to new
4. A backup of the original save is created

```python
# Example migration (future)
def migrate_1_0_to_1_1(data: dict) -> dict:
    """Migrate save format from 1.0 to 1.1"""
    # Add new fields with defaults
    if 'weather' not in data['world_state']:
        data['world_state']['weather'] = 'clear'
    
    data['version'] = '1.1.0'
    return data
```

## Human-Readable State Exports

In addition to save files, the system can export human-readable reports:

### Faction Report

```
=== FACTION STATUS REPORT ===
Generated: 2024-12-06 12:30:45
Game Time: 1000 ticks (Day 1, 16:40)

FACTION: Defenders of Hommlet
  Type: Good
  Power Level: 75/100
  Members: 12
  Territory: Hommlet, Hommlet Roads
  Status: Strong
  
  Relationships:
    - Cult of Fire Temple: -80 (Hostile)
    - Cult of Earth Temple: -80 (Hostile)
    - Nulb Bandits: -40 (Unfriendly)

FACTION: Cult of the Fire Temple
  Type: Evil
  Power Level: 60/100
  Members: 24
  Territory: Temple Level 1
  Status: Growing
  
  Relationships:
    - Defenders of Hommlet: -80 (Hostile)
    - Cult of Earth Temple: -20 (Rival)
```

### NPC Roster

```
=== NPC ROSTER ===
Generated: 2024-12-06 12:30:45

Location: Hommlet

Burne the Wizard (npc_001)
  Class: Magic-User, Level 7
  Status: Alive, Patrolling
  HP: 20/20
  Location: Hommlet [15, 20]
  Faction: Defenders of Hommlet
  Equipment: Staff, Robes

Rufus the Fighter (npc_002)
  Class: Fighter, Level 6
  Status: Alive, Guard Duty
  HP: 48/48
  Location: Hommlet [16, 20]
  Faction: Defenders of Hommlet
  Equipment: Longsword +1, Plate Mail

...
```

## Performance Considerations

### File Size

- Typical save file: 100-500 KB for moderate game state
- Large games with many entities: 1-5 MB
- Consider compression for very large saves

### Save Time

- YAML: ~100ms for typical save
- JSON: ~50ms for typical save (faster but less readable)

### Load Time

- YAML: ~200ms for typical save
- JSON: ~100ms for typical save

## Validation

Save files are validated on load:

1. **Schema Validation**: Ensures all required fields present
2. **Type Checking**: Validates data types
3. **Reference Integrity**: Checks entity/location references
4. **Game Rules**: Validates stats within legal ranges

```python
from src.persistence.save_manager import load

try:
    world_state = load("saves/slot_1.yaml")
except FileNotFoundError:
    print("Save file not found")
except ValueError as e:
    print(f"Invalid save file: {e}")
```

## Security Considerations

While save files are human-readable and editable:

1. **Validation**: All loaded data is validated
2. **Sanitization**: User input is sanitized
3. **Integrity**: Checksums could be added for competitive play
4. **Cheating**: Single-player game - manual editing is allowed

## Best Practices

1. **Auto-save**: Implement periodic auto-saves (every 10 minutes or 100 ticks)
2. **Quick-save**: Provide quick-save shortcut (Ctrl+S)
3. **Backups**: Keep previous save as backup before overwriting
4. **Naming**: Use descriptive save names with timestamps
5. **Organization**: Keep saves in dedicated directory
6. **Compression**: Consider compression for archival

## Example Usage

### Creating a New Save

```python
from src.game.game_engine import GameEngine
from src.persistence.save_manager import save

engine = GameEngine()
# ... play game ...

save(engine.world, "saves/my_game.yaml")
```

### Loading a Save

```python
from src.persistence.save_manager import load
from src.game.game_engine import GameEngine

world = load("saves/my_game.yaml")
engine = GameEngine(world=world)
# Continue playing...
```

### Export State Report

```python
from src.persistence.state_exporter import export_faction_report

export_faction_report(world_state, "reports/factions.txt")
```

## Troubleshooting

### Common Issues

**Save file won't load**
- Check file format (valid YAML/JSON)
- Verify file version compatibility
- Check error message for specific validation failure

**Corrupted save file**
- Restore from backup (`.bak` file)
- Check for manual editing errors
- Validate YAML/JSON syntax

**Missing entities**
- Check entity references in save file
- Verify location assignments
- Run save file validation

**Performance issues**
- Consider switching to JSON format
- Enable save file compression
- Reduce auto-save frequency

## Future Enhancements

Planned improvements to save system:

1. **Compression**: Automatic compression for large saves
2. **Streaming**: Streaming saves for very large worlds
3. **Delta Saves**: Only save changes since last save
4. **Cloud Sync**: Optional cloud save synchronization
5. **Replay**: Save game replay/recording functionality
6. **Screenshots**: Embedded terminal screenshots in saves
