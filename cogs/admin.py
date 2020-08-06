import discord
from discord.ext import commands
import json
from os import path

class Admin(commands.Cog):
    '''Commands that are for bot maintenance and administration.
    Restricted to server admins only.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', aliases=['wipe'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=10):
        '''!clear amount : Clears X amount of messages. Default = 10
        Note: This command can only be used by an administrator of the server.'''
        if amount > 100:
            amount = 100
        
        if amount < 1:
            amount = 1

        await ctx.channel.purge(limit=amount)

    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        '''!kick @user (Optional: Reason) : Kicks the mentioned user.
        A reason for the kick can be specified for logging purposes.
        Note: This command can only be used by an administrator of the server.'''
        await member.kick(reason=reason)
        await ctx.send(f'User {member.mention} has been kicked.')
    
    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        '''!ban @user (Optional: Reason) : Bans the mentioned user.
        A reason for the ban can be specified for logging purposes.
        Note: This command can only be used by an administrator of the server.'''
        await member.ban(reason=reason)
        await ctx.send(f'User {member.mention} has been banned.')

    @commands.command(name='unban')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        '''!unban user#1234 : Unbans the user given if they have been banned
        Note: This command can only be used by an administrator of the server.'''
        users_banned = await ctx.guild.bans()
        account_name, account_discriminator = member.split('#')

        for entry in users_banned:
            user = entry.user

            if (user.name, user.discriminator) == (account_name, account_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')
                return
            
        await ctx.send(f'{member} is not banned!')

def setup(bot):
    bot.add_cog(Admin(bot))
