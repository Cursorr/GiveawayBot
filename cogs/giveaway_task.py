import discord
import json
import time
import random

from discord.ext import commands, tasks


class GiveawayTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open("config.json", "r"))
        self.color = int(self.config["color"], 16) + 0x200
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        with open("cogs/giveaways.json", "r") as f:
            giveaways = json.load(f)

        if len(giveaways) == 0:
            return

        for giveaway in giveaways:
            data = giveaways[giveaway]
            if int(time.time()) > data["end_time"]:
                channel = self.bot.get_channel(data["channel_id"])
                giveaway_message = await channel.fetch_message(int(giveaway))
                users = await giveaway_message.reactions[0].users().flatten()
                users.pop(users.index(self.bot.user))
                if len(users) < data["winners"]:
                    winners_number = len(users)
                else:
                    winners_number = data["winners"]

                winners = random.sample(users, winners_number)
                users_mention = []
                for user in winners:
                    users_mention.append(user.mention)
                result_embed = discord.Embed(
                    title="🎉 {} 🎉".format(data["prize"]),
                    color=self.color,
                    description="Congratulations {} you won the giveaway !".format(", ".join(users_mention))
                )\
                    .set_footer(icon_url=self.bot.user.avatar_url, text="Giveaway Ended !")
                await giveaway_message.edit(embed=result_embed)

                with open("cogs/giveaways.json", "r") as file:
                    json_data = json.load(file)

                    del json_data[giveaway]

                with open("cogs/giveaways.json", "w") as file:
                    json.dump(json_data, file, indent=4)
def setup(bot):
    bot.add_cog(GiveawayTask(bot))
