import tkinter as tk
from tkinter import font  as tkfont

from HomePage import HomePage
from LoginPage import LoginPage

class KafkaTwitter(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # setup properties
        self.title_font = tkfont.Font(family='Helvetica', size=18)
        self.title('KafkaTwitter')
        self.geometry("500x500")
        self.resizable(0, 0)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, HomePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = KafkaTwitter()
    app.mainloop()
