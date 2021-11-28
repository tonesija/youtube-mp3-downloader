from tkinter import Entry, Frame, StringVar
from tkinter.ttk import Progressbar
from tkinter.constants import END, HORIZONTAL, LEFT, RIGHT


class VideoInput(Frame):

    def __init__(self, parent, name: str = "Example video"):

        super().__init__(parent)

        self.name = StringVar()
        self.entry = Entry(self, textvariable=self.name)
        #self.entry.delete(0, END)
        #self.entry.insert(0, name)

        self.progress = Progressbar(
            self, orient=HORIZONTAL, length=100)

        self.entry.pack(side=LEFT)
        self.progress.pack(side=RIGHT)

    def set_progress(self, val):
        self.progress["value"] = val

    def get_name(self):
        return self.name.get()
