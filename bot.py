import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from cogs.Task import Task
# from cogs.User import User
# from cogs.Track import Track
from cogs.Group import Group

DEBUG = True

# Load parameters
if DEBUG:
    load_dotenv(".dev_env")
else:
    load_dotenv(".env")
TOKEN = os.getenv("DC_TOKEN")


# FastAPI
app = FastAPI()
# Bot
intents = discord.Intents.default()  # Ask for permission
if DEBUG:
    intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@app.get("/ping", status_code=200)
async def ping():
    return {"Content": "Ping!"}


# Show us your status card
@bot.command()
async def card(ctx, arg):
    url = f"https://leetcard.jacoblin.cool/{arg}" + \
        "?theme=light&ext=activity&animation=false"
    await ctx.send(url)


# Bot status
@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    game = discord.Game('LeetCode')
    await bot.change_presence(
        status=discord.Status.online,
        activity=game
    )


# Just a run
async def run():
    try:
        bot.add_cog(Task(bot))
        bot.add_cog(Group(bot))
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        bot.remove_cog('Group')
        bot.remove_cog('Task')
        await bot.logout()


async def run_dev():
    try:
        await bot.add_cog(Task(bot))
        await bot.add_cog(Group(bot))
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        bot.remove_cog('Group')
        bot.remove_cog('Task')
        await bot.logout()

if DEBUG:
    asyncio.create_task(run_dev())
else:
    asyncio.create_task(run())
