from detect import angel_status, demon_status, detect_raid_angel, detect_raid_demon
from mss import mss
from flask import Flask
import json
from flask import jsonify

HOST = "0.0.0.0"
PORT = 80

app = Flask(__name__)


@app.route('/a4status')
def index():
    f = open('./data.json')
    # open json file and return its contents
    a4status = json.load(f)

    f.close()
    return a4status


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)