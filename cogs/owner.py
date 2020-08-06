import discord
from discord.ext import commands

class Owner(commands.Cog):
    '''Commands that can only be used by the owner (who the application itself is under).
    Also requires administrator permissions in the server used in.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='quit', aliases=['shutdown'], hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def _shutdown(self, ctx):
        '''Shutdown bot from discord client'''
        await ctx.send('Bot is now shutting down...')
        return await self.bot.logout()
    
    @commands.command(name='load', hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def _load(self, ctx, extension):
        '''Loads specified cog into the bot on runtime.''' 
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded.')
    
    @commands.command(name='unload', hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def _unload(self, ctx, extension):
        '''Unloads specified cog into the bot on runtime.'''
        if extension == 'owner': # Anti-lockout mechanism
            return await ctx.send(f'You can\'t unload the owner cog!')
        
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded.')

def setup(bot):
    bot.add_cog(Owner(bot))
