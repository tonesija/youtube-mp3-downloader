
import sys
import threading
import os
from os.path import join, dirname
from dotenv import load_dotenv
from requests.models import HTTPError
from api.downloader import Downloader
from api.listeners import ProgressListener

from api.progress_handler import ProgressHandler

dotenv_path = join(dirname(__file__), '.env.development')
load_dotenv(dotenv_path)
API_KEY = os.environ.get("YOUTUBE_API_KEY")


if __name__ == "__main__":
    # Get the video names from console arguements.
    video_names = sys.argv[1:]

    progress_handler = ProgressHandler()
    downloader = Downloader(API_KEY)
    downloader.attach_progress_listener(progress_handler)
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
    print("Finished.")
