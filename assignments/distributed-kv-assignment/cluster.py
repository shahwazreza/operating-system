import time
import threading
from node import Node
from consistent_hash import ConsistentHashRing

# Port assignments for the 5 nodes
NODE_CONFIG = [
    {"id": "node1", "port": 9001},
    {"id": "node2", "port": 9002},
    {"id": "node3", "port": 9003},
    {"id": "node4", "port": 9004},
    {"id": "node5", "port": 9005},
]


class Cluster:
    def __init__(self, latency: float = 0.0):
        self.latency = latency
        self.nodes: dict[str, Node] = {}
        self.ring = ConsistentHashRing(vnodes=100)

        # Build peer lists
        for cfg in NODE_CONFIG:
            peers = [p for p in NODE_CONFIG if p["id"] != cfg["id"]]
            node = Node(cfg["id"], cfg["port"], peers, latency=latency)
            self.nodes[cfg["id"]] = node
            self.ring.add_node(cfg["id"])

    def start(self):
        """Start all nodes and wait for a leader to be elected."""
        for node in self.nodes.values():
            node.start()

        print("[CLUSTER] Starting 5-node cluster...")
        # Wait for leader election (up to 5 seconds)
        deadline = time.time() + 5
        while time.time() < deadline:
            if self.get_leader():
                print(f"[CLUSTER] Leader elected: {self.get_leader()}")
                return
            time.sleep(0.1)
        print("[CLUSTER] Warning: no leader elected within timeout")

    def stop(self):
        for node in self.nodes.values():
            node.stop()
        print("[CLUSTER] All nodes stopped")

    def get_leader(self) -> str | None:
        """Return the ID of the current leader, or None if no leader."""
        for node in self.nodes.values():
            if node.is_leader:
                return node.node_id
        return None

    def put(self, key: str, value) -> dict:
        """Route a PUT to the current leader node."""
        leader_id = self.get_leader()
        if not leader_id:
            return {"ok": False, "error": "no leader"}
        return self.nodes[leader_id].put(key, value)

    def get(self, key: str, node_id: str = None) -> dict:
        if node_id:
            target = self.nodes.get(node_id)
        else:
            # Default: read from leader to avoid stale reads in demos
            leader_id = self.get_leader()
            target = self.nodes.get(leader_id) if leader_id else None
            # Fallback to consistent hash if no leader
            if not target:
                primary_id = self.ring.get_node(key)
                target = self.nodes.get(primary_id)

        if not target:
            return {"ok": False, "error": "node not found"}
        return target.get(key)

    def kill_node(self, node_id: str):
        """Simulate a node failure by stopping the node."""
        if node_id in self.nodes:
            self.nodes[node_id].stop()
            self.ring.remove_node(node_id)
            print(f"[CLUSTER] Node '{node_id}' killed")

    def get_status(self):
        """Print the current state of all nodes."""
        print("\n── Cluster Status ──────────────────────────────")
        for nid, node in self.nodes.items():
            if node.running:
                print(f"  {nid} | state={node.state:9s} | term={node.term} | leader={node.leader_id}")
            else:
                print(f"  {nid} | STOPPED")
        print("────────────────────────────────────────────────\n")
