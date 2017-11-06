from server.SocketHandler import SocketHandler
import time
socketHandler = SocketHandler()

port = input("Enter port: ")

resultOfBinding = socketHandler.startToAcceptConnection(port)

if resultOfBinding == "failed":
    print("Failed to start server")
else:
    print("hej")

time.sleep(999999)