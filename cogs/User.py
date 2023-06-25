from discord.ext import commands


class User(commands.Cog, name='User'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def user(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please give me a valid subcommand')

    @user.command(name="list")
    async def new(self, ctx: commands.Context):
        out = ""
        async for user in ctx.guild.fetch_members():
            out += f"{user.name}\n"
        await ctx.send(out)
