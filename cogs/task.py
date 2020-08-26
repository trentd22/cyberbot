import discord
from discord.ext import commands, tasks

class Task(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @tasks.loop(seconds=10.0)
    async def change_status(self):
        '''Changes bot status based on latency'''
        try:
            response = round(self.bot.latency * 1000)
        except OverflowError:
            response = 251
        
        if response > 250:
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game('Experiencing Latency'))
        else:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Ready To Go - !help'))
    
    @change_status.before_loop
    async def change_status_before(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Task(bot))
