import discord
import httpx
from discord.ext import commands

from lists import ignored_words, profanity_list
from modules.parsing import (get_original_word, is_offense_warning,
                             is_utf_warning)
from modules.utilities import user_can_run_command

"""
This cog handles stuff related to list commands.

WBOR has a script that checks for profanities in song/artist titles before the information is relayed to the RDS.
However, false positives are a thing, so we have a whitelist to quickly remove any words from the blacklist.
Also, the service deals with non-UTF-8 characters (because RDS only supports ASCII), so we have a list of "words to ignore".
"""


class ListUtilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Removes a word from the blacklist.
    """

    @commands.message_command(name="Remove profanity from blacklist")
    async def remove_from_blacklist(self, ctx, message):
        if not await user_can_run_command(ctx):
            return

        if not is_offense_warning(message.content):
            await ctx.respond("This is not a profanity warning.", ephemeral=True)
            return

        word = get_original_word(message.content)
        if not profanity_list.exists(word):
            await ctx.respond(f"**{word}** is not in the blacklist.", ephemeral=True)
            return

        profanity_list.remove(word)
        await ctx.respond(f"Removed **{word}** from the blacklist.")

    """
    Adds a word to the silenced warnings list. 
    This way, it won't trigger a webhook notification.
    """

    @commands.message_command(name="Silence warnings for these words")
    async def silence_warnings(self, ctx, message):
        if not await user_can_run_command(ctx):
            return

        if not is_offense_warning(message.content) and not is_utf_warning(
            message.content
        ):
            await ctx.respond("This is not a warning message.", ephemeral=True)
            return

        word = get_original_word(message.content)
        if ignored_words.exists(word):
            await ctx.respond(
                f"**{word}** is already in the silenced warnings list.", ephemeral=True
            )
            return

        ignored_words.add(word)
        await ctx.respond(f"Silenced warnings for **{word}**.")

    """
    This group fetches a list from an URL and adds it to the selected list.
    """
    import_grp = discord.SlashCommandGroup(
        name="import", description="Imports a list of words from a URL."
    )

    @import_grp.command(
        name="profanities", description="Imports a list of words to the profanity list."
    )
    async def import_profanities(self, ctx, url: str):
        if not await user_can_run_command(ctx):
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                await ctx.respond("Failed to fetch the list.", ephemeral=True)
                return

            words = []
            try:
                # try parsing as a JSON
                arr = response.json()
                words.extend(arr)
            except:
                # if it fails, split by newline
                arr = response.text.split("\n")
                words.extend(arr)

            # transform words into a tuple with n elements
            words_tuple = [(word,) for word in words]
            profanity_list.add_many(words_tuple)

            await ctx.respond(
                f"Added {len(words)} words to the profanity list. Sample: {', '.join(words[:5])}"
            )

    """
    This group shows stats for the selected list.
    """
    stats_grp = discord.SlashCommandGroup(
        name="stats", description="Shows stats for the selected list."
    )

    @stats_grp.command(
        name="profanities", description="Shows stats for the profanity list."
    )
    async def profanity_stats(self, ctx):
        count = profanity_list.count()
        await ctx.respond(f"Profanity list has {count} words.")

    @stats_grp.command(
        name="ignored-words", description="Shows stats for the ignored words list."
    )
    async def ignored_words_stats(self, ctx):
        count = ignored_words.count()
        await ctx.respond(f"Ignored words list has {count} words.")

    """
    This group allows words to be added to the selected list.
    """
    add_grp = discord.SlashCommandGroup(
        name="add", description="Adds a word to the selected list."
    )

    @add_grp.command(name="profanity", description="Adds a word to the profanity list.")
    async def add_profanity(self, ctx, word: str):
        if not await user_can_run_command(ctx):
            return

        if profanity_list.exists(word):
            await ctx.respond(
                f"**{word}** is already in the blacklist.", ephemeral=True
            )
            return

        profanity_list.add(word)
        await ctx.respond(f"Added **{word}** to the blacklist.")

    @add_grp.command(
        name="ignored-words", description="Adds a word to the ignored words list."
    )
    async def add_ignored_word(self, ctx, word: str):
        if not await user_can_run_command(ctx):
            return

        if ignored_words.exists(word):
            await ctx.respond(
                f"**{word}** is already in the ignored words list.", ephemeral=True
            )
            return

        ignored_words.add(word)
        await ctx.respond(f"Added **{word}** to the ignored words list.")

    """
    This group allows words to be removed from the selected list.
    """
    remove_grp = discord.SlashCommandGroup(
        name="remove", description="Removes a word from the selected list."
    )

    @remove_grp.command(
        name="profanity", description="Removes a word from the profanity list."
    )
    async def remove_profanity(self, ctx, word: str):
        if not await user_can_run_command(ctx):
            return

        if not profanity_list.exists(word):
            await ctx.respond(f"**{word}** is not in the blacklist.", ephemeral=True)
            return

        profanity_list.remove(word)
        await ctx.respond(f"Removed **{word}** from the blacklist.")

    @remove_grp.command(
        name="ignored-words", description="Removes a word from the ignored words list."
    )
    async def remove_ignored_word(self, ctx, word: str):
        if not await user_can_run_command(ctx):
            return

        if not ignored_words.exists(word):
            await ctx.respond(
                f"**{word}** is not in the ignored words list.", ephemeral=True
            )
            return

        ignored_words.remove(word)
        await ctx.respond(f"Removed **{word}** from the ignored words list.")


def setup(bot):
    bot.add_cog(ListUtilities(bot))
