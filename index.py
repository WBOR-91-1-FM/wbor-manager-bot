import os

import discord
import dotenv

cogs = ["utilities", "blacklist-manager"]

dotenv.load_dotenv()
token = str(os.getenv("DISCORD_BOT_TOKEN"))
if not token:
    raise ValueError("No token found in .env file")


def main():
    bot = discord.Bot()
    for cog in cogs:
        bot.load_extension(f"modules.{cog}")

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    bot.run(token)


if __name__ == "__main__":
    main()
