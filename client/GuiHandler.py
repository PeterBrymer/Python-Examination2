import tkinter
import tkinter.messagebox

class GuiHandler:
    def __init__(self,socketHandler_):
        self.socketHandler = socketHandler_

    def getIpAndPort(self):
        rootToGetIpAndPort = tkinter.Tk()
        lab1 = tkinter.Label(rootToGetIpAndPort,text="ip")
        lab1.grid(row = 0, column = 0)
        lab2 = tkinter.Label(rootToGetIpAndPort,text="port")
        lab2.grid(row = 1, column = 0)

        entOfIp = tkinter.Entry(rootToGetIpAndPort)
        entOfIp.grid(row = 0, column = 1)
        entOfPort = tkinter.Entry(rootToGetIpAndPort)
        entOfPort.grid(row = 1, column = 1)

        self.ipAndPortToReturn = "",""

        def confirmPortAndIpd():
            ip = entOfIp.get()
            port = entOfPort.get()
            self.ipAndPortToReturn = ip,port
            rootToGetIpAndPort.destroy()

        but = tkinter.Button(rootToGetIpAndPort,text="set ip and port",command = confirmPortAndIpd)
        but.grid(row = 2, column = 0)
        rootToGetIpAndPort.mainloop()

        return self.ipAndPortToReturn

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

        self.root.mainloop()

    def sendMsgBySocketHandler(self):
        self.socketHandler.sendMsg(self.entryOfUser.get())

    def startIntroGui(self):
        self.choiceRoot = tkinter.Tk()
        but1 = tkinter.Button(self.choiceRoot, text ="log in", command = self.funcToLogin)
        but1.pack()
        but1 = tkinter.Button(self.choiceRoot, text ="register", command = self.funcToRegister)
        but1.pack()
        self.choiceRoot.mainloop()

    def funcToLogin(self):
        self.loginChild = tkinter.Toplevel(self.choiceRoot)
        lab1 = tkinter.Label(self.loginChild,text = "username")
        lab1.grid(row = 0, column = 0)
        lab2 = tkinter.Label(self.loginChild, text="password")
        lab2.grid(row=1, column=0)

        entryOfUsername = tkinter.Entry(self.loginChild)
        entryOfUsername.grid(row=0, column=1)
        entryOfPassword = tkinter.Entry(self.loginChild)
        entryOfPassword.grid(row=1, column=1)

        def confirmLogin():
            username = entryOfUsername.get()
            password = entryOfPassword.get()
            self.socketHandler.sendMsg("login " + username + " " + password)
            self.loginChild.destroy()

        but = tkinter.Button(self.loginChild,text = "log in", command = confirmLogin)
        but.grid(row = 2, column = 0)

    def funcToRegister(self):
        self.registerChild = tkinter.Toplevel(self.choiceRoot)
        lab1 = tkinter.Label(self.registerChild,text = "username")
        lab1.grid(row = 0, column = 0)
        lab2 = tkinter.Label(self.registerChild, text="password")
        lab2.grid(row=1, column=0)
        lab3 = tkinter.Label(self.registerChild,text = "email")
        lab3.grid(row = 2, column = 0)
        lab4 = tkinter.Label(self.registerChild, text="name")
        lab4.grid(row=3, column=0)

        entryOfUsername = tkinter.Entry(self.registerChild)
        entryOfUsername.grid(row=0, column=1)
        entryOfPassword = tkinter.Entry(self.registerChild)
        entryOfPassword.grid(row=1, column=1)
        entryOfEmail = tkinter.Entry(self.registerChild)
        entryOfEmail.grid(row=2, column=1)
        entryOfName = tkinter.Entry(self.registerChild)
        entryOfName.grid(row=3, column=1)

        def confirmRegister():
            username = entryOfUsername.get()
            password = entryOfPassword.get()
            email = entryOfEmail.get()
            name = entryOfName.get()
            self.socketHandler.sendMsg("register " + username + " " + password + " " + email + " " + name)
            self.registerChild.destroy()

        but = tkinter.Button(self.registerChild,text = "register", command = confirmRegister)
        but.grid(row = 4, column = 0)

    def startGui(self):
        self.chattIsAllowed = False
        self.startIntroGui()
        if self.chattIsAllowed == True:
            self.startMainGui()

    def showMessage(self,text):
        if self.chattIsAllowed == False:
            if text == "ok":
                self.chattIsAllowed = True
                self.choiceRoot.destroy()
            elif text == "fine":
                tkinter.messagebox.showinfo(message="register is passed")
            elif text == "not ok":
                tkinter.messagebox.showinfo(message="log in failed")
            elif text == "not fine":
                tkinter.messagebox.showinfo(message="register is failed")
        else:
            self.chattContents.insert(tkinter.END,text+"\n")

    def showWarningMsg(self):
        tkinter.messagebox.showwarning(message="server is not found")