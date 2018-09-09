from PIL import Image, ImageDraw
from random import randrange,randint,choice
import time
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

def genPoints(radius, xor, yor, qty, side):
	rX = (xor,side)
	rY = (yor,side)

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

def genWall(points, side):
	img = random_gradient(side)
	idata = img.load()
	draw = ImageDraw.Draw(img)
	for p in points:
		tp = tuple(map(tuple,p))
		c = idata[calcCenter(tp)]
		# draw.polygon(tp, outline="#2c2c2c")
		draw.polygon(tp, fill=c)
	return img

side = 2000
points = genPoints(200, 0, 0, 100, side)
img = genWall(points, side+200)

img = img.crop((100,100,side-100,side-100))

img.show()

img.save("images/wall-{}.png".format(int(time.time())))
