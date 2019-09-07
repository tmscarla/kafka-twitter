import tkinter as tk
from TwitterUserAvro import TwitterUser
import requests
import json
from PIL import ImageTk, Image

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        twitter_blue = '#%02x%02x%02x' % (255,255,255) #(68,162,242)
        tk.Frame.__init__(self,
                        parent,
                        background = twitter_blue
                        )
        self.pages = controller.get_frames() # prende le pagine
        self.controller = controller
        # user creation
        # it does the following:
        # the first time that the page is shown, it triggers a funciton that
        # gets the user's username
        self.twitter_user = None
        self.n_times_shown = 0 # we'll use this to trigger the creation of the User at start
        self.bind("<<ShowFrame>>", self._on_first_show_frame) # binda all'evento, serve per dire quando viene mostrata

    def _read(self):
        print(f"Ok {self.twitter_user.get_username()}, let's see what is going on in the World!")
        self.controller.show_frame("ReadPage")

    def _write(self):
        print(f'Ok {self.twitter_user.get_username()}, write something!')
        self.controller.show_frame("WritePage")

    def _streaming(self):
        print(f'Ok {self.twitter_user.get_username()}, streaming mode!')
        self.controller.show_frame("StreamingKSQL")

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.twitter_user = self.controller.get_twitter_user()

            # label
            label = tk.Label(self, text=f"What do you want to do, {self.twitter_user.get_username()}?", height='5',font=self.controller.title_font)
            label.pack(side="top", fill='both')

            # read mode button
            read_button = tk.Button(self, text="Read", command=self._read, height="2", width="30").pack(pady=5)
            # filtering options
            """
            city_label_read = tk.Label(self, text="City Filter:", font=self.controller.title_font).pack(side="top", fill="x", pady=5)
            self.city_box_read = tk.Entry(self,width=20)
            self.city_box_read.pack()
            """
            # streaming mode button
            streaming_button = tk.Button(self, text="Streaming", command=self._streaming, height="2", width="30").pack(pady=5)
            # filtering options
            """
            city_label_streaming = tk.Label(self, text="City Filter:", font=self.controller.title_font).pack(side="top", fill="x", pady=5)
            self.city_box_streaming = tk.Entry(self,width=20)
            self.city_box_streaming.pack()
            """
            # write mode button
            write_button = tk.Button(self, text="Write", command=self._write, height="2", width="30").pack(pady=5)


            # carica logo
            """
            img = Image.open("images/logo.jpg")
            w,h = img.size
            img_resized = img.resize((w//4,h//4), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(img_resized)
            panel = tk.Label(self, image = image, background='white')
            panel.photo = image
            panel.pack(side='bottom',fill='both')
            """

            self.n_times_shown =-1
