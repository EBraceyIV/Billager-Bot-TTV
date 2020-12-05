import twitchio
import pyttsx3
from pyfirmata import Arduino, util
from pyfirmata import SERVO
from time import sleep
from twitchio.ext import commands

# board = Arduino('COM4')
# board.digital[6].mode = SERVO
#
#
# def move_servo(a):
#     board.digital[6].write(a)


# Cog class, not subclassed
class Auto:
    def __init__(self, bot):
        self.bot = bot

    # Simple ping to test with
    @commands.command(name="ping")
    async def test_ping(self, ctx):
        await self.bot.channel.send("Ponggers!")

    # @commands.command(name="chat")
    # async def test_chat(self, ctx, *, msg: str):
    #     engine = pyttsx3.init()
    #     sleep(1)
    #     engine.setProperty('rate', 125)
    #     engine.setProperty('volume', 0.8)
    #     # START MOTION
    #     move_servo(60)
    #
    #     # SPEAK
    #     engine.say(msg)
    #     engine.runAndWait()
    #     print("No talky")
    #     move_servo(0)
    #     sleep(1)
    #     engine.stop()


def prepare(bot):
    bot.add_cog(Auto(bot))
