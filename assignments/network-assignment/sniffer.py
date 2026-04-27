from scapy.all import sniff, IP, TCP, UDP

# Only show packets involving our server ports to avoid console spam
WATCHED_PORTS = {8080, 8081}

def process_packet(packet):
    """
    Called by Scapy for every captured packet.
    We check for IPv4, then inspect the transport layer (TCP or UDP).
    """

    # Only process IPv4 packets
    if not packet.haslayer(IP):
        return

    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst

    # TCP Detection
    if packet.haslayer(TCP):
        tcp_layer = packet[TCP]
        src_port = tcp_layer.sport
        dst_port = tcp_layer.dport

        if src_port in WATCHED_PORTS or dst_port in WATCHED_PORTS:
            print(f"[DETECTED TCP PACKAGE]")
            print(f"  Source IP     : {src_ip}")
            print(f"  Destination IP: {dst_ip}")
            print(f"  Source Port   : {src_port}")
            print(f"  Dest Port     : {dst_port}")
            print("-" * 45)

    # UDP Detection
    elif packet.haslayer(UDP):
        udp_layer = packet[UDP]
        src_port = udp_layer.sport
        dst_port = udp_layer.dport

        if src_port in WATCHED_PORTS or dst_port in WATCHED_PORTS:
            print(f"[DETECTED UDP DATAGRAM]")
            print(f"  Source IP     : {src_ip}")
            print(f"  Destination IP: {dst_ip}")
            print(f"  Source Port   : {src_port}")
            print(f"  Dest Port     : {dst_port}")
            print("-" * 45)

def main():
    INTERFACE = "lo"
    print(f"[SNIFFER] Starting on interface '{INTERFACE}' ...")
    print(f"[SNIFFER] Watching ports: {WATCHED_PORTS}")
    print(f"[SNIFFER] Press Ctrl+C to stop.\n")

    sniff(iface=INTERFACE, prn=process_packet, store=False)

if __name__ == "__main__":
    main()
