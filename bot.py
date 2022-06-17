import discord
from detect import angel_status, demon_status
import os
from dotenv import load_dotenv, find_dotenv
from mss import mss
import threading
import time
from datetime import datetime
import cv2

config = load_dotenv(find_dotenv())
client = discord.Client()

angels_raid_timestamp = datetime.now()
demons_raid_timestamp = datetime.now()

# 216000 seconds = 1 hour
# 108000 seconds = 30 minutes
# 180000 seconds = 50 minutes
async def check_for_raid_angels():

    while True:
        with mss() as sct:
            sct.shot(output="screenshot_angel.png")
            a = angel_status("./screenshot_angel.png")
            if a == -1:
                print("Raid")
                # send notification to discord server
                channel = client.get_channel(134343345815289856)
                await channel.send("Engel haben jetzt Raid!")
                angels_raid_timestamp = datetime.now()
                time.sleep(216000)
                continue
        time.sleep(60)

async def check_for_raid_demons():

    while True:
        with mss() as sct:
            sct.shot(output="screenshot_demon.png")
            d = demon_status("./screenshot_demon.png")
            if d == -1:
                print("Raid")
                # send notification to discord server
                channel = client.get_channel(134343345815289856)
                await channel.send("Dämonen haben jetzt Raid!")
                demons_raid_timestamp = datetime.now()
                time.sleep(216000)
                continue
        time.sleep(60)

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
                angels_text = "Die Engel haben gerade Raid! Es hat um " + angels_raid_timestamp.strftime("%H:%M:%S") + " angefangen."
            else:
                angels_text = "Die Engel sind bei " + str(a) + "%."

            if d == -1:
                demons_text = "Die Dämonen haben gerade Raid!"
            else:
                demons_text = "Die Dämonen sind bei " + str(d) + "%."

            print(angels_text)
            print(demons_text)

    elif message.content == "!verify":
        angel_percent = cv2.imread("./output/angel.png")
        demon_percent = cv2.imread("./output/demon.png")
        con = cv2.hconcat([angel_percent, demon_percent])
        cv2.imwrite("./output/debug.png", con)
        await message.channel.send(file=discord.File('./output/debug.png'))

t_angels = threading.Thread(target=check_for_raid_angels)
t_angels.start()

t_demons = threading.Thread(target=check_for_raid_demons)
t_demons.start()

client.run(os.environ.get("TOKEN"))