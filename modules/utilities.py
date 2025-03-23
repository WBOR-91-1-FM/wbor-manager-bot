import os

import discord
from discord import Interaction
from discord.ext import commands

role_id = str(os.getenv("DISCORD_ROLE_ID"))


async def user_can_run_command(ctx: Interaction):
    if ctx.guild is None:
        await ctx.respond("This command can only be run in a server.", ephemeral=True)
        return False

    role = discord.utils.find(lambda r: r.id == int(role_id), ctx.guild.roles)
    if role not in ctx.user.roles:
        await ctx.respond(
            "You don't have permission to run this command.", ephemeral=True
        )
        return False

    return True


"""
Simple cog meant for simple commands, such as the /ping command.
"""


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Check the bot's latency.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


def setup(bot):
    bot.add_cog(Utilities(bot))
