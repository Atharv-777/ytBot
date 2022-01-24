from pytube import YouTube
from moviepy.editor import *


def getVideo(url,start, end):
    yt = YouTube(url)
    # startAndEnd = "?start={}&end={}".format(start, end)
    # finalURL = yt.embed_url + startAndEnd
    # print(finalURL)
    # yt1 = YouTube(finalURL)
    stream = yt.streams.get_highest_resolution()
    fname = yt.title + '.mp4'
    stream.download(filename=fname)

    video = VideoFileClip(fname).subclip(start, end)
    video.write_videofile("edited.mp4")

getVideo("https://youtu.be/XsZZQPKLChY", 10, 30)