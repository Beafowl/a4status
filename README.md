Prerequisites for the image:
* The resolution of the OS has to be 1024x768
* Game needs to be set to fullscreen borderless
* Image needs to contain the game only

Prerequisites for the server:
* python

Prerequisites for the discord bot:
* Enable message content intent

Prerequisites for the OS
* Enabling the use of port 80 for flask (example is for python 3.8)
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.8
* Check the installed versions of python with ls /usr/bin | grep python
