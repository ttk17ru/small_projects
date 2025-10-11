import socket
import threading

HOST = "0.0.0.0"
PORT = 6999

clients = {}  # client_socket: {"room": room_name, "name": username}
lock = threading.Lock()

def broadcast(message, room, sender_socket=None):
    with lock:
        for client_socket, info in clients.items():
            if info["room"] == room and client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except:
                    pass

def handle_client(client_socket, addr):
    print(f"[+] Connection from {addr}")

    # Receive username right after connection
    try:
        username_data = client_socket.recv(1024)
        username = username_data.decode().strip()
        if not username:
            username = f"{addr[0]}"
    except:
        username = f"{addr[0]}"

    with lock:
        clients[client_socket] = {"room": "main", "name": username}

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break

            if data.startswith(b"/room "):
                new_room = data.decode().split(" ", 1)[1].strip()
                with lock:
                    clients[client_socket]['room'] = new_room
                client_socket.send(f"*** Switched to room: {new_room} ***".encode())
                continue

            if data.startswith(b"/file "):
                filename = data.decode().split(" ", 1)[1].strip()
                # Next 16 bytes represent file size (padded)
                file_size_data = client_socket.recv(16)
                file_size = int(file_size_data.decode().strip())
                file_data = b""
                while len(file_data) < file_size:
                    chunk = client_socket.recv(min(4096, file_size - len(file_data)))
                    if not chunk:
                        break
                    file_data += chunk
                broadcast(b"[FILE] " + filename.encode() + b"\n" + file_data, clients[client_socket]['room'], client_socket)
                continue

            message = f"[{clients[client_socket]['name']}] {data.decode()}".encode()
            broadcast(message, clients[client_socket]['room'], client_socket)

    except Exception as e:
        print(f"[-] Error with {addr}: {e}")

    finally:
        with lock:
            del clients[client_socket]
        client_socket.close()
        print(f"[-] Disconnected: {addr}")

def accept_clients(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[+] Server listening on {HOST}:{PORT}")

    accept_clients(server_socket)

if __name__ == "__main__":
    main()
