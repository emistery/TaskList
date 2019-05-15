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
        self.connect_button.grid(row=0, column=0)

        #e1.grid(row=0, column=1)
        #e2.grid(row=1, column=1)

        self.send_button = Button(master, text="Send", command=self.send)

        self.label1 = Label(master, text="What do you want to do?")
        self.e1 = Entry(master)
        self.statuslabel = Label(master, text="")

        self.s = socket.socket()

    def connect(self):
        print("Greetings!")
        port = 3125
        ip_address = simpledialog.askstring("input string", "Choose IP")
        connectionstat = "Connected to \n" + ip_address
        self.statuslabel.configure(text=connectionstat)
        self.s.connect((ip_address, port))
        self.connect_button.destroy()
        self.statuslabel.grid(row=0, column=0)
        self.label1.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.send_button.grid(row=2, column=1)

    def send(self):
        x = self.e1.get()
        self.s.sendall(x.encode())

        self.e1.delete(0, END)


    def on_closing(self):
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.s.shutdown(socket.SHUT_WR)
                self.s.close()
                root.destroy()
        except OSError:
            root.destroy()


root = Tk()
root.geometry("480x320")
my_gui = ClientGui(root)
root.protocol("WM_DELETE_WINDOW", partial(ClientGui.on_closing, my_gui))
root.mainloop()

