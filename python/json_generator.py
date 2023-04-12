from detect import angel_status, demon_status, detect_raid_angel, detect_raid_demon
from mss import mss
import json
import time
from datetime import datetime, date, timedelta
import requests

HOST = "192.168.178.141"
PORT = 5555

checked_for_lord_mukraju = False

# subclass JSONEncoder
# for serializing date to json
class DateTimeEncoder(json.JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()

# important variables that will be saved in the file
# percentage: 0-99 is actual percentage, 100 is open, -1 is error
# closes_in is in minutes, an integer is enough
a4status = {

    "angels": {
        "percentage": 0,
        "closes_in": 0
    },
    "demons": {
        "percentage": 0,
        "closes_in": 0
    }
}

def main():

    raid_already_detected_demons = False
    raid_already_detected_angels = False
    opened_demons = datetime.now()
    opened_angels = datetime.now()

    while 1:
        now = datetime.now()
        # first do a screenshot and get both statuses
        with mss() as sct:
            sct.shot(output="screenshot.png")

            # angel status and demon status can detect the values of the counter, but not the actual raid

            a_value = angel_status("./screenshot.png")
            d_value = demon_status("./screenshot.png")

            # for that we need detect raid angel and detect raid demon
            # they return true if there is a raid and false else 

            if a_value == -1:
                a_status = detect_raid_angel('./screenshot.png')
                if a_status:
                    a_value = 100
                else:
                    a_value = -1

            if d_value == -1:
                d_status = detect_raid_demon('./screenshot.png')
                if d_status:
                    d_value = 100
                else:
                    d_value = -1
        
        # after fetching values from the screenshot, save into the dictionary

        a4status["angels"]["percentage"] = a_value
        a4status["demons"]["percentage"] = d_value

        if a_value < 100:
            raid_already_detected_angels = False

        if d_value < 100:
            raid_already_detected_demons = False

        if a_value == 100 and not raid_already_detected_angels:
            raid_already_detected_angels = True
            opened_angels = now


        if d_value == 100 and not raid_already_detected_demons:
            raid_already_detected_demons = True
            opened_demons = now

        closing_time_demons = opened_demons + timedelta(minutes=60)
        minutes_left_demons = divmod((closing_time_demons - now).total_seconds(), 60)[0] + 1
        a4status["demons"]["closes_in"] = minutes_left_demons

        closing_time_angels = opened_angels + timedelta(minutes=60)
        minutes_left_angels = divmod((closing_time_angels - now).total_seconds(), 60)[0] + 1
        a4status["angels"]["closes_in"] = minutes_left_angels

        # save into a json file
        with open("data.json", "w", encoding='utf-8') as outfile:
            json.dump(a4status, outfile, indent=4, ensure_ascii=False)

        # logic for restarting the game in case of an error

        if a4status["angels"]["percentage"] == -1 and a4status["demons"]["percentage"] == -1:
            if not checked_for_lord_mukraju:
                # first assume lord mukraju, restart and wait for 60 seconds
                checked_for_lord_mukraju = True
                requests.get(f'http://{HOST}:{PORT}/restart_game?duration=60')
                time.sleep(1*60+5)
                continue
            else:
                # we will be here in the second run, so we can assume maintenance
                requests.get(f'http://{HOST}:{PORT}/restart_game?duration=1800')
                time.sleep(30*60+5)
                continue

        checked_for_lord_mukraju = False
        time.sleep(29)

if __name__ == "__main__":
    main()