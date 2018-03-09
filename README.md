### Python TCPChatServer
## Simple chatserver written in Python using TCP sockets
 Server creates a host on the local ipv4 adress on the standard port of "1337"
 maximum no of connections is set to 10
 Available commands:
 </br>
  NAMECHANGEME:    <-- Written name after ':' is the new name of user. 
  </br>
  GETUSERLIST:     <-- Returns list of names of connected users only to requested socket.
  </br>
## Features:
  * Greets clients with welcome msg.
  * Sends information about new clients to all users.
  * Informs all clients of namechanges of user.
  * Some console debug information.
