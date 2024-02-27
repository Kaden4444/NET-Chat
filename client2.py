import socket
import threading
import time

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

def main():
    server_ip = "196.47.211.160"
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    name = input("Enter your name: ")
    client.send(name.encode('utf-8'))

    # Receive and print the welcome message
    welcome_message = client.recv(1024).decode('utf-8')
    print(welcome_message)

    # Receive and print messages in a separate thread
    message_thread = threading.Thread(target=receive_messages, args=(client,))
    message_thread.start()

    while True:
        time.sleep(1)
        print("\nOptions:")
        print("1. Send Message")
        print("2. Request Chat")
        print("3. View Clients")
        print("4. Disconnect")

        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter your message: ")
            client.send(message.encode('utf-8'))
        elif choice == "2":
            target_name = input("Enter the name of the user you want to chat with: ")
            client.send(f"request_chat:{target_name}".encode('utf-8'))
            other_client = client.recv(1024).decode('utf-8')
            other_client_socket = socket.socket(other_client)
        elif choice == "3":
            client.send(f"get_clients".encode('utf-8'))
        elif choice == "4":
            client.send("disconnect".encode('utf-8'))
            break
        else:
            print("Invalid choice. Please try again.")

    client.close()

if __name__ == "__main__":
    main()
