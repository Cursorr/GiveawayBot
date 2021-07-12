import discord
import json

from discord.ext import commands, tasks

EXTENTIONS = [
    "cogs.giveaways"
]


class GiveawayBot(commands.Bot):
    def __init__(self):

        self.config = json.load(open("config.json", "r"))

        super().__init__(command_prefix=self.config["prefix"], intents=discord.Intents.all())

        for extention in EXTENTIONS:
            try:
                self.load_extension(extention)
                print(f"{extention} loaded.")

            except Exception as exc:
                print("Failed to load extention {}.".format(exc, type(exc).__name__))

    async def on_ready(self):
        print("{} is connected.".format(self.user.display_name))
        self.change_status.start()

    def run(self):
        super().run(self.config["token"])

    @tasks.loop(seconds=5)
    async def change_status(self):
        giveaways = len(json.load(open("cogs/giveaways.json", "r")))
        await super().change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{} Giveaways.".format(giveaways)))


if __name__ == '__main__':
    new_bot = GiveawayBot()
    new_bot.run()
