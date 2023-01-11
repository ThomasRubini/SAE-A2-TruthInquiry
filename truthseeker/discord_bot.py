import discord
import threading
import truthseeker
import asyncio

async def empty_coro():
    return

def init_bot(token):
    discord_bot = DiscordBot()

    thr = threading.Thread(target=discord_bot.__run__, args=(token,))
    thr.start()

    return discord_bot

class DiscordBot:
    def __init__(self):
        self.bot = discord.Client(intents=discord.Intents.default())
        self.__channel__ = None

        @self.bot.event
        async def on_ready():
            print('Discord bot connected !')
            self.event_loop = asyncio.get_event_loop()

            self.__setup__channel__()
            self.update_games_presence()

    def __setup__channel__(self):
        if len(self.bot.guilds) == 1:
            self.__channel__ = discord.utils.get(self.bot.guilds[0].channels, name="bot")
        else:
            print("Could not find channel #bot")

    def __run__(self, token):
        self.bot.run(token)

    def API(func):
        def decorator(self, *args, **kwargs):
            if self.bot and self.bot.is_ready():
                self.event_loop.create_task(func(self, *args, **kwargs))
            else:
                print(f"Discord bot not ready, not processing function {func.__name__}()")
        return decorator

    @API
    async def update_games_presence(self):
        games_n = len(truthseeker.APP.games_list)
        activity_name = f"Handling {games_n} game{'' if games_n==1 else 's'} !"
        activity = discord.Activity(name=activity_name, type=discord.ActivityType.watching)
        await self.bot.change_presence(activity=activity)

    @API
    async def send_message(self, text):
        if self.__channel__:
            await self.__channel__.send(text)
        else:
            print("channel member not defined, not sending discord message")
