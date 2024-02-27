import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect")
    client.connect(("196.47.211.160", 5555))
    print("Connected")

    name = input("Enter your name: ")
    client.send(name.encode('utf-8'))

    # Receive welcome message
    welcome_message = client.recv(1024).decode('utf-8')
    print(welcome_message)

    while True:
        print("Options:")
        print("1. Send a message")
        print("2. Request list of online clients")
        print("3. Initiate chat request")
        print("4. Quit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            message = input("Enter your message: ")
            client.send(message.encode('utf-8'))
        elif choice == "2":
            client.send("get_clients".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)
        elif choice == "3":
            target_name = input("Enter the name of the user you want to chat with: ")
            client.send(f"request_chat:{target_name}".encode('utf-8'))
            confirm_prompt = client.recv(1024).decode('utf-8')
            print(confirm_prompt)
            #change so that i am sending a request to a client, using server details
            response = client.recv(1024).decode('utf-8')
            print("Server response: " + response)

            # If the response is 'yes', initiate P2P connection
            if response.strip().lower() == "yes":
                print("Initiating P2P connection...")
                initiate_p2p_connection(client, target_name)
        elif choice == "4":
            client.send("disconnect".encode('utf-8'))
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    client.close()

def initiate_p2p_connection(client, target_name):
    # Assuming P2P connection details are received from the server
    print("Initiating p2p connection")
    p2p_address = client.recv(1024).decode('utf-8')
    print("Trying to connect with:" + p2p_address)
    print(f"P2P connection established with {target_name}. Address: {p2p_address}")

    # Now, you can use the P2P connection for direct communication

if __name__ == "__main__":
    start_client()
