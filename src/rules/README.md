# AD&D 1E Rules Engine

This directory contains the implementation of Advanced Dungeons & Dragons (1st Edition) game mechanics. The rules engine is designed to be modular, well-tested, and faithful to the original AD&D 1E Player's Handbook and Dungeon Master's Guide.

## Table of Contents

- [Architecture](#architecture)
- [Current Modules](#current-modules)
  - [Abilities](#abilities-module)
  - [Combat System](#combat-system-module)
- [Planned Modules](#planned-modules)
- [Public APIs](#public-apis)
- [Extension Points](#extension-points)
- [Testing Strategy](#testing-strategy)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)

## Architecture

The rules engine is organized into focused, single-responsibility modules that each handle a specific aspect of AD&D 1E mechanics. Each module:

- **Is self-contained**: Minimal dependencies on other rules modules
- **Is well-documented**: Comprehensive docstrings following Google style
- **Is fully tested**: >90% code coverage target for all modules
- **Follows AD&D 1E**: Implements canonical rules from official sources
- **Provides type hints**: Full type annotations for better IDE support

### Design Principles

1. **Separation of Concerns**: Each module handles one aspect of the rules (abilities, combat, spells, etc.)
2. **Immutability Preference**: Use immutable data structures where practical (dataclasses, tuples)
3. **Explicit Over Implicit**: Clear function names, no magic numbers, documented assumptions
4. **Testability**: All functions accept optional parameters for deterministic testing
5. **Extensibility**: Clear extension points for custom rules or variants

## Current Modules

### Abilities Module

**File**: `abilities.py`

Implements the six primary ability scores (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma) and their associated modifiers per AD&D 1E Player's Handbook Tables I, II, and III.

#### Key Classes

- `AbilityScores`: Dataclass storing all six ability scores with validation

#### Key Functions

- `get_strength_hit_modifier(strength: int) -> int`: Returns to-hit bonus/penalty
- `get_strength_damage_modifier(strength: int) -> int`: Returns damage bonus/penalty
- `get_strength_modifiers(strength: int) -> tuple[int, int]`: Returns both hit and damage modifiers
- `get_dexterity_ac_modifier(dexterity: int) -> int`: Returns AC adjustment (negative is better)
- `get_dexterity_initiative_modifier(dexterity: int) -> int`: Returns initiative bonus/penalty
- `get_dexterity_modifiers(dexterity: int) -> tuple[int, int]`: Returns both initiative and AC modifiers
- `get_constitution_hp_modifier(constitution: int) -> int`: Returns HP per level bonus/penalty

#### Coverage Status

- **Current**: 92% coverage
- **Target**: 95% coverage
- **Missing**: Edge cases for invalid input values

### Combat System Module

**File**: `combat_system.py`

Implements THAC0 (To Hit Armor Class 0) combat mechanics from AD&D 1E. Handles attack resolution, critical hits/misses, and class-based attack progression.

#### Key Classes

- `CombatStats`: Dataclass for attacker/defender combat statistics
- `AttackResult`: Dataclass for attack resolution results

#### Key Functions

- `get_thac0(level: int, class_group: str) -> int`: Returns THAC0 for a class/level
- `calculate_target_number(thac0: int, target_ac: int) -> int`: Calculates roll needed to hit
- `resolve_attack(attacker: CombatStats, defender: CombatStats, ...) -> AttackResult`: Full attack resolution
- `resolve_attack_simple(attacker_thac0: int, defender_ac: int, ...) -> tuple[bool, int]`: Simplified attack resolution

#### Class Groups

- `fighter`: Fighters, Paladins, Rangers (THAC0 improves every level)
- `cleric`: Clerics, Druids (THAC0 improves every 3 levels)
- `thief`: Thieves, Assassins, Monks (THAC0 improves every 4 levels)
- `magic_user`: Magic-Users, Illusionists (THAC0 improves every 5 levels)

#### Coverage Status

- **Current**: 95% coverage
- **Target**: 95% coverage
- **Status**: ✅ Target met

## Planned Modules

The following modules are planned to complete the AD&D 1E rules engine. Each represents a separate development effort:

### Character Classes

**Planned File**: `character_classes.py`

- Class definitions (Fighter, Cleric, Magic-User, Thief, Ranger, Paladin, Druid, etc.)
- Level progression tables
- Hit dice and hit point calculation
- Class-specific abilities and restrictions
- Multi-classing and dual-classing rules
- Level limits by race

**Estimated Complexity**: High  
**Dependencies**: abilities.py, combat_system.py  
**Target Coverage**: 90%

### Races

**Planned File**: `races.py`

- Race definitions (Human, Elf, Dwarf, Halfling, Half-Elf, Gnome, Half-Orc)
- Racial ability adjustments
- Level limits by class
- Special abilities (infravision, resistance to magic, etc.)
- Racial languages
- Height/weight tables

**Estimated Complexity**: Medium  
**Dependencies**: abilities.py  
**Target Coverage**: 90%

### Spells

**Planned File**: `spells.py`

- Spell definitions for all classes
- Spell effects and mechanics
- Spell level organization
- Memorization rules
- Casting time and components
- Duration and area of effect
- Saving throw mechanics

**Estimated Complexity**: Very High  
**Dependencies**: abilities.py, character_classes.py, saving_throws.py  
**Target Coverage**: 85%

### Magic Items

**Planned File**: `magic_items.py`

- Magic item types (weapons, armor, potions, scrolls, rings, etc.)
- Item effects and powers
- Cursed items
- Artifact and relic rules
- Item identification mechanics

**Estimated Complexity**: High  
**Dependencies**: abilities.py, spells.py  
**Target Coverage**: 85%

### Experience & Leveling

**Planned File**: `experience.py`

- XP awards for monsters defeated
- XP awards for treasure gained
- Level advancement tables by class
- Training time and cost
- Multi-class XP division

**Estimated Complexity**: Medium  
**Dependencies**: character_classes.py  
**Target Coverage**: 90%

### Saving Throws

**Planned File**: `saving_throws.py`

- Five saving throw categories (Paralyzation/Poison/Death Magic, Petrification/Polymorph, Rod/Staff/Wand, Breath Weapon, Spell)
- Saving throw tables by class and level
- Racial bonuses
- Magic item bonuses
- Situational modifiers

**Estimated Complexity**: Medium  
**Dependencies**: character_classes.py, races.py  
**Target Coverage**: 90%

### Morale

**Planned File**: `morale.py`

- Morale check mechanics
- Morale score calculations
- Morale modifiers (leader presence, casualties, etc.)
- NPC and monster morale behavior
- Surrender and retreat mechanics

**Estimated Complexity**: Low  
**Dependencies**: None  
**Target Coverage**: 90%

## Public APIs

All modules in the rules engine expose their public APIs through the `src/rules/__init__.py` file. This provides a clean import interface for game code:

```python
from src.rules import (
    AbilityScores,
    get_strength_modifiers,
    get_dexterity_modifiers,
    get_constitution_hp_modifier,
    CombatStats,
    resolve_attack,
    get_thac0,
)
```

### API Design Guidelines

When adding new modules to the rules engine:

1. **Export public classes and functions** in `__init__.py`
2. **Keep internal helpers private** (prefix with `_`)
3. **Use descriptive names** that indicate what the function calculates/does
4. **Provide comprehensive docstrings** including Args, Returns, Raises
5. **Include type hints** for all parameters and return values
6. **Support optional parameters** for testability (seed values, pre-determined rolls)

## Extension Points

The rules engine is designed to be extended in several ways:

### 1. Custom Ability Score Interpretations

The ability modifier functions are independent and can be wrapped or replaced for house rules:

```python
from src.rules.abilities import get_strength_hit_modifier

def get_custom_strength_hit_modifier(strength: int) -> int:
    """Custom strength modifier with house rule adjustments."""
    base_modifier = get_strength_hit_modifier(strength)
    # Apply custom logic
    return base_modifier + custom_adjustment
```

### 2. Additional Class Groups

New class groups can be added to the combat system by extending the THAC0 tables:

```python
# In custom_combat.py
from src.rules.combat_system import get_thac0

CUSTOM_CLASS_THAC0 = {
    1: 20,
    2: 19,
    # ... custom progression
}

def get_custom_thac0(level: int, class_name: str) -> int:
    if class_name == "my_custom_class":
        return CUSTOM_CLASS_THAC0.get(min(level, 20), 20)
    return get_thac0(level, class_name)
```

### 3. Combat Modifiers

The `CombatStats` dataclass can be extended or wrapped to include additional modifiers:

```python
from dataclasses import dataclass
from src.rules.combat_system import CombatStats

@dataclass
class ExtendedCombatStats(CombatStats):
    """Combat stats with additional house rule modifiers."""
    flanking_bonus: int = 0
    charging_bonus: int = 0
    
    def get_total_hit_modifier(self) -> int:
        return self.hit_modifier + self.flanking_bonus + self.charging_bonus
```

### 4. Custom Dice Rolling

All functions that involve randomness accept optional `roll` or `roller` parameters for deterministic behavior:

```python
from src.rules.combat_system import resolve_attack
from src.utils.dice import DiceRoller

# Use a seeded roller for reproducible combat
roller = DiceRoller(seed=12345)
result = resolve_attack(attacker, defender, roller=roller)

# Or provide a specific roll for testing
result = resolve_attack(attacker, defender, roll=15)
```

## Testing Strategy

### Coverage Goals

- **Overall Target**: 90% code coverage for all rules modules
- **Critical Paths**: 100% coverage for core mechanics (THAC0, attack resolution, modifier calculations)
- **Edge Cases**: Explicit tests for boundary conditions (min/max values, invalid inputs)

### Test Organization

Tests are organized by module in the `tests/` directory:

- `test_abilities.py`: Tests for ability scores and modifiers
- `test_combat_system.py`: Tests for combat mechanics
- Future: `test_character_classes.py`, `test_races.py`, etc.

### Testing Approach

1. **Unit Tests**: Each function tested independently
2. **Integration Tests**: Test module interactions (e.g., ability modifiers + combat)
3. **Canonical Values**: Tests verify against official AD&D 1E tables
4. **Deterministic Tests**: Use fixed rolls/seeds for reproducible results
5. **Error Cases**: Validate error handling for invalid inputs

### Running Tests

```bash
# Run all rules tests
pytest tests/test_abilities.py tests/test_combat_system.py -v

# Run with coverage
pytest --cov=src/rules --cov-report=term-missing tests/test_abilities.py tests/test_combat_system.py

# Run specific test class
pytest tests/test_abilities.py::TestStrengthModifiers -v
```

### Coverage Reports

Current coverage status can be checked with:

```bash
pytest --cov=src/rules --cov-report=html tests/
# Open htmlcov/index.html in a browser
```

## Usage Examples

### Example 1: Creating a Character with Ability Scores

```python
from src.rules import AbilityScores, get_constitution_hp_modifier

# Create ability scores for a character
scores = AbilityScores(
    strength=16,
    dexterity=14,
    constitution=15,
    intelligence=10,
    wisdom=12,
    charisma=8
)

# Calculate HP bonus per level
hp_bonus = get_constitution_hp_modifier(scores.constitution)
print(f"HP bonus per level: {hp_bonus}")  # Output: 1
```

### Example 2: Resolving a Combat Attack

```python
from src.rules import CombatStats, resolve_attack, get_thac0

# Create a level 5 fighter
fighter_thac0 = get_thac0(5, "fighter")  # THAC0 16
attacker = CombatStats(
    thac0=fighter_thac0,
    hit_modifier=1,  # +1 from STR 17
    damage_modifier=1
)

# Create a defender with chain mail (AC 5)
defender = CombatStats(armor_class=5)

# Resolve the attack
result = resolve_attack(attacker, defender)

if result.hit:
    print(f"Hit! Rolled {result.roll}, total attack {result.total_attack}")
    if result.critical_hit:
        print("Critical hit!")
else:
    print(f"Miss! Rolled {result.roll}, needed {result.target_number}")
```

### Example 3: Calculating All Modifiers for a Character

```python
from src.rules import (
    AbilityScores,
    get_strength_modifiers,
    get_dexterity_modifiers,
    get_constitution_hp_modifier
)

scores = AbilityScores(
    strength=18,
    dexterity=16,
    constitution=14,
    intelligence=10,
    wisdom=12,
    charisma=8
)

# Get all combat-relevant modifiers
str_hit, str_dmg = get_strength_modifiers(scores.strength)
dex_init, dex_ac = get_dexterity_modifiers(scores.dexterity)
con_hp = get_constitution_hp_modifier(scores.constitution)

print(f"To-hit: {str_hit:+d}")      # +1
print(f"Damage: {str_dmg:+d}")      # +2
print(f"Initiative: {dex_init:+d}") # +1
print(f"AC adjustment: {dex_ac:+d}") # -2 (better)
print(f"HP per level: {con_hp:+d}") # +0
```

## Contributing

When adding new modules to the rules engine:

1. **Reference Official Sources**: Cite specific tables/pages from AD&D 1E books
2. **Write Tests First**: Use TDD approach, write tests for canonical values
3. **Document Thoroughly**: Include module docstring, function docstrings, inline comments
4. **Type Everything**: Full type hints for parameters, returns, class attributes
5. **Export Public APIs**: Update `__init__.py` to export new public functions/classes
6. **Update This README**: Add documentation for new modules in the appropriate section

### Code Style

- Follow PEP 8 style guidelines
- Use Black for automatic formatting (line length 88)
- Use Ruff for linting
- Maximum line length: 88 characters
- Use descriptive variable names (no single letters except loop counters)
- Group imports: stdlib, third-party, local

### Documentation Style

- Use Google-style docstrings
- Include type hints in code, not docstrings (avoid redundancy)
- Document all public functions, classes, and methods
- Include usage examples for complex functions
- Cite AD&D 1E sources in comments (e.g., "AD&D 1E PHB Table I")

## References

- **AD&D 1E Player's Handbook**: Core rules, character classes, spells
- **AD&D 1E Dungeon Master's Guide**: Combat tables, magic items, treasure
- **AD&D 1E Monster Manual**: Monster statistics and special abilities
- **Temple of Elemental Evil Module**: Specific NPCs, locations, factions

---

**Last Updated**: 2025-12-06  
**Maintainer**: scottfrye/dnd project team  
**Status**: Active Development
