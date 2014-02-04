#!/usr/bin/python
from PIL import Image
from struct import pack
from sys import argv
if len(argv)<=2:
	print("gif2bwa: missing file operand\nTry 'gif2bwa.py --help' for more information")
elif argv[1]=="--help":
	print("Usage: gif2bwa.py INPUT OUTPUT\nConvert gif image INPUT to blinkenwall animation OUTPUT.\n\nINPUT has to be an animated 9*5 gif image. OUTPUT will be a blinkenwall animation, containing any number of frames each consisting of 2 bytes setting the duration for the frame to be shown (length will be 0x01*256+0x00) and 45 pixels of raw RGB image data, making each frame alltogether 137 bytes long. ")
else:
	im=Image.open(argv[1])
	pallette=im.resize((256,1))
	pallette.putdata(range(256))
	pallette=list(pallette.convert("RGB").getdata())
	lastframe=[]
	for i in range(0,9):
		row=[im.info["background"]]*5
		lastframe.append(row)
	anim=b''
	while 1:
		if "transparency" in im.info:
			transparency = im.info["transparency"]
		else:
			transparency = None
		anim+=pack("H",im.info["duration"])
		pix=im.load()
		for i in range(0,5):
			for j in range(0,9):
				if pix[j,i] != transparency:
					anim+=pack("B",pallette[pix[j,i]][0])+pack("B",pallette[pix[j,i]][1])+pack("B",pallette[pix[j,i]][2])
					lastframe[j][i]=pix[j,i]
				else:
					anim+=pack("B",pallette[lastframe[j][i]][0])+pack("B",pallette[lastframe[j][i]][1])+pack("B",pallette[lastframe[j][i]][2])
		try:
			im.seek(im.tell()+1)
		except EOFError:
			break
	saveto=open(argv[2],"wb")
	saveto.write(anim)
