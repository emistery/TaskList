#Emiel Kok © 2019
#gist at https://gist.github.com/emistery/dc9274936a187bad7a366373488af0db
import datetime
from peewee import *
from tkinter import *
from functools import partial
import _thread as thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

db = SqliteDatabase('tasklist.db')

labeldict = {}
buttondict = {}


def st_server():
    """Start server"""
    while True:
        httpd.handle_request()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>Hello!'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> Wat wil je toevoegen?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
                output += '</body></html>'
                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ''
            output += '<html><body>'
            output += '<h2> Dit heb je toegevoegd: </h2>'
            output += '<h1> %s </h1>' % messagecontent[0].decode("utf-8")
            print(messagecontent[0].decode("utf-8"))
            insert_task(messagecontent[0].decode("utf-8"))
            output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> Wat wil je toevoegen?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
            output += '</body></html>'
            self.wfile.write(output.encode())
            print(output)
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info())


def insert_task(taskname):
    newtask = Task(task=taskname)
    newtask.save()


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.start = Button(self)
        self.master = master
        self.init_window()
        self.show_items()
        self.show_buttons()
        self.create_test()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

    def start_server(self):
        thread.start_new_thread(st_server, ())
        self.start.config(state='disabled')

    def show_items(self):
        i = 0
        photo = PhotoImage(file="trash.png")
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
        Button(self, text="Refresh", command=self.show_items).grid(row=0, column=2, sticky=E)
        Button(self, text="Force refresh", command=self.force_refesh).grid(row=3, column=2, sticky=E)
        self.start["text"] = "Startserver"
        self.start["fg"] = "green"
        self.start["command"] = self.start_server

        self.start.grid(row=2, column=2, sticky=E)

    def force_refesh(self):
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

# newtask = Task(task="eten")
# newtask.save()

# uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
# uncle_bob.save() # bob is now stored in the database


PORT = 8080
# Handler = httpserver.SimpleHTTPRequestHandler
# httpd = socketserver.TCPServer(("", PORT), Handler)
httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
root = Tk()
root.geometry("480x320")


def create_app():
    app = Window(root)

    app.columnconfigure(0, weight=3)
    app.columnconfigure(1, weight=1)
    app.columnconfigure(2, weight=1)


create_app()

root.mainloop()
