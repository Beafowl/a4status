import discord
from detect import angel_status, demon_status
import os
from dotenv import load_dotenv, find_dotenv
from mss import mss
import threading
import time
from datetime import datetime
from datetime import timedelta
import cv2
import asyncio


config = load_dotenv(find_dotenv())
client = discord.Client()

channel_id = str(os.environ.get("CHANNEL"))

angels_raid_timestamp = datetime.now()
demons_raid_timestamp = datetime.now()

# 216000 seconds = 1 hour
# 108000 seconds = 30 minutes
# 180000 seconds = 50 minutes
def check_for_raid_angels():

    with mss() as sct:
        sct.shot(output="screenshot_angel.png")
        a = angel_status("./screenshot_angel.png")
        return a == -1

def check_for_raid_demons():

    with mss() as sct:
        sct.shot(output="screenshot_demon.png")
        d = demon_status("./screenshot_demon.png")
        return d == -1

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # get channel
    channel = await client.fetch_channel(channel_id)

    demons_have_raid = False
    angels_have_raid = False

    while True:
        await asyncio.sleep(29) 

        if check_for_raid_demons() and not demons_have_raid:
            demons_have_raid = True
            demons_raid_timestamp = datetime.now()
            await channel.send("Dämonen haben Raid!")

        if not check_for_raid_demons():
            demons_have_raid = False

        if check_for_raid_angels() and not angels_have_raid:
            angels_have_raid = True
            angels_raid_timestamp = datetime.now()
            await channel.send("Engel haben Raid!")

        if not check_for_raid_angels():
            angels_have_raid = False   

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
                angels_text = f"""Die Engel haben gerade Raid!\n
                Es hat um {angels_raid_timestamp.strftime("%H:%M")} angefangen.
                Der Raid öffnet um {(angels_raid_timestamp + timedelta(minutes=20)).strftime("%H:%M")},
                und man hat bis {(angels_raid_timestamp + timedelta(minutes=50)).strftime("%H:%M")} Zeit."""
            else:
                angels_text = "Die Engel sind bei " + str(a) + "%."

            if d == -1:
                demons_text = f"""Die Dämonen haben gerade Raid!\n
                Es hat um {demons_raid_timestamp.strftime("%H:%M:%S")} angefangen.
                Der Raid öffnet um {(demons_raid_timestamp + timedelta(minutes=20)).strftime("%H:%M")},
                und man hat bis {(demons_raid_timestamp + timedelta(minutes=50)).strftime("%H:%M")} Zeit."""
            else:
                demons_text = "Die Dämonen sind bei " + str(d) + "%."

            #print(angels_text)
            #print(demons_text)
            await message.channel.send(angels_text)
            await message.channel.send(demons_text)

    elif message.content == "!verify":
        angel_percent = cv2.imread("./output/angel.png")
        demon_percent = cv2.imread("./output/demon.png")
        con = cv2.hconcat([angel_percent, demon_percent])

        scale_percent = 400 # percent of original size
        width = int(con.shape[1] * scale_percent / 100)
        height = int(con.shape[0] * scale_percent / 100)
        dim = (width, height)
  
        # resize image
        con = cv2.resize(con, dim, interpolation = cv2.INTER_AREA)

        cv2.imwrite("./output/debug.png", con)
        await message.channel.send(file=discord.File('./output/debug.png'))

if __name__ == "__main__":
    client.run(os.environ.get("TOKEN"))