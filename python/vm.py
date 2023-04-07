from pywinauto import findwindows, keyboard, Application, mouse
import socket

ADDRESS = '127.0.0.1'
PORT = 1337

def close_nostale():

    window_handle = findwindows.find_windows(title_re="NosTale")[0]
    app = Application().connect(handle=window_handle)

    window = app.window(title='NosTale')
    window.set_focus()

    keyboard.send_keys('%{F4}')
    keyboard.send_keys('{ENTER}')

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

def goto_game():
    pass

def listen():
    server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen()
    print(f'Listening on {ADDRESS}:{PORT}')
    while True:
        (client_socket, addr) = server_socket.accept()
        print(client_socket.recv(1024))

listen()