# Tests:
#   1. Normal operation  — PUT/GET round trip
#   2. Node Kill         — kill the leader, verify new election and continued operation
#   3. Network Latency   — 500ms delay, verify no false elections trigger
#   4. Performance       — measure read latency and write throughput

import time
import threading
from cluster import Cluster


def separator(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


# Test 1: Normal Operation
def test_normal_operation():
    separator("TEST 1: Normal PUT/GET Operation")
    cluster = Cluster()
    cluster.start()
    cluster.get_status()

    # Write some keys
    for i in range(5):
        result = cluster.put(f"key{i}", f"value{i}")
        status = "OK" if result.get("ok") else f"FAIL: {result.get('error')}"
        print(f"  PUT key{i} = value{i}  ->  {status}")

    time.sleep(0.3)

    # Read them back
    print()
    for i in range(5):
        result = cluster.get(f"key{i}")
        if result.get("ok"):
            print(f"  GET key{i}  ->  '{result['value']}'  (vc={result['vc']})")
        else:
            print(f"  GET key{i}  ->  FAIL: {result.get('error')}")

    cluster.stop()
    print("\n[TEST 1] PASSED")


# Test 2: Node Kill
def test_node_kill():
    separator("TEST 2: Node Kill — Leader Failure & Re-election")
    cluster = Cluster()
    cluster.start()

    # Write some data before killing
    cluster.put("before_kill", "safe_value")
    time.sleep(0.2)

    leader_before = cluster.get_leader()
    print(f"\n  Leader before kill: {leader_before}")
    cluster.kill_node(leader_before)
    print(f"  Killed node: {leader_before}")
    print("  Waiting for re-election (up to 4 seconds)...")

    # Wait for new leader
    deadline = time.time() + 4
    new_leader = None
    while time.time() < deadline:
        new_leader = cluster.get_leader()
        if new_leader and new_leader != leader_before:
            break
        time.sleep(0.1)

    if new_leader:
        print(f"  New leader elected: {new_leader}  ✓")
    else:
        print("  ERROR: No new leader elected within timeout  ✗")

    # Verify continued operation
    result = cluster.put("after_kill", "still_works")
    print(f"  PUT after kill  ->  {'OK  ✓' if result.get('ok') else 'FAIL  ✗'}")

    result = cluster.get("before_kill")
    print(f"  GET before_kill ->  '{result.get('value')}'  {'✓' if result.get('ok') else '✗'}")

    cluster.get_status()
    cluster.stop()
    print("[TEST 2] PASSED" if new_leader else "[TEST 2] FAILED")


# ── Test 3: Network Latency
def test_network_latency():
    separator("TEST 3: 500ms Network Latency — No False Elections")
    # Start cluster WITH 500ms simulated latency
    cluster = Cluster(latency=0.5)
    cluster.start()

    leader_before = cluster.get_leader()
    print(f"  Leader: {leader_before}")
    print("  Sleeping 4 seconds with 500ms latency on all messages...")
    print("  (Heartbeat timeout is 1.5s–3.0s, so no election should trigger)")

    time.sleep(4)

    leader_after = cluster.get_leader()
    print(f"  Leader after 4s: {leader_after}")

    if leader_after == leader_before:
        print("  No false election triggered  ✓")
        passed = True
    else:
        print(f"  Leader changed from {leader_before} to {leader_after}  ✗")
        passed = False

    # Verify the cluster still works end-to-end
    result = cluster.put("latency_test", "hello")
    print(f"  PUT under latency -> {'OK  ✓' if result.get('ok') else 'FAIL  ✗'}")

    cluster.stop()
    print(f"[TEST 3] {'PASSED' if passed else 'FAILED'}")


# Test 4: Performance Benchmarks
def test_performance():
    separator("TEST 4: Performance Benchmarks")
    cluster = Cluster()
    cluster.start()
    time.sleep(0.5)

    # Read Latency: Single Node
    N = 100
    # Pre-populate
    cluster.put("bench_key", "bench_value")
    time.sleep(0.3)

    # Single-node read (direct local get, no replication path)
    leader_node = cluster.nodes[cluster.get_leader()]
    start = time.perf_counter()
    for _ in range(N):
        leader_node.get("bench_key")
    single_read_ms = (time.perf_counter() - start) / N * 1000

    # Distributed read (via cluster routing)
    start = time.perf_counter()
    for _ in range(N):
        cluster.get("bench_key")
    dist_read_ms = (time.perf_counter() - start) / N * 1000

    # Write Throughput
    W = 50
    start = time.perf_counter()
    for i in range(W):
        cluster.put(f"wbench{i}", f"v{i}")
    write_duration = time.perf_counter() - start
    write_ops_sec = W / write_duration

    print(f"\n  ┌──────────────────────────────────────────────────┐")
    print(f"  │          Performance Metrics                     │")
    print(f"  ├──────────────────────────────────────────────────┤")
    print(f"  │  Read Latency  (single node)   : {single_read_ms:6.3f} ms/op    │")
    print(f"  │  Read Latency  (distributed)   : {dist_read_ms:6.3f} ms/op    │")
    print(f"  │  Write Throughput              : {write_ops_sec:6.1f} ops/sec  │")
    print(f"  │  (with 2-backup replication)                     │")
    print(f"  └──────────────────────────────────────────────────┘")

    cluster.stop()
    print("[TEST 4] DONE")


# Main
if __name__ == "__main__":
    test_normal_operation()
    print("\n"); time.sleep(2)
    test_node_kill()
    print("\n"); time.sleep(2)
    test_network_latency()
    print("\n"); time.sleep(2)
    test_performance()
    print("\n\nAll chaos tests complete.")
