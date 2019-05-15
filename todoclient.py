import socket
from tkinter import *
from tkinter import simpledialog


class ClientGui:
    def __init__(self, master):
        self.master = master
        master.title("Client GUI")

        self.connect_button = Button(master, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.send_button = Button(master, text="Send", command=self.send)
        self.send_button.pack()

        self.s = socket.socket()

    def connect(self):
        print("Greetings!")
        port = 3125
        ip_address = simpledialog.askstring("input string", "Choose IP")
        self.s.connect((ip_address, port))
        #self.connect_button.destroy()


    def send(self):
        z = simpledialog.askstring("input string", "What do you want to do?")
        self.s.sendall(z.encode())
        #self.s.close()
        #self.s.shutdown(socket.SHUT_WR)


root = Tk()
root.geometry("480x320")
my_gui = ClientGui(root)
root.mainloop()

