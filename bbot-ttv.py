# EDBIV 2020
# Twitch.tv chat bot (Billager Bot) made using twitchIO and twitchAPI
# Primary feature is allowing chat members to control a talking box on my desk. The box contains an Arduino board that
# controls a servo. The servo rotates a mouth piece in and out of a gap in the front of the box to mimic a mouth moving.
# Their desired message gets played through text-to-speech while the mouth is open.
# This is fairly sloppy I will admit but this whole project went from an idea in my head to a functioning blend of
# hardware and software in about a week and a half. I intend to clean up / improve the code in time.

# Standard library
import os
from pprint import pprint
import json
from time import sleep
import pyttsx3
# TwitchIO -> Used for the major framework of the bot functionality
from twitchio.ext import commands
# Pyfirmata -> Used to control the attached Arduino UNO
from pyfirmata import Arduino
from pyfirmata import SERVO

# Load sensitive info for running the bot from a config file
with open("config.JSON") as config_file:
    config = json.load(config_file)

# Initialize the Arduino, be sure to use the correct USB address
board = Arduino('COM4')
board.digital[6].mode = SERVO

# Start up the tts engine
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.8)


def chatter(msg) -> None:
    move_servo(60)
    # Run the tts and log start and stop to console
    print("Running tts...")
    engine.say(str(msg))
    engine.runAndWait()
    print("Done talking.")
    move_servo(0)
    sleep(0.1)


# Function to rotate servo
def move_servo(a) -> None:
    board.digital[6].write(a)


# Main bot class, inherited from twitchIO's commands extension
class TwitchBot(commands.Bot):
    def __init__(self):
        # Sensitive information loaded from config JSON
        super().__init__(irc_token=config["irc_token"],
                         client_id=config["client_id"],
                         nick='Billager_Bot',
                         prefix='+',  # May or may not keep as is. Discord uses "bb:", but I feel as though Twitch
                                      # would benefit more from having a shorter prefix.
                         initial_channels=["kiwi_shark"])

    # Load cogs on initialization and send confirmation that bot is live to chat
    async def event_ready(self):
        self.channel = self.get_channel("kiwi_Shark")
        for cog in os.listdir("cogs"):
            if cog.endswith(".py"):  # Safety check to not process any non-cog files
                try:
                    self.load_module(f"cogs.{cog[:-3]}")
                    print(f"Cog loaded: {cog}")
                except Exception as e:  # Report any cog loading errors to the console
                    print(f"Error loading cog: \"{cog}\"")
                    print(f"Error: {e}")
        print("Done loading cogs, bot active.")
        # token from https://twitchtokengenerator.com
        await self.pubsub_subscribe(config["appauth_token"], f"channel-points-channel-v1.75246492",
                                                             f"channel-bits-events-v2.75246492",
                                                             f"channel-subscribe-events-v1.75246492")
        await self.channel.send("Billager Bot, logging on!")

    # Processes all incoming commands as case-insensitive
    async def handle_commands(self, message, ctx=None):
        # Separates "prefix:command" from the following text/args
        msg = message.content.split(maxsplit=1)
        # Fix the command to be lowercase for handling
        message.content = f"{msg[0].lower()} {msg[1:]}"
        await super().handle_commands(message)

    # Record incoming messages to console for logging
    async def event_message(self, message):
        print(message.author.name + ": " + message.content)
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        # The content of the pubsubs come through as JSON data, which gets converted to a dict and then sorted through
        if data["type"] == "PONG":
            pass
        elif data["type"] == "MESSAGE":
            message = json.loads(data["data"]["message"])
            if message["type"] == "reward-redeemed":
                user_input = message["data"]["redemption"]["user_input"]
                user_input_chars = len(user_input)
                reward = message["data"]["redemption"]["reward"]["title"]
                if reward == "Chatter":
                    if user_input_chars <= 100:
                        chatter(user_input)
                    else:
                        await self.channel.send("That's too many characters! This tier is only for 100 characters or "
                                                "less. You need to redeem a higher tier for that many.")
                elif reward == "Chatter M":
                    if user_input_chars <= 250:
                        chatter(user_input)
                    else:
                        await self.channel.send("That's too many characters! This tier is only for 250 characters or "
                                                "less. You need to redeem a higher tier for that many.")
                elif reward == "Chatter L":
                    chatter(user_input)
                else:
                    pass
        else:
            pprint(data)

    # Show me those errors front and center (Not 100% if this works as intended)
    async def event_error(self, error, data=None):
        print(f"Looks an error! This is it: {error}")
        raise error

    # Handle any requests for commands that don't exist
    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            print(f"The command {ctx.message} doesn't seem to exist.")


# Run the actual bot
bot = TwitchBot()
bot.run()
