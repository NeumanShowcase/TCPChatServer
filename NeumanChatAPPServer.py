# -*- coding: iso8859 -*-
import socket
import select
"""Create TCP server on port 80."""

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1337

connectionsOnServer = []
nameMsg = {}
nameClient = {}
outputs = []
sendbuffer_queue = []
clientID = ""
print("Server listen on: ", HOST, ":", PORT)
mainserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainserverSocket.bind((HOST, PORT))
mainserverSocket.listen(10)
mainserverSocket.setblocking(0)
connectionsOnServer.append(mainserverSocket)
madeChangeName = False
while connectionsOnServer:
    readable, writable, exceptional = select.select(
                                                    connectionsOnServer,
                                                    outputs,
                                                    connectionsOnServer
                                                    )
    for socket in readable:
        if socket is mainserverSocket:

            conn, addr = mainserverSocket.accept()
            clientID = str(addr[0]) + ":" + str(addr[1])
            nameClient[clientID] = clientID
            newClientMsg = "Client known as:" + clientID + " connected!\n"
            print(newClientMsg)
            connectionsOnServer.append(conn)
            welcomeMsg = "Welcome to chatserver " + clientID + "!\n"
            conn.sendall(bytearray(welcomeMsg, "utf-8"))
            sendbuffer_queue.append(newClientMsg)
            outputs.append(conn)

        else:
            madeChangeName = False
            msgFromClient = socket.recv(1024).decode("utf-8")

            print(nameClient.get(clientID))

            if msgFromClient:
                retrieveID = socket.getpeername()
                clientID = str(retrieveID[0]) + ":" + str(retrieveID[1])

                if "NAMECHANGEME:" in msgFromClient and len(msgFromClient) > 14:
                        clientNewName = msgFromClient[13:].rstrip()
                        formerName = nameClient.get(clientID)
                        msgFromClient = "Client " + formerName + " now known as: " + clientNewName
                        nameClient[clientID] = clientNewName
                        madeChangeName = True

                elif "GETUSERLIST:" in msgFromClient:
                        connectedUsers = list(nameClient.values())
                        userListBarr = bytearray("Connected user list:" + str(connectedUsers), "UTF-8")
                        socket.sendall(userListBarr)
                sendbuffer_queue.append(msgFromClient)

                print("Got msg from ", nameClient.get(clientID), "at: ", clientID)

                if not madeChangeName:
                    nameMsg[msgFromClient] = nameClient.get(clientID)
                # just for errorchecking
                if socket not in outputs:
                    print("adding socket to output list")
                    outputs.append(socket)
            else:
                connectionsOnServer.remove(socket)
                # remove name from list
                retrieveID = socket.getpeername()
                clientID = str(retrieveID[0]) + ":" + str(retrieveID[1])
                formerName = nameClient.get(clientID)
                print("Client known as ", formerName, " at ", clientID, "Just Disconnected!")
                del nameClient[clientID]
                if socket in writable:
                    print("must take away client from write")
                    writable.remove(socket)
                if socket in outputs:
                    print("must take away client from outputs")
                    outputs.remove(socket)
                socket.close()

    # dont end up here
    for e in exceptional:
        print("ERROR!")
        break

    while writable and sendbuffer_queue:
        sendNext = str(sendbuffer_queue.pop())
        # looking up ip of sent msg
        whoSent = nameMsg.get(sendNext)
        # Checking if ip has set username in table

        if whoSent:
            whoSent += " says: "
        elif not whoSent:
            whoSent = "Server says: "
        print(whoSent)
        msgOut = (whoSent + sendNext)
        print("sending: ", sendNext)
        for conn in writable:
                conn.sendall(bytearray(msgOut, "utf-8"))
