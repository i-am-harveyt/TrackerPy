from discord.ext import commands
from supabase import create_client, Client
from typing import List, Dict
import os
import hashlib


def get_hash(string: str):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


class Task(commands.Cog, name='Task'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.URL = os.getenv("SUPABASE_URL")
        self.API_KEY = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.URL, self.API_KEY)

    @commands.group()
    async def task(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please give me a valid subcommand')

    @task.command(name="new")
    async def user_new(self, ctx: commands.Context):
        # process input
        text = ctx.message.content
        names = text.split('\n')[1:]

        # handle
        if len(names) == 0:
            await ctx.send('Please give me a valid input')
            return

        # insert into db
        insert_data: List[Dict] = []
        hashed = get_hash(f'{ctx.author.id}')
        for name in names:
            insert_data.append({
                'user_id': f"{hashed}",
                'task_name': f"{name}"
            })
        self.supabase\
            .table("tasks")\
            .insert(insert_data)\
            .execute()
        await self.display_user(ctx)

    @task.command(name="delete")
    async def delete(self, ctx: commands.Context):
        # process input
        text = ctx.message.content
        names = text.split('\n')[1:]

        # handle input
        if len(names) == 0:
            await ctx.send('Please give me a valid input')
            return

        # query
        hashed = get_hash(f'{ctx.author.id}')
        for name in names:
            self.supabase.table("tasks").delete()\
                .match({
                    'user_id': f"{hashed}",
                    'task_name': f"{name}"
                })\
                .execute()
        await self.display_user(ctx)

    @task.command(name="done")
    async def done(self, ctx: commands.Context):
        # process input
        text = ctx.message.content
        names = text.split('\n')[1:]

        # handle input
        if len(names) == 0:
            await ctx.send('Please give me a valid input')
            return

        # query
        hashed = get_hash(f'{ctx.author.id}')
        for name in names:
            self.supabase.table("tasks")\
                .update({'done': True})\
                .match({
                    'user_id': f"{hashed}",
                    'task_name': f"{name}"
                })\
                .execute()
        await self.display_user(ctx)

    @task.command(name="undone")
    async def undone(self, ctx: commands.Context):
        # process input
        text = ctx.message.content
        names = text.split('\n')[1:]

        # handle input
        if len(names) == 0:
            await ctx.send('Please give me a valid input')
            return

        # query
        hashed = get_hash(f'{ctx.author.id}')
        for name in names:
            self.supabase.table("tasks")\
                .update({'done': False})\
                .match({
                    'user_id': f"{hashed}",
                    'task_name': f"{name}"
                })\
                .execute()
        await self.display_user(ctx)

    @task.command(name="archive")
    async def archive_task(self, ctx: commands.Context):
        await ctx.send("Revising, not available")
        return
        # process input
        text = ctx.message.content
        names = text.split('\n')[1:]

        # handle input
        if len(names) == 0:
            await ctx.send('Please give me a valid input')
            return

        # get task from table: task
        # hashed = get_hash(f'{ctx.author.id}')
        # tasks = self.db.fetch_eq(
        #     table='tasks',
        #     key='user_id', val=hashed).data
        # for task in tasks:
        #     for name in names:
        #         if name != task['task_name']:
        #             continue
        #         self.db.insert(
        #             table='archived',
        #             data={
        #                 'user_id': task['user_id'],
        #                 'task_name': task['task_name'],
        #                 'done': task['done']
        #             })
        #         self.db.delete(
        #             table='tasks',
        #             key='id',
        #             val=task['id']
        #         )
        await ctx.send("Archive Complete!")

    @task.group(name="display")
    async def display(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please give me a valid subcommand')

    @display.command(name="users")
    async def display_users(self, ctx: commands.Context):
        out = "# Tasks by users\n"
        # Display user tasks one by one
        async for user in ctx.guild.fetch_members():
            if user.name == "LeetcodeTrackerPyBot":
                continue
            out += f"## {user.name}\n"
            hashed = get_hash(f'{user.id}')
            res = self.supabase.table("tasks")\
                .select('*')\
                .match({'user_id': hashed}).execute()
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
        await ctx.send(out)

    @display.command(name="mine")
    async def display_mine(self, ctx: commands.Context):
        await self.display_user(ctx)

    @display.command(name='archived')
    async def display_archived(self, ctx: commands.Context):
        await self.display_user(ctx, 'archived')

    async def display_user(self, ctx: commands.Context, table: str = 'tasks'):
        hashed = get_hash(f'{ctx.author.id}')
        res = self.supabase\
            .table(table)\
            .select('*')\
            .match({'user_id': hashed})\
            .execute()
        tasks = res.data
        if len(tasks) == 0:
            await ctx.send("Jobs Done! Great Job!")
            return
        out = f"## {ctx.author.name}\n"
        for task in tasks:
            if task['done']:
                out += ":o: "
            else:
                out += ":x: "
            out += f"{task['task_name']}\n"
        await ctx.send(out)
