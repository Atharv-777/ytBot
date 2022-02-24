from fileinput import filename
from discord.ext import commands
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
import discord
import ffmpeg

bot = commands.Bot(command_prefix='#')

target_size = 7.9 * 1024
def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

def dlYoutube(url, format):
    yt = YouTube(url)
    if format == 'mp4':
        stream = yt.streams.filter(res="720p").first()
        fname = yt.title + '.mp4'
    if(format == 'mp3'):
        stream = yt.streams.filter(only_audio=True).first()
        fname = yt.title + '.mp3'
    stream.download(filename=fname)
    return fname
    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def convert(ctx, url, format):
    fname = dlYoutube(url,format)
    await ctx.send("Download completed..! wait let me share the file")
    if(os.path.getsize(fname) > 8 * 1024 * 1024):
        if format == 'mp4':
            # output_file = compress(fname, 'mp4')
            compress_video(fname, "compressed.mp4", target_size)
    await ctx.send("Here is your file \n", file=discord.File("compressed.mp4"))
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
    bot.run("OTMxNDgwNjgxMDAxOTE0Mzc5.YeFC_A.oUT2GaDyv5WUkra8JCbRAVjYhts")
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
