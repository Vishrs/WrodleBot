from discord.ext import tasks, commands
import requests
import datetime
import pytz
import asyncio
import aiohttp
latest = ''

def initialize(bot):

    async def fetch_wordle_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()

    @tasks.loop(hours=24)
    async def get_wordle_data():
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        today = now.strftime("%Y-%m-%d")
        print(f"Fetching latest word")
        url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"
        data = await fetch_wordle_data(url)
        if data:
            global latest
            latest = data.get('solution')
            # Process the word as needed
            print(f"Today's word: {latest}")

    @get_wordle_data.before_loop
    async def before_fetch_wordle_data():
        await bot.wait_until_ready()
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        # Calculate the time until midnight ET
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        seconds_until_midnight = (midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)
    
    get_wordle_data.start()
    #asyncio.run(get_wordle_data())
