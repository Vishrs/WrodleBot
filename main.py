import discord
import os
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from wordle_data_fetcher import WordleDataFetcher
load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
 
wdf = WordleDataFetcher(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='guess')
async def on_guess(ctx, guess: str):
    await ctx.send('Your guess was: ' + guess + ', but latest is ' + wdf.latest)



discord_token = os.getenv('DISCORD_TOKEN')

bot.setup_hook = wdf.run_task
bot.run(discord_token)
