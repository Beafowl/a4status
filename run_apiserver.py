from detect import angel_status, demon_status, detect_raid_angel, detect_raid_demon
from mss import mss
from flask import Flask
import json

HOST = "0.0.0.0"
PORT = 80

app = Flask(__name__)

@app.route('/a4status')
def index():
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
                a_value = "Das Tor zur Raidhöhle ist offen!"
            else:
                a_value = "Ein Fehler ist aufgetreten."

        if d_value == -1:
            d_status = detect_raid_demon('./screenshot.png')
            if d_status:
                d_value = "Das Tor zur Raidhöhle ist offen!"
            else:
                d_value = "Ein Fehler ist aufgetreten."
    
    a4_status = {

        "angel_status": a_value,
        "demon_status": d_value
    }
    return json.dumps(a4_status)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)