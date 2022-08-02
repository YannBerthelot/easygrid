from typing import TypedDict


class Action(TypedDict):
    battery: float
    grid: float


class BatteryConfig(TypedDict):
    capacity: float
    high_capacity: float
    low_capacity: float
    max_output: float
    min_output: float
    initial_energy: float


class Microgrid:
    def __init__(self, config: dict) -> None:
        battery_config: BatteryConfig = config["BATTERY"]
        self.battery = Battery(battery_config)
        # self.grid = Grid()
        # self.load = Load()

    def run_timestep(self, action: Action):
        self.battery.process_action(action["battery"])
        # self.grid.process_action
        raise NotImplementedError

    def print_info(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class Battery:
    def __init__(self, battery_config: BatteryConfig) -> None:
        self.capacity = battery_config["capacity"]
        self.high_capacity = battery_config["high_capacity"]
        self.low_capacity = battery_config["low_capacity"]
        self.max_output = battery_config["max_output"]
        self.min_output = battery_config["min_output"]
        self._energy = battery_config["initial_energy"]

    @property
    def state_of_charge(self) -> float:
        return self._energy / self.capacity

    @property
    def energy(self) -> float:
        assert self._energy >= 0, "Energy is negative, there is a problem"
        if self._energy >= 0:
            return self._energy

    def charge(self, energy: float) -> None:
        if energy < 0:
            raise ValueError(
                f"Input energy for charge is negative ({energy}),\
                    should be positive, you may want to check\
                     if it's correctly computed"
            )
        self._energy = max(
            self.low_capacity, min(self.high_capacity, self._energy + energy)
        )

    def discharge(self, energy: float) -> None:
        if energy < 0:
            raise ValueError(
                f"Input energy for discharge is negative ({energy}),\
                     should be positive,\
                     you may want to check if it's correctly computed"
            )
        self._energy = max(self.low_capacity, self._energy - energy)

    def process_action(self, energy: float) -> None:
        if energy >= 0:
            self.charge(energy)
        else:
            self.discharge(-energy)


# class Grid:
#     def __init__(self) -> None:
#         pass


# class Load:
#     def __init__(self) -> None:
#         pass
