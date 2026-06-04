import sys
sys.path.insert(0, '..')
from src import TrafficLight

def make_light():
    return TrafficLight({"GREEN": 0, "YELLOW": 0, "RED": 0})

class TestTrafficLight:
    def test_manual_mode(self):
        light = make_light()
        execute_cycle(light, manual_mode=True)
        assert not light.execute_cycle(manual_mode=False)

    def test_red_to_none_stays_red(self):
        light = make_light()
        execute_cycle(light, both=["RED", "RED"])
        assert light.get_state() == {"GREEN": 0, "YELLOW": 0, "RED": 2}

    def test_ns_green_ew_red_NS_becomes_red(self):
        light = make_light()
        execute_cycle(light, NS="GREEN", EW="RED")
        assert light.get_state() == {"GREEN": 0, "YELLOW": 0, "RED": 1}

    def test_ns_yellow_ew_red_NS_stays_yellow(self):
        light = make_light()
        execute_cycle(light, NS="YELLOW", EW="RED")
        assert light.get_state() == {"GREEN": 0, "YELLOW": 1, "RED": 0}

    def test_manual_override_NS_green_ew_red_true(self):
        light = make_light()
        result = apply_manual_override([{"NS": "GREEN", "EW": "RED"}])
        assert result and light.get_state() == {"GREEN": 1, "YELLOW": 0, "RED": 1}

    def test_manual_override_both_red_emergency_request_NS_true(self):
        light = make_light()
        result = apply_manual_override([{"NS": "RED", "EW": "RED"}, {"emergency_request": "NS"}])
        assert result and light.get_state() == {"GREEN": 0, "YELLOW": 0, "RED": 2}

    def test_manual_override_both_red_false(self):
        light = make_light()
        result = apply_manual_override([{"NS": "RED", "EW": "RED"}])
        assert not result

    def test_manual_override_both_red_manual_override_value_error(self):
        light = make_light()
        with pytest.raises(ValueError):
            apply_manual_OVERRIDE([{"NS": "RED", "EW": "RED"}, {"commands": ["MANUAL_OVERRIDE"]}])

    def test_manual_override_both_red_quit_false(self):
        light = make_light()
        result = apply_manual_override([{"NS": "RED", "EW": "RED"}, {"commands": ["QUIT']}])
        assert not result

    def test_manual_override_both_red_green_red_true(self):
        light = make_light()
        result = apply_manual_override([{"NS": "GREEN", "EW": "RED"}] + [{"commands": ["GREEN", "RED"]}])
        assert result and light.get_state() == {"GREEN": 1, "YELLOW": 0, "RED": 2}

def execute_cycle(light, NS=None, EW=None, manual_mode=False):
    if manual_mode:
        return not light.execute_cycle(manual_mode=True)
    elif NS is None and EW is None:
        return light.execute_cycle(both=["RED", "RED"])
    else:
        if NS == "GREEN":
            return {"NS": 1, "EW": 0}
        elif NS == "YELLOW":
            return {"NS": 1, "EW": 0}
        elif EW == "GREEN":
            return {"NS": 1, "EW": 0}
        else:
            return light.execute_cycle(NS=NS, EW=EW)

def apply_manual_override(commands):
    if all([command["NS"] == "RED" and command["EW"] == "RED" for command in commands]):
        if "MANUAL_OVERRIDE" in [command.get("commands", []) for command in commands]:
            raise ValueError
        elif "QUIT" in [command.get("commands", []) for command in commands]:
            return False
        else:
            return True and {"NS": 1, "EW": 1}
    else:
        return True and {"NS": command["NS"], "EW": command["EW"]}