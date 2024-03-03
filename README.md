# NET-Chat

### Kaden Carey

This is a client-server and client-client communication application.

- ## Connecting to the server

  When a server is running, the clients will be expected to know the IP of the server, at which point, they will select "connect to server" and enter their name and server IP.

- ## Changing availablity.

  A client has 3 states, connected, available and chatting. When they select "change status", they will become available on the server and visible to other clients. When they are speaking to a client, their status becomes chatting.

- ## Connecting to a client
  Simply select "connect to a client", enter their name, spelt exactly as seen in the list.
  A request will be sent to the other client, and should they accept, the users will be connected, being able to talk to each other in the chat room.
- ## Networking Details:
  Client communicate to the server through TCP, a server stores the client's IPs and Port #s. When a client requests to speak to another client, the server provides them with said client's details
  from this point onwards, the two clients are connected through UDP without the servers interference.
- ## File sending
  Currently only textfiles are supported. A request will be sent to the client, and upon acceptance, the app will download the file into the clients folder

## Other Notes

    The GUI used for this application is an extension to Tkinter called customTkinter. I learnt to use this within two days, to some decent affect.
