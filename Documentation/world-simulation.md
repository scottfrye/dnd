# World Simulation - Core Systems and AI

## Overview

This document describes the world simulation architecture for the Temple of Elemental Evil AD&D 1E roguelike game. The world simulation enables autonomous gameplay where NPCs, factions, and the game world evolve over time without player intervention. This supports both player-driven gameplay and headless simulation modes.

## Architecture

The world simulation consists of five core interconnected systems:

1. **World State** - Central registry for all game entities and world data
2. **Time System** - Manages game time progression and time unit conversions
3. **Event System** - Schedules and dispatches time-based events
4. **Faction Manager** - Tracks faction relationships, power, and territory
5. **NPC/Faction AI** - Autonomous behavior for NPCs and faction-level strategies

## System Components

### 1. World State (`src/world/world_state.py`)

**Purpose**: Central registry and single source of truth for all game entities and world time.

**Status**: ✅ **Implemented**

**Key Responsibilities**:
- Maintain registry of all game entities (characters, monsters, items, locations)
- Track current game time (tick counter)
- Provide entity query and management operations
- Support serialization for save/load functionality

**Data Structure**:
```python
WorldState {
    _entities: dict[str, Entity]  # Entity registry by ID
    _time: int                     # Current game tick
}
```

**Key Operations**:
- `add_entity(entity)` - Register new entity in world
- `remove_entity(entity_id)` - Remove entity from world
- `get_entity(entity_id)` - Retrieve entity by ID
- `get_all_entity_ids()` - List all registered entity IDs
- `tick()` - Advance world time by one tick
- `to_dict()` / `from_dict()` - Serialization support

**Data Flow**:
```
GameEngine → WorldState.add_entity() → Entity Registry
GameEngine → WorldState.tick() → Time advancement → Event System trigger
NPC AI → WorldState.get_entity() → Entity queries for decision making
```

**Related Sub-Issues**:
- **Issue: World State Enhancement** - Extend world state to track faction territories, global flags, and environmental conditions

---

### 2. Time System (`src/world/time_system.py`)

**Purpose**: Manage game time progression and conversions between different time units following AD&D 1E conventions.

**Status**: ✅ **Implemented**

**Key Responsibilities**:
- Track current game time in ticks (1 tick = 1 second)
- Convert between time units (ticks, rounds, turns, hours, days)
- Advance time with validation
- Provide time component breakdown

**Time Unit Definitions** (AD&D 1E standard):
- **Tick**: 1 second (base unit)
- **Round**: 10 ticks (10 seconds, combat round)
- **Turn**: 600 ticks (10 minutes, exploration unit)
- **Hour**: 3600 ticks (60 minutes)
- **Day**: 86400 ticks (24 hours)

**Data Structure**:
```python
TimeSystem {
    _current_tick: int
    TICKS_PER_ROUND: 10
    TICKS_PER_TURN: 600
    TICKS_PER_HOUR: 3600
    TICKS_PER_DAY: 86400
}
```

**Key Operations**:
- `advance(ticks)` - Move time forward
- `ticks_to_rounds/turns/hours/days()` - Convert to larger units
- `rounds/turns/hours/days_to_ticks()` - Convert to ticks
- `get_time_components()` - Break down current time

**Data Flow**:
```
GameEngine → TimeSystem.advance() → Time progression
Event System → TimeSystem.current_tick → Event dispatch timing
Faction AI → TimeSystem.ticks_to_days() → Long-term planning
```

**Related Sub-Issues**:
- **Issue: Time System Integration** - Integrate time system with event triggers, NPC schedules, and day/night cycles

---

### 3. Event System (`src/world/event_system.py`)

**Purpose**: Schedule and dispatch callable events at specific future game ticks, enabling time-based game mechanics.

**Status**: ✅ **Implemented**

**Key Responsibilities**:
- Schedule events to fire at future ticks
- Dispatch events when their time arrives
- Support event cancellation
- Track pending events
- Handle event execution errors gracefully

**Data Structure**:
```python
ScheduledEvent {
    tick: int                      # When to fire
    callback: Callable             # Function to execute
    args: tuple                    # Positional arguments
    kwargs: dict                   # Keyword arguments
    event_id: str                  # Unique identifier
}

EventSystem {
    _events: list[ScheduledEvent]  # Event queue
    _next_event_id: int           # Auto-incrementing ID
}
```

**Event Types** (examples to be scheduled):

#### Combat & Action Events
- **attack_resolution** - Resolve delayed attack effects
- **spell_effect** - Apply spell effects over time
- **status_effect_tick** - Process ongoing status effects (poison, paralysis)
- **regeneration** - Apply creature regeneration

#### World Events
- **wandering_monster** - Spawn wandering monsters
- **npc_patrol** - Trigger NPC patrol movement
- **faction_recruitment** - Execute faction recruitment
- **faction_battle** - Resolve faction conflicts
- **treasure_respawn** - Repopulate cleared areas

#### Environmental Events
- **day_night_transition** - Change lighting and NPC schedules
- **weather_change** - Alter weather conditions
- **temple_ceremony** - Trigger special module events

#### NPC Behavior Events
- **npc_decision** - Process NPC AI decision points
- **guard_rotation** - Change guard positions
- **merchant_restock** - Refresh merchant inventory

**Key Operations**:
- `schedule(tick, callback, *args, event_id, **kwargs)` - Schedule new event
- `tick(current_tick)` - Dispatch events for current tick
- `cancel_event(event_id)` - Cancel scheduled event
- `get_pending_events()` - Query upcoming events
- `clear_all_events()` - Reset event queue

**Data Flow**:
```
Game Action → EventSystem.schedule() → Event queued
WorldState.tick() → EventSystem.tick() → Events dispatched → Callbacks executed
Faction AI → EventSystem.schedule(faction_battle) → Future battle planned
Event Callback → WorldState changes → World evolution
```

**Related Sub-Issues**:
- **Issue: Event System Enhancement** - Add event priorities, repeating events, event dependencies, and event history logging

---

### 4. Faction Manager

**Purpose**: Track faction relationships, power dynamics, territorial control, and inter-faction interactions.

**Status**: ⚠️ **Not Yet Implemented**

**Key Responsibilities**:
- Maintain faction registry and relationships
- Track faction power levels and territories
- Manage faction alliances and hostilities
- Resolve inter-faction conflicts
- Handle faction-wide events (recruitment, battles)

**Planned Data Structure**:
```python
Faction {
    id: str                           # Unique faction identifier
    name: str                         # Display name
    leader_id: str                    # Reference to leader entity
    members: set[str]                 # Set of member entity IDs
    power_level: int                  # Current faction strength
    territories: list[str]            # Controlled location IDs
    relationships: dict[str, int]     # Faction ID -> relationship value
    resources: dict[str, int]         # Resource pools (gold, influence)
    goals: list[str]                  # Current faction objectives
}

FactionManager {
    _factions: dict[str, Faction]     # Faction registry
    _territory_control: dict[str, str] # Location ID -> Faction ID
    _global_tensions: int             # Overall conflict level
}
```

**Faction Relationship Values**:
- **100+**: Strong alliance
- **50-99**: Friendly
- **0-49**: Neutral
- **-1 to -49**: Unfriendly
- **-50 to -99**: Hostile
- **-100 or less**: Open warfare

**Key Operations** (planned):
- `add_faction(faction)` - Register new faction
- `get_faction(faction_id)` - Retrieve faction data
- `get_entity_faction(entity_id)` - Find entity's faction membership
- `add_member(faction_id, entity_id)` - Add entity to faction
- `remove_member(faction_id, entity_id)` - Remove entity from faction
- `update_relationship(faction_a, faction_b, change)` - Modify relationship
- `claim_territory(faction_id, location_id)` - Assert territorial control
- `get_faction_power(faction_id)` - Calculate current power level
- `resolve_conflict(faction_a, faction_b)` - Handle faction battles

**Data Flow** (planned):
```
NPC Death → FactionManager.remove_member() → Power recalculation
Leader Recruitment → FactionManager.add_member() → Power increase
Faction AI → FactionManager.get_faction_power() → Strategy decisions
Territory Capture → FactionManager.claim_territory() → Control shift
Conflict Event → FactionManager.resolve_conflict() → Battle outcome → World changes
```

**Temple of Elemental Evil Factions**:

Based on the adventure module, key factions include:

1. **Fire Temple** (Cult of the Salamander)
   - Leader: Alrem (8th level cleric)
   - Goal: Dominate through force and destruction
   - Hostile to: Water, Air, Earth temples
   
2. **Water Temple** (Cult of the Crayfish)
   - Leader: Belsornig (9th level cleric)
   - Goal: Infiltration and subversion
   - Hostile to: Fire, Air, Earth temples
   
3. **Air Temple** (Cult of the Air)
   - Leader: Kelashein (7th level cleric)
   - Goal: Espionage and sabotage
   - Hostile to: Fire, Water, Earth temples
   
4. **Earth Temple** (Cult of the Black Earth)
   - Leader: Romag (9th level cleric)
   - Goal: Slow, steady conquest
   - Hostile to: Fire, Water, Air temples
   
5. **Greater Temple** (Zuggtmoy's Servants)
   - Leader: Zuggtmoy (demon)
   - Goal: Free Zuggtmoy, corrupt surroundings
   - Controls: All elemental temples nominally
   
6. **Hommlet Defenders**
   - Leaders: Burne (8th level wizard), Rufus (6th level fighter)
   - Goal: Protect Hommlet, oppose evil temple
   - Allied with: Good-aligned parties
   
7. **Nulb Raiders**
   - Leader: Various low-level bandits
   - Goal: Raiding and pillaging
   - Loosely allied with: Temple forces

**Related Sub-Issues**:
- **Issue: Faction Manager Implementation** - Implement faction system with relationship tracking, power calculations, and territory management

---

### 5. NPC/Faction AI (`src/simulation/npc_ai.py`)

**Purpose**: Autonomous behavior systems for individual NPCs and faction-level strategic AI.

**Status**: 🟡 **Partially Implemented**

**Current Implementation**:

The module currently provides basic NPC behaviors:

```python
Action {
    action_type: str                # "move", "attack", "idle", etc.
    target_position: Position       # For movement
    target_entity_id: str           # For attacks
    data: dict                      # Additional parameters
}
```

**Implemented Behaviors**:

1. **idle_behavior(npc, world)** - NPC does nothing
2. **patrol_behavior(npc, world)** - NPC moves between waypoints
3. **attack_on_sight_behavior(npc, world)** - NPC attacks nearby hostiles

**Helper Functions**:
- `apply_action(action, npc, world)` - Execute action in world state

**Planned Enhancements**:

#### Individual NPC AI Behaviors

1. **Guard Behavior**
   - Patrol assigned area
   - Investigate disturbances
   - Call for reinforcements
   - Return to post after combat

2. **Priest Behavior**
   - Perform temple duties
   - Cast buff spells on allies
   - Heal injured faction members
   - Lead ceremonies

3. **Leader Behavior**
   - Command subordinates
   - Recruit new followers
   - Make strategic decisions
   - Coordinate with other leaders

4. **Merchant Behavior**
   - Open/close shop on schedule
   - Adjust prices based on supply/demand
   - Restock inventory
   - Flee or hide during danger

5. **Commoner Behavior**
   - Follow daily schedule
   - Flee from danger
   - Seek help from guards
   - Gossip and spread information

6. **Monster Behavior** (by type)
   - Territorial predators
   - Pack hunters
   - Ambush predators
   - Mindless wanderers
   - Intelligent tacticians

#### Faction-Level AI (To Be Implemented)

**Data Structure** (planned):
```python
FactionStrategy {
    faction_id: str
    recruitment_rate: float        # New members per day
    expansion_priority: int        # Territorial ambition
    aggression_level: int          # Likelihood to attack
    resource_allocation: dict      # How to spend resources
    current_objective: str         # Active goal
}

FactionAI {
    _strategies: dict[str, FactionStrategy]
}
```

**Faction AI Behaviors** (planned):

1. **Recruitment Strategy**
   - Assess faction strength
   - Allocate resources to recruitment
   - Select appropriate recruit types
   - Schedule recruitment events

2. **Territorial Strategy**
   - Identify expansion targets
   - Assess target strength
   - Plan invasion timing
   - Coordinate multi-faction attacks

3. **Diplomatic Strategy**
   - Evaluate relationship values
   - Form temporary alliances
   - Break alliances when advantageous
   - Respond to provocations

4. **Resource Management**
   - Collect tribute from territories
   - Invest in infrastructure
   - Stockpile for major offensives
   - Trade with neutral factions

5. **Conflict Resolution**
   - Assess relative power
   - Decide to attack, defend, or retreat
   - Calculate battle outcomes
   - Apply consequences (casualties, territory changes)

**Key Operations** (planned):
- `execute_turn(faction_id, world)` - Process faction AI turn
- `should_recruit(faction_id)` - Decide if recruiting this turn
- `select_recruitment_target()` - Choose what to recruit
- `should_attack(faction_id, target_faction_id)` - Evaluate attack decision
- `plan_battle(attacker_id, defender_id)` - Prepare conflict
- `should_seek_alliance(faction_id, other_faction_id)` - Diplomatic decision

**Data Flow**:
```
Simulation Tick → NPC AI behaviors → Actions generated
Actions → apply_action() → WorldState changes
WorldState.tick() → Faction AI evaluates → Strategic decisions
Faction AI → EventSystem.schedule(recruitment/battle) → Future events
Event fires → Faction AI executes → World evolution
NPC dies → FactionManager updates → AI adapts strategy
```

**AI Decision Factors**:

Individual NPC decisions consider:
- Personality traits (brave, cowardly, loyal, etc.)
- Current HP/status effects
- Nearby allies and enemies
- Faction orders/objectives
- Environmental factors

Faction AI decisions consider:
- Current power level
- Relationship with other factions
- Territorial holdings
- Resource availability
- Global tensions
- Leader personality traits

**Related Sub-Issues**:
- **Issue: NPC AI Enhancement** - Expand individual NPC behaviors, add personality system, improve decision-making
- **Issue: Faction AI Implementation** - Create faction-level strategic AI for recruitment, diplomacy, and warfare

---

## System Integration

### Simulation Loop

The complete simulation cycle integrates all five systems:

```
1. GameEngine.run_headless(ticks)
   ↓
2. For each tick:
   a. WorldState.tick()
      - Increment time counter
      - Log tick event
      ↓
   b. EventSystem.tick(current_tick)
      - Dispatch scheduled events
      - Events may modify WorldState
      - Events may schedule new events
      ↓
   c. For each NPC entity:
      - Get NPC's AI behavior function
      - Execute behavior(npc, world) → Action
      - apply_action(action, npc, world)
      - Actions may schedule events
      ↓
   d. For each faction (if tick % FACTION_TURN_INTERVAL == 0):
      - FactionAI.execute_turn(faction, world)
      - May schedule recruitment events
      - May schedule conflict events
      - May update relationships
      ↓
   e. Log simulation state
      - Save world snapshot (optional)
      - Record statistics
      ↓
3. Return final world state
```

### Event-Driven Architecture

The systems communicate primarily through events:

**NPC Action → Event**:
```python
# NPC decides to recruit
action = recruit_behavior(leader, world)
# Schedule recruitment event in 1 day
event_system.schedule(
    time_system.current_tick + time_system.TICKS_PER_DAY,
    faction_manager.add_member,
    faction_id=leader.faction,
    entity_id=new_recruit_id
)
```

**Faction Battle → Events**:
```python
# Faction AI decides to attack
faction_ai.plan_battle(fire_temple, water_temple)
# Schedule battle resolution
event_system.schedule(
    time_system.current_tick + 3600,  # 1 hour from now
    faction_manager.resolve_conflict,
    attacker="fire_temple",
    defender="water_temple"
)
# Battle resolution may generate more events:
# - Member deaths → remove_member events
# - Territory changes → claim_territory events
# - Reputation changes → update_relationship events
```

### Data Flow Summary

```
┌─────────────────┐
│   GameEngine    │
│  (Orchestrator) │
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌─────────────┐  ┌─────────────┐
│ WorldState  │  │ TimeSystem  │
│   (Data)    │  │   (Time)    │
└──────┬──────┘  └──────┬──────┘
       │                │
       │                │
       ▼                ▼
┌──────────────────────────────┐
│       EventSystem            │
│  (Temporal Coordination)     │
└───────────┬──────────────────┘
            │
    ┌───────┴────────┐
    ▼                ▼
┌─────────┐    ┌──────────────┐
│ NPC AI  │    │FactionManager│
│(Micro)  │◄──►│   (Macro)    │
└─────────┘    └──────────────┘
    │                │
    └────────┬───────┘
             ▼
      ┌─────────────┐
      │ Faction AI  │
      │ (Strategy)  │
      └─────────────┘
```

**Arrows indicate**:
- **Read**: Query data for decision-making
- **Write**: Modify state
- **Schedule**: Create future events

---

## Headless Simulation Mode

The architecture supports autonomous world simulation without player input:

**Activation**:
```python
from src.game.game_engine import GameEngine, GameMode

# GameMode enum values: PLAYER, HEADLESS
engine = GameEngine(mode=GameMode.HEADLESS)
final_state = engine.run_headless(86400)  # Simulate 1 day
```

**Headless Mode Features**:
- Accelerated time progression (no player input delays)
- NPC AI controls all entities
- Faction AI drives strategic decisions
- Events fire automatically
- State snapshots at intervals
- Statistics tracking (battles, deaths, recruitments)
- Logging for analysis

**Use Cases**:
- Generate evolved world states for new games
- Test faction balance and AI behavior
- Create narrative history for ongoing campaigns
- Simulate passage of time between player sessions
- Debug world dynamics at scale

---

## Performance Considerations

### Scalability

The system must handle:
- **100+ NPCs** with individual AI
- **7 factions** with active AI
- **50+ locations** with territorial control
- **1000+ events** in the queue simultaneously
- **10,000+ ticks** (2.7+ hours game time) per simulation run

### Optimization Strategies

1. **Spatial Partitioning**
   - Only evaluate NPCs in active locations
   - Cache entity queries by location
   - Use spatial hash maps for proximity searches

2. **Event Queue Optimization**
   - Maintain sorted event queue (heap)
   - Batch event dispatch
   - Prune expired events

3. **AI Update Frequency**
   - Individual NPCs: Every tick (if in active areas)
   - Faction AI: Every 600 ticks (10 minutes)
   - Background NPCs: Every 3600 ticks (1 hour)

4. **State Caching**
   - Cache faction power calculations
   - Memoize relationship queries
   - Lazy-load entity properties

5. **Incremental Saves**
   - Checkpoint world state periodically
   - Delta compression for entity changes
   - Asynchronous save operations

---

## Testing Strategy

### Unit Tests

Each system has dedicated test coverage:

- **WorldState**: ✅ Entity management, time tracking, serialization
- **TimeSystem**: ✅ Time advancement, unit conversions, validation
- **EventSystem**: ✅ Event scheduling, dispatch, cancellation
- **FactionManager**: ⚠️ To be implemented
- **NPC AI**: 🟡 Basic behaviors tested, needs expansion

### Integration Tests

Required test scenarios:

1. **NPC AI → WorldState**: NPC actions modify entities correctly
2. **TimeSystem → EventSystem**: Events fire at correct ticks
3. **FactionAI → FactionManager**: Faction decisions update state
4. **EventSystem → NPC AI**: Events trigger NPC behavior changes
5. **Full Simulation**: 1000-tick headless run completes successfully

### Simulation Tests

Long-running validation:

- **Balance Test**: No faction dominates completely after 10,000 ticks
- **Liveness Test**: World continues evolving (no deadlock states)
- **Correctness Test**: Entity counts remain consistent
- **Performance Test**: 10,000 ticks completes within reasonable time

---

## Future Enhancements

### Short-Term

1. **Implement FactionManager** (High Priority)
   - Basic faction registry and relationships
   - Power level calculations
   - Territory tracking

2. **Expand NPC AI Behaviors** (High Priority)
   - Guard, priest, leader behaviors
   - Personality system
   - Schedule-based behaviors

3. **Implement Faction AI** (High Priority)
   - Recruitment strategy
   - Conflict resolution
   - Basic diplomacy

4. **Event System Enhancements** (Medium Priority)
   - Repeating events
   - Event priorities
   - Event dependencies

### Long-Term

1. **Advanced AI Features**
   - Machine learning for strategy optimization
   - Dynamic difficulty adjustment
   - Emergent storytelling

2. **Distributed Simulation**
   - Multi-threaded faction AI
   - Parallel entity processing
   - Cloud-based mega-simulations

3. **Analytics and Visualization**
   - Power dynamics graphs over time
   - Territory control heat maps
   - Faction relationship network diagrams
   - Battle outcome statistics

4. **Modding Support**
   - Custom faction definitions
   - Pluggable AI behaviors
   - Event scripting API

---

## Related Sub-Issues

To complete this epic, the following sub-issues should be created and tracked:

### 1. Issue: World State Enhancement
**Description**: Extend WorldState to support faction territories, global flags, and environmental conditions.

**Acceptance Criteria**:
- WorldState tracks faction-controlled territories
- Global flags system for module-specific events
- Environmental state (weather, time of day)
- Enhanced serialization for new features

### 2. Issue: Time System Integration
**Description**: Integrate TimeSystem with day/night cycles, NPC schedules, and event triggers.

**Acceptance Criteria**:
- Day/night cycle tracking
- Time-of-day helper methods
- Schedule system for recurring events
- Calendar/date tracking for long-term simulations

### 3. Issue: Event System Enhancement
**Description**: Add advanced event features including priorities, dependencies, and history.

**Acceptance Criteria**:
- Event priority system for conflict resolution
- Event dependencies (events that require others)
- Repeating/recurring events
- Event history log for debugging
- Performance optimization for large event queues

### 4. Issue: Faction Manager Implementation
**Description**: Implement complete faction management system.

**Acceptance Criteria**:
- Faction registry with full Temple of Elemental Evil factions
- Relationship tracking between factions
- Power level calculations
- Territory control system
- Conflict resolution mechanics
- Integration with WorldState and EventSystem
- Comprehensive unit tests

### 5. Issue: NPC/Faction AI Enhancement
**Description**: Expand NPC behaviors and implement faction-level strategic AI.

**Acceptance Criteria**:
- 6+ distinct NPC behavior types implemented
- Personality system for behavior variation
- Faction AI with recruitment strategy
- Faction AI with conflict decision-making
- Faction AI with diplomacy
- Integration with FactionManager
- Performance profiling and optimization
- Integration and simulation tests

---

## References

- **AD&D 1E Rules**: Player's Handbook, Dungeon Master's Guide, Monster Manual
- **Temple of Elemental Evil Module**: Adventure background, faction descriptions
- **Implementation Plan**: `Documentation/Temple of Elemental Evil - AD&D 1E Roguelike Implementation Plan.md`
- **Source Code**:
  - `src/world/world_state.py` - World state management
  - `src/world/time_system.py` - Time tracking
  - `src/world/event_system.py` - Event scheduling
  - `src/simulation/npc_ai.py` - NPC behaviors
  - `tests/test_world_state.py` - WorldState tests
  - `tests/test_time_system.py` - TimeSystem tests
  - `tests/test_event_system.py` - EventSystem tests

---

## Conclusion

The world simulation architecture provides a robust foundation for autonomous gameplay and world evolution. With three systems fully implemented (WorldState, TimeSystem, EventSystem) and two systems planned (FactionManager, enhanced AI), the architecture supports:

1. **Modularity**: Each system has clear responsibilities and interfaces
2. **Extensibility**: New behaviors and events can be added easily
3. **Testability**: Each system is independently testable
4. **Performance**: Designed for 100+ NPCs and 1000+ events
5. **Integration**: Systems communicate through clear data flows and events

The planned sub-issues provide a clear roadmap for completing the world simulation epic, with each issue building on the existing foundation to create a living, breathing game world that evolves whether players are present or not.
