from twitchio.ext import commands
import random

# Cog class, not subclassed
class General:
    def __init__(self, bot):
        self.bot = bot

    # Simple ping to test with
    @commands.command(name="ping")
    async def ping(self, ctx):
        await self.bot.channel.send("Ponggers!")

    @commands.command(name="clatterbox")
    async def clatter(self, ctx):
        await self.bot.channel.send("Clatterbox is a physical TTS gimmick that I created. Using channel points (bits, "
                                    "subs, etc. in development) you can request a message. Clatter S, M, and L give "
                                    "you 100, 250, and 500 characters for your message, respectively.")

    @commands.command(name="links")
    async def links(self, ctx):
        await self.bot.channel.send("See my wacky YouTube uploads :)\n"
                                    "https://www.youtube.com/channel/UCnDjyvy0DWJaTwvWonSq_0g")

    @commands.command(name="clip")
    async def clip(self, ctx):
        clipComment = ["Wow this is a fun one", "A real knee-slapper", "5/5 stars, top tier content"]
        clips = ["https://www.twitch.tv/kiwi_shark/clip/PeppyStylishNoodleRalpherZ",
                 "https://www.twitch.tv/kiwi_shark/clip/YummyRichDinosaurKeyboardCat",
                 "https://www.twitch.tv/kiwi_shark/clip/WrongConsideratePoxVoteNay",
                 "https://www.twitch.tv/kiwi_shark/clip/SteamyGlamorousFloofOptimizePrime"]
        await self.bot.channel.send(random.choice(clipComment) + "\n" + random.choice(clips))


def prepare(bot):
    bot.add_cog(General(bot))
