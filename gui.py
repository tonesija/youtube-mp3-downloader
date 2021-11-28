import tkinter as tk
import sys
import threading
import os
from os.path import join, dirname
from dotenv import load_dotenv

from gui.command_board import CommandBoard
from gui.video_list import VideoList

from api.downloader import Downloader


dotenv_path = join(dirname(__file__), '.env.development')
load_dotenv(dotenv_path)
API_KEY = os.environ.get("YOUTUBE_API_KEY")


def submit():
    task = threading.Thread(target=process)
    task.start()


def process():
    video_names = video_list.set_and_get_names()

    downloader = Downloader(API_KEY)
    downloader.attach_progress_listener(video_list)
    downloader.attach_real_video_name_found_listener(video_list)
    tasks = []
    # Create a thread for each of the queries (video names).
    for video_name in video_names:
        task = threading.Thread(target=downloader.process_video_name,
                                args=(video_name, ))
        tasks.append(task)

    # Strart the queries.
    for task in tasks:
        task.start()

    # Wait for the all to finish.
    for task in tasks:
        task.join()

    show_finished()


def show_finished():
    finished_lbl.pack()

    # ------- GUI -------
window = tk.Tk()
window.geometry("480x640")
window.title("Youtube MP3 Downloader")


greeting = tk.Label(window, text="Hello, Tkinter")
greeting.pack()

video_list = VideoList(window)
video_list.pack()

command_board = CommandBoard(window)
command_board.add_command_to_add_btn(video_list.add_video_input)
command_board.add_command_to_submit_btn(submit)
command_board.pack()

finished_lbl = tk.Label(window, text="Finished download.")


window.mainloop()
