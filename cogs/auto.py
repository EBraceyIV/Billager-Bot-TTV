from twitchio.ext import commands
from pprint import pprint


# Cog class, not subclassed
class Auto:
    def __init__(self, bot):
        self.bot = bot

    # async def event_raw_pubsub(self, data):
    #     # Server response, just let it happen
    #     if data["type"] == "PONG":
    #         pass
    #     else:
    #         pprint(data)

    # async def event_message(self, message):
    #     if "msg-id" in message.tags:
    #         if message.tags["msg-id"] == "highlighted-message":
    #             print(message.author.name + ": " + message.content + " [HIGHLIGHTED]")
    #     else:
    #         print(message.author.name + ": " + message.content)

    # @commands.command(name="links")
    # async def links(self, ctx):
    #     await self.bot.channel.send("")


def prepare(bot):
    bot.add_cog(Auto(bot))
