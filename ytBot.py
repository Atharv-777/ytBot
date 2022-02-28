from discord.ext import commands
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
import discord
import json
import requests

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

bot = commands.Bot(command_prefix='#')

def dlYoutube(url, format):
    yt = YouTube(url)
    if format == 'mp4':
        stream = yt.streams.filter(res="720p").first()
        fname = yt.title + '.mp4'
    if format == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
        fname = yt.title + '.mp3'
    fname = fname.replace(" ", "-")      
    stream.download(filename=fname)
    return fname

def uploadDrive(format, toBeSavedAs, file):
    headers = {"Authorization": "Bearer ya29.A0ARrdaM_uf9JdBUpKP63txdGWTkJInXaz9w6H3c7k_izMYt4uHH7GZBuYhw0dfCmHW4_9DzroEERMvhj3oMuhxImJNMgLPo0lccDDj-lcq1dBTolnEcFVaS5xe7nsq3wZyVGqlM-Nm6jbsvkrF9K6rSnaff-r"}
    # file = file.replace(" " , "-")
    # baseLink = "https://drive.google.com/drive/u/3/my-drive/"
    if format == "mp4":
        folder = "1lNlZW9M1AN7DvT_6vIcOW6CgzSpfFtPJ"
    elif format == "mp3":
        folder = "11dCZPIpLFhTrI-jG-2pxNLaZA6FGwvWM"
    # generatedLink = baseLink + folder

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    f = drive.CreateFile({'title':toBeSavedAs, 'parents': [{'id': folder}]})
    f.Upload()
        
    # return generatedLink + "/" + file

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def convert(ctx, url, format):
    fname = dlYoutube(url,format)
    await ctx.send("Download completed..! wait let me share the link to your file")
    geneartedLink = uploadDrive(format, fname, fname)
    await ctx.send(geneartedLink)
    # await ctx.send("Here is your file \n", file=discord.File("compressed.mp4"))
    # os.remove(fname)
    

@bot.command()
async def clip(ctx, url, start, end, format):
    fname = dlYoutube(url, 'mp4')
    print("{} video downloaded.".format(fname))
    clip = VideoFileClip(fname).subclip(start, end)
    if format == 'mp4':
        clipName = "clipped.mp4"
        clip.write_videofile(clipName)
        clip.close()
    elif format == 'mp3':
        audio = clip.audio
        clipName = "clipped.mp3"
        audio.write_audiofile(clipName)
        clip.close()
    await ctx.send("Video is clipped..! \n Rename the file from {} to any other name...".format(clipName))
    await ctx.send("Here is your clipped file", file=discord.File(clipName))
    os.remove(clipName)
    os.remove(fname)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {}, how are ya?".format(ctx.message.author.mention))
     
@bot.command()
async def service(ctx):
    await ctx.send("Well {}, Really good question.. I can \n 1. Download youtube video into mp3/mp4 format. \n 2. Cut(clip) any youtube video for specified time(in seconds).".format(ctx.message.author.mention))

#Put this at the bottom of your .py file
try:
    bot.run("OTMxNDgwNjgxMDAxOTE0Mzc5.YeFC_A.p7nCzanYtmsSqMyyH2CF-zJFYIo")
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
