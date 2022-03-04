from discord.ext import commands
from pytube import YouTube
from mega import Mega
import os
from moviepy.editor import VideoFileClip
import discord

from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix='#')
bot_token = os.environ.get("BOT_TOKEN")
email = os.environ.get("EMAIL")
password = os.environ.get("PASS")
mega = Mega()
m = mega.login(email, password)

def dlYoutube(url, format):
    yt = YouTube(url)
    if format == 'mp4':
        stream = yt.streams.filter(res="720p").first()
        fname = yt.title + '.mp4'
    if format == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
        fname = yt.title + '.mp3'
    stream.download(filename=fname)
    return fname

def uploadDrive(file):
    uploadedFile = m.upload(file)
    return m.get_upload_link(uploadedFile)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def convert(ctx, url, format):
    fname = dlYoutube(url,format)
    embed = discord.Embed(title="Download completed..!", description="wait lemme share the link to your file...", color=0xffffff)
    await ctx.send(embed=embed)
    geneartedLink = uploadDrive(fname)
    await ctx.send(geneartedLink)
    os.remove(fname)
    

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
    geneartedLink = uploadDrive(clipName)
    embed = discord.Embed(title="Video is clipped..!", description="Recommended : Rename the file from {} to any other name...".format(clipName), color=0x1a9fad)
    await ctx.send(embed=embed)
    await ctx.send(geneartedLink)
    os.remove(clipName)
    os.remove(fname)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {}, how are ya?".format(ctx.message.author.mention))
     
@bot.command()
async def service(ctx):
    await ctx.send("Well {}, Really good question.. I can \n 1. Download youtube video into mp3/mp4 format. \n 2. Cut(clip) any youtube video for specified time(in seconds).".format(ctx.message.author.mention))
    
try:
    bot.run(bot_token)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
