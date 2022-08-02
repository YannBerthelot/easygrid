from typing import TypedDict


class Action(TypedDict):
    battery: float
    grid: float


class Microgrid:
    def __init__(self) -> None:
        self.battery = Battery()
        self.grid = Grid()
        self.load = Load()

    def run_timestep(self, action: Action):
        self.battery.process_action(action["battery"])
        self.grid.process_action
        raise NotImplementedError


class Battery:
    def __init__(
        self,
        capacity: float,
        high_capacity: float,
        low_capacity: float,
        max_output: float,
        min_output: float,
    ) -> None:
        self.capacity = capacity
        self.high_capacity = high_capacity
        self.low_capacity = low_capacity
        self.max_output = max_output
        self.min_output = min_output
        self._energy = self.low_capacity

    @property
    def state_of_charge(self) -> float:
        return self._energy / self.capacity

    @property
    def energy(self) -> float:
        if self._energy >= 0:
            return self._energy
        else:
            raise ValueError(
                f"Energy stored in the battery is negative : {self._energy}, there is a problem."
            )

    def check_energy(self, energy: float, source: str) -> None:
        if energy < 0:
            raise ValueError(
                f"Input energy for {source} is negative ({energy}), should be positive, you may want to check if it's correctly computed"
            )

    def charge(self, energy: float) -> None:
        self.check_energy(energy, "charge")
        self._energy = max(
            self.low_capacity, min(self.high_capacity, self._energy + energy)
        )

    def discharge(self, energy: float) -> None:
        self.check_energy(energy, "discharge")
        self._energy = max(self.low_capacity, self._energy - energy)

    def process_action(self, energy: float) -> None:
        if energy >= 0:
            self.charge(energy)
        else:
            self.discharge(-energy)


class Grid:
    def __init__(self) -> None:
        pass


class Load:
    def __init__(self) -> None:
        pass
