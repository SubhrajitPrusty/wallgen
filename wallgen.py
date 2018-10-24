import sys
from PIL import Image, ImageDraw
from random import randrange,randint
import time
import click
from scipy.spatial import Delaunay
import math

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

def gradient(side, rgb1, rgb2):
	img = Image.new("RGB", (side,side), "#FFFFFF")

	draw = ImageDraw.Draw(img)

	r,g,b = rgb1[0], rgb1[1], rgb1[2]
	dr,dg,db = (rgb2[0]-r)/side, (rgb2[1]-g)/side, (rgb2[2]-b)/side 

	for i in range(side):
		r,g,b = r+dr, g+dg, b+db
		draw.line((i,0,i,side), fill=(int(r),int(g),int(b)))

	return img

def dualGradient(side, color1, color2, color3):
	img = Image.new("RGB", (side,side), "#FFFFFF")
	draw = ImageDraw.Draw(img)

	div = side//2
	[r,g,b] = color1
	p=0
	for i in range(2):
		dc = [(y-x)/div for x,y in zip(color1, color2)]
		for x in range(p, p+div):
			draw.line([x,0,x,side], fill=tuple(map(int, [r,g,b])))
			r+=dc[0]
			g+=dc[1]
			b+=dc[2]
		p+=div
		color1 = color2
		color2 = color3
	
	return img

def randcolor():
	return (randint(0,255),randint(0,255),randint(0,255))

def drawSlants(side):
	img = Image.new("RGB", (side,side), "#FFFFFF")
	draw = ImageDraw.Draw(img)
	y = 0
	ad = side//10
	while y <= side+ad:
		w = randint(5,20)
		c = randcolor()
		draw.line([0-ad, y,  y, 0-ad], width=w+1, fill=c)
		draw.line([y, side,  side, y], width=w+1, fill=c)
		y+=w

	return img

def genPoints(qty, side):
	radius = side // 20 # radius is set to 5% - good config
	rX = (0,side)
	rY = (0,side)

	deltas = set()
	for x in range(-radius,radius+1):
		for y in range(-radius, radius+1):
			if x**2 + y**2 <= radius**2:
				deltas.add((x,y)) # populate with all possible points within radius

	excluded = set()
	randPoints = []
	i = 0

	while i<=qty:
		x = randrange(*rX)
		y = randrange(*rY)

		if (x,y) in excluded:
			continue
		randPoints.append((x,y)) # add a point
		i+=1
		excluded.update((x+dx,y+dx) for (dx,dy) in deltas) # update all points inside circumference

	tri = Delaunay(randPoints) # calculate D triangulation of points
	points = tri.points[tri.simplices] # find all groups of points
	return points

def calcCenter(ps):
	""" calculate incenter of a triangle given all vertices"""
	mid1 = ((ps[0][0]+ps[1][0])/2, (ps[0][1]+ps[1][1])/2)
	mid = ((mid1[0]+ps[2][0])/2, (mid1[1]+ps[2][1])/2)
	return mid

def genWall(img, points, side, shift):
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img)
	for p in points:
		tp = tuple(map(tuple,p)) # convert each pair of points to tuples
		c = (255,255,255) # default color incase of exception
		try:
			c = idata[calcCenter(tp)]
		except Exception as e:
			pass
		# draw.polygon(tp, outline="#2c2c2c")
		draw.polygon(tp, fill=c) # draw one triangle
	img = img.crop((shift,shift,side-shift,side-shift)) # crop back to normal size

	return img

def genPattern(x, y, side, boxes, img, square=False):
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img) 
	inc = side//boxes #increment size
	xback = x # backup of x
	mult = 2 
	boxes = boxes//mult # adjustment
	for i in range(boxes):
		for j in range(boxes):
			if square:
				points = [(x,y),(x,y+inc),(x+inc,y+inc),(x+inc,y)] # squares
			else:
				points = [(x,y),(x-inc,y+inc),(x,y+2*inc),(x+inc,y+inc)] #rhombus

			a,b = x+inc,y+inc # to get pixel data
			a = a if a>0 else 0 # prevent underflow
			a = a if a<side else a-2*inc # prevent overflow
			b = b if b>0 else 0 # prevent underflow
			b = b if b<side else b-2*inc # prevent overflow
			c = idata[a,b] # color data

			draw.polygon((points), fill=tuple(c)) # draw one polygon
			x+=mult*inc # shift cursor horizontally
	
		y+=mult*inc # shift cursor vertically
		x=xback # restore horizontal starting point

	return img # return final image

def genHexagon(side, radius, img):
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img)

	ang = 2 * math.pi / 6 # angle inside a hexagon
	s = radius * math.cos(math.pi/6)
	width = 2*s # horizontal width of a hexagon
	boxes = side// int(width) + 1 # adjustment

	x,y = 0,s # start here
	xback = s # backup of x	

	for i in range(boxes+1):
		for j in range(boxes):			
			points = [((x + radius * math.sin(i * ang)), (y + radius * math.cos(i * ang))) for i in range(6)]
			
			a,b = x,y
			a = a if a < side else side-1
			b = b if b < side else side-1
			a = a if a > 0 else 1
			b = b if b > 0 else 1

			c = idata[a,b]
			
			draw.polygon((points), fill=c) # draw one hexagon
			x += width

		y += radius * 1.5 # shift cursor vertically
		if i%2 == 0:
			x=xback # restore horizontal starting point
		else:
			x=xback-s # restore horizontal starting point, but for honeycombing

	return img # return final image


@click.group()
def cli():
	pass

@cli.command()
@click.argument("side", type=click.INT)
# @click.option("--pic",type=click.Path(exists=True,dir_okay=False),help="Use a pic instead of gradient background")
@click.option("--colors", nargs=2, type=click.STRING, help="use custom gradient, e.g --colors #ff0000 #0000ff")
@click.option("--colors2", nargs=3, type=click.STRING, help="use 2 color custom gradient, e.g --colors2 #ff0000 #000000 #0000ff")
@click.option("--np", default=100, help="number of points to use, default = 100")
@click.option("--show", is_flag=True, help="open the image")

def poly(side, np, show, colors, colors2):
	""" Generates a HQ low poly image """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"
	elif np < 3:
		error = "Too less points. Minimum points 3"
	elif np > side//2:
		error = "Too many points. Maximum points {}".format(side//2)

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	shift = side//10
	side += shift*2 # increase size to prevent underflow
	
	# if pic:
	# 	img = img.load(pic)
	if colors:
		rgb1 = tuple(bytes.fromhex(colors[0][1:]))
		rgb2 = tuple(bytes.fromhex(colors[1][1:]))
		img = gradient(side, rgb1, rgb2)
	if colors2:
		rgb1 = tuple(bytes.fromhex(colors2[0][1:]))
		rgb2 = tuple(bytes.fromhex(colors2[1][1:]))
		rgb3 = tuple(bytes.fromhex(colors2[2][1:]))
		img = dualGradient(side, rgb1, rgb2, rgb3)
	else:
		img = random_gradient(side)

	points = genPoints(np, side)
	img = genWall(img, points, side, shift)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))

@cli.command()
@click.argument("side", type=click.INT)
@click.option("--sq", is_flag=True, help="use squares instead of rhombus")
@click.option("--hex", is_flag=True, help="use Hexagons instead of rhombus (Experimental)")
@click.option("--colors", nargs=2, type=click.STRING, help="use custom gradient, e.g --colors #ff0000 #0000ff")
@click.option("--colors2", nargs=3, type=click.STRING, help="use 2 color custom gradient, e.g --colors2 #ff0000 #000000 #0000ff")
@click.option("--show", is_flag=True, help="open the image")
def pattern(side, colors, show, sq, hex, colors2):
	""" Generate a HQ image of a beautiful pattern """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)
	
	if colors:
		rgb1 = tuple(bytes.fromhex(colors[0][1:]))
		rgb2 = tuple(bytes.fromhex(colors[1][1:]))
		img = gradient(side, rgb1, rgb2)
	elif colors2:
		rgb1 = tuple(bytes.fromhex(colors2[0][1:]))
		rgb2 = tuple(bytes.fromhex(colors2[1][1:]))
		rgb3 = tuple(bytes.fromhex(colors2[2][1:]))
		img = dualGradient(side, rgb1, rgb2, rgb3)
	else:
		img = random_gradient(side)

	if hex:
		img = genHexagon(side, side//20, img) # this looks good
	else:
		boxes = side // 100 + 2 # this config looks good
		img = genPattern(0, 0, side, boxes, img, sq)
		temp = side//boxes
		img = genPattern(temp, temp, side, boxes, img, sq)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--show", is_flag=True, help="open the image")
def slants(side, show):
	""" Generates slanting lines of various colors """
	img = drawSlants(side)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))