from typing import Dict


class VectorClock:
    def __init__(self, node_id: str, clock: Dict[str, int] = None):
        self.node_id = node_id
        # If no clock provided, start with all zeros
        self.clock: Dict[str, int] = clock.copy() if clock else {}

    def tick(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def merge(self, other: "VectorClock"):
        for node, ts in other.clock.items():
            self.clock[node] = max(self.clock.get(node, 0), ts)

    def copy(self) -> "VectorClock":
        return VectorClock(self.node_id, self.clock)

    def to_dict(self) -> Dict[str, int]:
        return self.clock.copy()

    @staticmethod
    def from_dict(node_id: str, d: Dict[str, int]) -> "VectorClock":
        return VectorClock(node_id, d)

    def __le__(self, other: "VectorClock") -> bool:
        all_nodes = set(self.clock) | set(other.clock)
        return all(self.clock.get(n, 0) <= other.clock.get(n, 0) for n in all_nodes)

    def __lt__(self, other: "VectorClock") -> bool:
        return self <= other and self.clock != other.clock

    def concurrent_with(self, other: "VectorClock") -> bool:
        return not (self <= other) and not (other <= self)

    def __repr__(self):
        return f"VC({self.clock})"
