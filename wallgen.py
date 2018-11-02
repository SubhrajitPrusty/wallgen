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

def genPoints(qty, side):
	radius = side // 100
	randPoints = []
	og = side
	side = side // 2

	qty //= 4

	def populate(a, b, n, side):
		radius = side // 100
		points = []
		while len(points) < n:
			x = randint(a,a+side)
			y = randint(b,b+side)

			if len(points) == 0:
				points.append((x,y))
			else:
				for p in points:
					if distance(p, (x,y)) <= radius:
						break
				else:
					points.append((x,y))

		return points
	
	randPoints = populate(0,0, qty, side)
	randPoints += populate(side, 0, qty, side)
	randPoints += populate(0, side, qty, side)
	randPoints += populate(side, side, qty, side)
	
	tri = Delaunay(randPoints) # calculate D triangulation of points
	points = tri.points[tri.simplices] # find all groups of points
	return points

def calcCenter(ps):
	""" calculate incenter of a triangle given all vertices"""
	mid1 = ((ps[0][0]+ps[1][0])/2, (ps[0][1]+ps[1][1])/2)
	mid = ((mid1[0]+ps[2][0])/2, (mid1[1]+ps[2][1])/2)
	return mid


#############
# TRIANGLES #
#############

def genPoly(img, points, side, shift, outl=False):
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img)
	for p in points:
		tp = tuple(map(tuple,p)) # convert each pair of points to tuples
		c = (255,255,255) # default color incase of exception
		try:
			c = idata[calcCenter(tp)]
		except Exception as e:
			pass
	
		if outl:
			draw.polygon(tp, fill=c, outline="#2c2c2c")
		else:
			draw.polygon(tp, fill=c) # draw one triangle
	
	img = img.crop((shift,shift,side-shift,side-shift)) # crop back to normal size

	return img


###########
# diamond #
###########

def genDiamond(side, img, outl=False):

	x = y = 0
	boxes = side//50 # good config

	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img) 

	inc = side//boxes #increment size

	xback = x # backup of x
	boxes = boxes+2 # adjustment

	for i in range(boxes-1): # one extra line
		for j in range(boxes//2 - 1): # ¯\_(ツ)_/¯
			
			points = [(x,y),(x+inc,y+inc),(x+2*inc,y),(x+inc,y-inc)] # diamond

			a,b = (x + x+2*inc)//2, y

			try: # adjustment to not overflow
				b = b-2 if b>=side else b
				b = b+2 if b<=0 else b

				a = a-2 if a>=side else a
				a = a+2 if a<=0 else a

				c = idata[a,b]

			except Exception as e:
				# print(a,b)
				c = "#00ff00" # backup

			if outl:
				draw.polygon((points), fill=c, outline="#2c2c2c")
			else:
				draw.polygon((points), fill=c)
			x+=2*inc

		y+=inc

		if i%2==0:
			x=-inc
		else:
			x=0

	return img # return final image


###########
# SQUARES #
###########

def genSquares(side, img, outl=False):

	x = y = 0
	boxes = int(0.01*side) # good config
	
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img) 
	
	inc = side//boxes #increment size
	boxes += 1

	for i in range(boxes):
		for j in range(boxes):
			points = [(x,y),(x,y+inc),(x+inc,y+inc),(x+inc,y)] # squares

			a,b = (x+x+inc)//2,(y+y+inc)//2 # to get pixel data
			try: # adjustment to not overflow
				b = b-5 if b>=side else b
				b = b+5 if b<=0 else b

				a = a-5 if a>=side else a
				a = a+5 if a<=0 else a

				c = idata[a,b]

			except Exception as e:
				# print(a,b)
				c = "#00ff00" # backup

			# draw one square

			if outl:
				draw.polygon((points), fill=c, outline="#2c2c2c")
			else:
				draw.polygon((points), fill=c)
			
			x+=inc # shift cursor horizontally
		
		y+=inc # shift cursor vertically
		x=0 # restore horizontal starting point

	return img # return final image


###########
# HEXAGON #
###########

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
@click.option("--outline", "-o", is_flag=True, help="outline the triangles")

def poly(side, points, show, colors, outline):
	""" Generates a HQ low poly image """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"
	elif points < 3:
		error = "Too less points. Minimum points 3"
	elif points > side:
		error = "Too many points. Maximum points {}".format(side//2)

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
	img = genPoly(img, pts, side, shift, outl=outline)

	if show:
		img.show()

	img.save("wall-{}.png".format(int(time.time())))

@cli.command()
@click.argument("side", type=click.INT)
@click.option("--type", "-t", "shape", type=click.Choice(['square', 'hex', 'diamond']))
@click.option("--colors", "-c", multiple=True, type=click.STRING, help="use many colors custom gradient, e.g -c #ff0000 -c #000000 -c #0000ff")
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--outline", "-o", is_flag=True, help="outline the shapes")

def shape(side, shape, colors, show, outline):
	""" Generate a HQ image of a beautiful shapes """

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

	if shape == 'hex':
		img = genHexagon(side, side//20, img) # this looks good
	elif shape == 'square':
		img = genSquares(side, img, outline)
	elif shape == 'diamond':
		img = genDiamond(side, img, outline)
	else:
		error = "No shape given. To see list of shapes \"wallgen pattern --help\""
		click.secho(error, fg='red', err=True)
		sys.exit(1)

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


if __name__ == "__main__":
	cli()