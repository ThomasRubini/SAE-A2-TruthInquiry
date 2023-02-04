import threading
import asyncio

import discord
import truthinquiry.app as app


class DiscordBot:
    """
    Wrapper around a discord bot, providing utility methods to interact with it

    :attr Client bot: the underlying discord bot from discord.py
    :attr TextChannel __channel__: the channel used by the bot to send messages
    :attr event_loop: event_loop used by discord.py. Used to schedule tasks from another thread
    """

    def __init__(self):
        self.bot = discord.Client(intents=discord.Intents.default())
        self.__channel__ = None

        @self.bot.event
        async def on_ready():
            print('Discord bot connected !')
            self.event_loop = asyncio.get_event_loop()

            self.__setup__channel__()
            self.update_games_presence()

    def __setup__channel__(self) -> None:
        """
        Setup the channel that the bot will send message in
        """
        if len(self.bot.guilds) == 1:
            self.__channel__ = discord.utils.get(self.bot.guilds[0].channels, name="bot")
        else:
            print("Could not find channel #bot")

    def start(self, token):
        thr = threading.Thread(target=self.bot.run, args=(token,))
        thr.start()
        return thr

    def API(func):
        """
        Decorator used to wrap APIs methods, to handle thread context change, and ready check
        """
        def decorator(self, *args, **kwargs):
            if self.bot and self.bot.is_ready():
                self.event_loop.create_task(func(self, *args, **kwargs))
            else:
                print(f"Discord bot not ready, not processing function {func.__name__}()")
        return decorator

    @API
    async def update_games_presence(self) -> None:
        """
        Update the bot's status using the app's current context
        """
        games_n = len(app.APP.games_list)
        activity_name = f"Handling {games_n} game{'' if games_n==1 else 's'} !"
        activity = discord.Activity(name=activity_name, type=discord.ActivityType.watching)
        await self.bot.change_presence(activity=activity)

    @API
    async def send_message(self, text):
        """
        Send a message to the channel used by the bot
        """
        if self.__channel__:
            await self.__channel__.send(text)
        else:
            print("channel not defined, not sending discord message")
