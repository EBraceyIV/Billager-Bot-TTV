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
import pyttsx3
# TwitchIO -> Used for the major framework of the bot functionality
from twitchio.ext import commands
# GPIOZero -> Send a signal to Arduino from one of the Pi's GPIO pins
from gpiozero import LED

# TODO: Configure subs and bits TTS
# TODO: Expand general usage, e.g., add more commands
# TODO: Work on automod removal of spam messages
#   # Example for regexing --> xcqw12345432186: W͎annͭa beco̻me ̖faͭm͖ous?̥ Buy f̧ọllowers, pr̊imes an̡d vie̷w͠ers ͫon https://clck.ru/R9gQV (bigfollows .com)!
# TODO: Have fun (?)

# Load sensitive info for running the bot from a config file
with open("config.JSON") as config_file:
    config = json.load(config_file)

# Start up the tts engine
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)

# Define the TTS indicator pin
tts_indicator = LED(4)


def chatter(msg) -> None:
    # Tell Arduino that TTS is running
    tts_indicator.on()

    # Run the tts and log start and stop to console
    print("TTS: " + str(msg))
    engine.say(str(msg))
    engine.runAndWait()
    print("Done talking.")

    # Tell Arduino that TTS is off
    tts_indicator.off()


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
        if message.tags is not None:
            if "msg-id" in message.tags:
                if message.tags["msg-id"] == "highlighted-message":
                    print("[HIGHLIGHTED]" + " " + message.author.name + ": " + message.content)
            else:
                print(message.author.name + ": " + message.content)
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        try:
            # Server response, just let it happen
            if data["type"] == "PONG":
                pass
            # Handle channel point redemptions
            elif data["type"] == "MESSAGE":
                # The content of the pubsubs come through as JSON data, convert to a dict and then sorted through
                message = json.loads(data["data"]["message"])
                # The type of event is described most readily in the "topic" field
                # Process incoming channel points events
                if data["data"]["topic"] == "channel-points-channel-v1.75246492":
                    # Parse relevant info from the data received
                    user = message["data"]["redemption"]["user"]["display_name"]
                    user_input = message["data"]["redemption"]["user_input"]
                    reward = message["data"]["redemption"]["reward"]["title"]
                    # Clatterbox messages are split up by character count for quality control / spam prevention / etc
                    # More characters require more points to redeem
                    # Users are notified if they are using too many characters for their redemption tier
                    if reward == "Clatter S":
                        if len(user_input) <= 100:
                            chatter(user_input)
                        else:
                            await self.channel.send(f"@{user}, too many characters! "
                                                    f"This tier is only for 100 characters or less. "
                                                    f"You need to redeem a higher tier for that many.")
                    elif reward == "Clatter M":
                        if len(user_input) <= 250:
                            chatter(user_input)
                        else:
                            await self.channel.send(f"@{user}, too many characters! "
                                                    f"This tier is only for 250 characters or less. "
                                                    f"You need to redeem a higher tier for that many.")
                    elif reward == "Clatter L":
                        chatter(user_input)
                    else:
                        pass
                # Process incoming bits events
                elif data["data"]["topic"] == "channel-bits-events-v2.75246492":
                    if message["data"]["is_anonymous"] == "false":
                        user = message["data"]["user_name"]
                        await self.channel.send(f"Thank you for the bits {user}, they fuel my brain like gasoline.")
                    else:
                        await self.channel.send("Thank you for those secret bits, I use them like bath bombs.")
                # Process incoming subscription events
                elif data["data"]["topic"] == "channel-subscribe-events-v1.75246492":
                    user = message["user_name"]
                    await self.channel.send(f"Thanks for that spicy subscription, @{user}! I use them to fund my "
                                            f"next cybernetic enhancement.")
                else:
                    # Print other MESSAGE messages to console for sorting through later
                    pprint(data)
            # Print other events to console for sorting through later
            else:
                pprint(data)
        except Exception as e:
            print(f"Some error happened: {e}")
            pprint(data)

# Bits text:
    # Thank you for the bits {username}, they fuel my brain like gasoline.
    # Wow, some bits. Thanks, {username}, maybe I can eat tonight.
    #

# Subs text:
    # {username} just subscribed for the first time, what a rush pog pog
    # {username} just subscribed for {#} months, wowowowowow
    # {username}

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
