import discord
from detect import angel_status, demon_status
import os
from dotenv import load_dotenv, find_dotenv
from mss import mss

config = load_dotenv(find_dotenv())

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content == "!a4" or message.content == "!status":
        with mss() as sct:
            sct.shot(output="screenshot.png")
            a = angel_status("./screenshot.png")
            d = demon_status("./screenshot.png")
        
            demons_text = ""
            angels_text = ""

            if a == -1:
                angels_text = "Die Engel haben gerade Raid!"
            else:
                angels_text = "Die Engel sind bei " + str(a) + "%."

            if d == -1:
                demons_text = "Die Dämonen haben gerade Raid!"
            else:
                demons_text = "Die Dämonen sind bei " + str(d) + "%."

            print(angels_text)
            print(demons_text)

    elif message.content == "!verify":
        print("todo")


client.run(os.environ.get("TOKEN"))