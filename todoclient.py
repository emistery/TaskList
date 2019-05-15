import socket
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from functools import partial


class ClientGui:
    def __init__(self, master):
        self.master = master
        master.title("Client GUI")

        self.connect_button = Button(master, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.send_button = Button(master, text="Send", command=self.send)

        self.s = socket.socket()

    def connect(self):
        print("Greetings!")
        port = 3125
        ip_address = simpledialog.askstring("input string", "Choose IP")
        self.s.connect((ip_address, port))
        #self.connect_button.destroy()
        self.send_button.pack()

    def send(self):
        z = simpledialog.askstring("input string", "What do you want to do?")
        self.s.sendall(z.encode())
        #self.s.close()
        #self.s.shutdown(socket.SHUT_WR)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.s.shutdown(socket.SHUT_WR)
            self.s.close()
            root.destroy()


root = Tk()
root.geometry("480x320")
my_gui = ClientGui(root)
root.protocol("WM_DELETE_WINDOW", partial(ClientGui.on_closing, my_gui))
root.mainloop()

