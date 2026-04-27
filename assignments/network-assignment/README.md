# Network Traffic Analysis Assignment
**Author:** Reza Shahwaz

## Overview
This project implements TCP and UDP client-server communication alongside a packet sniffer that captures and parses the traffic they generate.

## Files
| File | Description |
|------|-------------|
| `tcp_server.py` | TCP server listening on port 8080 |
| `tcp_client.py` | TCP client that sends `TCP_TEST_PACKET` to the server |
| `udp_server.py` | UDP server listening on port 8081 |
| `udp_client.py` | UDP client that sends `UDP_TEST_DATAGRAM` to the server |
| `sniffer.py` | Packet sniffer that detects TCP/UDP traffic on ports 8080 and 8081 |

## Dependencies
Install Scapy before running the sniffer:
```bash
pip install scapy
```

## How to Run

You will need **three terminal windows** open simultaneously.

---

### Terminal 1 — Start the Sniffer (must be first, requires sudo)
```bash
sudo python3 sniffer.py
```
The sniffer listens on the `lo` (loopback) interface and will print any TCP or UDP packets it detects on ports 8080 or 8081.

---

### Terminal 2 — TCP Test

Start the TCP server:
```bash
python3 tcp_server.py
```

Then in **Terminal 3**, run the TCP client:
```bash
python3 tcp_client.py
```

Expected output in Terminal 2 (server):
```
[TCP SERVER] Listening on 127.0.0.1:8080 ...
[TCP SERVER] Connection accepted from ('127.0.0.1', <ephemeral_port>)
[TCP SERVER] Received: TCP_TEST_PACKET
[TCP SERVER] Acknowledgment sent. Closing connection.
```

Expected output in Terminal 3 (client):
```
[TCP CLIENT] Connected to 127.0.0.1:8080
[TCP CLIENT] Sent: TCP_TEST_PACKET
[TCP CLIENT] Received acknowledgment: ACK: Message received by TCP server
[TCP CLIENT] Connection closed.
```

---

### Terminal 2 — UDP Test

Start the UDP server:
```bash
python3 udp_server.py
```

Then in **Terminal 3**, run the UDP client:
```bash
python3 udp_client.py
```

Expected output in Terminal 2 (server):
```
[UDP SERVER] Listening on 127.0.0.1:8081 ...
[UDP SERVER] Received datagram from ('127.0.0.1', <ephemeral_port>): UDP_TEST_DATAGRAM
```

---

### Sniffer Output (Terminal 1)
While the clients run, the sniffer should print detections like:
```
[DETECTED TCP PACKAGE]
  Source IP     : 127.0.0.1
  Destination IP: 127.0.0.1
  Source Port   : <ephemeral>
  Dest Port     : 8080
---------------------------------------------
[DETECTED UDP DATAGRAM]
  Source IP     : 127.0.0.1
  Destination IP: 127.0.0.1
  Source Port   : <ephemeral>
  Dest Port     : 8081
---------------------------------------------
```

## Network Interface
The sniffer uses the **`lo` (loopback)** interface to capture localhost traffic (`127.0.0.1`). This is set in `sniffer.py` via `INTERFACE = "lo"`.

## Notes
- The sniffer requires `sudo` because raw packet capture is a privileged operation on Linux.
- Run the sniffer **before** the clients so no packets are missed.
- The UDP server runs in an infinite loop — stop it with `Ctrl+C` after testing.
