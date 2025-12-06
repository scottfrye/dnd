# UI Manual Test Instructions

This document provides step-by-step manual test instructions for the terminal UI implementation.

## Prerequisites

1. Ensure Python 3.12+ is installed
2. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the UI Demo

Launch the terminal UI demo:

```bash
python scripts/terminal_ui_demo.py
```

## Test Cases

### Test 1: Initial Display Rendering

**Objective**: Verify that the UI renders correctly on startup.

**Steps**:
1. Run `python scripts/terminal_ui_demo.py`
2. Observe the display

**Expected Results**:
- Map area displays in the upper left with a border of `#` characters
- Floor tiles are represented by `.` characters
- Player character is shown as a bold green `@` in the center
- Status area displays on the right showing:
  - Name: Hero
  - Level: 1
  - Hp: 10
  - Max_hp: 15
  - Ac: 5
- Message area displays at the bottom with welcome messages:
  - "Welcome to the Temple of Elemental Evil!"
  - "Use hjkl or arrow keys to move."
  - "Press ? for help, q to quit."

### Test 2: Vi-Keys Movement

**Objective**: Test movement using classic roguelike vi-keys.

**Steps**:
1. With the demo running, press `k` (north)
2. Press `j` (south)
3. Press `h` (west)
4. Press `l` (east)

**Expected Results**:
- Player `@` moves one tile north when `k` is pressed
- Player `@` moves one tile south when `j` is pressed
- Player `@` moves one tile west when `h` is pressed
- Player `@` moves one tile east when `l` is pressed
- Each movement displays "You move [direction]." in the message log
- Movement is blocked by walls (`#`), showing "You can't move there!" message

### Test 3: Arrow Key Movement

**Objective**: Test movement using arrow keys.

**Steps**:
1. With the demo running, press the UP arrow
2. Press the DOWN arrow
3. Press the LEFT arrow
4. Press the RIGHT arrow

**Expected Results**:
- Player `@` moves one tile north when UP arrow is pressed
- Player `@` moves one tile south when DOWN arrow is pressed
- Player `@` moves one tile west when LEFT arrow is pressed
- Player `@` moves one tile east when RIGHT arrow is pressed
- Each movement displays "You move [direction]." in the message log

### Test 4: Numpad Movement

**Objective**: Test movement using numpad keys.

**Steps**:
1. With the demo running, press `8` (north)
2. Press `2` (south)
3. Press `4` (west)
4. Press `6` (east)

**Expected Results**:
- Player `@` moves correctly in all four cardinal directions
- Movement messages appear in the message log

### Test 5: Diagonal Movement

**Objective**: Test diagonal movement using vi-keys.

**Steps**:
1. With the demo running, press `y` (northwest)
2. Press `u` (northeast)
3. Press `b` (southwest)
4. Press `n` (southeast)

**Expected Results**:
- Player `@` moves diagonally in the specified directions
- Movement is blocked by walls, showing "You can't move there!" message

### Test 6: Wait Action

**Objective**: Test the wait/rest command.

**Steps**:
1. With the demo running, press `.` (period)
2. Press `5` (numpad 5)

**Expected Results**:
- Player position remains unchanged
- Message log displays "You wait." for each wait command
- Player `@` stays in the same location

### Test 7: Wall Collision

**Objective**: Verify that movement is blocked by walls.

**Steps**:
1. With the demo running, move the player to any wall
2. Attempt to move through the wall

**Expected Results**:
- Player position does not change
- Message "You can't move there!" appears in the message log
- Wall `#` character remains in place

### Test 8: Help Command

**Objective**: Test the help action.

**Steps**:
1. With the demo running, press `?`

**Expected Results**:
- Message log displays: "Help: hjkl=move, q=quit, ?=help"
- Display remains otherwise unchanged

### Test 9: Quit Command

**Objective**: Test the quit action.

**Steps**:
1. With the demo running, press `q`

**Expected Results**:
- Message log displays "Goodbye!"
- Demo exits gracefully after a brief pause
- Terminal returns to normal state

### Test 10: Message Log Scrolling

**Objective**: Verify that the message log handles multiple messages.

**Steps**:
1. With the demo running, perform many movements (e.g., move around the room 10+ times)

**Expected Results**:
- Message log shows the most recent 5 messages
- Older messages scroll off the top
- New messages appear at the bottom of the message log

### Test 11: Multiple Input Schemes

**Objective**: Test switching between different input schemes.

**Steps**:
1. With the demo running, move using vi-keys (hjkl)
2. Move using arrow keys
3. Move using numpad (2468)
4. Mix input schemes

**Expected Results**:
- All input schemes work correctly
- Player can switch between schemes seamlessly
- All movements are processed correctly regardless of input scheme

### Test 12: Unknown Input

**Objective**: Test handling of unmapped keys.

**Steps**:
1. With the demo running, press various unmapped keys (e.g., `x`, `~`, `[`, etc.)

**Expected Results**:
- Message log displays "Unknown command. Press ? for help."
- Player position remains unchanged
- Display continues to function normally

### Test 13: Terminal Resize Behavior

**Objective**: Test behavior when terminal is resized (if applicable).

**Steps**:
1. With the demo running, resize the terminal window (if your terminal supports it)
2. Continue interacting with the demo

**Expected Results**:
- Display continues to render (may clip if terminal is too small)
- Input continues to work
- No crashes or errors

### Test 14: Rapid Input

**Objective**: Test handling of rapid key presses.

**Steps**:
1. With the demo running, rapidly press movement keys
2. Observe the display and message log

**Expected Results**:
- All inputs are processed in order
- Display updates correctly for each movement
- Message log shows all movement messages
- No input is lost or causes errors

### Test 15: Context Manager Cleanup

**Objective**: Verify that terminal state is restored on exit.

**Steps**:
1. Note the terminal state before running the demo
2. Run the demo and quit normally with `q`
3. Observe the terminal state after exit
4. Run the demo again and interrupt with Ctrl+C
5. Observe the terminal state after interrupt

**Expected Results**:
- Terminal returns to normal state after normal quit
- Terminal returns to normal state after interrupt
- Cursor is visible
- Terminal colors are reset
- No visual artifacts remain

## Automated Test Verification

After completing manual tests, verify with automated tests:

```bash
# Run all UI tests
pytest tests/test_display.py tests/test_input.py \
       tests/test_terminal_display.py tests/test_input_handler.py \
       tests/test_ui_integration.py -v

# Quick test count verification
pytest tests/test_ui_integration.py -v --tb=no
# Should show: 18 passed
```

## Troubleshooting

### Display Not Rendering Correctly

**Issue**: Map, status, or messages appear garbled or misaligned.

**Solutions**:
- Ensure terminal window is at least 100x30 characters
- Try a different terminal emulator
- Check that `blessed` library is installed correctly: `pip list | grep blessed`

### Input Not Responding

**Issue**: Key presses don't move the character.

**Solutions**:
- Ensure terminal is in focus
- Try different input schemes (vi-keys, arrows, numpad)
- Check that you're pressing valid movement keys

### Colors Not Displaying

**Issue**: Player character is not green or colors are missing.

**Solutions**:
- Ensure your terminal supports ANSI colors
- Try setting `TERM=xterm-256color` environment variable
- Use a modern terminal emulator (e.g., iTerm2, Windows Terminal, GNOME Terminal)

### Demo Won't Start

**Issue**: Demo fails to launch or crashes immediately.

**Solutions**:
- Verify Python version: `python --version` (should be 3.12+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for error messages in the output

## Reporting Issues

If you encounter any issues during manual testing:

1. Note which test case failed
2. Document the exact steps to reproduce
3. Include terminal type and size
4. Include Python version and OS
5. Include any error messages or screenshots
6. Report in the project issue tracker

## Test Coverage Summary

The UI system includes:
- **56 unit tests** for display and input components
- **18 integration tests** for complete workflows
- **15 manual test cases** for user experience verification
- **1 interactive demo** for exploratory testing

Total: **90+ test scenarios** ensuring robust UI functionality.
