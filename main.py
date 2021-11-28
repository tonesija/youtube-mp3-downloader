import requests
import re
import sys
import threading
import os
from os.path import join, dirname
from dotenv import load_dotenv
from requests.models import HTTPError

from progress_handler import ProgressHandler

dotenv_path = join(dirname(__file__), '.env.development')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("YOUTUBE_API_KEY")


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def find_str_between(string, char):
    i1 = find_nth(string, char, 1)
    i2 = find_nth(string, char, 2)
    return string[i1+1:i2]


def download(url, filesize, progress_handler: ProgressHandler):
    res = requests.get(url, stream=True)
    totalbytes = 0
    filename = find_str_between(res.headers["Content-Disposition"], "\"")
    with open(f"{filename}", "wb") as f:
        for chunk in res.iter_content(1000*1000):
            if chunk:
                totalbytes += len(chunk)
                percentage = round((totalbytes/(1000*1000)/filesize)*100)

                progress_handler.update_progress(filename, percentage)

                f.write(chunk)


def extract_url_and_mbs(video_id):
    convert_html = requests.get(
        f"https://www.yt-download.org/api/button/mp3/{video_id}").text
    print("Video converted, loaded the html for download")

    url = ""
    mbs = 0
    for line in convert_html.split("\n"):
        if f"<a href=\"https://www.yt-download.org/download/{video_id}/mp3/320" in line:
            url = find_str_between(line, "\"")
            print("Extracted the download url:", url)
            continue
        if "MB" in line:
            mbs = re.findall("\d+\.\d+", line)
            return url, mbs


def query_to_video_id(q):
    res = requests.get("https://www.googleapis.com/youtube/v3/search", params={
        "key": API_KEY,
        "q": q
    })

    try:
        res.raise_for_status()
    except HTTPError as e:
        print(e)
        return None

    res_json = res.json()
    if len(res_json["items"]) == 0:
        return None
    else:
        return res_json["items"][0]["id"]["videoId"]


def process_video_name(video_name, progress_handler: ProgressHandler):
    video_id = query_to_video_id(video_name)
    if not video_id:
        print(f"Could not find a video {video_name}.")
        return
    url, mbs = extract_url_and_mbs(video_id)
    download(url, float(mbs[0])*1.046, progress_handler)


video_names = sys.argv[1:]

progress_handler = ProgressHandler()
tasks = []
for video_name in video_names:
    task = threading.Thread(target=process_video_name,
                            args=(video_name, progress_handler))
    tasks.append(task)

for task in tasks:
    task.start()

for task in tasks:
    task.join()
