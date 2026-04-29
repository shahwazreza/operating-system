# Distributed Key-Value Store
**Author:** Reza Shahwaz | **Course:** Operating Systems

## Files
| File | Description |
|------|-------------|
| `consistent_hash.py` | Consistent hashing ring with virtual nodes |
| `vector_clock.py` | Vector clock implementation for conflict detection |
| `node.py` | Single node: RPC server, Raft election, KV store, replication |
| `cluster.py` | 5-node cluster bootstrap and client API |
| `chaos_test.py` | All 4 tests: normal op, node kill, latency, benchmarks |

## Setup
No external dependencies required — only Python standard library.

## Running the Chaos Tests
```bash
python3 chaos_test.py
```
This runs all 4 tests sequentially:
1. Normal PUT/GET operation
2. Kill the leader, verify re-election
3. 500ms network latency — no false elections
4. Performance benchmarks

## Node Ports
| Node | Port |
|------|------|
| node1 | 9001 |
| node2 | 9002 |
| node3 | 9003 |
| node4 | 9004 |
| node5 | 9005 |

## Design Summary
- **Consistency:** Eventual consistency with vector clock conflict detection
- **Election:** Simplified Raft (randomised timeouts 1.5s–3.0s)
- **Replication:** Primary-backup, 2 backups required before ACK
- **Hashing:** Consistent hashing ring with 100 virtual nodes per physical node
- **CAP Choice:** AP — availability over strict consistency during partitions
