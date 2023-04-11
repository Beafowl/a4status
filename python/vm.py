from pywinauto import findwindows, keyboard, Application, mouse
from flask import Flask, request
import flask
import win32api
import time
import random
import threading

# this code will be run on the virtual machine
# create a an api server to control the state of the game

# pywinauto only works for windows

HOST = '192.168.178.141'
PORT = 5555

# positions of the mouse. Tuple has form (y,x)

SELECT_SERVER = (473, 283)
SELECT_CHANNEL_7 = (704, 443)
SELECT_CHARACTER = (205, 56)
CLOSE_NOSMALL = (953, 735)

# estimated times for transitioning to the next state (in seconds)
# because of the low end hardware, the numbers will be chosen leniently

TIME_START_NOSTALE = 30
TIME_TO_CHARACTER_SELECTION = 5
TIME_TO_GAME = 10
TIME_CLOSE_NOSTALE = 10

# waits an additional random time between 0 and 5 seconds in order to have
# natural transitions. t is the base waiting time
def wait_randomly(t):
    time.sleep(t + random.uniform(0.0, 5.0))

app = Flask(__name__)

@app.route('/close_game')
def close_game():

    window_handle = findwindows.find_windows(title_re="NosTale")[0]
    app = Application().connect(handle=window_handle)

    window = app.window(title='NosTale')
    window.set_focus()

    keyboard.send_keys('%{F4}')
    keyboard.send_keys('{ENTER}')
    return "Game has been closed"

@app.route('/start_game')
def start_game():

    window_handle = findwindows.find_windows(title_re="Gameforge")[0]
    app = Application().connect(handle=window_handle)

    # after focusing on the gameforge launcher, we can easily start
    # nostale by pressing tab and enter

    # tab selects an item, reset the selection by left clicking (TODO)

    window = app.window()
    window.set_focus()

    keyboard.send_keys('{TAB}')
    keyboard.send_keys('{ENTER}')

    return "Game has been started"

@app.route('/goto_game')
def goto_game():
    mouse.click(button='left', coords=SELECT_SERVER)
    mouse.click(button='left', coords=SELECT_CHANNEL_7)

    wait_randomly(TIME_TO_CHARACTER_SELECTION)

    mouse.double_click(button='left', coords=SELECT_CHARACTER)

    wait_randomly(TIME_TO_GAME)

    mouse.click(button='left', coords=CLOSE_NOSMALL)

    return "Server has been selected"

# this is needed in development in order to find out mouse positions for
# the automated script
@app.route('/get_mouse_position')
def get_mouse_position():
    y, x = win32api.GetCursorPos()
    return flask.jsonify({ "x": x, "y": y})

# for testing purposes
@app.route('/test')
def testing():
    mouse.move(coords=(283,472))
    return "Test"

# task in order to execute this in parallel
def restart_game_task(restart_type):

    restart_type = request.args.get('type')

    if restart_type == 'mukraju':
        wait_randomly(60)
    elif restart_type == 'maintenance':
        wait_randomly(30*60)
    
    close_game()
    wait_randomly(TIME_CLOSE_NOSTALE)
    start_game()
    wait_randomly(TIME_START_NOSTALE)
    goto_game()

# /restart_game?type=mukraju/maintenance
# in case of mukraju: Wait for 60 seconds before restarting the game, else wait for 30 mins
@app.route('/restart_game')
def restart_game():

    restart_type = request.args.get('type')

    threading.Thread(target=restart_game_task, args=(restart_type,)).start()

    return "Execution for restarting game has been started"

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)