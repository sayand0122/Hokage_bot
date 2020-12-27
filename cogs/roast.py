import discord
from discord.ext import commands
import random


class roast(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.insults = insult

    @commands.Cog.listener()
    async def on_ready(self):
        print('Roast cog is ready')

    @commands.command(aliases=['slam'])
    async def roast(self, ctx, *, link):
        embed = discord.Embed(title='Roast', color=0x11ad4b)
        embed.add_field(
            name='😈', value=f'{link} , {random.choice(self.insults)}')
        await ctx.send(embed=embed)


insult = ["You have your entire life to be a jerk. Why not take today off?",
          "Your ass must be pretty jealous of all the shit that comes out of your mouth.",
          "Remember when I asked for your opinion? Me neither",
          "Some day you’ll go far—and I really hope you stay there.",
          "I’m trying my absolute hardest to see things from your perspective, but I just can’t get my head that far up my ass.",
          " Sometimes it’s better to keep your mouth shut and give the impression that you’re stupid than open it and remove all doubt.",
          "I’m not a proctologist, but I know an asshole when I see one.",
          "You only annoy me when you’re breathing, really.",
          "Do yourself a favor and ignore anyone who tells you to be yourself. Bad idea in your case.",
          "I don’t know what your problem is, but I’m guessing it’s hard to pronounce.",
          "Do your parents even realize they’re living proof that two wrongs don’t make a right?",
          "Remember that time I said I thought you were cool? I lied.",
          " Everyone’s entitled to act stupid once in awhile, but you really abuse the privilege.",
          " I can’t help imagining how much awesomer the world would be if your dad had just pulled out in time.",
          "Do you ever wonder what life would be like if you’d gotten enough oxygen at birth?",
          "Please, save your breath. You’ll probably need it to blow up your next date.",
          "Can you die of constipation? I ask because I’m worried about how full of shit you are.",
          "Good story, but in what chapter do you shut the fuck up?",
          "Don’t hate me because I’m beautiful. Hate me because your boyfriend thinks so.",
          "Were you born on the highway? That is where most accidents happen.",
          "Please, keep talking. I only yawn when I’m super fascinated.",
          " Jesus might love you, but everyone else definitely thinks you’re an idiot",
          "Sorry, I didn’t get that. I don’t speak bullshit.",
          "The only way you’ll ever get laid is if you crawl up a chicken’s ass and wait.",
          "If ignorance is bliss, you must be the happiest person on the planet.",
          "Are you always such an idiot, or do you just show off when I’m around?",
          "There are some remarkably dumb people in this world. Thanks for helping me understand that.",
          "I could eat a bowl of alphabet soup and shit out a smarter statement than whatever you just said.",
          "I was pro life. Then I met you.",
          "You’re about as useful as a screen door on a submarine.",
          "Whenever we hang out, I remember that God really does have a sense of humor.",
          "It’s kind of hilarious watching you try to fit your entire vocabulary into one sentence.",
          "Please just tell me you don’t plan to home-school your kids. Cuz then they'll just end-up dumb like you....",
          " You always bring me so much joy—as soon as you leave the room",
          " I was hoping for a battle of wits but it would be wrong to attack someone who’s totally unarmed.",
          "I’d tell you how I really feel about you, but I wasn’t born with enough middle fingers to express myself in this case.",
          "Stupidity’s not a crime, so feel free to go.",
          "I’d tell you to go fuck yourself, but that would be cruel and unusual punishment.",
          "You have the right to remain silent because whatever you say will probably be stupid anyway.",
          "Your family tree must be a cactus ‘cause you’re all a bunch of pricks.",
          " I was going to give you a nasty look but I see that you’ve already got one.",
          "You’re about as useful as an ashtray on a motorcycle",
          "People like you are the reason I’m on medication.",
          "I believed in evolution until I met you.",
          " If I threw a stick, you’d leave, right?",
          "You’ll never be the man your mom is.",
          "Everybody is better than you.....",
          "Jesus loves you... But everyone else thinks you're an asshole",
          "When you stare into the mirror, even your reflection looks away...",
          "Wow you have a really smart brain, wait no, I take that back, you have a really smart mouth",
          "I'd call you a donkey but you look more like shrek.",
          "If your so smart then you’d realize your proof of reverse evolution"]


def setup(bot):
    bot.add_cog(roast(bot))
