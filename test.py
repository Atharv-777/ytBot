# from moviepy.editor import *
# clip = VideoFileClip("song.mp4")
# print(str(clip.w) + "x" + str(clip.h))
# clip2 = clip.resize(0.2)
# print(str(clip2.w) + "x" + str(clip2.h))
# clip2.write_videofile("test.mp4")


# input_file = 'hello.mp4'
# inpName = input_file.split('.')
# output_file = inpName[0] + '(compressed).' + inpName[1]
# print(output_file)

# import ffmpy
# from moviepy.editor import VideoFileClip
# import os
# def compress(input_file):
#     clip = VideoFileClip(input_file).resize(0.2)
#     clip.write_videofile("test.mp4")
#     inpName = input_file.split('.')
#     output_file = inpName[0] + '(compressed).' + inpName[1]
#     crf = 24
#     ff = ffmpy.FFmpeg(
#         inputs={'test.mp4':None},
#         outputs={output_file:'-vcodec libx264 -crf {}'.format(crf)}
#     )
#     ff.run()
#     print("Done!")
#     os.remove(input_file)
#     os.remove("test.mp4")

# compress("song.mp4")

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
path = 'video'

file = "t1.mp4"
f = drive.CreateFile({'title':file, 'parents': [{'id': '1lNlZW9M1AN7DvT_6vIcOW6CgzSpfFtPJ'}]})
f.Upload()