from PIL import Image, ImageDraw
from random import randrange,randint
import time
import click
from scipy.spatial import Delaunay

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


def genPoints(qty, side):
	radius = side // 20
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
	mid1 = ((ps[0][0]+ps[1][0])/2, (ps[0][1]+ps[1][1])/2)
	mid = ((mid1[0]+ps[2][0])/2, (mid1[1]+ps[2][1])/2)
	return mid

def genWall(img, points, side, shift):
	idata = img.load()
	draw = ImageDraw.Draw(img)
	for p in points:
		tp = tuple(map(tuple,p))
		c = idata[calcCenter(tp)]
		# draw.polygon(tp, outline="#2c2c2c")
		draw.polygon(tp, fill=c)
	img = img.crop((shift,shift,side-shift,side-shift))
	return img

@click.command()
@click.argument("side", type=click.INT)
@click.option("--colors", nargs=2, type=click.STRING, help="use color1 --> color2 gradient, e.g #ff0000 #0000ff")
@click.option("--np", default=100, help="number of points to use, default = 100")
@click.option("--radius", default=200, help="radius, within which no other point is generated, default=200")
@click.option("--show", is_flag=True, help="open the image")
def cli(side,np,radius,show,colors):
	""" Generates a side X side HQ low poly image of random gradient """

	shift = side//10
	side += shift*2
	
	if not colors:
		img = random_gradient(side)
	else:
		rgb1 = tuple(bytes.fromhex(colors[0][1:]))
		rgb2 = tuple(bytes.fromhex(colors[1][1:]))
		img = gradient(side, rgb1, rgb2)

	points = genPoints(radius, np, side)
	img = genWall(img, points, side, shift)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))