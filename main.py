from TwitterUser import TwitterUser
import requests
import json
from colorama import Fore, Back, Style

def login(self, name, surname):
    url=f"http://localhost:8082/consumers/{surname}"

    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    payload = {
      "name": f"{name}",
      "format": "binary",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    json_data = json.loads(r.text)
    if 'error_code' in json_data:
        if json_data['error_code'] == 40902:
            print(f'Welcome back, {name}!')
    else:
        print(f"We're creating your KafkaTwitter account, {name}!")
    return TwitterUser(name, surname)

from tkinter import *
from tkinter import font as tkfont
from LoginPage import LoginPage
from HomePage import HomePage

class MainView(Tk):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, HomePage, StartPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# LOGIN PAGE
class LoginPage(Frame):
    def __init__(self, parent, controller):
         super().__init__(parent)
         self.controller = controller
         # set label
         label = Label(self, text="This is the Login page!", font=controller.title_font)
         label.pack(side="top", fill="x", pady=10)
         # entry boxes
         self.name_box = Entry(self,width=20)
         self.name_box.pack()
         self.surname_box = Entry(self,width=20)
         self.surname_box.pack()
         submit_btn = Button(self, text="Login", command=self._submit, height="2", width="30").pack()

    def _submit(self):
        #self.login(self.name_box.get(), self.surname_box.get())
        print(self.name_box.get())
        print(self.surname_box.get())
        self.controller.show_frame("HomePage")

# HOME PAGE
class HomePage(Frame):
    def __init__(self, parent, controller):
         super().__init__(parent)
         self.controller = controller
         self.label = Label(self, text='HOMEPAGE!').pack()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("LoginPage"))
        button2 = Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("HomePage"))
        button1.pack()
        button2.pack()

if __name__ == '__main__':
    from KafkaTwitter import KafkaTwitter
    app = KafkaTwitter()
    app.mainloop()
    
