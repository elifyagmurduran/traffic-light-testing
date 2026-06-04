import time

class TrafficLight:
    def __init__(self):
        self.colors = {"GREEN": 30, "YELLOW": 4, "RED": 2}
        self.directions = ["NS", "EW"]
        self.current_directions = {"NS": "RED", "EW": "RED"}
        self.manual_mode = False
        self.emergency_request = None

    def execute_cycle(self):
        if self.manual_mode:
            return self.apply_manual_override([])
        if not self.is_safe_state():
            self.set_all_red()
            return
        for direction in self.directions:
            if self.current_directions[direction] == "GREEN":
                if self.check_synchronization(direction):
                    self.yellow_transition(direction)
                else:
                    self.set_all_red()
                    return
            elif self.current_directions[direction] == "YELLOW":
                self.red_clearance_phase(direction)

    def yellow_transition(self, direction):
        if self.current_directions[direction] == "GREEN":
            time.sleep(self.colors["YELLOW"])
            self.set_red(direction)
        else:
            raise ValueError("Invalid condition")

    def red_clearance_phase(self, direction):
        if self.current_directions[direction] == "RED" and self.current_directions[self.get_opposite_direction(direction)] == "YELLOW":
            time.sleep(self.colors["RED"])
            self.set_green(self.get_opposite_direction(direction))

    def check_synchronization(self, direction):
        for d in self.directions:
            if d != direction and self.current_directions[d] == self.current_directions[direction]:
                return False
        return True

    def emergency_preemption(self):
        if not self.emergency_request or self.is_manual_mode():
            raise ValueError("Invalid condition")
        self.set_all_red()
        self.set_green(self.emergency_request)
        self.emergency_request = None

    def manual_override(self, direction, color):
        if not self.is_manual_mode() and not self.is_safe_state():
            raise ValueError("Invalid condition")
        self.current_directions[direction] = color
        if color == "GREEN":
            self.set_yellow(direction)

    def power_failure_recovery(self):
        for direction in self.directions:
            self.current_directions[direction] = "RED"
        time.sleep(1)

    def apply_time_based_schedule(self, schedule):
        if not all(duration >= self.colors["GREEN"] for duration in schedule.values()):
            raise ValueError("Invalid condition")
        for direction, duration in schedule.items():
            self.current_directions[direction] = "GREEN"
            time.sleep(duration)

    def get_opposite_direction(self, direction):
        return {"NS": "EW", "EW": "NS"}.get(direction)

    def is_safe_state(self):
        for direction1 in self.directions:
            for direction2 in self.directions:
                if direction1 != direction2 and self.current_directions[direction1] == self.current_directions[direction2]:
                    return False
        return True

    def set_all_red(self):
        for direction in self.directions:
            self.current_directions[direction] = "RED"

    def is_manual_mode(self):
        return self.manual_mode

    def apply_manual_override(self, commands):
        """Refactored: consumes actions from `commands` (a list) instead of input().
        Returns True if a safe state is reached, False on QUIT or running out of
        commands. Raises ValueError on a MANUAL_OVERRIDE action.
        Control flow (while + nested for + branches) is unchanged, so CC is preserved.
        """
        index = 0
        while not self.is_safe_state():
            if self.emergency_request:
                self.emergency_preemption()
                break
            for direction in self.directions:
                if index >= len(commands):
                    return False
                action = commands[index]
                index += 1
                if action == "MANUAL_OVERRIDE":
                    raise ValueError("Invalid condition")
                elif action == "QUIT":
                    return False
                else:
                    self.current_directions[direction] = action.upper()
        return True

    def set_green(self, direction):
        self.current_directions[direction] = "GREEN"

    def set_red(self, direction):
        self.current_directions[direction] = "RED"

    def set_yellow(self, direction):
        self.current_directions[direction] = "YELLOW"