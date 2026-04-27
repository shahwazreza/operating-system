import socket

HOST = '127.0.0.1'
PORT = 8080

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST, PORT))

        server_socket.listen(1)
        print(f"[TCP SERVER] Listening on {HOST}:{PORT} ...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[TCP SERVER] Connection accepted from {addr}")

            data = conn.recv(1024)
            print(f"[TCP SERVER] Received: {data.decode()}")

            ack_message = "ACK: Message received by TCP server"
            conn.sendall(ack_message.encode())
            print("[TCP SERVER] Acknowledgment sent. Closing connection.")

if __name__ == "__main__":
    run_server()
