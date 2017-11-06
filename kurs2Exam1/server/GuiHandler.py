import tkinter
import tkinter.messagebox

class GuiHandler:
    def __init__(self,socketHandler_):
        self.socketHandler = socketHandler_

    def getPort(self):
        rootToGetPort = tkinter.Tk()
        lab = tkinter.Label(rootToGetPort,text="port")
        lab.grid(row = 0, column = 0)
        entOfPort = tkinter.Entry(rootToGetPort)
        entOfPort.grid(row = 0, column = 1)

        self.portToReturn = ""
        def confirmPort():
            self.portToReturn = entOfPort.get()
            rootToGetPort.destroy()
        but = tkinter.Button(rootToGetPort,text="set port",command = confirmPort)
        but.grid(row = 1, column = 0)
        rootToGetPort.mainloop()
        return self.portToReturn

    def startMainGui(self):
        self.root = tkinter.Tk()

        scroll = tkinter.Scrollbar(self.root)
        scroll.grid(row = 0, column = 1, sticky=tkinter.N+tkinter.S)
        self.chattContents = tkinter.Text(self.root, yscrollcommand  = scroll.set)
        self.chattContents.grid(row = 0,column = 0)
        scroll.config(command=self.chattContents.yview)
        self.entryOfUser = tkinter.Entry(self.root)
        self.entryOfUser.grid(row = 1,column = 0)
        self.buttonToTrigg = tkinter.Button(self.root, text = "enter", command = self.sendMsgBySocketHandler)
        self.buttonToTrigg.grid(row = 1,column = 1)
        self.buttonToTrigg = tkinter.Button(self.root, text = "close", command = self.closeConnection)
        self.buttonToTrigg.grid(row = 2,column = 0)
        self.root.mainloop()

    def sendMsgBySocketHandler(self):
        self.socketHandler.sendAndShowMsg("Admin: " + self.entryOfUser.get())

    def closeConnection(self):
        self.socketHandler.closeEveryThing()

    def startGui(self):
        self.startMainGui()

    def showMessage(self,text):
        self.chattContents.insert(tkinter.END,text+"\n")

    def showWarningMsg(self):
        tkinter.messagebox.showwarning(message="could not bind port")