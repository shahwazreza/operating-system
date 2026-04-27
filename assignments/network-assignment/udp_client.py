import socket

HOST = '127.0.0.1'
PORT = 8081
PAYLOAD = "UDP_TEST_DATAGRAM"

def run_client():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

        client_socket.sendto(PAYLOAD.encode(), (HOST, PORT))
        print(f"[UDP CLIENT] Sent datagram to {HOST}:{PORT} -> {PAYLOAD}")

    print("[UDP CLIENT] Done.")

if __name__ == "__main__":
    run_client()
