from tkinter import Button, Frame
from tkinter.constants import LEFT, RIGHT


class CommandBoard(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.add_btn = Button(self, text="Add")
        self.submit_btn = Button(self, text="Submit")

        self.add_btn.pack(side=LEFT)
        self.submit_btn.pack(side=RIGHT)

    def add_command_to_add_btn(self, handler):
        self.add_btn.config(command=handler)

    def add_command_to_submit_btn(self, handler):
        self.submit_btn.config(command=handler)
