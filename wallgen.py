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


def distance(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2

	d = int((y2-y1)**2 + (x2-x1)**2)**0.5
	return d

def genPoints(n, side):
	radius = side // 100
	randPoints = []

	while len(randPoints)<n: 
		x = randint(0,side)
		y = randint(0,side)

		if len(randPoints) == 0:
			randPoints.append((x,y))
		else:
			for p in randPoints:
				if distance(p, (x,y)) <= radius:
					break
			else:
				randPoints.append((x,y))
	
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
@click.option("--colors", "-c", multiple=True, type=click.STRING, help="use many colors custom gradient, e.g -c #ff0000 -c #000000 -c #0000ff")
@click.option("--points", "-p", default=100, help="number of points to use, default = 100")
@click.option("--show", "-s", is_flag=True, help="open the image")

def poly(side, points, show, colors):
	""" Generates a HQ low poly image """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"
	elif points < 3:
		error = "Too less points. Minimum points 3"
	elif points > side:
		error = f"Too many points. Maximum points {side//2}"

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	shift = side//10
	side += shift*2 # increase size to prevent underflow
	
	if colors:
		if len(colors) < 2:
			click.secho("One color gradient not possible.", fg="red", err=True)
			sys.exit(1)
		cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
		img = nGradient(side, *cs)
	else:
		img = random_gradient(side)

	pts = genPoints(points, side)
	img = genWall(img, pts, side, shift)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))

@cli.command()
@click.argument("side", type=click.INT)
@click.option("--squares", "-sq", is_flag=True, default=False, help="use squares instead of rhombus")
@click.option("--hexagons", "-hx", is_flag=True, default=False, help="use Hexagons instead of rhombus (Experimental)")
@click.option("--colors", "-c", multiple=True, type=click.STRING, help="use many colors custom gradient, e.g -c #ff0000 -c #000000 -c #0000ff")
@click.option("--show", "-s", is_flag=True, help="open the image")
def pattern(side, squares, hexagons, colors, show):
	""" Generate a HQ image of a beautiful pattern """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)
	
	if colors:
		if len(colors) < 2:
			click.secho("One color gradient not possible.", fg="red", err=True)
			sys.exit(1)
		cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
		img = nGradient(side, *cs)
	else:
		img = random_gradient(side)

	if hexagons:
		img = genHexagon(side, side//20, img) # this looks good
	else:
		boxes = side // 100 + 2 # this config looks good
		img = genPattern(0, 0, side, boxes, img, squares)
		temp = side//boxes
		img = genPattern(temp, temp, side, boxes, img, squares)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--show", "-s", is_flag=True, help="open the image")
def slants(side, show):
	""" Generates slanting lines of various colors """
	img = drawSlants(side)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))