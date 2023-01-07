import discord
from detect import detect_raid_angel, detect_raid_demon, angel_status, demon_status
import os
from dotenv import load_dotenv, find_dotenv
from mss import mss
from datetime import datetime
from datetime import timedelta
import cv2
import asyncio
import json


config = load_dotenv(find_dotenv())
client = discord.Client()

channel_id = str(os.environ.get("CHANNEL"))

# 216000 seconds = 1 hour
# 108000 seconds = 30 minutes
# 180000 seconds = 50 minutes
def check_for_raid_angels():

    with mss() as sct:
        sct.shot(output="screenshot_angel.png")
        return detect_raid_angel("screenshot_angel.png")

def check_for_raid_demons():

    with mss() as sct:
        sct.shot(output="screenshot_demon.png")
        return detect_raid_demon("screenshot_demon.png")

def print_with_timestamp(string):
    current_time = datetime.now()
    print(f"[{current_time.hour}:{current_time.second}] {string}")


@client.event
async def on_ready():
    print_with_timestamp(f'{client.user} has connected to Discord!')

    # get channel
    channel = await client.fetch_channel(channel_id)

    demons_have_raid = False
    angels_have_raid = False

    while True:
        await asyncio.sleep(29)

        # serialize the status to json and save it to a file

        #status_object = f'"angel_status": {angel_status('./screenshot_angel.png')}, "demon_status": {demon_status('./screenshot_demon.png')}'

        #status_object_json = json.loads(status_object)

        # detecting an angel raid can be done 100%, so check it

        if check_for_raid_angels() and not angels_have_raid:        
            angels_have_raid = True
            angels_raid_timestamp = datetime.now()
            print_with_timestamp("Engel haben Raid!")
            await channel.send(f"Engel haben Raid!")

        if not check_for_raid_angels():
            angels_have_raid = False

        if check_for_raid_demons() and not demons_have_raid:
            demons_have_raid = True
            print_with_timestamp("Dämonen haben Raid!")
            await channel.send("Dämonen haben Raid!")

        if not check_for_raid_demons():
            demons_have_raid = False

@client.event
async def on_message(message):
    if message.content == "!a4" or message.content == "!status":
        with mss() as sct:
            sct.shot(output="screenshot.png")
            a = angel_status("./screenshot.png")
            d = demon_status("./screenshot.png")
        
            demons_text = ""
            angels_text = ""

            # debug print

            #print(a)
            #print(check_for_raid_angels())
            #print(d)
            #print(check_for_raid_demons())


            if check_for_raid_angels():
                angels_text = "Die Engel haben gerade Raid!"
            else:
                angels_text = "Die Engel sind bei " + str(a) + "%."

            if check_for_raid_demons():
                demons_text = "Die Dämonen haben gerade Raid!"
            else:
                demons_text = "Die Dämonen sind bei " + str(d) + "%."

            if a == -1 and not check_for_raid_angels():
                angels_text = f"Irgendwas ist bei Auslesen der Engel schiefgelaufen. Einmal Alamad Bescheid geben"

            if d == -1 and not check_for_raid_demons():
                demons_text = f"Irgendwas ist bei Auslesen der Dämonen schiefgelaufen. Einmal Alamad Bescheid geben"

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