from collections import defaultdict
from discord.ext import commands, tasks
from core.classes.DB import DataBase
from dotenv import load_dotenv
import os
import datetime


class Track(commands.Cog, name='Track'):
    times = [
        datetime.time(
            hour=23, minute=59, second=30,
            tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        ),
        datetime.time(
            hour=12, minute=0, second=0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        ),
        datetime.time(
            hour=17, minute=0, second=0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        ),
        datetime.time(
            hour=22, minute=0, second=0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        ),
    ]
    everyday = [
        datetime.time(
            hour=0, minute=0, second=0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=8))
        ),
    ]

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db = DataBase()
        load_dotenv(".env")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
        self.track.start()
        self.expire_to_archive.start()

    @tasks.loop(time=times)
    async def track(self):
        guild = await self.bot.fetch_guild(self.GUILD_ID)
        channel = await guild.fetch_channel(self.CHANNEL_ID)
        await channel.send("# Daily Track!")
        out = ""
        async for user in guild.fetch_members():
            if user.name == "LeetcodeTrackerPyBot":
                continue
            out += f"## {user.name}\n"
            res = self.db.fetch_eq('tasks', key="user_id", val=user.id)
            tasks = res.data
            if len(tasks) == 0:
                out += "Jobs Done! Great Job! :partying_face:\n"
                continue
            for task in tasks:
                if task['done']:
                    out += ":o: "
                else:
                    out += ":x: "
                out += f"{task['task_name']}\n"
        await channel.send(out)

    @tasks.loop(time=everyday)
    async def expire_to_archive(self):
        # if not Sunday, do nothing
        if (datetime.date.today().weekday() != 6):
            return

        undone = await self.check_undone()
        out = await self.process_output(undone)
        if len(out) == 0:
            out = "## Well Done :partying_face:"
        guild = await self.bot.fetch_guild(self.GUILD_ID)
        channel = await guild.fetch_channel(self.CHANNEL_ID)
        await channel.send("# Weekly Check!\n" + out)

    async def check_undone(self) -> defaultdict:
        # get task from table: task
        tasks = self.db.fetch('tasks').data
        undone = defaultdict(int)  # id : cnt
        for task in tasks:
            if not task['done']:
                undone[task['user_id']] += 1
            self.db.insert(
                table='archived',
                data={
                    'user_id': task['user_id'],
                    'task_name': task['task_name'],
                    'done': task['done']
                })
            self.db.delete(
                table='tasks',
                key='id',
                val=task['id']
            )
        return undone

    async def process_output(self, undone: defaultdict) -> str:
        guild = await self.bot.fetch_guild(self.GUILD_ID)
        out = ""
        async for user in guild.fetch_members():
            if user.name == "LeetcodeTrackerPyBot":
                continue
            if f"{user.id}" in undone:
                out += \
                    f"### {user.name}: {undone[f'{user.id}']} " +\
                    "problems :smiling_imp:\n"
        return out
