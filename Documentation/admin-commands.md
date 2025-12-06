# Admin Commands Reference

## Overview

Admin commands provide powerful tools for inspecting, debugging, and manipulating the game world. These commands are essential for testing, demonstration, and understanding the autonomous simulation system.

## Accessing Admin Mode

Admin commands can be accessed in two ways:

1. **From Game**: Press `~` or `:` to enter admin mode, then type commands
2. **Command Prefix**: Prefix any command with `/` or `!` while playing

```
Press '~' to enter admin mode:
> status
[Status information displayed]

Or use prefix during gameplay:
/status
```

## Command Categories

- [World Inspection](#world-inspection-commands)
- [World Manipulation](#world-manipulation-commands)
- [State Export](#state-export-commands)
- [Debugging](#debugging-commands)
- [System](#system-commands)

---

## World Inspection Commands

### `status`

Display overall world state summary.

**Usage:**
```
status
```

**Output:**
```
=== WORLD STATUS ===
Game Time: 1000 ticks (Day 1, 16:40)
Game Mode: Player
Locations: 45 loaded
Entities: 324 active (150 NPCs, 120 monsters, 54 items)
Factions: 8 active
Events Queued: 12

Player: Adventurer (Level 3 Fighter)
Location: Village of Hommlet [10, 5]
HP: 24/28
Status: Healthy
```

**Aliases:** `state`, `info`

---

### `factions [detail]`

Display faction power levels and relationships.

**Usage:**
```
factions                  # Brief overview
factions detail          # Detailed information
factions <faction_id>    # Specific faction
```

**Output:**
```
=== FACTION STATUS ===

Defenders of Hommlet (Power: 75/100) [GOOD]
  Members: 12 | Territory: 2 locations
  Status: Strong, Defensive Posture
  
Cult of Fire Temple (Power: 60/100) [EVIL]
  Members: 24 | Territory: 1 location
  Status: Growing, Recruiting
  Hostile to: Defenders of Hommlet (-80)
  
Cult of Earth Temple (Power: 55/100) [EVIL]
  Members: 20 | Territory: 1 location
  Status: Stable
  Rival to: Cult of Fire Temple (-20)
```

**Aliases:** `faction`, `fac`

---

### `npcs [faction|location]`

List NPCs with locations and stats.

**Usage:**
```
npcs                              # All NPCs
npcs hommlet                      # NPCs in Hommlet
npcs faction:hommlet_defenders    # NPCs in faction
npcs alive                        # Only living NPCs
npcs level>5                      # NPCs above level 5
```

**Output:**
```
=== NPC ROSTER ===

Location: Village of Hommlet (12 NPCs)

Burne the Wizard [npc_001]
  Class: Magic-User 7 | HP: 20/20 | AC: 8
  Status: Patrolling | Faction: Defenders of Hommlet
  Position: [15, 20] | AI State: patrol

Rufus the Fighter [npc_002]
  Class: Fighter 6 | HP: 48/48 | AC: 2
  Status: Guard Duty | Faction: Defenders of Hommlet
  Position: [16, 20] | AI State: guard
  Equipment: Longsword +1, Plate Mail

...
```

**Aliases:** `npc`, `characters`

---

### `monsters [location]`

List monsters in the world or specific area.

**Usage:**
```
monsters                     # All monsters
monsters temple_level_1      # Monsters in location
monsters alive               # Only living monsters
monsters hd>3                # Monsters with HD > 3
```

**Output:**
```
=== MONSTER ROSTER ===

Location: Temple Level 1 (15 monsters)

Gnoll Warrior x5 [monster_001-005]
  HD: 2 | HP: 12-15 | AC: 5
  Status: Guarding | Faction: Temple Guards
  Position: Patrol route A
  
Ogre [monster_006]
  HD: 4+1 | HP: 28 | AC: 5
  Status: Sleeping | Faction: Temple Guards
  Position: [12, 8]
  Treasure: 50 GP
```

**Aliases:** `monster`, `mon`

---

### `location <name>`

Show detailed information about a location.

**Usage:**
```
location hommlet
location temple_level_1
location                     # Current location
```

**Output:**
```
=== LOCATION: Village of Hommlet ===
ID: hommlet
Type: Town
Size: 30x40
Cleared: No
Last Visit: 950 ticks ago

Entities Present:
  NPCs: 12 (list: Burne, Rufus, ...)
  Monsters: 0
  Items: 5
  
Faction Control: Defenders of Hommlet (Strong)

Connections:
  North: Hommlet Roads
  South: Path to Moathouse
  West: Nulb Road
  
Features:
  - Inn of the Welcome Wench
  - Trading Post
  - Church of St. Cuthbert
  - Tower of Burne and Rufus
```

**Aliases:** `loc`, `where`

---

### `events [count]`

Show recent significant events.

**Usage:**
```
events              # Last 10 events
events 20           # Last 20 events
events all          # All events
events queued       # Upcoming scheduled events
```

**Output:**
```
=== RECENT EVENTS ===

[Tick 998] Combat: Gnoll defeated by Adventurer at Temple Level 1
[Tick 995] Recruitment: Temple of Fire recruited 2 new cultists
[Tick 990] Movement: Burne patrolled to [15, 25]
[Tick 985] Faction: Defenders of Hommlet power increased to 75
[Tick 980] Discovery: Adventurer found secret door at [10, 5]

=== QUEUED EVENTS ===

[Tick 1500] Faction Recruitment: Temple of Fire
[Tick 2000] Wandering Monster: Moathouse Ruins
[Tick 2500] Faction Conflict: Fire Temple vs Hommlet
```

**Aliases:** `event`, `log`, `history`

---

### `time`

Display current game time and calendar.

**Usage:**
```
time
```

**Output:**
```
=== GAME TIME ===
Ticks: 1000 (1 tick = 1 round = 1 minute)
Time: Day 1, 16:40 (4:40 PM)
Date: Coldeven 1, 579 CY
Season: Spring

Time Played: 2 hours 15 minutes
Next Event: Faction Recruitment in 500 ticks
```

**Aliases:** `clock`, `date`

---

## World Manipulation Commands

### `teleport <location> [x] [y]`

Teleport player to a location.

**Usage:**
```
teleport hommlet                    # Teleport to default position
teleport temple_level_1 10 5        # Teleport to specific coordinates
teleport @npc_001                   # Teleport to NPC location
```

**Output:**
```
Teleported to: Village of Hommlet [15, 20]
```

**Aliases:** `tp`, `goto`, `warp`

**Safety:** Prompts for confirmation if target is dangerous

---

### `reveal [area]`

Reveal map areas (remove fog of war).

**Usage:**
```
reveal                  # Reveal current location
reveal all              # Reveal entire game map
reveal hommlet          # Reveal specific location
reveal off              # Re-enable fog of war
```

**Output:**
```
Map revealed: Village of Hommlet (100% explored)
```

**Aliases:** `map`, `show`

---

### `spawn <entity> [location] [x] [y]`

Spawn an entity at a location.

**Usage:**
```
spawn gnoll                         # Spawn at player location
spawn gnoll temple_level_1 10 5     # Spawn at specific location
spawn burne hommlet                 # Spawn named NPC
spawn longsword+1                   # Spawn item at feet
```

**Output:**
```
Spawned: Gnoll Warrior [monster_new_001]
Location: Temple Level 1 [10, 5]
```

**Aliases:** `summon`, `create`

**Validation:** Checks if entity type exists and location is valid

---

### `kill <entity>`

Remove an entity from the game (instant death/destruction).

**Usage:**
```
kill monster_001                    # Kill specific monster
kill @target                        # Kill targeted entity
kill all:gnoll                      # Kill all gnolls
kill all:monsters:temple_level_1    # Kill all monsters in area
```

**Output:**
```
Killed: Gnoll Warrior [monster_001]
```

**Aliases:** `destroy`, `remove`, `delete`

**Safety:** Prompts for confirmation for mass kills

---

### `advance <ticks>`

Advance game time by specified ticks.

**Usage:**
```
advance 100             # Advance 100 ticks (~1.5 hours)
advance 1000            # Advance 1000 ticks (~16 hours)
advance 10000           # Advance 10000 ticks (~7 days)
```

**Output:**
```
Advancing 100 ticks...
[Processing events...]
Advanced to: Day 1, 18:20
Events processed: 3
- Faction Recruitment
- NPC patrol movements (x5)
- Wandering monster spawn
```

**Aliases:** `skip`, `fast-forward`, `ff`

**Note:** Processes all scheduled events and AI actions during advancement

---

### `setfaction <faction> <attribute> <value>`

Modify faction attributes.

**Usage:**
```
setfaction temple_of_fire power 80      # Set power level
setfaction hommlet_defenders add_member npc_001
setfaction temple_of_fire relation:temple_of_earth -50
```

**Output:**
```
Faction updated: Cult of Fire Temple
Power: 60 -> 80
```

**Aliases:** `modfaction`, `editfaction`

**Safety:** Prompts for confirmation for major changes

---

## State Export Commands

### `export state <filename>`

Export full world state to file.

**Usage:**
```
export state snapshot.yaml          # Export to YAML
export state snapshot.json          # Export to JSON
export state states/current.yaml    # Export to subdirectory
```

**Output:**
```
Exporting world state...
Written: states/snapshot.yaml (245 KB)
Entities: 324 | Locations: 45 | Factions: 8
```

**Aliases:** `save-state`, `dump`

---

### `export factions <filename>`

Export faction status report.

**Usage:**
```
export factions report.txt          # Export as text
export factions report.md           # Export as markdown
export factions report.html         # Export as HTML
```

**Output:**
```
Faction report exported: reports/factions.txt
8 factions documented
```

**Aliases:** `export-factions`

---

### `export npcs <filename>`

Export NPC roster with stats.

**Usage:**
```
export npcs roster.txt              # All NPCs
export npcs hommlet_npcs.txt location:hommlet
export npcs defenders.txt faction:hommlet_defenders
```

**Output:**
```
NPC roster exported: reports/roster.txt
150 NPCs documented
```

**Aliases:** `export-npcs`

---

### `export events <filename>`

Export event history log.

**Usage:**
```
export events history.txt           # All events
export events recent.txt last:100   # Last 100 events
export events combat.txt type:combat
```

**Output:**
```
Event log exported: logs/history.txt
523 events documented
```

**Aliases:** `export-log`, `export-history`

---

### `snapshot [name]`

Create a named snapshot of current world state.

**Usage:**
```
snapshot                            # Auto-named with timestamp
snapshot before_combat              # Named snapshot
snapshot list                       # List all snapshots
snapshot restore before_combat      # Restore from snapshot
```

**Output:**
```
Snapshot created: snapshots/before_combat_20241206_1230.yaml
World time: 1000 ticks
```

**Aliases:** `checkpoint`, `backup`

**Note:** Snapshots are saved separately from regular saves

---

## Debugging Commands

### `debug ai <entity>`

Show AI decision-making process for an entity.

**Usage:**
```
debug ai npc_001                    # Debug specific NPC
debug ai @target                    # Debug targeted entity
debug ai all                        # Enable AI debugging for all
debug ai off                        # Disable AI debugging
```

**Output:**
```
=== AI DEBUG: Burne the Wizard ===
Current State: patrol
Goal: Defend Hommlet
Perception: No threats detected
Decision Tree:
  1. Check for threats -> None
  2. Check patrol route -> Position 3/8
  3. Move to next waypoint -> [15, 25]
Action: Move North
```

**Aliases:** `ai`, `debug-ai`

---

### `debug combat`

Toggle detailed combat logging.

**Usage:**
```
debug combat on                     # Enable detailed combat logs
debug combat off                    # Disable
debug combat                        # Toggle
```

**Output:**
```
Combat debugging: ENABLED

Combat logs will show:
- Attack rolls and modifiers
- Damage calculations
- AC calculations
- THAC0 resolution
- Special attack details
```

**Aliases:** `debug-combat`, `combat-debug`

---

### `debug path <from> <to>`

Show pathfinding information between locations.

**Usage:**
```
debug path hommlet temple_level_1
debug path [10,5] [20,15]           # Coordinate-based
debug path @player @npc_001         # Between entities
```

**Output:**
```
=== PATHFINDING DEBUG ===
From: Hommlet [10, 5]
To: Temple Level 1 [5, 8]

Path found: Yes (12 steps)
Distance: 150 (manhattan) / 120 (actual)
Estimated time: 12 ticks

Route:
  Hommlet [10,5] -> Hommlet Roads [5,2] 
  -> Temple Approach [15,8] -> Temple Level 1 [5,8]

Obstacles: None
Hazards: Temple Guards (hostile)
```

**Aliases:** `path`, `route`

---

### `trace <entity>`

Enable detailed tracing for specific entity.

**Usage:**
```
trace npc_001                       # Trace specific entity
trace all:monsters                  # Trace all monsters
trace off                           # Disable all tracing
```

**Output:**
```
Tracing enabled for: Burne the Wizard [npc_001]

Trace will log:
- All actions and decisions
- State changes
- Position updates
- Combat participation
- AI processing

Trace log: traces/npc_001.log
```

**Aliases:** `watch`, `monitor`

---

## System Commands

### `help [command]`

Show help for admin commands.

**Usage:**
```
help                                # List all commands
help teleport                       # Help for specific command
help category:debug                 # Help for command category
```

**Output:**
```
=== ADMIN COMMAND HELP ===

Available Categories:
- World Inspection: status, factions, npcs, monsters, location, events, time
- World Manipulation: teleport, reveal, spawn, kill, advance, setfaction
- State Export: export, snapshot
- Debugging: debug, trace
- System: help, history, alias, exit

Use 'help <command>' for detailed information
Use 'help category:<name>' for category help
```

**Aliases:** `?`, `man`

---

### `history`

Show command history.

**Usage:**
```
history                             # Show all history
history 10                          # Show last 10 commands
history clear                       # Clear history
```

**Output:**
```
=== COMMAND HISTORY ===
1. status
2. factions detail
3. npcs hommlet
4. teleport temple_level_1
5. debug ai npc_001
```

**Aliases:** `hist`

---

### `alias <name> <command>`

Create command aliases.

**Usage:**
```
alias st status                     # Create alias
alias list                          # List all aliases
alias remove st                     # Remove alias
```

**Output:**
```
Alias created: 'st' -> 'status'
```

---

### `exit`

Exit admin mode and return to game.

**Usage:**
```
exit
```

**Aliases:** `quit`, `q`, `x`

---

## Command Syntax

### General Rules

1. **Case Insensitive**: Commands are case-insensitive
2. **Completion**: Tab completion for commands and arguments
3. **History**: Up/down arrows for command history
4. **Abbreviation**: Commands can be abbreviated if unambiguous
5. **Chaining**: Multiple commands separated by `;`

### Special Syntax

- `@entity_id` - Reference entity by ID
- `@target` - Reference currently targeted entity
- `@player` - Reference player character
- `location:name` - Filter by location
- `faction:name` - Filter by faction
- `all:type` - Apply to all of type

### Examples

```
# Command abbreviation
stat                   # Same as 'status'
fac det                # Same as 'factions detail'

# Command chaining
status; factions; npcs hommlet

# Entity references
kill @target
teleport @npc_001

# Filters
npcs location:hommlet faction:defenders
monsters hd>3 alive
```

## Configuration

Admin commands can be configured in `config.yaml`:

```yaml
admin:
  enabled: true
  prefix: ["/", "!"]              # Command prefixes
  activation_key: "~"             # Key to enter admin mode
  require_confirmation: true      # Prompt before destructive actions
  log_commands: true              # Log all admin commands
  command_history_size: 100       # Number of commands to remember
```

## Security

For multiplayer or competitive scenarios:

1. **Authentication**: Admin mode requires password
2. **Logging**: All admin commands are logged
3. **Restrictions**: Some commands can be disabled
4. **Audit Trail**: Complete audit trail of admin actions

## Best Practices

1. **Use exports**: Regularly export state for backup
2. **Snapshots**: Create snapshots before major changes
3. **Confirmation**: Pay attention to confirmation prompts
4. **Documentation**: Use `help` to discover commands
5. **Debugging**: Enable AI/combat debugging to understand behavior
6. **Testing**: Use admin commands to test game scenarios

## Scripting

Admin commands can be scripted for automation:

```bash
# script.txt
status
factions detail
export state test_state.yaml
spawn gnoll temple_level_1 10 5
advance 100
export events test_events.txt
```

Run with:
```
load script.txt
```

## Troubleshooting

### Common Issues

**Command not recognized**
- Check spelling
- Use `help` to see available commands
- Try tab completion

**Permission denied**
- Ensure admin mode is enabled
- Check configuration settings

**Invalid arguments**
- Use `help <command>` for syntax
- Check entity/location IDs
- Verify filters and selectors

## Future Enhancements

Planned improvements:

1. **Scripting**: Full scripting language for commands
2. **Macros**: Record and replay command sequences
3. **Remote Admin**: Network-based admin interface
4. **GUI Admin**: Graphical admin console
5. **Autocompletion**: Smarter context-aware completion
6. **Command Templates**: Saved command templates
