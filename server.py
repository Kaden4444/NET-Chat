from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

def main():
    active_clients = {}
    while True:
        connectionSocket, addr = serverSocket.accept()

        # The request received from the client
        request = connectionSocket.recv(1024).decode()
        request_list = request.split("-")

        # These is the implementation of all the [REQ] commands that we defined.
        if request_list[0] == "REQ":
            print("Received request from client")
            
            if request_list[1] == "CONNECTION":
                print("Client is requesting connection")
                # We have a request for connectionw
                if request_list[2] not in active_clients.keys():
                    active_clients[request_list[2]] = ("CONNECTED", addr[0])
                    print("Currently Active Clients: ", active_clients)

            # Returns the current client list from the server, (only available clients are returned) the list returned is a space seperated list of names with the headers RET-CLIENTLIST prepended
            if request_list[1] == "CLIENT_LIST":
                print("Client is requesting the client list")
                available_clients = "RETURN-CLIENTLIST-" + get_available_clients(active_clients)
                connectionSocket.send(available_clients.encode())

            # Returns the IP address and listening port of a client requested, the string sent back is just the ip and port seperated by a space with the headers RET-CLIENTINFO prepended
            if request_list[1] == "CLIENT":
                print("Client is requesting a client's information")
                client_id = request_list[2]
                print("The client requested is " + client_id)
                if client_id in active_clients.keys():
                    udp_ip_of_client_requested = active_clients[client_id][1]
                    udp_ip_port = active_clients[client_id][2]
                    connectionSocket.send(("RET-CLIENTINFO-" + udp_ip_of_client_requested + " " +  udp_ip_port).encode())
                    print(udp_ip_of_client_requested + " " + udp_ip_port)


        elif request_list[0] == "COMMAND":
            if request_list[1] == "AVAIL":
                # This command changes the status of a client to available on the server's list.
                if (request_list[2] in active_clients.keys()):
                    active_clients[request_list[2]] = ("AVAILABLE", ) + (active_clients[request_list[2]][1],) + (request_list[3],)
                    print(f"Added a new user: {request_list[2]} to the server.")
                    print("Currently Active Clients: ", active_clients)
                else:
                    print("ERROR: An availability check without prior connection attempted")

            if request_list[1] == "NAVAIL":
                # This command removes a client from the list of connected clients
                if (request_list[2] in active_clients.keys()):
                    del active_clients[request_list[2]]
                    print(f"Removed {request_list[2]} from the server.")
                    print("Currently Active Clients: ", active_clients)
                else:
                    print("ERROR: Invalid operation involving NAVAIL command")

            if request_list[1] == "CHANGEVIS":
                # This command will change visibility on the server from available to only connected 
                if (request_list[2] in active_clients.keys()):
                    active_clients[request_list[2]] = ("CONNECTED", ) + (active_clients[request_list[2]][1],)
                    print(f"Changed the visibility of {request_list[2]} from CONNECTED to AVAILABLE")
                    print("Currently Active Clients: ", active_clients)
                else:
                    print("ERROR: Invalid operation involving CHANGEVIS")

        connectionSocket.close()

def get_available_clients(d):
    out = ''
    for client in d.keys():
        if d[client][0] == "AVAILABLE":
            out += " " + client
    return out

main()
