# from mega import Mega
# import os
import time
# from dotenv import load_dotenv
# load_dotenv()
# email = os.environ.get("EMAIL")
# password = os.environ.get("PASS")

# start = time.time()
# mega = Mega()
# m = mega.login(email, password)
# file = "t1.mp4"
# uploaded = m.upload(file)
# print(m.get_upload_link(uploaded))
# end = time.time()

# print(end-start)


from pytube import YouTube

start = time.time()
yt = YouTube("https://youtu.be/t8tMTjBMPWs")
stream = yt.streams.first()
stream.download()

end = time.time()

print(end-start)