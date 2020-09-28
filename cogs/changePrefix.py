import discord
import json
from discord.ext import commands

def jsonLoad(fileLocation: str) -> dict:
    with open(fileLocation, 'r') as f:
        return json.load(f)

def jsonDump(fileLocation: str, jsonTowrite: dict) -> None:
    with open(fileLocation, 'w') as f:
        json.dump(jsonTowrite, f, indent=4)

class changePrefix(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def changePrefix(self, ctx: commands.Context, newprefix: str) -> None:
        config = jsonLoad("config.json")

        config[str(ctx.guild.id)] = newprefix

        jsonDump("config.json", config)

def setup(bot: commands.Bot):
    bot.add_cog(changePrefix(bot))