import json
import discord.ext.commands as commands

from leaderboard import LeaderboardCog

with open('config.json') as f:
    print('Loading Config Values')
    config = json.loads(f.read())
    print('Config Values Loaded')


class AoCLeaderboardBot(commands.Bot):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    async def on_ready(self):
        print('in on_ready')
        self.load_extension('leaderboard')


bot = AoCLeaderboardBot(config, command_prefix=None)
bot.run(config['Token'])
