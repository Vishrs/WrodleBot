
import datetime
import pytz
import aiohttp
from discord.ext import tasks
import asyncio

class WordleDataFetcher:
    def __init__(self, bot):
        self.latest = None
        self.bot = bot
        self.run_once = True

    async def run_task(self):
        self.get_wordle_data.start()

    @tasks.loop(hours=24)
    async def get_wordle_data(self):
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        today = now.strftime("%Y-%m-%d")
        url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"
        print(url)
        word = await self.fetch_wordle_data(url)
        print(word)
        if word:
            self.latest = word
            print(f"Today's word: {''.join(str(ord(c)) for c in self.latest)}")


    async def fetch_wordle_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('solution')

    @get_wordle_data.before_loop
    async def before_get_wordle_data(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if now.hour >= 0 and not self.run_once:  # Adjust if needed
            next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        else:
            next_run = now.replace(hour=0, minute=0, second=0, microsecond=0)
            self.run_once = False
        seconds_until_next_run = (next_run - now).total_seconds()
        await asyncio.sleep(seconds_until_next_run)