from pywinauto import findwindows, keyboard, Application, mouse
from flask import Flask
import flask
import win32api
import time

# this code will be run on the virtual machine
# create a an api server to control the state of the game

# positions of the mouse

SELECT_SERVER = (283, 473)
SELECT_CHANNEL_7 = (443, 704)
SELECT_CHARACTER = (56, 205)
CLOSE_NOSMALL = (735, 953)

# estimated times for transitioning to the next state (in seconds)

TIME_START_NOSTALE = 20
TIME_TO_CHARACTER_SELECTION = 3
TIME_TO_GAME = 5

# pywinauto only works for windows

HOST = '192.168.178.141'
PORT = 5555

app = Flask(__name__)

@app.route('/close_nostale')
def close_nostale():

    window_handle = findwindows.find_windows(title_re="NosTale")[0]
    app = Application().connect(handle=window_handle)

    window = app.window(title='NosTale')
    window.set_focus()

    keyboard.send_keys('%{F4}')
    keyboard.send_keys('{ENTER}')
    return "Game has been closed"

@app.route('/start_nostale')
def start_nostale():

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

    time.sleep(TIME_TO_CHARACTER_SELECTION)

    mouse.double_click(button='left', coords=SELECT_CHARACTER)

    time.sleep(TIME_TO_GAME)

    mouse.click(button='left', coords=CLOSE_NOSMALL)

    return "Server has been selected"

# this is needed in development in order to find out mouse positions for
# the automated script
@app.route('/get_mouse_position')
def get_mouse_position():
    x, y = win32api.GetCursorPos()
    return flask.jsonify({ "x": x, "y": y})

@app.route('/test')
def testing():
    mouse.move(coords=(283,472))
    return "Test"

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
