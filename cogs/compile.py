import discord
import aiohttp
import json
from discord.ext import commands

languages = {'c': ("6", "-Wall -std=gnu99 -O2 -o a.out source_file.c"),
             'c#': ("1", ""),
             'cs': ("1", ""),
             'csharp': ("1", ""),
             'cpp': ("7", "-Wall -std=c++17 -O3 -o a.out source_file.cpp"), 
             'c++': ("7", "-Wall -std=c++17 -O3 -o a.out source_file.cpp"), 
             'python': ("24", ""), 
             'py': ("24", ""), 
             'java': ("4", ""), 
             'js': ("23", ""),
             'javascript': ("23", "")}

def trimCode(code: str) -> str:
    code = list(code)
    for i in range(6):
        code[i] = ""
    for i in range(1, 4):
        x = i*-1
        code[x] = ""
    return ''.join(code)

def codeColor(data: dict) -> discord.Color:
    if data['Errors'] != None:
        return discord.Color.red()
    elif data['Warnings'] != None:
        return discord.Color.from_rgb(255, 255, 0)
    return discord.Color.green()

def compileTime(data: dict) -> str:
    compiletime = ''
    buffer = ''
    iterate = -1
    while (buffer != 's'):
        compiletime += buffer
        buffer = data['Stats'][18+iterate]
        iterate += 1
    return compiletime

class compiler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = commands.Bot

    @commands.command()
    async def compile(self, ctx: commands.Context, language: str , *, code: str) -> None:
        if code[0] == '`':
            code = trimCode(code)

        data_to_compile = {
            "LanguageChoice": languages[language.lower()][0],
            "Program": code,
            "Input": "",
            "CompilerArgs": languages[language.lower()][1]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://rextester.com/rundotnet/api", data=data_to_compile) as resp:
                postdata = json.loads(await resp.text())

                embed = discord.Embed(title="Output", color=codeColor(postdata), description=f"COMPILE TIME:{compileTime(postdata)}sec")
                embed.add_field(name="ERRORS:", value=postdata['Errors'])
                embed.add_field(name="WARNINGS:", value=postdata['Warnings'])
                embed.add_field(name="OUTPUT:", value=postdata['Result'], inline=False)
                embed.set_footer(text="Compiler Bot is powered by https://rextester.com/")

                await ctx.send(embed=embed)
            
def setup(bot: commands.Bot):
    bot.add_cog(compiler(bot))