from detect import angel_status, demon_status, detect_raid_angel, detect_raid_demon
from mss import mss
from flask import Flask, render_template
import json

HOST = "0.0.0.0"
PORT = 80

app = Flask(__name__, static_url_path='/static')


# api, returns important information for the website to render
@app.route('/a4status')
def index():
    f = open('./data.json')
    # open json file and return its contents
    a4status = json.load(f)

    f.close()
    return a4status

# this is for loading the actual website
@app.route('/')
def home():
    return render_template('index.html')
    

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)