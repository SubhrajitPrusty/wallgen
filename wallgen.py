import sys
from PIL import Image, ImageDraw
from random import randrange,randint
import time
import click
from scipy.spatial import Delaunay
import math

Image.MAX_IMAGE_PIXELS = 200000000

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

def genPoints(qty, width, height):
	side = (width+height)//2
	randPoints = []
	og = side
	width = width // 4
	height = height // 4

	qty //= 16

	def populate(a, b, n, width, height):
		side = (width+height)//2
		radius = side // 100
		points = []
		while len(points) < n:
			x = randint(a,a+width)
			y = randint(b,b+height)

			if len(points) == 0:
				points.append((x,y))
			else:
				for p in points:
					if distance(p, (x,y)) <= radius:
						break
				else:
					points.append((x,y))

		return points
	
	w,h = 0,0
	for i in range(4):
		for j in range(4):
			randPoints += populate(w,h, qty, width, height)
			w+=width
		w=0
		h+=height

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

def genPoly(width, height, img, points, wshift, hshift, outl=None, pic=False):

	baseImg = Image.new("RGB", (width+(wshift*2), height+(hshift*2)), "#000000")

	baseImg.paste(img, box=(wshift, hshift))
	bw = baseImg.width
	bh = baseImg.height

	if pic:
		idata = baseImg.load() # load pixel data
	else:
		idata = img.load() # load pixel data

	draw = ImageDraw.Draw(baseImg)

	for p in points:
		tp = tuple(map(tuple,p)) # convert each pair of points to tuples
		a,b = calcCenter(tp)
		try:
			b = bh-5 if b>=bh else b
			b = bh+5 if b<=0 else b

			a = bw-5 if a>=bw else a
			a = bw+5 if a<=0 else a

			c = idata[a,b]
		except Exception as e:
			# print(a,b)
			c = "#00ff00"
	
		if outl:
			draw.polygon(tp, fill=c, outline=outl)
		else:
			draw.polygon(tp, fill=c) # draw one triangle
	
	img = baseImg.crop((wshift, hshift, baseImg.width - wshift, baseImg.height - hshift)) # crop back to normal size

	return img


###########
# diamond #
###########

def genDiamond(width, height, img, outl=None, pic=False, per=1):

	x = y = 0

	wboxes = int(per/100.0*width)
	hboxes = int(per/100.0*height)
	
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img) 
	
	inc = width//wboxes # increment size

	wboxes += 2
	hboxes += 2

	for i in range(hboxes-1): # one extra line
		for j in range(wboxes//2-1): # ¯\_(ツ)_/¯

			points = [(x,y),(x+inc,y+inc),(x+2*inc,y),(x+inc,y-inc)] # diamond

			a,b = (x + x+2*inc)//2, y

			try: # adjustment to not overflow
				b = height-2 if b>=height else b
				b = 2 if b<=0 else b

				a = width-2 if a>=width else a
				a = 2 if a<=0 else a

				c = idata[a,b]

			except Exception as e:
				# print(a,b)
				c = "#00ff00" # backup

			if outl:
				draw.polygon((points), fill=c, outline=outl)
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

def genSquares(width, height, img, outl=None, pic=False, per=1):

	x = y = 0

	wboxes = int(per/100.0*width)
	hboxes = int(per/100.0*height)
	
	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img) 
	
	inc = width//wboxes #increment size

	wboxes += 1
	hboxes += 1

	for i in range(hboxes):
		for j in range(wboxes):
			points = [(x,y),(x,y+inc),(x+inc,y+inc),(x+inc,y)] # squares

			a,b = (x+x+inc)//2,(y+y+inc)//2 # to get pixel data
			try: # adjustment to not overflow
				b = height-5 if b>=height else b
				b = 5 if b<=0 else b

				a = width-5 if a>=width else a
				a = 5 if a<=0 else a

				c = idata[a,b]

			except Exception as e:
				# print(a,b)
				c = "#00ff00" # backup

			# draw one square

			if outl:
				draw.polygon((points), fill=c, outline=outl)
			else:
				draw.polygon((points), fill=c)
			
			x+=inc # shift cursor horizontally
		
		y+=inc # shift cursor vertically
		x=0 # restore horizontal starting point

	return img # return final image


###########
# HEXAGON #
###########

def genHexagon(width, height, img, outl=None, pic=False, per=5):

	x = y = 0
	
	radius = int(per/100.0 * min(height, width))

	idata = img.load() # load pixel data
	draw = ImageDraw.Draw(img)

	ang = 2 * math.pi / 6 # angle inside a hexagon
	apothem = radius * math.cos(math.pi/6) # radius of inner circle
	side = 2 * apothem * math.tan(math.pi/6) # length of each side
	hexwidth = 2 * apothem # horizontal width of a hexagon
	wboxes = width // int(hexwidth) # adjustment
	hboxes = height // int((side + radius) * 0.75)  # adjustment

	x,y = 0, radius # start here
	xback = 0 # backup of x 

	if pic:
		hboxes+=1

	for i in range(hboxes):
		for j in range(wboxes+1):
			points = [((x + radius * math.sin(k * ang)), (y + radius * math.cos(k * ang))) for k in range(6)]

			a,b = x,y
			try: # adjustment to not overflow
				b = b - side//2 if b>=height else b
				b = b + side//2 if b<=0 else b

				a = a - radius if a>=width else a
				a = a + radius if a<=0 else a

				c = idata[a,b]

			except Exception as e:
				# print(a,b)
				c = "#00ff00" # backup

			if outl:
				draw.polygon((points), fill=c, outline=outl) # draw one hexagon
			else:
				draw.polygon((points), fill=c) # draw one hexagon
			x += hexwidth

		y += radius + (side/2) # shift cursor vertically
		if i%2 == 0:
			x=xback+apothem # restore horizontal starting point
		else:
			x=xback # restore horizontal starting point, but for honeycombing

	return img # return final image


@click.group()
def cli():
	pass

@cli.command()
@click.argument("side", type=click.INT)
@click.option("--colors", "-c", multiple=True, type=click.STRING, help="use many colors custom gradient, e.g -c #ff0000 -c #000000 -c #0000ff")
@click.option("--points", "-p", default=100, help="number of points to use, default = 100")
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--outline", "-o", default=None, help="outline the triangles")
@click.option("--name", "-n", help="rename the output")

def poly(side, points, show, colors, outline, name):
	""" Generates a HQ low poly image """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"
	elif points < 3:
		error = "Too less points. Minimum points 3"
	elif points > 50000:
		error = "Too many points. Maximum points 50000"

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	side = side * 2 # increase size to anti alias

	shift = side//10
	nside = side + shift*2 # increase size to prevent underflow
	
	if colors:
		if len(colors) < 2:
			click.secho("One color gradient not possible.", fg="red", err=True)
			sys.exit(1)
		cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
		img = nGradient(nside, *cs)
	else:
		img = random_gradient(nside)

	if outline:
		try:
			outline = tuple(bytes.fromhex(outline[1:]))
		except Exception as e:
			click.secho("Invalid color hex", fg='red', err=True)
			sys.exit(1)


	pts = genPoints(points, nside, nside)
	img = genPoly(side, side, img, pts, shift, shift, outl=outline)

	img = img.resize((side//2, side//2), resample=Image.BICUBIC)

	if show:
		img.show()

	if name:
		img.save("{}.png".format(name))
	else:   
		img.save("wall-{}.png".format(int(time.time())))

@cli.command()
@click.argument("side", type=click.INT)
@click.option("--type", "-t", "shape", type=click.Choice(['square', 'hex', 'diamond']), help="choose which shape to use")
@click.option("--colors", "-c", multiple=True, type=click.STRING, help="use many colors custom gradient, e.g -c #ff0000 -c #000000 -c #0000ff")
@click.option("--percent", "-p", default=1, help="Use this percentage to determine number of polygons")
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--outline", "-o", default=None, help="outline the shapes")
@click.option("--name", "-n", help="rename the output")

def shape(side, shape, colors, show, outline, name, percent):
	""" Generates a HQ image of a beautiful shapes """

	error = ""
	if side < 50:
		error = "Image too small. Minimum size 50"
	if percent < 1 or percent > 10:
		error = "Percent range 1-10"

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	side = side * 2 # increase size to anti alias
	
	if colors:
		if len(colors) < 2:
			click.secho("One color gradient not possible.", fg="red", err=True)
			sys.exit(1)
		cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
		img = nGradient(side, *cs)
	else:
		img = random_gradient(side)

	if outline:
		try:
			outline = tuple(bytes.fromhex(outline[1:]))
		except Exception as e:
			click.secho("Invalid color hex", fg='red', err=True)
			sys.exit(1)


	if shape == 'hex':
		img = genHexagon(side, side, img, outline, per=percent)
	elif shape == 'square':
		img = genSquares(side, side, img, outline, per=percent)
	elif shape == 'diamond':
		img = genDiamond(side, side, img, outline, per=percent)
	else:
		error = "No shape given. To see list of shapes \"wallgen shape --help\""
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	img = img.resize((side//2, side//2), resample=Image.BICUBIC)

	if show:
		img.show()

	if name:
		img.save("{}.png".format(name))
	else:   
		img.save("wall-{}.png".format(int(time.time())))


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--name", "-n", help="rename the output")

def slants(side, show, name):
	""" Generates slanting lines of various colors """

	side = side * 2 # increase size to anti alias

	img = drawSlants(side)

	if show:
		img.show()

	if name:
		img.save("{}.png".format(name))
	else:   
		img.save("wall-{}.png".format(int(time.time())))

@cli.group()
def pic():
	""" Use a picture instead of a gradient """ 
	pass

@pic.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option("--points", "-p", default=1000, help="number of points to use, default = 1000")
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--outline", "-o", default=None, help="outline the triangles")
@click.option("--name", "-n", help="rename the output")

def poly(image, points, show, outline, name):
	""" Generates a HQ low poly image """

	if points < 3:
		error = "Too less points. Minimum points 3"
	elif points > 50000:
		error = "Too many points. Maximum points {}".format(50000)
	else:
		error = None

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	img = Image.open(image)
	
	width = img.width
	height = img.height
	wshift = img.width//10
	hshift = img.height//10
	width += wshift*2
	height += hshift*2

	if outline:
		try:
			outline = tuple(bytes.fromhex(outline[1:]))
		except Exception as e:
			click.secho("Invalid color hex", fg='red', err=True)
			sys.exit(1)


	pts = genPoints(points, width, height)
	img = genPoly(img.width, img.height, img, pts, wshift, hshift, outline, pic=True)

	if show:
		img.show()

	if name:
		img.save("{}.png".format(name))
	else:   
		img.save("wall-{}.png".format(int(time.time())))


@pic.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option("--type", "-t", "shape", type=click.Choice(['square', 'hex', 'diamond']), help="choose which shape to use")
@click.option("--percent", "-p", default=1, help="Use this percentage to determine number of polygons")
@click.option("--show", "-s", is_flag=True, help="open the image")
@click.option("--outline", "-o", default=None, help="outline the shapes")
@click.option("--name", "-n", help="rename the output")

def shape(image, shape, show, outline, name, percent):
	""" Generate a HQ image of a beautiful shapes """

	if percent < 1 or percent > 10:
		error = "Percent range 1-10"
	else:
		error = None

	if error:
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	img = Image.open(image)

	width = img.width
	height = img.height

	if outline:
		try:
			outline = tuple(bytes.fromhex(outline[1:]))
		except Exception as e:
			click.secho("Invalid color hex", fg='red', err=True)
			sys.exit(1)

	if shape == 'hex':
		img = genHexagon(width, height, img, outline, pic=True, per=percent)
	elif shape == 'square':
		img = genSquares(width, height, img, outline, pic=True, per=percent)
	elif shape == 'diamond':
		img = genDiamond(width, height, img, outline, pic=True, per=percent)
	else:
		error = "No shape given. To see list of shapes \"wallgen pic shape --help\""
		click.secho(error, fg='red', err=True)
		sys.exit(1)

	if show:
		img.show()

	if name:
		img.save("{}.png".format(name))
	else:   
		img.save("wall-{}.png".format(int(time.time())))


if __name__ == "__main__":
	cli()
