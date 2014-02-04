#!/usr/bin/python
import socket
from struct import unpack
from sys import argv
from time import sleep
from urllib.request import urlopen
if len(argv)<=1:
	print("sendbwa: missing file operand\nTry 'sendbwa.py --help' for more information")
elif argv[1]=="--help":
	print("Usage: sendbwa.py FILE\nSend FILE to blinkenwall.\n\nFILE has to be a blinkenwall animation, containing any number of frames each consisting of 2 bytes setting the duration for the frame to be shown (length will be 0x01*256+0x00) and 45 pixels of raw RGB image data, making each frame alltogether 137 bytes long. ")
else:
	with open(argv[1],"rb") as f:
		urlopen("http://10.20.30.26/cgi-bin/togglesocket.cgi")
		sleep(1)
		s=socket.socket()
		s.connect(('10.20.30.26',1337))
		while True:
			durdat=f.read(2)
			if len(durdat)==0:
				break
			dur=unpack("H",durdat)[0]
			s.sendall(f.read(135))
			sleep(dur/1000)
		s.close()
		urlopen("http://10.20.30.26/cgi-bin/togglesocket.cgi")