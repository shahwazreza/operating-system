import socket

HOST = '127.0.0.1'
PORT = 8081

def run_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")
        print("[UDP SERVER] Waiting for datagrams (Ctrl+C to stop) ...")

        # Loop continuously to receive multiple datagrams
        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"[UDP SERVER] Received datagram from {addr}: {data.decode()}")

if __name__ == "__main__":
    run_server()
