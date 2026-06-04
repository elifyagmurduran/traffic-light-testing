"""
Task 3 - White-box (BRANCH COVERAGE) tests for the Task 2 TrafficLight code.

Target methods (reused from Task 2, both CC = 7, different loop types):
  * execute_cycle          -> for-loop
  * apply_manual_override  -> while-loop

Each test is labelled with the decision/branch it forces. Durations are zeroed
(make_light) so time.sleep() is instant -> the suite is fast and deterministic.

execute_cycle branch map:
  T1 D1=True | T2 D1=False,D2=True | T3 D2=False,D4=T/F,D5=True,D6=False
  T4 D6=True | D5=False is INFEASIBLE (two greens => unsafe, caught at D2)
apply_manual_override branch map:
  M1 W=False | M2 W=T,E=True | M3 E=False,C1=True | M4 C2=True
  M5 C3=True | M6 C3=False + loop back-edge + W=False exit
"""
import os, sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from src.traffic_light import TrafficLight


def make_light():
    """A TrafficLight with all durations zeroed so time.sleep is instant."""
    tl = TrafficLight()
    tl.colors = {"GREEN": 0, "YELLOW": 0, "RED": 0}
    return tl


# ---------- execute_cycle : BRANCH COVERAGE (4 tests) ----------

def test_ec_T1_manual_mode_true():            # D1 = True
    tl = make_light(); tl.manual_mode = True
    assert tl.execute_cycle() is False

def test_ec_T2_auto_unsafe():                 # D1 = False, D2 = True
    tl = make_light()
    assert tl.execute_cycle() is None
    assert tl.current_directions == {"NS": "RED", "EW": "RED"}

def test_ec_T3_green_synchronized():          # D2=F, D4=T/F, D5=True, D6=False
    tl = make_light(); tl.current_directions = {"NS": "GREEN", "EW": "RED"}
    tl.execute_cycle()
    assert tl.current_directions["NS"] == "RED"

def test_ec_T4_yellow_branch():               # D6 = True
    tl = make_light(); tl.current_directions = {"NS": "YELLOW", "EW": "RED"}
    tl.execute_cycle()
    assert tl.current_directions["NS"] == "YELLOW"


# ---------- apply_manual_override : BRANCH COVERAGE (6 tests) ----------

def test_amo_M1_already_safe():               # W = False (skip loop)
    tl = make_light(); tl.current_directions = {"NS": "GREEN", "EW": "RED"}
    assert tl.apply_manual_override([]) is True

def test_amo_M2_emergency():                  # W = True, E = True
    tl = make_light(); tl.emergency_request = "NS"
    assert tl.apply_manual_override([]) is True
    assert tl.current_directions["NS"] == "GREEN"

def test_amo_M3_run_out_of_commands():        # E = False, C1 = True
    tl = make_light()
    assert tl.apply_manual_override([]) is False

def test_amo_M4_manual_override_raises():     # C1 = False, C2 = True
    tl = make_light()
    with pytest.raises(ValueError):
        tl.apply_manual_override(["MANUAL_OVERRIDE"])

def test_amo_M5_quit():                        # C2 = False, C3 = True
    tl = make_light()
    assert tl.apply_manual_override(["QUIT"]) is False

def test_amo_M6_normal_reaches_safe():         # C3 = False + loop back-edge + W exit
    tl = make_light()
    assert tl.apply_manual_override(["GREEN", "RED"]) is True
    assert tl.current_directions == {"NS": "GREEN", "EW": "RED"}