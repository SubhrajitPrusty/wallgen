import os
import sys
import click
import struct
import ctypes
import warnings
import subprocess
import numpy as np
from skimage import img_as_ubyte
from skimage.transform import swirl
from random import randrange, randint
from PIL import Image, ImageDraw, ImageFilter

def random_gradient(side):
	img = Image.new("RGB", (side,side), "#FFFFFF")
	draw = ImageDraw.Draw(img)

	r,g,b = randint(0,255), randint(0,255), randint(0,255)
	dr = (randint(0,255) - r)/side
	dg = (randint(0,255) - g)/side
	db = (randint(0,255) - b)/side
	for i in range(side):
		r,g,b = r+dr, g+dg, b+db
		draw.line((i,0,i,side), fill=(int(r),int(g),int(b)))

	return img

def nGradient(side, *colors):
	img = Image.new("RGB", (side,side), "#FFFFFF")
	draw = ImageDraw.Draw(img)

	nc = len(colors)
	div = side//(nc-1)
	[r,g,b] = colors[0]
	p=0
	for i in range(1,nc):
		dc = [(y-x)/div for x,y in zip(colors[i-1], colors[i])]
		for x in range(p, p+div):
			draw.line([x,0,x,side], fill=tuple(map(int, [r,g,b])))
			r+=dc[0]
			g+=dc[1]
			b+=dc[2]
		p+=div
	
	return img

def NbyNGradient(side):
	base_color = "#00ffff"
	img = Image.new("RGB", (side,side), base_color)
	draw = ImageDraw.Draw(img)

	n_boxes = 5
	boxes_size = side//n_boxes

	xmin, xmax = 0, boxes_size
	ymin, ymax = 0, boxes_size


	for i in range(n_boxes):
		for j in range(n_boxes):
			r, g, b = [randint(0, 255),randint(0, 255), randint(0, 255)]

			dr = (randint(0, 255) - r)/boxes_size
			dg = (randint(0, 255) - g)/boxes_size
			db = (randint(0, 255) - b)/boxes_size
			
			for k in range(xmin, xmax):
				draw.line([k, ymin, k, ymax], fill=(int(r), int(g), int(b)))
				r += dr
				g += dg
				b += db

			xmin += boxes_size
			xmax += boxes_size

		xmin = 0
		xmax = boxes_size
		ymin += boxes_size
		ymax += boxes_size

	img = img.filter(ImageFilter.GaussianBlur(radius=boxes_size//n_boxes))
	return img


def swirl_image(image):
	image = np.array(image)
	w, h = image.shape[:2]
	sw = swirl(image, rotation=0, strength=10, radius=max(w,h))
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		sw = img_as_ubyte(sw)
	
	pil_img = Image.fromarray(sw)

	return pil_img

def is_64_windows():
	"""Find out how many bits is OS. """
	return struct.calcsize('P') * 8 == 64

def get_sys_parameters_info():
	"""Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
	return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
		else ctypes.windll.user32.SystemParametersInfoA

def set_wallpaper(file_name, flag=False):
	if sys.platform == 'win32':
		try:
			sys_parameters_info = get_sys_parameters_info()
			if flag or ":\\" not in file_name[:4]:
				r = sys_parameters_info(20, 0, os.getcwd()+"\\"+file_name, 3)
			else:
				r = sys_parameters_info(20, 0, os.getcwd()+"\\"+file_name, 3)
			print(f"Wallpaper has been set successfully !!")
		except:
			error = "There was some unknown error while setting up your wallpaper"
			click.secho(error, fg='red', err=True)
			sys.exit(1)
	elif sys.platform == 'linux' and 'gnome' in os.environ['DESKTOP_SESSION']:
		try:
			if flag or not file_name.startswith("/"):
				r = subprocess.Popen("gsettings set org.gnome.desktop.background picture-uri file://"+os.getcwd()+"/"+file_name, stdout=subprocess.PIPE, shell=True)
			else:
				r = subprocess.Popen("gsettings set org.gnome.desktop.background picture-uri file://"+file_name, stdout=subprocess.PIPE, shell=True)
			assert not r.communicate()[1]
			print(f"Wallpaper has been set successfully !!")
		except:
			error = "There was some unknown error while setting up your wallpaper"
			click.secho(error, fg='red', err=True)
			sys.exit(1)
	else:	
		error = "You can only set up wallpaper in Windows System and GNOME based Linux System"
		click.secho(error, fg='red', err=True)
		sys.exit(1)