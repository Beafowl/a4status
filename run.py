import discord
from detect import angel_status, demon_status
import os
from dotenv import load_dotenv, find_dotenv
from mss import mss
import threading
import time
from datetime import datetime
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
async def check_for_raid_angels(channel):

    while True:
        with mss() as sct:
            sct.shot(output="screenshot_angel.png")
            a = angel_status("./screenshot_angel.png")
            if a == -1:
                print("Raid")
                # send notification to discord server
                await channel.send("Engel haben jetzt Raid!")
                angels_raid_timestamp = datetime.now()
                time.sleep(216000)
                continue
            else:
                print("Currently checking for angels raid.. it is at " + str(a) + "%")
        time.sleep(60)
    return True

async def check_for_raid_demons(channel):

    while True:
        with mss() as sct:
            sct.shot(output="screenshot_demon.png")
            d = demon_status("./screenshot_demon.png")
            if d == -1:
                print("Raid")
                # send notification to discord server
                await channel.send("Dämonen haben jetzt Raid!")
                demons_raid_timestamp = datetime.now()
                time.sleep(216000)
                continue
            else:
                print("Currently checking for demons raid.. it is at " + str(d) + "%")
        time.sleep(60)
    return True

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # get channel
    channel = await client.fetch_channel(channel_id)

    # init threads
    #t_angels = threading.Thread(target=check_for_raid_angels, args=(channel,))
    #t_angels.start()

    #t_demons = threading.Thread(target=check_for_raid_demons, args=(channel,))
    #t_demons.start()

    #asyncio.run(check_for_raid_angels(channel))
    #asyncio.run(check_for_raid_demons(channel))
    
    task1 = asyncio.create_task(check_for_raid_demons(channel))
    task2 = asyncio.create_task(check_for_raid_angels(channel))

    #await task2

    #await check_for_raid_angels(channel)
    #await check_for_raid_demons(channel)

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
                angels_text = "Die Engel haben gerade Raid! Es hat um " + angels_raid_timestamp.strftime("%H:%M:%S") + " angefangen."
            else:
                angels_text = "Die Engel sind bei " + str(a) + "%."

            if d == -1:
                demons_text = "Die Dämonen haben gerade Raid!"
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

client.run(os.environ.get("TOKEN"))