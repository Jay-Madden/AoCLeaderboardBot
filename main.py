import json
import discord.ext.commands as commands
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('bot')
log.setLevel(logging.DEBUG)

with open('config.json') as f:
    log.info('Loading Config Values')
    config = json.loads(f.read())
    log.info('Config Values Loaded')


class AoCLeaderboardBot(commands.Bot):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.load_extension('leaderboard')
        log.info('Leaderboard Cog loaded')

    async def on_ready(self):
        log.info('Leaderboard Bot started up')

    async def on_message(self, message):
        pass


log.info('Running Bot')
bot = AoCLeaderboardBot(config, command_prefix=None)
bot.run(config['Token'])
