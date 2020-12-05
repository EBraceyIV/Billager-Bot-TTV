import pyttsx3
import sys

# The filename and each individual string in the user message is treated as a separate argument,
# this separates the message are merges it into one string for the tts engine
msg = sys.argv[1:]
msg = " ".join(msg)
print(msg)
# Start up the tts engine
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.8)
# Run the tts and log start and stop to console
print("Running tts...")
engine.say(str(msg))
engine.runAndWait()
print("Done talking.")

