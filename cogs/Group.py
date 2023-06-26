from discord.ext import commands
from supabase import create_client, Client
import os
import hashlib


def get_hash(string: str):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


class Group(commands.Cog, name='Group'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.URL = os.getenv("SUPABASE_URL")
        self.API_KEY = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.URL, self.API_KEY)

    @commands.group()
    async def group(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please give me a valid subcommand')

    @group.command(name="list")
    async def list(self, ctx: commands.Context):
        res = self.supabase.table('group').select('group_name').execute()
        names = set([e['group_name'] for e in res.data])
        cnt, out = 1, ""
        for name in names:
            out += f"{cnt}. {name}\n"
            cnt += 1
        await ctx.send(out)

    @group.command(name="join")
    async def join(self, ctx: commands.Context):
        # process input
        text = ctx.message.content
        lines = text.split('\n')
        group_name = ' '.join(lines[0].split(' ')[2:]).strip()

        # query
        hashed = get_hash(f'{ctx.author.id}')
        self.supabase.table('group')\
            .insert({
                'group_name': f"{group_name}",
                'user_id': f"{hashed}",
            })
        await ctx.send(f"{ctx.author.name} joined {group_name}!")

    @group.command(name="leave")
    async def leave(self, ctx: commands.Context):
        # handle input
        text = ctx.message.content
        lines = text.split('\n')
        if len(lines) <= 1:
            await ctx.send('Please give me a valid string')
            return

        # insert into db
        group_name = ' '.join(lines[0].split(' ')[2:]).strip()
        hashed = get_hash(f"{ctx.author.id}")

        # query
        self.supabase.table('group')\
            .delete().match({
                'group_name': group_name,
                'user_id': f"{hashed}"
            })

    @group.command(name="assign")
    async def assign(self, ctx: commands.Context):
        # handle input
        text = ctx.message.content
        lines = text.split('\n')
        if len(lines) <= 1:
            await ctx.send('Please give me a valid string')
            return

        # insert into db
        group_name = ' '.join(lines[0].split(' ')[2:]).strip()
        res = self.supabase.table('group')\
            .select('*')\
            .match({'group_name': group_name})\
            .execute()
        user_ids = [e['user_id'] for e in res.data]  # id is already hashed
        names = lines[1:]
        for user_id in user_ids:
            insert_data = []
            for name in names:
                insert_data.append({
                    'user_id': f"{user_id}",
                    'task_name': f"{name}",
                })
            self.supabase.table('tasks')\
                .insert(insert_data).execute()
        await ctx.send(f"{group_name} assigned!")
