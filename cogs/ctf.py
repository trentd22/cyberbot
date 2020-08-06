import discord
from os import path
from discord.ext import commands
import requests
from datetime import datetime, timezone
import json
from time import time

class CTF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}

        self.fp = path.dirname(__file__)
        self.rp = 'data/teams.json'
        self.file_path = path.join(self.fp, self.rp)
        self.ctftime = 'https://ctftime.org/'

        if not path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('{}')
    


    @commands.command(name='ctf', aliases=['ctfs','upcoming'])
    async def upcoming(self, ctx, limit=7):
        '''!ctf (Optional: limit) : Returns 3-12 upcoming ctf events. Default = 7.'''
        if limit < 3:
            limit = 3

        if limit > 12:
            limit = 12

        begin = int(datetime.now(timezone.utc).timestamp()) + 259200  # Converting current time in UTC to Epoch time
        end = begin + 5184000  # Max end date is 2 months in the event max limit is not hit
        url = f'https://ctftime.org/api/v1/events/?limit={limit}&start={begin}&finish={end}'  # Skips first few days from present that are likely closed
        request = requests.get(url, headers=self.header)

        try:
            results = request.json()
        except json.decoder.JSONDecodeError:
            print(f'[{datetime.now(timezone.utc)}]  CTF Events were not properly fetched. HTTP Code: {request.status_code}')
            return await ctx.send('Oh no, I can\'t fetch the events! Please try again later.')

        embed = discord.Embed(
            title = 'CTFTime Events',
            description = f'Showing up to {limit} events',
            color = discord.Color.red()
        )

        for event in results:
            restrictions = event['restrictions']
            if restrictions != 'Open':
                continue

            #String formatting done below to change time to UTC, may base time off of Discord server location later on
            start = datetime.strptime(event['start'][:-6], "%Y-%m-%dT%H:%M:%S")
            start_formatted = start.strftime("%a, %d %B %Y at %H:%M (%I:%M%p) UTC")
            try:
                title = event['title']
                format = event['format']
                event_url = event['url']
                ctftime_url = event['ctftime_url']
            except KeyError:
                return await ctx.send('Sorry, there seems to be an issue retrieving events. Please try again!')
            embed.add_field(name=f'[{format}] {title} ({event_url})', value=f'{start_formatted}\nMore Info: {ctftime_url}', inline=False)
            embed.set_footer(text=f'Powered by the CTFTime API')
        await ctx.send(embed=embed)



    @commands.command(name='setteam', aliases=['teamset'])
    @commands.has_permissions(administrator=True)
    async def set_team(self, ctx, id):
        '''!setteam (CTFTime Team ID) : Sets team to track for use of !myteam. Use ID in team page URL, not team name!
        Note: This command can only be used by an administrator of the server.'''
        
        if not path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('{}')


        team_id = id
        url = f'https://ctftime.org/api/v1/teams/{team_id}/'
        request = requests.get(url, headers=self.header)

        try:
            results = request.json()
        except json.decoder.JSONDecodeError:
            team_id = None
            print(f'[{datetime.now(timezone.utc)}]  Set team request not properly fetched. HTTP Code: {request.status_code}')
            return await ctx.send('I can\'t seem to fetch that team! Make sure it is the proper team id, otherwise try again later.')
        
        with open(self.file_path, 'r') as f:
            try:
                team_db = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f'[{datetime.now(timezone.utc)}]  Local team DB not fetched properly.')
                return await ctx.send('Sorry, there seems to be an issue retrieving the team database.')

        team_db[str(ctx.guild.id)] = team_id

        with open(self.file_path, 'w') as f:
            json.dump(team_db, f)

        team_name = results['name']

        await ctx.send(f'Hi there, {team_name}! Team related commands will now be in regards to your team.')



    @commands.command(name='myteam', aliases=['teamstats'])
    async def team_stats(self, ctx):
        '''!myteam : Displays CTFTime rating and point stats of the given team'''

        if not path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('{}')


        with open(self.file_path, 'r') as f:
            try:
                team_db = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f'[{datetime.now(timezone.utc)}]  Local team DB not fetched properly.')
                return await ctx.send('Sorry, there seems to be an issue retrieving the team database.')

        
        if (str(ctx.guild.id) not in team_db) or (team_db[str(ctx.guild.id)] == None):
            return await ctx.send('You do not have a valid team set. Use !setteam [team_id] to set it, or !help setteam for more info.')

        team_id = team_db[str(ctx.guild.id)]
        url = f'https://ctftime.org/api/v1/teams/{team_id}/'
        request = requests.get(url, headers=self.header)

        try:
            results = request.json()
        except json.decoder.JSONDecodeError:
            print(f'[{datetime.now(timezone.utc)}]  Could not fetch team data. HTTP Code: {request.status_code}')
            return await ctx.send('Team data can not be fetched, please try again later!')
        
        team_name = results['name']

        bot_message = f'Team Info for {team_name} (Team ID: {team_id}):\n\n'
        embed = discord.Embed(
            title = team_name,
            url = f'https://ctftime.org/team/{team_id}',
            description = f'Team ID: {team_id}',
            color = discord.Color.red()
        )

        if not results['rating']:  #Checking if the "ratings" list in JSON file is empty. AKA: The team has no score for any year
            bot_message += 'Your team does not have any rating as of now.'
            embed.add_field(name='No Ratings', value='Compete in more CTFs to add rating points!')
        else:
            rating_info = {}
            for d in results['rating']:
                rating_info.update(d)
            
            for year in rating_info:
                rate_pts = round(rating_info[year]['rating_points'])
                rate_rank = rating_info[year]['rating_place']
                embed.add_field(name=f'{year} Rating', value=f'Points: {rate_pts}  -  Rank: {rate_rank}')
                embed.set_footer(text=f'Powered by the CTFTime API')
        await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(CTF(bot))