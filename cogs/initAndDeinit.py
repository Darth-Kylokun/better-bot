import discord
import json
from discord.ext import commands

def jsonLoad(fileLocation: str) -> dict:
    with open(fileLocation, 'r') as f:
        return json.load(f)

def jsonDump(fileLocation: str, jsonTowrite: dict) -> None:
    with open(fileLocation, 'w') as f:
        json.dump(jsonTowrite, f, indent=4)

class initAndDeinit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Put me in couch")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        config = jsonLoad("config.json")

        config[str(guild.id)] = '!C'
        
        jsonDump("config.json", config)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild) -> None:
        config = jsonLoad("config.json")

        config = config.pop(str(guild.id))

        jsonDump("config.json", config)

def setup(bot: commands.Bot):
    bot.add_cog(initAndDeinit(bot))
