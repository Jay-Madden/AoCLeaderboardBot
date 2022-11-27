import datetime
import json
import time

import aiohttp
import discord
from discord.ext import commands, tasks
import logging

log = logging.getLogger("bot")

ICON_URL = "https://camo.githubusercontent.com/5dd06562878c98a85ffc0703941a73947b2c2cfafa7f1f3875e7de7aa39c01bb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f45467332316d30585941496a7134543f666f726d61743d6a7067266e616d653d6c61726765"


class LeaderboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_leaderboard.start()
        self.leaderboard_endpoint = bot.config["LeaderboardEndpoint"]

    @tasks.loop(minutes=15.0)
    async def update_leaderboard(self):
        log.info(self.update_leaderboard.next_iteration)
        log.info("Getting leaderboard channel")
        channel: discord.TextChannel = self.bot.get_channel(
            self.bot.config["LeaderboardChannel"]
        )

        lb_embed = await self.get_leaderboard_embed()

        if lb_embed is None:
            log.error("Failed to get leaderboard embed, bailing out")
            return

        try:
            leaderboard_message = await channel.fetch_message(channel.last_message_id)
        except Exception:
            log.info("Previous embed not found, generating and sending new one")
            await channel.send(embed=lb_embed)
            return

        if leaderboard_message.author != self.bot.user:
            log.info(
                "Previous message found was not a leaderboard, generating and sending new one"
            )
            await channel.send(embed=lb_embed)
            return

        log.info("Sending leaderboard embed")
        await leaderboard_message.edit(embed=lb_embed)

    @update_leaderboard.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    async def get_leaderboard_embed(self):
        log.info("Updating Leaderboard")
        try:
            lb = await self.get_aoc_leaderboard()
        except Exception as e:
            log.error(
                "Failed to get aoc_leaderboard: make sure your session cookie isn't expired",
                e,
            )
            return None

        log.info(f"Got a response with content: {json.dumps(lb)}")
        members = [v for k, v in lb["members"].items()]

        # Remove everyone from the list that doesn't have a score yet
        members = list(filter(lambda x: x["local_score"] > 0, members))

        members.sort(key=lambda x: x["local_score"], reverse=True)

        leaderboard_string = []
        if members:
            for i, g in enumerate(members):
                leaderboard_string.append(
                    f'{i + 1}: Anonymous#{g["id"]} ({g["local_score"]})'
                    if g["name"] is None
                    else f'{i + 1: >2}: {g["name"]} ({g["local_score"]})'
                )
            leaderboard_string = leaderboard_string[:20]
            leaders = "\n".join(leaderboard_string)
        else:
            leaders = "No leaderboard entries yet, get to solving!"

        embed = discord.Embed(
            title=f'**{self.bot.config["LeaderboardTitle"]} Advent Of Code Leaderboard!**',
            color=discord.Colour.green(),
        )
        embed.add_field(
            name=f"Invite Id",
            value=f'`{self.bot.config["LeaderboardInvite"]}`',
            inline=False,
        )
        embed.add_field(name="Top 20", value=f"```{leaders}```", inline=False)
        embed.add_field(name="Last Updated", value=get_timestamp())
        embed.set_image(url=ICON_URL)
        embed.set_footer(text=f"This leaderboard will update every 15 minutes")
        return embed

    async def get_aoc_leaderboard(self):
        cookies = {"session": self.bot.config["SessionCookie"]}
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(self.leaderboard_endpoint) as resp:
                return await resp.json()


def get_timestamp() -> str:
    """
    Formats the given datetime to a Discord timestamp.
    Used over discord.utils.format_dt due to incorrect timestamp output.
    """
    return f"<t:{int(time.mktime(datetime.datetime.now().timetuple()))}:f>"


async def setup(bot):
    log.info("Loading Leaderboard Cog")
    await bot.add_cog(LeaderboardCog(bot))
