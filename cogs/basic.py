import discord
from discord.ext import commands
import random

class Basic(commands.Cog):
    '''Basic commands for troubleshooting and/or fun.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='version')
    async def version(self, ctx):
        with open('version.txt', 'r') as f:
            bot_message = f.read()

        await ctx.send(bot_message)


    @commands.command(name='ping')
    async def ping(self, ctx):
        '''!ping : Checks bot reponse latency'''
        await ctx.send(f'Bot response took {round(self.bot.latency * 1000, 1)}ms')

    @commands.command(name='roll', aliases=['dice'])
    async def roll_dice(self, ctx, n=10):
        '''!roll (number) : Rolls dice between 1 to N, default = 10.'''
        
        if n > 1000000 or n <= 1:
            return await ctx.send('Please enter a value from 2 to 1,000,000.')
            
        await ctx.send(f'You rolled a {random.randrange(1, n+1)}')

def setup(bot):
    bot.add_cog(Basic(bot))