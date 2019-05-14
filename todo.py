import socket
import datetime
import os
from tkinter import *
from tkinter import simpledialog
import configparser
from functools import partial
from peewee import SqliteDatabase, Model, CharField, DateTimeField, BooleanField
import _thread as thread


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 3125
ip_address = config.get("serversettings", "ipaddress")
s.bind((ip_address, port))
print ('Socket binded to port 3125')
s.listen(3)
print ('socket is listening')

config = configparser.ConfigParser()

if os.name == 'nt':
    configFilePath = 'settings.ini'
else:
    configFilePath = '/home/pi/TaskList/settings.ini'

config.read(configFilePath)

# if linux, change to own folder
if os.name == 'nt':
    db = SqliteDatabase('tasklist.db')
else:
    db = SqliteDatabase('/home/pi/TaskList/tasklist.db')

labeldict = {}
buttondict = {}


def st_server():
    """Start server"""
    while True:
        c, addr = s.accept()
        print('Got connection from ', addr)
        #print(c.recv(1024))
        newtask = c.recv(1024)
        print(newtask)
        insert_task(newtask)
        s.close

def insert_task(taskname):
    newtask = Task(task=taskname)
    newtask.save()


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.show_items()
        self.show_buttons()
        # self.create_test()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

    def start_server(self):
        thread.start_new_thread(st_server, ())

    def show_items(self):
        i = 0
        if os.name == 'nt':
            photo = PhotoImage(file="trash.png")
        else:
            photo = PhotoImage(file="/home/pi/TaskList/trash.png")
        for task in Task.select():
            labeldict["nummer" + str(i)] = Label(self, text=str(task.task), highlightbackground="black", bd=1,
                                                 relief=GROOVE, width=40)
            labeldict["nummer" + str(i)].grid(row=i, column=0, sticky=W)
            buttondict["nummer" + str(i)] = Button(self, text="del " + str(i + 1), command=partial(self.delete_item, i),
                                                   image=photo)
            buttondict["nummer" + str(i)].image = photo
            buttondict["nummer" + str(i)].grid(row=i, column=1)
            print(i)
            i = i + 1

    def show_buttons(self):
        # Button(self, text="Refresh", command=self.show_items).grid(row=0, column=2, sticky=E)
        Button(self, text="Refresh", command=self.force_refresh).grid(row=0, column=2, sticky=E)
        Button(self, text="Resize", command=self.resize_window).grid(row=1, column=2, sticky=E)
        Button(self, text="Choose IP", command=self.change_ip).grid(row=2, column=2, sticky=E)
        self.start_server()
        # self.start["text"] = "Startserver"
        # self.start["fg"] = "green"
        # self.start["command"] = self.start_server

        # self.start.grid(row=2, column=2, sticky=E)

    def change_ip(self):
        newip = simpledialog.askstring("input string", "choose IP Address")
        if newip is None:
            config.set('serversettings', 'ipaddress', str("127.0.0.1"))
            with open(configFilePath, 'w') as configfile:
                config.write(configfile)
        else:
            config.set('serversettings', 'ipaddress', str(newip))
            print(config.get('serversettings', 'ipaddress'))
            with open(configFilePath, 'w') as configfile:
                config.write(configfile)

    def resize_window(self):
        if root.attributes("-fullscreen"):
            root.attributes("-fullscreen", False)
        else:
            root.attributes("-fullscreen", True)

    def force_refresh(self):
        self.destroy()
        create_app()

    def delete_item(self, number):
        try:
            print(number)
            print(labeldict["nummer" + str(number)].cget('text'))
            query = Task.delete().where(Task.task == labeldict["nummer" + str(number)].cget('text'))
            query.execute()
            labeldict["nummer" + str(number)].grid_forget()
            buttondict["nummer" + str(number)].grid_forget()
            del labeldict["nummer" + str(number)]
            del buttondict["nummer" + str(number)]
            self.force_refesh()
        except KeyError:
            self.force_refesh()

    def create_test(self):
        Button(self, text="create new", command=create_new).grid(row=1, column=2, sticky=E)


def create_new():
    newtask1 = Task(task="eten")
    newtask1.save()
    newtask2 = Task(task="lopen")
    newtask2.save()
    newtask3 = Task(task="fietsen")
    newtask3.save()
    newtask3 = Task(task="koken")
    newtask3.save()
    newtask3 = Task(task="schoonmaken")
    newtask3.save()
    newtask3 = Task(task="wassen")
    newtask3.save()
    newtask3 = Task(task="bellen")
    newtask3.save()
    newtask3 = Task(task="rennen")
    newtask3.save()


class Task(Model):
    task = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    done = BooleanField(default=False)

    class Meta:
        database = db


db.connect()
db.create_tables([Task], safe=True)

for task in Task.select():
    print(task.task)


# change to own IP address
# print(config.get('DEFAULT', 'database'))


root = Tk()
root.geometry("480x320")
# root.overrideredirect(1) #Remove border
root.attributes("-fullscreen", True)


def create_app():
    app = Window(root)

    app.columnconfigure(0, weight=3)
    app.columnconfigure(1, weight=1)
    app.columnconfigure(2, weight=1)


create_app()

root.mainloop()