from typing import List
import requests
import re
import sys
import threading
from requests.models import HTTPError
from .listeners import ProgressListener

from .progress_handler import ProgressHandler


def find_nth(string, seq, n):
    """Find the nth occurence in the string.

    Args:
        string (string): target string.
        seq (str): patternt to find.
        n (int): n-1 occurences will be skipped.

    Returns:
        (int): index of the nth occurence.
    """

    start = string.find(seq)
    while start >= 0 and n > 1:
        start = string.find(seq, start+len(seq))
        n -= 1
    return start


def find_str_between(string, char):
    """Finds the substring between sequences.

    Args:
        string (str): target string.
        char (str): bounding sequences.

    Returns:
        (str): substring.
    """

    i1 = find_nth(string, char, 1)
    i2 = find_nth(string, char, 2)
    return string[i1+1:i2]


class Downloader:

    def __init__(self, youtube_api_key):
        self.progress_listeners: List[ProgressListener] = []
        self.api_key = youtube_api_key

    def download(self, url, filesize):
        """Downloads and writes the file from url.

        Args:
            url (str): url of the file.
            filesize (int): filesize in MBs, used for progress calculation.
        """

        res = requests.get(url, stream=True)
        totalbytes = 0
        last_percentage = 0
        filename = find_str_between(res.headers["Content-Disposition"], "\"")
        print(f"Download of {filename} started.")
        with open(f"{filename}", "wb") as f:
            for chunk in res.iter_content(1000*1000):
                if chunk:
                    totalbytes += len(chunk)
                    percentage = round((totalbytes/(1000*1000)/filesize)*100)

                    if percentage != last_percentage:
                        last_percentage = percentage
                        self.notify_progress_listeners(
                            filename, last_percentage)

                    f.write(chunk)

    def extract_url_and_mbs(self, video_id, video_name):
        """Extracts the file url for downloading from a youtube video id.

        Uses yt-download api.

        Args:
            video_id (str): youtube video id.
            video_name (str): name of the video, used only for printing.

        Returns:
            (str, int): url and filesize in megabytes.
        """

        convert_html = requests.get(
            f"https://www.yt-download.org/api/button/mp3/{video_id}").text

        url = ""
        mbs = 0
        for line in convert_html.split("\n"):
            if f"<a href=\"https://www.yt-download.org/download/{video_id}/mp3/320" in line:
                url = find_str_between(line, "\"")
                print(f"{video_name} converted.")
                continue
            if "MB" in line:
                mbs = re.findall("\d+\.\d+", line)
                return (url, mbs)
        return None, None

    def query_to_video_id(self, q):
        """Gets the video id from a youtube query.

        Uses youtube data api.

        Args:
            q (str): youtube query, eg. name of a song.

        Returns:
            (str): youtube video id.
        """

        res = requests.get("https://www.googleapis.com/youtube/v3/search", params={
            "key": self.api_key,
            "q": q
        })

        try:
            res.raise_for_status()
        except HTTPError as e:
            print(res.json())
            return None

        res_json = res.json()
        if len(res_json["items"]) == 0:
            return None
        else:
            return res_json["items"][0]["id"]["videoId"]

    def process_video_name(self, video_name):
        """Take a youtube query and download a .mp3 file of a first result.

        Args:
            video_name (str): youtube query.
        """

        video_id = self.query_to_video_id(video_name)
        if not video_id:
            print(f"Could not find a video {video_name}.")
            return
        print(f"Video ID: {video_id} found for {video_name}.")
        url, mbs = self.extract_url_and_mbs(video_id, video_name)
        if not url:
            print(f"Could not extract a download url from {video_name}")
            return
        self.download(url, float(mbs[0])*1.046)

    def attach_progress_listener(self, progress_listener: ProgressListener):
        self.progress_listeners.append(progress_listener)

    def notify_progress_listeners(self, name, value):
        for progress_listener in self.progress_listeners:
            progress_listener.on_progress_change(name, value)
