from pywinauto import findwindows, keyboard, Application, mouse
from flask import Flask
import flask
import win32api

# pywinauto only works for windows

HOST = '127.0.0.1'
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
    pass
    return "Server has been selected"

@app.route('/get_mouse_position')
def get_mouse_position():
    x, y = win32api.GetCursorPos()
    return flask.jsonify({ x: x, y: y})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)