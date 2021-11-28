from tkinter import Frame
from api.listeners import ProgressListener, RealVideoNameFoundListener

from gui.video_input import VideoInput


class VideoList(Frame, ProgressListener, RealVideoNameFoundListener):

    def __init__(self, parent):
        super().__init__(parent)

        self.name_to_video_input: dict(str, VideoInput) = {}
        self.real_name_to_video_input: dict(str, VideoInput) = {}

        self.add_video_input()

    def add_video_input(self, name="Example video"):
        video_input = VideoInput(self, name)
        video_input.pack()

    def on_progress_change(self, name, value):
        self.real_name_to_video_input[name].set_progress(value)

    def on_real_video_name_found(self, user_typed_name, real_video_name):
        self.real_name_to_video_input[real_video_name] = self.name_to_video_input[user_typed_name]

    def set_and_get_names(self):
        video_inputs = self.pack_slaves()
        for video_input in video_inputs:
            self.name_to_video_input[video_input.get_name()] = video_input
        return self.name_to_video_input.keys()
