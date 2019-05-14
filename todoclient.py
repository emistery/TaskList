import socket
from tkinter import *
from tkinter import simpledialog


class ClientGui:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Connect", command=self.connect)
        self.greet_button.pack()

        self.greet_button = Button(master, text="Send", command=self.send)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.s = socket.socket()

    def connect(self):
        print("Greetings!")
        port = 3125
        ip_address = simpledialog.askstring("input string", "Choose IP")
        self.s.connect((ip_address, port))


    def send(self):
        z = simpledialog.askstring("input string", "What do you want to do?")
        self.s.sendall(z.encode())
        self.s.close()

root = Tk()
my_gui = ClientGui(root)
root.mainloop()

