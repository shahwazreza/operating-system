import threading
import time
import random
import socket
import json
import logging
from typing import Dict, Optional, List
from vector_clock import VectorClock

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s] %(message)s',
                    datefmt='%H:%M:%S')


# Node States
FOLLOWER  = "FOLLOWER"
CANDIDATE = "CANDIDATE"
LEADER    = "LEADER"

# Timeouts (seconds)
HEARTBEAT_INTERVAL    = 0.5
ELECTION_TIMEOUT_MIN  = 1.5
ELECTION_TIMEOUT_MAX  = 3.0
NETWORK_LATENCY       = 0.0
RPC_TIMEOUT           = 3.0


class KVEntry:
    def __init__(self, value, vc: VectorClock):
        self.value = value
        self.vc = vc

    def to_dict(self):
        return {"value": self.value, "vc": self.vc.to_dict()}


class Node:
    def __init__(self, node_id: str, port: int, peers: List[dict],
                 latency: float = 0.0):
        self.node_id   = node_id
        self.port      = port
        self.peers     = peers
        self.latency   = latency
        self.logger    = logging.getLogger(node_id)

        # Raft state
        self.state     = FOLLOWER
        self.term      = 0
        self.voted_for: Optional[str] = None
        self.vote_count = 0
        self.leader_id: Optional[str] = None

        # Election timer
        self.last_heartbeat = time.time()
        self.election_timeout = random.uniform(ELECTION_TIMEOUT_MIN,
                                               ELECTION_TIMEOUT_MAX)

        # KV store
        self.store: Dict[str, KVEntry] = {}
        self.vc = VectorClock(node_id)   # this node's vector clock
        self.store_lock = threading.Lock()

        # Control flags
        self.running = True
        self._server_thread   = threading.Thread(target=self._serve, daemon=True)
        self._election_thread = threading.Thread(target=self._election_loop, daemon=True)

    # Startup / Shutdown

    def start(self):
        self._server_thread.start()
        self._election_thread.start()
        self.logger.info(f"Node started on port {self.port}")

    def stop(self):
        self.running = False
        self.logger.info("Node stopped")

    # RPC Server

    def _serve(self):
        """Listen for incoming RPC messages from peers and clients."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind(('127.0.0.1', self.port))
            s.listen(10)
            s.settimeout(0.5)
            while self.running:
                try:
                    conn, _ = s.accept()
                    t = threading.Thread(target=self._handle_rpc, args=(conn,), daemon=True)
                    t.start()
                except socket.timeout:
                    continue

    def _handle_rpc(self, conn):
        """Dispatch an incoming RPC to the correct handler."""
        try:
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if data.endswith(b"\n"):
                    break
            msg = json.loads(data.decode())
            rpc = msg.get("rpc")

            if rpc == "request_vote":
                reply = self._on_request_vote(msg)
            elif rpc == "heartbeat":
                reply = self._on_heartbeat(msg)
            elif rpc == "replicate":
                reply = self._on_replicate(msg)
            elif rpc == "put":
                reply = self._client_put(msg["key"], msg["value"])
            elif rpc == "get":
                reply = self._client_get(msg["key"])
            else:
                reply = {"ok": False, "error": "unknown rpc"}

            conn.sendall((json.dumps(reply) + "\n").encode())
        except Exception as e:
            self.logger.error(f"RPC handler error: {e}")
        finally:
            conn.close()

    def _send_rpc(self, peer_port: int, msg: dict) -> Optional[dict]:
        """Send an RPC message to a peer and return the response."""
        try:
            time.sleep(self.latency)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(RPC_TIMEOUT)
                s.connect(('127.0.0.1', peer_port))
                s.sendall((json.dumps(msg) + "\n").encode())
                data = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if data.endswith(b"\n"):
                        break
                return json.loads(data.decode())
        except Exception:
            return None   # peer unreachable

    # Leader Election (Simplified Raft)

    def _election_loop(self):
        while self.running:
            time.sleep(0.1)
            if self.state == LEADER:
                self._send_heartbeats()
                time.sleep(HEARTBEAT_INTERVAL)
            else:
                elapsed = time.time() - self.last_heartbeat
                if elapsed > self.election_timeout:
                    self._start_election()

    def _start_election(self):
        self.state = CANDIDATE
        self.term += 1
        self.voted_for = self.node_id
        self.vote_count = 1   # vote for self
        self.election_timeout = random.uniform(ELECTION_TIMEOUT_MIN,
                                               ELECTION_TIMEOUT_MAX)
        self.last_heartbeat = time.time()
        self.logger.info(f"Starting election for term {self.term}")

        votes_needed = (len(self.peers) + 1) // 2 + 1  # majority

        for peer in self.peers:
            reply = self._send_rpc(peer["port"], {
                "rpc": "request_vote",
                "term": self.term,
                "candidate_id": self.node_id,
            })
            if reply and reply.get("vote_granted"):
                self.vote_count += 1

        if self.vote_count >= votes_needed and self.state == CANDIDATE:
            self._become_leader()

    def _become_leader(self):
        self.state = LEADER
        self.leader_id = self.node_id
        self.logger.info(f"Became LEADER for term {self.term}")
        self._send_heartbeats()

    def _send_heartbeats(self):
        for peer in self.peers:
            self._send_rpc(peer["port"], {
                "rpc": "heartbeat",
                "term": self.term,
                "leader_id": self.node_id,
            })

    def _on_request_vote(self, msg: dict) -> dict:
        grant = False
        if msg["term"] > self.term:
            self.term = msg["term"]
            self.state = FOLLOWER
            self.voted_for = None

        if (msg["term"] >= self.term and
                (self.voted_for is None or self.voted_for == msg["candidate_id"])):
            self.voted_for = msg["candidate_id"]
            grant = True
            self.last_heartbeat = time.time()

        return {"vote_granted": grant, "term": self.term}

    def _on_heartbeat(self, msg: dict) -> dict:
        if msg["term"] >= self.term:
            self.term = msg["term"]
            self.state = FOLLOWER
            self.leader_id = msg["leader_id"]
            self.last_heartbeat = time.time()
        return {"ok": True}

    # KV Operations & Replication

    def _client_put(self, key: str, value) -> dict:
        if self.state != LEADER:
            # Forward to leader
            leader = next((p for p in self.peers if p["id"] == self.leader_id), None)
            if leader:
                return self._send_rpc(leader["port"], {"rpc": "put", "key": key, "value": value}) or \
                       {"ok": False, "error": "leader unreachable"}
            return {"ok": False, "error": "no leader known"}

        # Increment vector clock for this write
        with self.store_lock:
            self.vc.tick()
            new_vc = self.vc.copy()

            # Conflict detection: check if existing entry is concurrent
            if key in self.store:
                existing_vc = self.store[key].vc
                if new_vc.concurrent_with(existing_vc):
                    self.logger.warning(
                        f"CONFLICT on key '{key}': concurrent writes detected. "
                        f"Applying Last-Write-Wins."
                    )
            self.store[key] = KVEntry(value, new_vc)

        # Replicate to at least 2 backup nodes
        replication_msg = {
            "rpc": "replicate",
            "key": key,
            "value": value,
            "vc": new_vc.to_dict(),
            "term": self.term,
        }
        acks = 0
        for peer in self.peers:
            reply = self._send_rpc(peer["port"], replication_msg)
            if reply and reply.get("ok"):
                acks += 1
            if acks >= 2:
                break

        if acks >= 2:
            self.logger.info(f"PUT '{key}'='{value}' replicated to {acks} backups. ACK sent.")
            return {"ok": True, "vc": new_vc.to_dict()}
        else:
            self.logger.warning(f"PUT '{key}' only replicated to {acks} backups (degraded).")
            return {"ok": True, "vc": new_vc.to_dict(), "warning": "fewer than 2 backups confirmed"}

    def _client_get(self, key: str) -> dict:
        """Handle a GET request. Served locally (eventual consistency)."""
        with self.store_lock:
            if key in self.store:
                entry = self.store[key]
                return {"ok": True, "value": entry.value, "vc": entry.vc.to_dict()}
            return {"ok": False, "error": f"key '{key}' not found"}

    def _on_replicate(self, msg: dict) -> dict:
        """Receive a replicated write from the leader and apply it locally."""
        if msg.get("term", 0) < self.term:
            return {"ok": False, "error": "stale term"}

        key   = msg["key"]
        value = msg["value"]
        remote_vc = VectorClock.from_dict(self.node_id, msg["vc"])

        with self.store_lock:
            # Merge remote clock into our own
            self.vc.merge(remote_vc)

            # Only apply if the incoming write is newer (or concurrent — apply anyway)
            if key not in self.store or not (remote_vc <= self.store[key].vc):
                self.store[key] = KVEntry(value, remote_vc)

        return {"ok": True}

    # Public API (for tests and clients)

    def put(self, key: str, value) -> dict:
        return self._client_put(key, value)

    def get(self, key: str) -> dict:
        return self._client_get(key)

    @property
    def is_leader(self) -> bool:
        return self.state == LEADER
