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
async def convert(ctx, url, format):
    yt = YouTube(url)
    if format == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
        fname = yt.title + '.mp3'
    elif format == 'mp4':
        stream = yt.streams.get_highest_resolution()
        fname = yt.title + '.mp4'
    print(fname)
    print("Reached till download phase...")
    stream.download(filename=fname)
    yt.register_on_complete_callback(await ctx.send("Download completed..! wait let me share the file"))
    await ctx.send("Here is your file \n", file=discord.File(fname))
    os.remove(os.getcwd() + '/' + fname)

@bot.command()
async def clip(ctx, url, start, end, format):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    fname = yt.title + '.mp4'
    stream.download(filename=fname)
    print("{} video downloaded.".format(yt.title))
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
    yt.register_on_complete_callback(await ctx.send("Video is clipped..! \n Rename the file from {} to any other name...".format(clipName)))
    await ctx.send("Here is your clipped file", file=discord.File(clipName))
    os.remove(os.getcwd() + '/' + fname)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {}, how are ya?".format(ctx.message.author.mention))
     
@bot.command()
async def service(ctx):
    await ctx.send("Well {}, Really good question.. I can \n 1. Download youtube video into mp3/mp4 format. \n 2. Cut(clip) any youtube video for specified time(in seconds).".format(ctx.message.author.mention))

#Put this at the bottom of your .py file
try:
    bot.run("<token here>")
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
