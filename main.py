import asyncio
import json
import os
import discord
import discord.ext.commands as commands
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)

with open("config.json") as f:
    log.info("Loading Config Values")

    config = {}
    if bool(os.getenv("PROD")):
        config["Token"] = os.getenv("Token")
        config["LeaderboardTitle"] = os.getenv("LeaderboardTitle")
        config["LeaderboardChannel"] = os.getenv("LeaderboardChannel")
        config["LeaderboardInvite"] = os.getenv("LeaderboardInvite")
        config["SessionCookie"] = os.getenv("SessionCookie")
        config["LeaderboardEndpoint"] = os.getenv("LeaderboardEndpoint")
    else:
        config = json.loads(f.read())

    log.info("Config Values Loaded")


class AoCLeaderboardBot(commands.Bot):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        log.info("Leaderboard Cog loaded")

    async def setup_hook(self):
        await self.load_extension("leaderboard")
        log.info("Leaderboard Bot started up")

    async def on_message(self, message):
        pass


async def main():
    log.info("Running Bot")
    bot = AoCLeaderboardBot(
        config, command_prefix=None, intents=discord.Intents.default()
    )

    async with bot:
        log.info("Bot starting up")
        await bot.start(config["Token"])


if __name__ == "__main__":
    asyncio.run(main())
