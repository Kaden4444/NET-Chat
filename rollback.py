# GUI
import tkinter
import tkinter.messagebox
import customtkinter

# Networking
import socket
import threading
import time
import random

#general notes:
    # lamba allows you to pass parameters to functions that buttons will use, allowing you to configure a button when you click it (VERY USEFUL)

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), button_colour, "dark-blue"
background = "#232222"
frame_colour = "#b07289"
button_colour= "green"

main_server_port = 12000
port_we_listen_on = random.randrange(12001, 15000)
port_we_send_on = random.randrange(12001, 15000)
    
class DemoGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=background)

        # configure window
        self.title("Shit WhatsApp")

        self.geometry(f"{1000}x{400}")
    
        # stick the window the same size, we don't need more space 
        self.resizable(width=False, height=False)

        # configure layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        
        self.rowconfigure(0,weight=1)

        # sidebar frame
        self.clients_frame = customtkinter.CTkFrame(master=self , fg_color= frame_colour )
        self.clients_frame.grid(row=0, column=0, rowspan="3", sticky="nswe")
        
        # main frame (hehe)
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=10, fg_color=frame_colour) 
        self.main_frame.grid(row=0, column=1, padx=(5,0), sticky="nswe")
        self.main_frame.columnconfigure(0, weight=1)
        
        # Setting up rows for the messaging part of the app
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=10)
        self.main_frame.rowconfigure(2, weight=5)
        self.main_frame.rowconfigure(3, weight=1)

        # setting up label that tells us who we are talking to
        global label
        self.chat_label = customtkinter.CTkLabel(master=self.main_frame, text="Connect to a client to chat:", font=("Times", 30, "bold"), text_color="black")
        self.chat_label.grid(row=0, padx=15, pady=10, sticky="nsw")
        label = self.chat_label

        # button to disconnect from the client
        self.disconnect_from_client = customtkinter.CTkButton(master=self.main_frame, text="Disconnect", fg_color="red", border_width=1, border_color="black",text_color="black")
        self.disconnect_from_client.grid(row=0, padx=10, pady=10 , sticky='nse')
        #self.disconnect_from_client.configure(command= lambda:)

        # setting up the textbox where text will appear
        global chat_box
        self.chat_textbox = customtkinter.CTkTextbox(self.main_frame,fg_color="white", activate_scrollbars=True,text_color="black", border_color="black", border_width=1)
        self.chat_textbox.grid(row=1, rowspan=1, padx=10, pady=(0,10), sticky="nsew")
        # assign global var
        chat_box= self.chat_textbox

        # text entry textbox
        global entry_box
        self.entry_textbox = customtkinter.CTkTextbox(self.main_frame,height=10,fg_color="white", activate_scrollbars=True,text_color="black", border_color="black", border_width=1)
        self.entry_textbox.grid(row=2, padx=10, pady=(10,0), sticky="nsew")
        # assign global var
        entry_box = self.entry_textbox

        # enter button
        self.chat_button = customtkinter.CTkButton(master=self.main_frame, text="Send", fg_color=button_colour, border_width=1, border_color="black",text_color="black",command=send_message)
        self.chat_button.grid(row=3, sticky='ne', padx=(0,10), pady=(10,0))
        #self.chat_button.configure(command= lambda:connect_to_server(client,self.server_button))

        #configure client frame grid
        self.clients_frame.columnconfigure(0, weight=1)
        self.clients_frame.rowconfigure(0, weight=1)
        self.clients_frame.rowconfigure(1, weight=1)
        #self.clients_frame.rowconfigure(2, weight=1)

         
        # create the "Connect to server" button 
        self.server_button = customtkinter.CTkButton(master=self.clients_frame, text="Connect to server", fg_color=button_colour, border_width=1, border_color="black",text_color="black")
        self.server_button.grid(row=0, padx=10, pady=10 , sticky='ne')
        self.server_button.configure(command= lambda:connect_to_server(self.server_button))
        
        # button for changing client status
        self.set_status_button = customtkinter.CTkButton(master=self.clients_frame, text="Change Status", fg_color=button_colour, border_width=1, border_color="black",text_color="black")
        self.set_status_button.grid(row=0, padx=10, pady=10 , sticky='nw')
        self.set_status_button.configure(command= lambda:change_status_to_available(self.set_status_button))
        
        # create textbox         
        self.textbox = customtkinter.CTkTextbox(self.clients_frame, fg_color="white", activate_scrollbars=True,text_color="black", border_color="black", border_width=1)
        self.textbox.insert("0.0", "Not connected to server\nPlease connect and click the refresh button")
        self.textbox.grid(row=0, column=0, rowspan=1, padx=10, pady=(50,0), sticky="nsew")
        # disable its input
        self.textbox.configure(state="disabled")

        # create the refresh button
        self.refresh_button = customtkinter.CTkButton(master=self.clients_frame, text="Refresh", fg_color=button_colour, border_width=1, border_color="black",text_color="black")
        self.refresh_button.grid(row=1, column=0,padx=(10,10),pady=10 , sticky='ne')
        self.refresh_button.configure(command=lambda: populate_client_list(self.textbox))
  
        # create the client connect button 
        self.client_connect_button = customtkinter.CTkButton(master=self.clients_frame, text="Connect to client", fg_color=button_colour,command=connect_to_client, border_width=1, border_color="black",text_color="black")
        self.client_connect_button.grid(row=1, column=0,padx=(10,10),pady=10 , sticky='nw')

def connect_to_server(button):
    name=""
    global client_id
    try: 
        dialog = customtkinter.CTkInputDialog(text="Enter your name", title="Connecting to server")
        name = dialog.get_input()
        client_id = name
        #enter Ip manually
        global main_server_ip
        server_ip_prompt = customtkinter.CTkInputDialog(text="Enter the server IP", title="Connect to a server")
        main_server_ip = server_ip_prompt.get_input()
        
        #set it manually
        #global main_server_ip
        #main_server_ip="192.168.68.118"
        #"192.168.249.65"

        send_TCP_message(CreateRequestConnectionMessage(name))

        button.configure(text="Disconnect",fg_color="Red", command= lambda: disconnect_from_server(button))
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Server not found", title = "Error")
        errorbox.show()

def disconnect_from_server(button):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.send("DISCONNECT".encode('utf-8'))
    client.close()
    button.configure(text="Connect to server", fg_color=button_colour , command= lambda:connect_to_server(button))

def send_TCP_message(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(main_server_ip + " is supposed to be IP")
    try:
        client.connect((main_server_ip, main_server_port)) 
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to send message to / receive response from the server ", title = "Error")
        errorbox.show()
    client.close()
    return response


def populate_client_list(textbox):
    try:
        response = send_TCP_message(CreateRequestClientListMessage()).split("-")[2]
        
        print(response)
        if response == "":
            textbox.configure(state="normal")
            textbox.delete(0.0, 'end')
            textbox.insert("0.0","No clients available currently")
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.delete(0.0, 'end')
            new = response.split(" ")
            new = "\n".join(new)  #this took forever to figure out fml
            print(new)
            textbox.insert("0.0",f"Available clients:\n{new}")
            print(response)
            
            textbox.configure(state="disabled")
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to receive clients.", title = "Error")
        errorbox.show()

def change_status_to_available(button):
    send_TCP_message(CreateAssertAvailableMessage(client_id,port_we_listen_on))
    waiterthread = threading.Thread(target=request_waiter)
    waiterthread.start()
    button.configure(fg_color="red", text="Change Status", command=lambda: change_status_to_connected(button))

def change_status_to_connected(button):
    send_TCP_message(CreateAssertChangeVis(client_id,port_we_listen_on))
    button.configure(fg_color=button_colour, text="Change Status", command=lambda: change_status_to_available(button))

    
def connect_to_client():
    dialog = customtkinter.CTkInputDialog(text="Please enter a client's name to chat to them", title="Connecting to another client")
    client_name = dialog.get_input()
    other_client_details = send_TCP_message(CreateRequestClientInfoMessage(client_name)).split("-")

    other_client_ip_and_port = other_client_details[2]
    other_ip = other_client_ip_and_port.split(" ")[0]
    other_port = (int)(other_client_ip_and_port.split(" ")[1])
    
    
    other_client_ip = other_ip
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending to client {other_ip} {other_port}")
    
    print(f"my ip: {client_id}\nmy port: {port_we_listen_on}\nTheir ip: {other_ip}\nTheir port: {other_port}")
    
    
    client.sendto(CreateRequestPeerToPeerCommunication(client_id, port_we_send_on).encode(),(other_ip, other_port))
    Message_Received, client_address = client.recvfrom(2048)
    print(Message_Received)
    if Message_Received.decode()[0:4] == "OKAY":
        global connectedToPeer
        global client_connected_ip
        global client_connected_port
        global client_connected_name
        connectedToPeer = True
        client_connected_ip = other_ip
        client_connected_port = other_port
        client_connected_name = Message_Received.decode().split("-")[1]
        label.configure(text=f"Chatting to {client_name}")
        
        #client.close()
        #listenerthread = threading.Thread(target= request_waiter())
        #listenerthread.start()
        
    while connectedToPeer:
        message = client.recv(2048)
        print(message)
        current = chat_box.get("0.0", "end")
        chat_box.delete("0.0", "end")
        current_time = time.strftime('%H:%M')  
        chat_box.insert(("0.0"),f"{current}{client_connected_name}: {message.decode()}      [{current_time}]\n\n")
        
        return

# wait for request
# idea is that this is created on a seperate thread, it spins and waits for a message
def request_waiter():
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind(('', port_we_listen_on))
    connectedToPeer=False
    while True: # Wait for communication from a client
        
        while connectedToPeer:   # spinning on this the entire time while waiting for first message 
                    message = udpSocket.recv(2048)
                    print(message)
                    current = chat_box.get("0.0", "end")
                    chat_box.delete("0.0", "end")
                    current_time = time.strftime('%H:%M')  
                    chat_box.insert(("0.0"),f"{current}{requesters_name}: {message.decode()}      [{current_time}]\n\n")

        message, clientAddress = udpSocket.recvfrom(2048)
        print("Message Received:", message)
        request = message.decode().split("-")
        requesters_name= request[2]
        if message.decode()[0:17] == "REQ-COMMUNICATION":
            print("Invite to chat received!")
            reqbox = tkinter.messagebox.askyesno(title="A request has arrived", message=f"{requesters_name} would like to chat, accept? (y/n)", )
            if reqbox:
                udpSocket.sendto(f"OKAY-{client_id}".encode(), clientAddress)
                connectedToPeer = True
                global client_connected_ip
                global client_connected_port
                client_connected_ip = clientAddress[0]
                client_connected_port = clientAddress[1]
                label.configure(text=f"Chatting to {requesters_name} ")
        
        #udpSocket.close()




### TESTING

def send_message():
        # This is the function running in the main thread
        
        user_input = entry_box.get("0.0", "end")
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #print(client_connected_ip + "is the IP being sent to")

        entry_box.delete("0.0", "end")
        clientSocket.sendto(user_input.encode(),(client_connected_ip, client_connected_port))
        clientSocket.close() 

        # Add locally but must also send it forward
        if user_input:
            current = chat_box.get("0.0", "end")
            chat_box.delete("0.0", "end")
            current_time = time.strftime('%H:%M')
            chat_box.insert("0.0",f"{current}You: {user_input}      [{current_time}]\n\n")

def recieve_message(name):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.bind(('', port_we_listen_on))

        while True:
            # Receive the message from the client conversing withgit 
            message = udpSocket.recv(2048)
            print(message)
            current = chat_box.get("0.0", "end")
            chat_box.delete("0.0", "end")
            current_time = time.strftime('%H:%M')  
            chat_box.insert(("0.0"),f"{current}{name}: {message.decode()}      [{current_time}]\n\n")
            udpSocket.close()




def CreateRequestConnectionMessage(name):
    return f"REQ-CONNECTION-{name}"

def CreateAssertAvailableMessage(name, udp_port):
    return f"COMMAND-AVAIL-{name}-{udp_port}"

def CreateAssertUnavailableMessage(name, udp_port):
    return f"COMMAND-NAVAIL-{name}-{udp_port}"

def CreateAssertChangeVis(name, udp_port):
    return f"COMMAND-CHANGEVIS-{name}-{udp_port}"

def CreateRequestClientListMessage():
    return f"REQ-CLIENT_LIST"

def CreateRequestClientInfoMessage(user):
    return f"REQ-CLIENT-{user}"

def CreateRequestPeerToPeerCommunication(name, our_port):
    return f"REQ-COMMUNICATION-{name}-{our_port}"

if __name__ == "__main__":
    app = DemoGUI()
    app.mainloop()