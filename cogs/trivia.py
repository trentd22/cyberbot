import discord
from discord.ext import commands
import random
import time
import json
from os import path
from asyncio import TimeoutError
from operator import itemgetter



class Leaderboard:

    def __init__(self, guild):
        self.guild = guild
        
        self.fp = path.dirname(__file__)
        self.rp = f'data/lb_{self.guild}.json'
        self.file_path = path.join(self.fp, self.rp)

        if not path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('{}')

    def update_user(self, user):
        with open(self.file_path, 'r') as f:
            lb = json.load(f)
   
        if user in lb:
            lb[user] += 1
        else:
            lb[user] = 1

        total = lb[user]

        with open(self.file_path, 'w') as f:
            json.dump(lb, f)

        return total

    def lookup_user(self, user):
        with open(self.file_path, 'r') as f:
            lb = json.load(f)

        return lb.get(user, None)

    def send_leaderboard(self):
        with open(self.file_path, 'r') as f:
            lb = json.load(f)

        #itemgetter() used over lambda expression for slightly better time complexity
        return {k : v for k,v in sorted(lb.items(), reverse=True, key=itemgetter(1))}
    


class Trivia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fp = path.dirname(__file__)
        self.rp = 'data/trivia.json'
        self.file_path = path.join(self.fp, self.rp)
        
    
    @commands.command(name='trivia')
    async def trivia_question(self, ctx):
        '''!trivia : Retrives a multiple-choice or fill-in-the-blank trivia question.
        Multiple Choice: React to the question with the reaction shown to the left of your answer.
        Fill-in-the-blank: Simply type your answer in the chat, do not prepend any commands or extra text.'''
        def check_blank(m):
            #Checks if user message is an answer to trivia, and that it is the correct answer (case-insensitive)
            return (m.channel == ctx.message.channel) and (x.lower() in m.content.strip().lower() for x in answers) and (bot_message.author.id != m.author.id)
        
        def check_multi(reaction, user):
            #Checks if user reaction is equal to the reaction related to the correct answer
            return (str(reaction.emoji) == choice_dict[answer]) and (bot_message.id == reaction.message.id) and (bot_message.author.id != user.id)
        
        
        with open(self.file_path, 'r') as f:
            t_json = json.load(f)

        t_question = t_json.get(str(random.randrange(0, len(t_json))))
        
        question = t_question['question']
        
        bot_message = f'Trivia:\n\n{question}'
        

        if t_question['multi_choice']:
            choice_num = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', \
                '5️⃣', '6️⃣', '7️⃣', '8️⃣')
            choice_dict = {}

            answer = t_question['answer']
            choices = t_question['others']
            choices.append(answer)

            choice_count = 0
            bot_message += '\n\nChoices:\n'
            while choices:
                number = choice_num[choice_count]
                c = choices.pop(random.randrange(0, len(choices)))

                choice_dict[c] = number
                bot_message += f'{number}  {c}\n'
                choice_count += 1

            bot_message = await ctx.send(bot_message)

            for r in list(choice_dict.values()):
                await bot_message.add_reaction(r)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check_multi, timeout=30.0)
            except TimeoutError:
                return await ctx.send('Time\'s up! No one was awarded for that trivia question.')
        else:
            answers = t_question['answers']

            await ctx.send(bot_message)

            try:
                msg = await self.bot.wait_for('message', check=check_blank, timeout=30.0)
                user = msg.author
            except TimeoutError:
                return await ctx.send('Time\'s up! No one was awarded for that trivia question.')


        board = Leaderboard(ctx.guild.id)

        total_pts = board.update_user(str(user.id))

        await ctx.send(f'{user.display_name} got it right! Total Points: {total_pts}.')

    
    @commands.command(name='check')
    async def check(self, ctx, member : discord.Member=None):
        '''!check (Optional: @member) : Check the amount of trivia points someone has.
        Mention the person using @[their_display_or_username_here] to search someone.
        If no member is specified, this command will check your own point amount.'''
        
        board = Leaderboard(ctx.guild.id)
        
        
        if member is None:
            points = board.lookup_user(str(ctx.author.id))

            if points is None:
                await ctx.send(f'You have no points on the leaderboard.')
            else:
                await ctx.send(f'You have {points} points from trivia!')
        else:
            points = board.lookup_user(str(member.id))

            if points is None:
                await ctx.send(f'{member.display_name} has no points on the leaderboard.')
            else:
                await ctx.send(f'{member.display_name} has {points} points from trivia!')

    
    @commands.command(name='leaders')
    async def leaders(self, ctx):
        '''!leaders : Shows up to the top 10 trivia leaders in the server, in descending order.
        The name used on the leaderboard is the user's server nickname. If the user changes
        their nickname, they will retain their points and the leaderboard will show their
        new nickname.'''
        board = Leaderboard(ctx.guild.id)

        board_dict = board.send_leaderboard()

        bot_message = 'Trivia Leaders:\n'

        count = 0

        for key in board_dict:
            if count == 10:
                break 
            user = ctx.guild.get_member(int(key))
            bot_message += f'{user.display_name}  -  {board_dict[key]} Points\n'
            count += 1
        
        await ctx.send(bot_message)


def setup(bot):
    bot.add_cog(Trivia(bot))