from detect import angel_status, demon_status, detect_raid_angel, detect_raid_demon
from mss import mss
import json
import time
from datetime import datetime, date, timedelta

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
        "opened": datetime.now(),
        "closes_in": 0
    },
    "demons": {
        "percentage": 0,
        "opened": datetime.now(),
        "closes_in": 0
    }
}

raid_already_detected_demons = False
raid_already_detected_angels = False

def main():

    while 1:
        now = datetime.now()
        # first do a screenshot and get both statuses
        with mss() as sct:
            screenshot = sct.shot()

            # angel status and demon status can detect the values of the counter, but not the actual raid

            a_value = angel_status(screenshot)
            d_value = demon_status(screenshot)

            # for that we need detect raid angel and detect raid demon
            # they return true if there is a raid and false else 

            if a_value == -1:
                a_status = detect_raid_angel(screenshot)
                if a_status:
                    a_value = 100
                else:
                    a_value = -1

            if d_value == -1:
                d_status = detect_raid_demon(screenshot)
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
            a4status["angels"]["opened"] = now


        if d_value == 100 and not raid_already_detected_demons:
            raid_already_detected_demons = True
            a4status["demons"]["opened"] = now

        closing_time_demons = a4status["demons"]["opened"] + timedelta(minutes=60)
        minutes_left_demons = divmod((closing_time_demons - now).total_seconds(), 60)[0]
        a4status["demons"]["closes_in"] = minutes_left_demons + 1

        closing_time_angels = a4status["angels"]["opened"] + timedelta(minutes=60)
        minutes_left_angels = divmod((closing_time_angels - now).total_seconds(), 60)[0]
        a4status["angels"]["closes_in"] = minutes_left_angels + 1

        # save into a json file

        with open("data.json", "w") as outfile:
            outfile.write(json.dumps(a4status, indent=4, cls=DateTimeEncoder))
        time.sleep(29)


if __name__ == "__main__":
    main()
