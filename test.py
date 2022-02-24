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

import json
import requests
headers = {"Authorization": "Bearer ya29.A0ARrdaM8fyOAEJvRR9TYdLvS30l9fHm6jnPz2MlA17zTbJ68iGMTmIhNXpQUwYIlcQoo6sfSJV7isCNEg6UKHJsiuf_6AoEELtEpfH8UbMq1JBX9f1MX5gNXCgXBVWKSlzDiEPCofFn1X4C-xK6feqSFUClMv"}
para = {
    "name": "test.mp4",
    "parents": ["1cf1dUm6l9fsaF0AaeGVjINB8bxQnsscT"]
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./song.mp4", "rb")
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)
print(r.text)