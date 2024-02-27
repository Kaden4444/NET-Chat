import socket
import threading
import time
clients = {}  # Dictionary to store client information (name, socket)
p2p_connections = {}  # Dictionary to store P2P connections
HOST = "192.168.68.126"
# HOST = "196.47.211.160"

def receive_name(client_socket, client_address):
    name = client_socket.recv(1024).decode('utf-8')
    clients[client_address] = {"name": name, "socket": client_socket}
    print(f"[*] {name} connected from {client_address[0]}:{client_address[1]}")

    welcome_message = f"Welcome, {name}!"
    #client_socket.send(welcome_message.encode('utf-8'))
    
    handle_client(client_socket, client_address)

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
        except: 
            time.sleep(1)
        if not message:
            break
        
        if message.lower() == "disconnect":
            print(f"[*] {clients[client_address]['name']} disconnected")
            del clients[client_address]
            close_p2p_connection(client_address)
            client_socket.close()
            break
        elif message.startswith("request_chat:"):
            target_name = message.split(":")[1].strip()
            request_client = find_client_by_name(target_name)
            client_socket.send(client_address).encode('utf-8')
            establish_p2p_connection(client_address, request_client['socket'])

          #  if request_client:
           #     request_message = f"{clients[client_socket]['name']} wants to start a chat. Accept? (yes/no)"
         #       request_client['socket'].send(request_message.encode('utf-8'))
          #      response = request_client['socket'].recv(1024).decode('utf-8')
         #       print("Response when trying was: " + response)
            #    if response.strip() == "yes":
            #          establish_p2p_connection(client_address, request_client['socket'])
                    
        elif message.lower() == "get_clients":
            print(f"Request from {clients[client_address]['name']}")
            print(message)
            send_clients_list(client_socket)
        else:
            print(f"{clients[client_address]['name']}: {message}")

def find_client_by_name(name):
    for addr, client_info in clients.items():
        if client_info['name'].lower() == name.lower():
            return client_info
    return None

def establish_p2p_connection(client1_address, client2_socket):
    client2_address = get_client_address_by_socket(client2_socket)

    p2p_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p2p_socket1.bind(("0.0.0.0", 0))  # Bind to any available port
    p2p_port1 = p2p_socket1.getsockname()[1]
    p2p_connections[client1_address] = {"socket": p2p_socket1, "port": p2p_port1}

    p2p_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p2p_socket2.bind(("0.0.0.0", 0))  # Bind to any available port
    p2p_port2 = p2p_socket2.getsockname()[1]
    p2p_connections[client2_address] = {"socket": p2p_socket2, "port": p2p_port2}

    # Inform clients about each other's P2P address
    p2p_message1 = f"P2P_CONNECT {client2_address[0]} {p2p_port2}"
    clients[client1_address]['socket'].send(p2p_message1.encode('utf-8'))

    p2p_message2 = f"P2P_CONNECT {client1_address[0]} {p2p_port1}"
    clients[client2_address]['socket'].send(p2p_message2.encode('utf-8'))

def get_client_address_by_socket(client_socket):
    for addr, client_info in clients.items():
        if client_info['socket'] == client_socket:
            return addr
    return None

def close_p2p_connection(client_address):
    if client_address in p2p_connections:
        p2p_connections[client_address]['socket'].close()
        del p2p_connections[client_address]

def send_clients_list(client_socket):
    online_clients = [client_info['name'] for client_info in clients.values()]
    clients_list = "\n".join(online_clients)
    print(f"Available clients:\n{clients_list}")
    client_socket.send(f"Online clients:\n{clients_list}".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, 5555))
    server.listen(5)
    print(f"[*] Listening on {HOST}:5555")

    while True:
        client, addr = server.accept()

        # Start a separate thread to receive the name
        name_receiver = threading.Thread(target=receive_name, args=(client, addr))
        name_receiver.start()

if __name__ == "__main__":
    start_server()
