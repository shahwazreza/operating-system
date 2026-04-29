import hashlib
import bisect


class ConsistentHashRing:
    def __init__(self, vnodes=100):
        self.vnodes = vnodes
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key: str) -> int:
        """SHA-256 hash of the key, truncated to a 32-bit integer."""
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)

    def add_node(self, node_id: str):
        for i in range(self.vnodes):
            vkey = f"{node_id}#vnode{i}"
            h = self._hash(vkey)
            self.ring[h] = node_id
            bisect.insort(self.sorted_keys, h)

    def remove_node(self, node_id: str):
        for i in range(self.vnodes):
            vkey = f"{node_id}#vnode{i}"
            h = self._hash(vkey)
            if h in self.ring:
                del self.ring[h]
                idx = bisect.bisect_left(self.sorted_keys, h)
                self.sorted_keys.pop(idx)

    def get_node(self, key: str) -> str:
        if not self.ring:
            raise RuntimeError("Ring is empty — no nodes available")
        h = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_nodes(self) -> set:
        return set(self.ring.values())
