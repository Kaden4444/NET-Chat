# GUI
import tkinter
import tkinter.messagebox
import customtkinter
from customtkinter import filedialog

# Networking
import socket
import threading
import time
import random
import queue

#general notes:
    # lamba allows you to pass parameters to functions that buttons will use, allowing you to configure a button when you click it (VERY USEFUL)

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), button_colour, "dark-blue"
background = "#232222"
frame_colour = "#b07289"
button_colour= "green"

main_server_port = 12000
port_we_listen_on = random.randrange(12001, 15000)

hostname = socket.gethostname()
our_ip = socket.gethostbyname(hostname)

# global messages_sent
# messages_sent=0

#global messages_sent_map
#messages_sent_map = {}

class DemoGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=background)
        global q
        q = queue.Queue()
        global other_client_address

        # configure window
        self.title("NET Chat")

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
        self.main_frame = customtkinter.CTkFrame(master=self, fg_color=frame_colour) 
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
        global disconnect_from_client_button
        self.disconnect_from_client = customtkinter.CTkButton(master=self.main_frame, text="Disconnect", fg_color="red", border_width=1, border_color="black",text_color="black", state="disabled", command=disconnect_client)
        self.disconnect_from_client.grid(row=0, padx=10, pady=10 , sticky='nse')
        disconnect_from_client_button = self.disconnect_from_client
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
        global send_button
        self.chat_button = customtkinter.CTkButton(master=self.main_frame, text="Send", fg_color=button_colour, border_width=1, border_color="black",text_color="black",command=send_message)
        self.chat_button.grid(row=3, sticky='ne', padx=(0,10), pady=(10,0))
        self.chat_button.configure(state="disabled")
        send_button = self.chat_button
        
        global file_button
        self.file_button = customtkinter.CTkButton(master=self.main_frame, text="Send a file", fg_color=button_colour, border_width=1, border_color="black",text_color="black",command=upload_file)
        self.file_button.grid(row=3, sticky='nw', padx=(10,0), pady=(10,0))
        self.file_button.configure(state="disabled")
        file_button = self.file_button
        

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
        global status_button
        self.set_status_button = customtkinter.CTkButton(master=self.clients_frame, text="Change Status", fg_color=button_colour, border_width=1, border_color="black",text_color="black")
        self.set_status_button.grid(row=0, padx=10, pady=10 , sticky='nw')
        self.set_status_button.configure(command= lambda:change_status_to_available(self.set_status_button,q), state="disabled")
        status_button = self.set_status_button
        
        # create textbox         
        self.textbox = customtkinter.CTkTextbox(self.clients_frame, fg_color="white", activate_scrollbars=True,text_color="black", border_color="black", border_width=1)
        self.textbox.insert("0.0", "Not connected to server\nPlease connect and click the refresh button")
        self.textbox.grid(row=0, column=0, rowspan=1, padx=10, pady=(50,0), sticky="nsew")
        # disable its input
        self.textbox.configure(state="disabled")

        # create the refresh button
        global refresh_button
        self.refresh_button = customtkinter.CTkButton(master=self.clients_frame, text="Refresh", fg_color=button_colour, border_width=1, border_color="black",text_color="black", state="disabled")
        self.refresh_button.grid(row=1, column=0,padx=(10,10),pady=10 , sticky='ne')
        self.refresh_button.configure(command=lambda: populate_client_list(self.textbox), state="disabled")
        refresh_button = self.refresh_button
  
        # create the client connect button 
        global client_connect_button
        self.client_connect_button = customtkinter.CTkButton(master=self.clients_frame, text="Connect to client", fg_color=button_colour,command=connect_to_client, border_width=1, border_color="black",text_color="black", state="disabled")
        self.client_connect_button.grid(row=1, column=0,padx=(10,10),pady=10 , sticky='nw')
        client_connect_button = self.client_connect_button
        
def enable_server_buttons():
    status_button.configure(state="normal")
    refresh_button.configure(state="normal")
    client_connect_button.configure(state="normal")

def disable_server_buttons():
    status_button.configure(state="disabled")
    refresh_button.configure(state="disabled")
    client_connect_button.configure(state="disabled")

def connect_to_server(button):
    name=""
    global our_name
    try: 
        dialog = customtkinter.CTkInputDialog(text="Enter your name", title="Connecting to server")
        name = dialog.get_input()
        our_name = name
        
        if our_name=="":
            errorbox = tkinter.messagebox.Message(master=None, message="Please enter a name", title = "Error")
            errorbox.show() 
            return
        
        #set it 
        #main_server_ip=""
        
        #enter Ip manually
        global main_server_ip
        server_ip_prompt = customtkinter.CTkInputDialog(text="Enter the server IP", title="Connect to a server")
        main_server_ip = server_ip_prompt.get_input()
        
        if main_server_ip=="":
            errorbox = tkinter.messagebox.Message(master=None, message="Please enter an IP", title = "Error")
            errorbox.show() 
            return

        send_TCP_message(CreateRequestConnectionMessage(name))
        enable_server_buttons()
        button.configure(text="Disconnect",fg_color="Red", command= lambda: disconnect_from_server(button))
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Server not found", title = "Error")
        errorbox.show()

def disconnect_from_server(button):
    try:
        send_TCP_message(CreateAssertUnavailableMessage(our_name, port_we_listen_on))
        button.configure(text="Connect to server", fg_color=button_colour , command= lambda:connect_to_server(button))
        disable_server_buttons()
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to disconnect", title = "Error")
        errorbox.show()

def send_TCP_message(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((main_server_ip, main_server_port))
    client.send(message.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    client.close()
    return response

def populate_client_list(textbox):
    try:
        response = send_TCP_message(CreateRequestClientListMessage()).split("-")[2]
        
        if response == "":
            textbox.configure(state="normal")
            textbox.delete(0.0, 'end')
            textbox.insert("0.0","No clients available currently")
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.delete(0.0, 'end')
            new = response.split(" ")
            new = "\n".join(new)  #this took forever to figure out 
            textbox.insert("0.0",f"Available clients:\n{new}")

            
            textbox.configure(state="disabled")
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to receive clients.", title = "Error")
        errorbox.show()

def change_status_to_available(button,q):
    try:
        send_TCP_message(CreateAssertAvailableMessage(our_name,port_we_listen_on))
        global UDPSocket 
        UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ('',port_we_listen_on)
        UDPSocket.bind(address)
        global waiterthread
        waiterthread = threading.Thread(target=lambda: request_waiter(q))
        waiterthread.start()
        button.configure(fg_color="red", text="Change Status", command=lambda: change_status_to_connected(button))
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to change status", title = "Error")
        errorbox.show()

def change_status_to_connected(button):
    try:
        send_TCP_message(CreateAssertChangeVis(our_name,port_we_listen_on))
        button.configure(fg_color=button_colour, text="Change Status", command=lambda: change_status_to_available(button))
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to change status", title = "Error")
        errorbox.show()   
    
def connect_to_client():
    try:
        dialog = customtkinter.CTkInputDialog(text="Please enter a client's name to chat to them", title="Connecting to another client")
        client_name = dialog.get_input()
        if client_name == "":
            errorbox = tkinter.messagebox.Message(master=None, message="No name entered", title = "Error")
            errorbox.show() 
            return
        other_client_details = send_TCP_message(CreateRequestClientInfoMessage(client_name)).split("-")
        other_client_ip_and_port = other_client_details[2]
        other_ip = other_client_ip_and_port.split(" ")[0]
        other_port = (int)(other_client_ip_and_port.split(" ")[1])

        print(f"Sending to {client_name} {other_ip} {other_port}")
        
        UDPSocket.sendto(CreateRequestPeerToPeerCommunication(our_name, our_ip , port_we_listen_on).encode(),(other_ip, other_port)) # Only sends, then is finished
    except:
        errorbox = tkinter.messagebox.Message(master=None, message="Failed to connect to a client - please check that they are available and their username is spelt correctly", title = "Error")
        errorbox.show() 

def enable_client_buttons():
    send_button.configure(state="normal")
    disconnect_from_client_button.configure(state="normal") 
    file_button.configure(state="normal")
    

def disable_client_buttons():
    send_button.configure(state="disabled")
    disconnect_from_client_button.configure(state="disabled")
    file_button.configure(state="disabled")

# wait for request
# idea is that this is created on a seperate thread, it spins and waits for a message
def request_waiter(q): # this port is (port we listen on - whoever is running this thread will recieve messages on the port that is randomly made)
        print(f"Listener socket for {our_name} ")
        connectedToPeer = False
        peer_address=""
        peer_ip=""
        message=""
        
        while True:
            if not connectedToPeer: # While this thread is alive 
                message, peer_address = UDPSocket.recvfrom(2024)   # receive messages from anyone 
                peer_ip = peer_address[0]
                message = message.decode()
                
                if message[0:17] == "REQ-COMMUNICATION":
                        accepted_peer = peer_address[0]
                        accepted_peer_name = message.split("-")[2]
                        
                        msg_box = tkinter.messagebox.askquestion('Incoming request', f'{accepted_peer_name} has requested to speak to you, do you accept?', icon='question')
                        if msg_box == 'yes':
                            UDPSocket.sendto(f"OKAY-{our_name}".encode(), peer_address)
                            q.put(peer_address)
                            label.configure(text=f"Chatting to {accepted_peer_name} ")
                            enable_client_buttons()
                            disable_server_buttons()
                            connectedToPeer = True
                            send_TCP_message(CreateBusyChatMessage(our_name))
                        else:
                            return
                        
                if message[0:5] == "OKAY-":  # the other receiver must also know
                    accepted_peer = peer_address[0]
                    accepted_peer_name = message.split("-")[1]  #this is not getting back to the main thread
                    q.put(peer_address)
                    print(f"OKAY FROM {accepted_peer_name}")
                    label.configure(text=f"Chatting to {accepted_peer_name} ")
                    
                    send_TCP_message(CreateBusyChatMessage(our_name))
                    enable_client_buttons()
                    disable_server_buttons()
                    connectedToPeer=True
                    
                
            while connectedToPeer:
                message, peer_address = UDPSocket.recvfrom(4096)
                peer_ip = peer_address[0]
                message = message.decode() 
                if peer_ip == accepted_peer:

                
                
                    if message=="END-CHAT":
                        chat_box.delete("0.0", "end")
                        entry_box.delete("0.0", "end")
                        UDPSocket.sendto(f"END-CHAT".encode(), peer_address)
                        label.configure(text=f"Connect to a client to chat:")
                        connectedToPeer=False
                        send_TCP_message(CreateAssertAvailableMessage(our_name, port_we_listen_on))
                        disconnect_from_client_button.configure(state="disabled")
                        send_button.configure(state="disabled")
                        enable_server_buttons()
                        disable_client_buttons()
                        continue
                                             
                    if message == "CONTROL-RETRANS":
                        errorbox = tkinter.messagebox.Message(master=None, message="Your last message failed to arrive, please resend it", title = "Message not sent")
                        errorbox.show()
                        continue
                    
                    if message[0:4] == "FILE":
                        peer_name = message.split("-")[1]
                        filename = message.split("-")[2]
                        filesize = message.split("-")[3]
                        file_contents = message.split("-")[4]
                        
                        msg_box = tkinter.messagebox.askquestion('Incoming file', f'{accepted_peer_name} has sent you a file called: {filename} Would you like to download it?', icon='question')
                        if msg_box == 'yes':
                                
                            f = open(filename, "w")
                            f.write(file_contents)
                            
                            filebox = tkinter.messagebox.Message(master=None, message="File Downloaded", title = "File")
                            filebox.show()
                            f.close()
                                            
                    elif message[0:4] == "DATA":
                        messagesize = int(message.split("-")[1])
                        message=message.split("-")[2]

                        if len(message) != messagesize:
                            UDPSocket.sendto("CONTROL-RETRANS".encode(),(peer_address))
                            continue
                        
                        current = chat_box.get("0.0", "end")
                        chat_box.delete("0.0", "end")
                        current_time = time.strftime('%H:%M')
                        chat_box.insert("0.0",f"{current}Peer: {message}      [{current_time}]\n")
                        chat_box.yview(tkinter.END)
                continue

def send_message():
        user_input = entry_box.get("0.0", "end")
        entry_box.delete("0.0", "end")
        
        if not q.empty():
            other_client_address = q.get()
            q.put(other_client_address)
            message = CreateMessage(user_input)
            UDPSocket.sendto(message.encode(), other_client_address)
            current = chat_box.get("0.0", "end")
            chat_box.delete("0.0", "end")
            current_time = time.strftime('%H:%M')
            chat_box.insert("0.0",f"{current}You: {user_input}      [{current_time}]\n")
            chat_box.yview(tkinter.END)
            #messages_sent += 1
        else:
                print("Send failed")

def CreateMessage(message):
    size = len(message)
    return f"DATA-{size}-{message}"

def disconnect_client():
    entry_box.delete("0.0", "end")
        
    if not q.empty():
        other_client_address = q.get()
        q.put(other_client_address)
        message = "END-CHAT"
        UDPSocket.sendto(message.encode(), other_client_address)
        
    label.configure(text=f"Connect to a client to chat:")
    send_TCP_message(CreateAssertAvailableMessage(our_name, port_we_listen_on))
    disable_client_buttons()
    enable_server_buttons()

def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("Image Files", ".png .jpg")])
    if filename is not None:
        f = open(filename, "r")
        file_contents = f.read()
        print("File Contents:\n" + file_contents)
        other_client_address = q.get()
        q.put(other_client_address)
        f.close()
    else:
        errorbox = tkinter.messagebox.Message(master=None, message="Unable to get file", title = "File Error")
        errorbox.show()

    filename = filename.split("/").pop() 
    message = CreateFilePackageForClient(our_name,filename,0,file_contents)
    UDPSocket.sendto(message.encode(), other_client_address)
    print(f"File being sent: {filename}")


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

def CreateRequestPeerToPeerCommunication(name, our_ip ,our_port):
    return f"REQ-COMMUNICATION-{name}-{our_ip}-{our_port}"

def CreateBusyChatMessage(client_id):
    return f"COMMAND-BUSYCHAT-{client_id}"

def CreateFilePackageForClient(our_name,filename, filesize, filecontents):
    return f"FILE-{our_name}-{filename}-{filesize}-{filecontents}"

if __name__ == "__main__":
    app = DemoGUI()
    app.mainloop()