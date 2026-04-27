import socket

HOST = '127.0.0.1'
PORT = 8080
PAYLOAD = "TCP_TEST_PACKET"

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"[TCP CLIENT] Connected to {HOST}:{PORT}")

        # Send the test payload
        client_socket.sendall(PAYLOAD.encode())
        print(f"[TCP CLIENT] Sent: {PAYLOAD}")

        # Wait for the server's acknowledgment
        response = client_socket.recv(1024)
        print(f"[TCP CLIENT] Received acknowledgment: {response.decode()}")

    print("[TCP CLIENT] Connection closed.")

if __name__ == "__main__":
    run_client()
