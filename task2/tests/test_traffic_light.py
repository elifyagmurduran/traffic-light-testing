"""
Task 2 - Test cases for the two selected methods, designed with
category partition testing (redundant/infeasible partitions removed).

Target methods:
  - execute_cycle        (cyclomatic complexity 7, for-loop)
  - apply_manual_override (cyclomatic complexity 7, while-loop)

Run from the task2 folder with:  pytest
"""

import os
import sys

# Make src/traffic_light.py importable regardless of where pytest is launched
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from src.traffic_light import TrafficLight


def fresh():
    """A TrafficLight with zero durations so tests don't actually sleep."""
    tl = TrafficLight()
    tl.colors = {"GREEN": 0, "YELLOW": 0, "RED": 0}
    return tl


# ----------------------------------------------------------------------
# execute_cycle  -  4 partitions (the "GREEN but unsynchronized" partition
# is infeasible with two directions, so it was removed as redundant).
# ----------------------------------------------------------------------

def test_execute_cycle_manual_mode_delegates():
    # Partition 1: manual_mode = True -> delegates to manual override
    tl = fresh()
    tl.manual_mode = True
    result = tl.execute_cycle()
    assert result is False  # apply_manual_override([]) runs out of commands

def test_execute_cycle_unsafe_state_fails_safe():
    # Partition 2: auto mode, unsafe state (both RED) -> set_all_red
    tl = fresh()
    result = tl.execute_cycle()
    assert result is None
    assert tl.current_directions == {"NS": "RED", "EW": "RED"}

def test_execute_cycle_green_synchronized_goes_to_yellow_then_red():
    # Partition 3: safe, one direction GREEN (synchronized) -> yellow_transition
    tl = fresh()
    tl.current_directions = {"NS": "GREEN", "EW": "RED"}
    result = tl.execute_cycle()
    assert result is None
    assert tl.current_directions["NS"] == "RED"  # GREEN -> (yellow) -> RED

def test_execute_cycle_yellow_triggers_clearance_branch():
    # Partition 4: safe, one direction YELLOW -> red_clearance_phase branch
    tl = fresh()
    tl.current_directions = {"NS": "YELLOW", "EW": "RED"}
    result = tl.execute_cycle()
    assert result is None
    assert tl.current_directions["NS"] == "YELLOW"  # clearance condition not met, unchanged


# ----------------------------------------------------------------------
# apply_manual_override  -  5 partitions
# ----------------------------------------------------------------------

def test_manual_override_emergency_preempts():
    # Partition 1: emergency_request set -> preemption, returns True
    tl = fresh()
    tl.emergency_request = "NS"
    result = tl.apply_manual_override([])
    assert result is True
    assert tl.current_directions == {"NS": "GREEN", "EW": "RED"}

def test_manual_override_rejects_manual_override_action():
    # Partition 2: a MANUAL_OVERRIDE action -> ValueError
    tl = fresh()
    with pytest.raises(ValueError):
        tl.apply_manual_override(["MANUAL_OVERRIDE"])

def test_manual_override_quit_returns_false():
    # Partition 3: a QUIT action -> returns False
    tl = fresh()
    result = tl.apply_manual_override(["QUIT"])
    assert result is False

def test_manual_override_reaches_safe_state():
    # Partition 4: normal commands producing a safe (differing) state -> True
    tl = fresh()
    result = tl.apply_manual_override(["GREEN", "RED"])
    assert result is True
    assert tl.current_directions == {"NS": "GREEN", "EW": "RED"}

def test_manual_override_runs_out_of_commands():
    # Partition 5: commands run out before a safe state -> returns False
    tl = fresh()
    result = tl.apply_manual_override(["RED"])
    assert result is False
