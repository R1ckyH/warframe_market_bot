import discord
from discord.ext import commands

from formatting import *
from key import key
from query import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def riven(message, *, name: str):
    if name == "":
        return
    try:
        data = await load_data()
        result = await search_riven_price(data, name)
        respond = format_query(result, riven=True)
        if respond == "":
            respond = "Nothing found"
    except Exception as e:
        respond = f"Error: {e}"
    await message.send(respond)


@bot.command()
async def riven3(message, *, name: str):
    if name == "":
        return
    try:
        data = await load_data()
        result = await search_riven_price(data, name, 3)
        respond = format_query(result, riven=True)
        if respond == "":
            respond = "Nothing found"
    except Exception as e:
        respond = f"Error: {e}"
    await message.send(respond)


@bot.command()
async def riven5(message, *, name: str):
    if name == "":
        return
    try:
        data = await load_data()
        result = await search_riven_price(data, name, 5)
        respond = format_query(result, riven=True)
        if respond == "":
            respond = "Nothing found"
    except Exception as e:
        respond = f"Error: {e}"
    await message.send(respond)


@bot.command()
async def query(message, *, name: str):
    if name == "":
        return
    try:
        data = await load_data()
        result = await search_price(data, name)
        respond = format_query(result)
        if respond == "":
            respond = "Nothing found"
    except Exception as e:
        respond = f"Error: {e}"
    await message.send(respond)


bot.run(key)