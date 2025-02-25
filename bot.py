import discord
import openai
import asyncio
import random
import requests
import os
import yt_dlp
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ffmpeg_path = os.getenv("ffmpeg")

intents = discord.Intents.all()

intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} is online!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def info(ctx):
    await ctx.send('I am a bot developed by <@385851727905030144>')

@bot.command()
async def github(ctx):
    await ctx.send('https://github.com/moyom1337')

@bot.command()
async def server(ctx):
    server = ctx.guild
    await ctx.send(f'Server: {server.name}\nMembers: {server.member_count}')

@bot.command()
async def user(ctx, member: discord.Member):
    await ctx.send(f'Member: {member.name}\nID: {member.id}\nArrived: {member.joined_at}')

@bot.command()
async def rps(ctx, rps: str):
    options = ['rock', 'paper', 'scissors']
    user_rps = rps.lower()

    if user_rps not in options:
        await ctx.send("Please only choose between rock, paper, or scissors.")
        return
    
    bot_rps = random.choice(options)

    if user_rps == bot_rps:
        result = "It's a tie!"
    elif (user_rps == 'rock' and bot_rps == 'scissors') or \
         (user_rps == 'paper' and bot_rps == 'rock') or \
         (user_rps == 'scissors' and bot_rps == 'paper'):
        result = "You win!"
    else:
        result = "You lose!"

    await ctx.send(
        f"**You chose:** {user_rps.lower()}\n"
        f"**Bot chose:** {bot_rps.lower()}\n"
        f"**Result:** {result}"
    )


@bot.tree.command(name="wagwan")
async def wagwan(interaction: discord.Interaction):
    await interaction.response.send_message(f"Wagwan {interaction.user.mention}!")

@bot.tree.command(name="countfour")
async def countfour(interaction: discord.Interaction):
    await interaction.response.send_message("One...")
    await asyncio.sleep(2) 
    await interaction.followup.send("Two...")
    await asyncio.sleep(2)
    await interaction.followup.send("Three...")
    await asyncio.sleep(2)
    await interaction.followup.send("FOUR!")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def play(ctx):
    if not ctx.voice_client:
        await ctx.invoke(join)

    vc = ctx.voice_client

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=YLslsZuEaNE", download=False)
        audio_url = info["url"]

    ffmpeg_options = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"
    }
    
    vc.play(discord.FFmpegPCMAudio(audio_url, executable= ffmpeg_path, **ffmpeg_options))

bot.run(TOKEN)