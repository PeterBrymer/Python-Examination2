import socket
import _thread
import sys
from Users import CollectionOfUsers

class SocketHandler:
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.users = CollectionOfUsers()
        self.users.readUsersFromFile()

    def closeEveryThing(self):
        self.serverSocket.close()
        self.users.writeUsersToFile()
        sys.exit(0)

    def startAccepting(self):
        while True:
            try:
                clientSocket, clientAddr = self.serverSocket.accept()
                self.list_of_unknown_clientSockets.append(clientSocket)
                self.list_of_unknown_clientAddr.append(clientAddr)
                self.startReceiverThread(clientSocket, clientAddr)

            except:
                pass

    def startToAcceptConnection(self,port):
        try:
            self.serverSocket.bind(('',int(port)))
        except:
            return "failed"
        self.serverSocket.listen(10)

        self.list_of_username = []
        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []

        _thread.start_new_thread(self.startAccepting,())
        return "succeed"

    def sendAndShowMsg(self,text):
        if text[0] == "#":
            text_complete = text[1:]
            for clientSock in self.list_of_known_clientSockets:
                clientSock.send(str.encode("Admin: "+text_complete))
            print("We send this message to the clients: "+text)
        elif text[:6] =="/close":
            print("Sever shutting down")
            self.closeEveryThing()
        elif text[:5] =="/kick":
            user = text[6:]
            for i in range (len(self.list_of_username)):
                if self.list_of_username[i] == user:
                    self.list_of_username.pop(i)
                    self.list_of_known_clientSockets[i].close()

                    break

    def startReceiverThread(self, clientSocket, clientAddr):
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))

    def startReceiving(self,clientSocket, clientAddr):
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin

            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)
            self.list_of_username.append(username)
            self.list_of_known_clientSockets.append(clientSocket)
            self.list_of_known_clientAddr.append(clientAddr)

            self.listenToknownClinet(clientSocket,clientAddr,username)

    def listenToUnknownClinet(self,clientSocket, clientAddr):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
            except:
                self.list_of_unknown_clientSockets.remove(clientSocket)
                self.list_of_unknown_clientAddr.remove(clientAddr)
                return False

            args = msg.split(' ')
            if len(args) == 3 and args[0] == "login":
                username = args[1]
                password = args[2]
                if self.users.doesThisUserExistAndNotActive(username,password):
                    clientSocket.send(str.encode("ok"))
                    self.sendAndShowMsg(username + " is connected")
                    return username
                else:
                    clientSocket.send(str.encode("not ok"))

            if len(args) >= 5 and args[0] == "register":
                username = args[1]
                password = args[2]
                email = args[3]
                name = ""
                for rest in args[4:]:
                    name += rest + " "
                if username != "" and password != "" and email != "" and name != "":
                    resultOfAdding = self.users.add_user(username,password,email,name)
                    if resultOfAdding == True:
                        clientSocket.send(str.encode("fine"))
                    else:
                        clientSocket.send(str.encode("not fine"))
                else:
                    clientSocket.send(str.encode("not fine"))

    def listenToknownClinet(self,clientSocket, clientAddr,username):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
                for clientSock in self.list_of_known_clientSockets:
                    clientSock.send(str.encode(username+": "+msg))
                print(username+": "+msg)
            except:
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg("#"+username+" disconnected")
                self.users.inactiveUser(username)
                return
