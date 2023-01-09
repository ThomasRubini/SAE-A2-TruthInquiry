import discord
import threading
import truthseeker


def init_bot(token):
    discord_bot = DiscordBot()

    thr = threading.Thread(target=discord_bot.__run__, args=(token,))
    thr.start()

    return discord_bot

class DiscordBot:
    def __init__(self):
        self.bot = discord.Client(intents=discord.Intents.default())

        @self.bot.event
        async def on_ready():
            print('Discord bot connected !')

            await self.update_games_presence()

    def __run__(self, token):
        self.bot.run(token)

    async def update_games_presence(self):
        games_n = len(truthseeker.APP.games_list)
        activity_name = f"Handling {games_n} game{'' if games_n==1 else 's'} !"
        activity = discord.Activity(name=activity_name, type=discord.ActivityType.watching)
        await self.bot.change_presence(activity=activity)
