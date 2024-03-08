import discord
import json
import os

from datetime import datetime
from discord import app_commands
from discord.ext import commands

from api import *
from formatting import *
from key import key
from query import *
from utils import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

def load_data():
    data = {}
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    if data == {} or datetime.now().timestamp() > data["time"] + 10:
        data = get_data()
        print(f"Updated in {int_to_time(data['time'])}")
    else:
        print(f"Used data in {int_to_time(data['time'])}")
    return data


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def query(message, *, name: str):
    if name == "":
        return
    try:
        data = load_data()
        result = search_price(data, name)
        respond = format_query(result)
        if respond == "":
            respond = "Nothing found"
    except Exception as e:
        respond = f"Error: {e}"
    await message.send(respond)

bot.run(key)


#data = load_data()
#print(similar("arcane grace", "arcane_rage"))
##print(json.dumps(search_price(data, "khora prime"), indent=4, ensure_ascii=False))