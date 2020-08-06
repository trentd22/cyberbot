import discord
from discord.ext import commands


class ErrHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Error Handling'''
        if isinstance(error, commands.MissingRole):
            await ctx.send(f'{ error }')

        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')

def setup(bot):
    bot.add_cog(ErrHandler(bot))
