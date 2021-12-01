import json
import aiohttp
import discord
from discord.ext import commands, tasks
import logging

log = logging.getLogger('bott')

ICON_URL = 'https://camo.githubusercontent.com/5dd06562878c98a85ffc0703941a73947b2c2cfafa7f1f3875e7de7aa39c01bb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f45467332316d30585941496a7134543f666f726d61743d6a7067266e616d653d6c61726765'


class LeaderboardCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_leaderboard.start()
        self.leaderboard_endpoint = bot.config['LeaderboardEndpoint']

    @tasks.loop(minutes=15)
    async def update_leaderboard(self):
        channel: discord.TextChannel = self.bot.get_channel(self.bot.config['LeaderboardChannel'])

        try:
            leaderboard_message = await channel.fetch_message(channel.last_message_id)
        except:
            await channel.send(embed=await self.get_leaderboard_embed())
            return

        lb_embed = await self.get_leaderboard_embed()
        await leaderboard_message.edit(embed=lb_embed)

    @update_leaderboard.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    async def get_leaderboard_embed(self):
        lb = await self.get_aoc_leaderboard()
        members = [v for k, v in lb['members'].items()]
        members.sort(key=lambda x: x['local_score'], reverse=True)

        bar = []
        for i, g in enumerate(members):
            bar.append(
                f'{i + 1}: Anonymous#{g["id"]} ({g["local_score"]})' if g["name"] is None else f'{i + 1}: {g["name"]} ({g["local_score"]})')
        bar = bar[:20]
        leaders = '\n'.join(bar)

        embed = discord.Embed(title=f'**{self.bot.config["LeaderboardTitle"]} Advent Of Code Leaderboard!**', color=discord.Colour.green())
        embed.add_field(name='Top 20', value=f'```{leaders}```')
        embed.set_image(url=ICON_URL)
        embed.set_footer(text='This leaderboard will update every 15 minutes')
        return embed

    async def get_aoc_leaderboard(self):
        cookies = {'session': self.bot.config['SessionCookie']}
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(self.leaderboard_endpoint) as resp:
                return await resp.json()


def setup(bot):
    log.info('Loading Leaderboard Cog')
    bot.add_cog(LeaderboardCog(bot))
