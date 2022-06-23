from datetime import datetime
import asyncio
from detect import angel_status, demon_status

async def on_ready(number):

    print("Hallo")

    # get channel

    demons_have_raid = False
    angels_have_raid = False

    global angels_raid_timestamp
    global demons_raid_timestamp

    angels_raid_timestamp = datetime.now()
    demons_raid_timestamp = datetime.now()

    while True:
        await asyncio.sleep(2) 

        if demon_status(f"./samples/image{str(number)}.jpg") == -1 and not demons_have_raid:
            demons_have_raid = True
            demons_raid_timestamp = datetime.now()
            print("Dämonen haben Raid")

        if not demon_status(f"./samples/image{str(number)}.jpg") == -1:
            demons_have_raid = False

        if angel_status(f"./samples/image{str(number)}.jpg") == -1 and not angels_have_raid:
            angels_have_raid = True
            angels_raid_timestamp = datetime.now()
            print("Engel haben Raid")

        if not angel_status(f"./samples/image{str(number)}.jpg") == -1:
            angels_have_raid = False
    return True




if __name__ == "__main__":
    asyncio.run(on_ready(6))