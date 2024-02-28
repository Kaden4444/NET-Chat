from socket import *
import tkinter as tk
import threading
import time
import sys
import random

class App:
    def __init__(self, root, client_connected_to, client_connected_ip, client_connected_port, our_listening_port):
        self.root = root
        self.root.title("Threaded Label Update")
        self.root.geometry("600x500")  # Set window size (width x height)

        self.client_connected_to = client_connected_to
        self.client_connected_ip = client_connected_ip
        self.client_connected_port = int(client_connected_port)
        self.our_listening_port = int(our_listening_port)

        self.title_label = tk.Label(root, text=f"Chatting with {client_connected_to}", fg="#c9d1cc", bg="#2d2d2d", font=("Helvetica", 16, "bold"))
        self.title_label.pack(side="top", fill="x")


        self.label = tk.Label(root, text="", justify="left", anchor="nw", bg="#1e1e1e", fg="#a1ffc6", font=("Helvetica", 12))
        self.label.pack(fill="both", expand=True)
        # Create an input box

        self.frame = tk.Frame(root, bg="#2d2d2d")
        self.frame.pack(side="bottom", fill="both")

        self.entry = tk.Entry(self.frame, font=("Helvetica", 12), bd=0, bg="#3d3d3d", fg="white")
        self.entry.pack(side="left", fill="both", expand=True)

        self.send_button = tk.Button(self.frame, text="Send", command=self.handle_enter,bg="#6fab87", fg="white", font=("Helvetica", 12), bd=0, relief="flat")
        self.send_button.pack(side="right", fill="y")

        # Start a thread for listening to incoming messages
        t1 = threading.Thread(target=self.update_label, args=("Thread 1",))
        t1.start()

    def update_label(self, thread_name):
        # This one will need to be listening for incoming messages on the port, construct them and then display them onto the screen
        serverPort = self.our_listening_port
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', serverPort))

        while True:
            # Receive the message from the client conversing with
            message, clientAddress = serverSocket.recvfrom(2048)
            print(message, clientAddress)
            if clientAddress[0] == self.client_connected_ip:
                # The message comes from the guy connected to us Display the message
                current_time = time.strftime('%H:%M')
                self.label.config(text=self.label.cget("text") + f"{self.client_connected_to}: {message.decode()}      [{current_time}]\n\n")


    def get_user_input(self):
        # This is the function running in the main thread
        self.root.update()  # Update the GUI
        user_input = self.entry.get()
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(user_input.encode(),(self.client_connected_ip, self.client_connected_port))
        clientSocket.close()

        # Add locally but must also send it forward
        if user_input:
            self.label.config(text=self.label.cget("text") + f"You: {user_input}\n")
            self.entry.delete(0, tk.END)  # Clear the input box

    def handle_enter(self):
        self.get_user_input()

client_id = ""
connectedToServer = False
connectedToPeer = False
client_connected_ip = ""
client_connected_port = ""
client_connected_name = ""
port_we_listen_on = ""

def main():
    print("Welcome to Peer2Peer!\n")
    showMainMenu()

def showMainMenu():
    global connectedToServer
    global client_id
    global connectedToPeer
    global client_connected_ip
    global client_connected_port
    global port_we_listen_on

    if not connectedToServer:
        n = input("1: Connect to the server.\n2: See list of active users.\n")
        if n == '1':
            # we connect to the server 
            name = input("Please enter your name:\n")
            client_id = name
            sendMessageToTCPServer(CreateRequestConnectionMessage(name))
            connectedToServer = True # We have now established a connection to the server
            showMainMenu()

        if n == '2':
            response = sendMessageToTCPServer(CreateRequestClientListMessage()).split("-")[2]
            if response == "":
                print("No available clients at this moment")
                showMainMenu()
            else:
                print("Current online users:", response, sep = "\n")
                userToConnectTo = input("Please enter the name of a user you wish to connect to:\n")

                if userToConnectTo not in response.split(" "):
                    print("The user you have entered is not available.")

                port_we_listen_on = random.randrange(12000, 15000)
                client_id = input("Please enter your name:\n")
                
                
                receivedMessage = sendMessageToTCPServer(CreateRequestClientInfoMessage(userToConnectTo)).split("-")
                if receivedMessage[0] == "RET" and receivedMessage[1] == "CLIENTINFO":
                    client_ip_and_port = receivedMessage[2]
                    # print(f"{userToConnectTo}'s ip is:", client_ip_and_port)
                    ip = client_ip_and_port.split(" ")[0]
                    port = client_ip_and_port.split(" ")[1]

                    # Establishing P2P connection now. 
                    SendOpeningUDPMessage(ip, port, port_we_listen_on)

                # Now we can send a message to the client waiting. 

    else:
        n = input("1: Wait for connection from a peer\n2: Change Visibility Level:\n\n")
        if n == '1':
            udp_port = 12000 # By default we just listen on port 12000, TODO allow for manual entering of preffered port number?
            port_we_listen_on = udp_port
            sendMessageToTCPServer(CreateAssertAvailableMessage(client_id, udp_port))
        
            # Now we are listed as available on the server
    
            serverPort = int((udp_port))
            serverSocket = socket(AF_INET, SOCK_DGRAM)
            serverSocket.bind(('', serverPort))

            while True: # Wait for communication from a client
                message, clientAddress = serverSocket.recvfrom(2048)
                global connectedToPeer
                global client_connected_ip
                global client_connected_port
                global client_connected_name
                # print("Message Received:", message)
                if message.decode()[0:17] == "REQ-COMMUNICATION":
                    # print("Request to communicate received")
                    print("Invite to chat received!")
                    serverSocket.sendto(f"OKAY-{client_id}".encode(), clientAddress)
                    connectedToPeer = True
                    client_connected_ip = clientAddress[0]
                    client_connected_port = message.decode().split("-")[3]
                    client_connected_name = message.decode().split("-")[2]
                    serverSocket.close()
                    break
                else:
                    continue

            if connectedToPeer:
                ConnectionAchievedRendezvous()

def SendOpeningUDPMessage(ip, port, port_listening):
    # print("Trying to send opening message to", ip, port)
    print("Establishing Peer-to-Peer Connection...")
    PeerName = ip
    PeerPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(CreateRequestPeerToPeerCommunication(client_id, port_listening).encode(),(PeerName, PeerPort))

    Message_Received, serverAddress = clientSocket.recvfrom(2048)
    if Message_Received.decode()[0:4] == "OKAY":
        global connectedToPeer
        global client_connected_ip
        global client_connected_port
        global client_connected_name
        connectedToPeer = True
        client_connected_ip = ip
        client_connected_port = port
        client_connected_name = Message_Received.decode().split("-")[1]
    clientSocket.close()
    if connectedToPeer:
        ConnectionAchievedRendezvous()

def ConnectionAchievedRendezvous():
    # print("Our Name:", client_id)
    # print("Connected to host @", client_connected_ip)
    # print("Port client is listening on:", client_connected_port)
    # print("Connected to Client Name:", client_connected_name)
    # print("Port we are listening on:", port_we_listen_on)
    print(f"You have successfully connected with {client_connected_name}!")
    root = tk.Tk()
    app = App(root, client_connected_name, client_connected_ip, client_connected_port, port_we_listen_on)
    root.mainloop()


def sendMessageToTCPServer(message):
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(message.encode())
    modifiedSentence = clientSocket.recv(1024)
    clientSocket.close()
    return modifiedSentence.decode()





def CreateRequestConnectionMessage(name):
    return f"REQ-CONNECTION-{name}"

def CreateAssertAvailableMessage(name, udp_port):
    return f"COMMAND-AVAIL-{name}-{udp_port}"

def CreateAssertUnavailableMessage(name, udp_port):
    return f"COMMAND-NAVAIL-{name}-{udp_port}"

def CreateRequestClientListMessage():
    return f"REQ-CLIENT_LIST"

def CreateRequestClientInfoMessage(user):
    return f"REQ-CLIENT-{user}"

def CreateRequestPeerToPeerCommunication(name, our_port):
    return f"REQ-COMMUNICATION-{name}-{our_port}"

if __name__ == "__main__":
    main()