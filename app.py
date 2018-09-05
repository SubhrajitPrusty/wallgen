from PIL import Image, ImageDraw
from random import randrange,randint,choice
import time
from scipy.spatial import Delaunay

side = 2000

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

img = random_gradient(side)

radius = 200
rX = (0,side)
rY = (0,side)
qty = 200

deltas = set()
for x in range(-radius,radius+1):
	for y in range(-radius, radius+1):
		if x**2 + y**2 <= radius**2:
			deltas.add((x,y))

randPoints = []
excluded = set()

i = 0

while i<=qty:
	x = randrange(*rX)
	y = randrange(*rY)

	if (x,y) in excluded:
		continue
	randPoints.append((x,y))
	i+=1
	excluded.update((x+dx,y+dx) for (dx,dy) in deltas)

tri = Delaunay(randPoints)
points = tri.points[tri.simplices]

def calcCenter(ps):
	mid1 = ((ps[0][0]+ps[1][0])/2, (ps[0][1]+ps[1][1])/2)
	mid = ((mid1[0]+ps[2][0])/2, (mid1[1]+ps[2][1])/2)
	return mid


def genWall(points, img, rot=False):
	idata = img.load()
	draw = ImageDraw.Draw(img)
	for p in points:
		tp = tuple(map(tuple,p))
		c = idata[calcCenter(tp)]
		# draw.polygon(tp, outline="#2c2c2c")
		draw.polygon(tp, fill=c)

genWall(points, img)

img.show()

img.save("images/wall-{}.png".format(int(time.time())))
