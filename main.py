import discord
import json
import os
from discord.ext import commands

def getPrefix(bot: commands.Bot, message: discord.Message):
    with open('config.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def main():
    bot = commands.Bot(command_prefix=getPrefix)
    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            bot.load_extension(f'cogs.{f[:-3]}')
    f = open('token.txt', 'r')
    token = f.readlines()
    f.close()
    bot.run(token[0])

if __name__ == '__main__':
    main()