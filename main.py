import discord
import json
import os

from discord.ext import commands, tasks


class GiveawayBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.config["prefix"], 
            intents=discord.Intents.all())

        self.config = json.load(open("config.json", "r"))
        self.color = int(self.config["color"], 16) + 0x200

        self.GUILD = discord.Object(self.config["guild_id"])

        
    async def load_cogs(self):
        try:
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    await self.load_extension(f"cogs.{file[:-3]}")
        except commands.ExtensionAlreadyLoaded:
            pass
            
    async def on_ready(self):
        print("{} is connected.".format(self.user.display_name))
        # self.change_status.start()

    def run(self):
        super().run(self.config["token"])

    # @tasks.loop(seconds=5)
    # async def change_status(self):
    #     giveaways = len(json.load(open("cogs/giveaways.json", "r")))
    #     await super().change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{} Giveaways.".format(giveaways)))


if __name__ == '__main__':
    new_bot = GiveawayBot()
    new_bot.run()
