def send_message(entry, textbox):
        # This is the function running in the main thread
        
        user_input = entry.get("0.0", "end")
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.sendto(user_input.encode(),(other_client_ip, other_client_port))
        clientSocket.close()

        # Add locally but must also send it forward
        if user_input:
            current = textbox.get
            textbox.delete()
            textbox.insert(f"{current}You: {user_input}\n")
            
def recieve_message(textbox):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #serverSocket.bind(('127.0.0.1', port_we_listen_on))

        while True:
            # Receive the message from the client conversing with
            message, clientAddress = serverSocket.recvfrom(2048)
            print(message, clientAddress)
            if clientAddress[0] == client_connected_ip:
                # The message comes from the guy connected to us Display the message
                current_time = time.strftime('%H:%M')  
                the_chat.insert(f"{client_connected_name}: {message.decode()}      [{current_time}]\n\n")