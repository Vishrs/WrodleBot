import discord
import os
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from wordle_data_fetcher import WordleDataFetcher
from PIL import Image,ImageDraw, ImageFont
import io
from discord import File
load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
 
# wdf = WordleDataFetcher(bot)
# bot.setup_hook = wdf.run_task

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



blank = Image.open("./resources/BlankImage.png").convert('RGBA')
gray = Image.open('./resources/gray.png').convert('RGBA')
green = Image.open('./resources/green.png').convert('RGBA')
yellow = Image.open('./resources/yellow.png').convert('RGBA')
empty = Image.open('./resources/EmptySquare.png').convert('RGBA')

tile_map = {
        'empty': empty,
        'blank': blank,
        'gray': gray,
        'yellow': yellow,
        'green': green
    }

def getSquare(guess, actual, i):
    if not guess:
        return 'empty'
    elif guess[i] == actual[i]:
        return 'green'
    elif guess[i] in actual:
        return 'yellow'
    
    return 'gray'

SQUARE_SIZE = 62

async def loadState(guess,actual, ctx, guessMode=False):
    if not guess and guessMode or len(guess) != 5:
        await ctx.send("Not enough letters. Guess must be 5 letters")
        return
    

    img = Image.new('RGBA', (350,420), (18, 18, 19))

    context = ImageDraw.Draw(img)
    
    font = ImageFont.truetype('./resources/franklin-normal-600.ttf',42)

    padding = 0
    initial = 10
    rowpadding = 0
    initialrow = 10
    for i in range(6):
        for j in range(5):
            tile_image = tile_map[getSquare(guess, actual, j)]
            tile_left = j * SQUARE_SIZE + initial + padding
            tile_top = rowpadding + initialrow
            img.paste(tile_image, (tile_left, tile_top),tile_image)
            
            if guess:
                text_bbox  = context.textbbox((0, 0), guess[j], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = tile_left + SQUARE_SIZE//2 - text_width//2
                text_y = tile_top+2

                context.text((text_x, text_y), guess[j], fill=(215, 218, 220), font=font)

            padding += 5
        padding = 0
        initial = 10
        rowpadding += 62+5

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Create a File object from the buffer
    file = File(fp=buffer, filename='wordle.png')
    await ctx.send("Here's your Wordle image!", file=file)


@bot.command(name='play')
async def on_play(ctx):
    await loadState("","", ctx, False)

@bot.command(name='guess')
async def on_guess(ctx, guess: str):
    #await ctx.send('Your guess was: ' + guess + ', but latest is ' + wdf.latest)

    await loadState(guess=guess, actual="hello", ctx=ctx, guessMode=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Not enough letters")

bot.run(os.getenv('DISCORD_TOKEN'))
