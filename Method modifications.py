# def recieve_message(name):
#         udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         udpSocket.bind(('', port_we_listen_on))

#         while True:
#             # Receive the message from the client conversing withgit 
#             message = udpSocket.recv(2048)
#             print(message)
#             current = chat_box.get("0.0", "end")
#             chat_box.delete("0.0", "end")
#             current_time = time.strftime('%H:%M')  
#             chat_box.insert(("0.0"),f"{current}{name}: {message.decode()}      [{current_time}]\n\n")
#             udpSocket.close()
            
            
# def send_message():
#         # This is the function running in the main thread
        
#         user_input = entry_box.get("0.0", "end")
#         clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         #print(client_connected_ip + "is the IP being sent to")

#         entry_box.delete("0.0", "end")
#         clientSocket.sendto(user_input.encode(),(client_connected_ip, client_connected_port))
#         clientSocket.close() 

#         # Add locally but must also send it forward
#         if user_input:
#             current = chat_box.get("0.0", "end")
#             chat_box.delete("0.0", "end")
#             current_time = time.strftime('%H:%M')
#             chat_box.insert("0.0",f"{current}You: {user_input}      [{current_time}]\n")
            
            
# def request_waiter(port):
#     udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udpSocket.bind(('', port))
#     connectedToPeer=False
#     while True: # Wait for communication from a client
#             message, clientAddress = udpSocket.recvfrom(2048)
#             print("Message Received:", message)
#             incoming_ip = 
#             request = message.decode().split("-")
#             requesters_name= request[2]
#             if message.decode()[0:17] == "REQ-COMMUNICATION":
#             elif message.decode().split("-")[0] == "OKAY":  # we make this return the clients 
#             elif message
                
                
                
                
#                 print("Invite to chat received!")
#                 reqbox = tkinter.messagebox.askyesno(title="A request has arrived", message=f"{requesters_name} would like to chat, accept? (y/n)", )
#                 if reqbox:
#                     udpSocket.sendto(f"OKAY-{client_id}".encode(), clientAddress)
#                     connectedToPeer = True
#                     global client_connected_ip
#                     global client_connected_port
#                     client_connected_ip = clientAddress[0]
#                     client_connected_port = clientAddress[1]
#                     label.configure(text=f"Chatting to {requesters_name} ")
#                     udpSocket.close()
                    
                    
#     dialog = customtkinter.CTkInputDialog(text="Please enter a client's name to chat to them", title="Connecting to another client")
#     client_name = dialog.get_input()
#     other_client_details = send_TCP_message(CreateRequestClientInfoMessage(client_name)).split("-")

#     other_client_ip_and_port = other_client_details[2]
#     other_ip = other_client_ip_and_port.split(" ")[0]
#     other_port = (int)(other_client_ip_and_port.split(" ")[1])

#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     print(f"Sending to client {other_ip} {other_port}")
#     print(f"my ip: {client_id}\nmy port: {port_we_listen_on}\nTheir ip: {other_ip}\nTheir port: {other_port}")
    
    
#     client.sendto(CreateRequestPeerToPeerCommunication(client_id, port_we_send_on).encode(),(other_ip, other_port)) #spinning somewhere here
#     Message_Received, client_address = client.recvfrom(2048)
#     print(Message_Received)
#     if Message_Received.decode()[0:4] == "OKAY":
#         global connectedToPeer
#         global client_connected_ip
#         global client_connected_port
#         global client_connected_name
#         connectedToPeer = True
#         client_connected_ip = other_ip
#         client_connected_port = other_port
#         client_connected_name = Message_Received.decode().split("-")[1]
#         label.configure(text=f"Chatting to {client_name}")
#     client.close() # we want to close the port anyway, even if they say now

# Python Program to Get IP Address
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
 
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)
