import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('CyberBot is ready!')

        
    #@commands.Cog.listener()
    #async def on_member_join(self, member):
    #    intros = ['the true cyber warrior.', 'the HTML hacker.', 'the mainframe destroyer.',\
    #        'the cookie stealer.', 'they brought cookies!', 'the 1337h4x0r.']
    #    await self.bot.send(f'Welcome {member.display_name}, {intros}')
        
def setup(bot):
    bot.add_cog(Events(bot))    