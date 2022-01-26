from discord.ext import commands
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
import discord

bot = commands.Bot(command_prefix = '#')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def convert(ctx, url, format, filename=''):
    yt = YouTube(url)
    if format == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
        fname = yt.title + '.mp3'
    elif format == 'mp4':
        stream = yt.streams.get_highest_resolution()
        fname = yt.title + '.mp4'
    if filename:
        fname = filename
    stream.download(filename=fname)
    ctx.send(file=discord.File(os.path.join(os.getcwd(), fname)))
    yt.register_on_complete_callback(await ctx.send("Download completed..! {}".format(fname)))

@bot.command()
async def cut(ctx, url, start, end, format):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    fname = yt.title
    stream.download(filename=fname + '.mp4')
    await ctx.send("Your video {}".format(yt.title))
    print("{} video downloaded.".format(yt.title))
    # clip = VideoFileClip(fname+'.mp4').subclip(start, end)
    # if format == 'mp4':
    #     clip.write_videofile("edited.mp4")
    #     clip.close()
    # elif format == 'mp3':
    #     audio = clip.audio
    #     audio.write_audiofile("edited.mp3")
    #     clip.close()
    # yt.register_on_complete_callback(await ctx.send("Video is clipped..! \n Rename the file from edited.{} to any other name...".format(format)))
    # os.remove(os.getcwd() + '/' + fname + '.mp4')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {}, how are ya?".format(ctx.message.author.mention))
     
@bot.command()
async def service(ctx):
    await ctx.send("Well {}, Really good question.. I can \n 1. Download youtube video into mp3/mp4 format. \n 2. Cut(clip) any youtube video for specified time(in seconds).".format(ctx.message.author.mention))

#Put this at the bottom of your .py file
try:
    bot.run("OTMxNDgwNjgxMDAxOTE0Mzc5.YeFC_A.TSKv3dQRIoJ4LhfA8HLDHvhdeb4")
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
