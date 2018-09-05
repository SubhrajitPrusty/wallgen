from PIL import Image, ImageDraw
from random import randrange,randint,random,choice
import seaborn as sns
import time
from scipy.spatial import Delaunay

side = 2000
bg = "#2c2c2c"
# bg = '#f9499e'

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
# img.show()

radius = 200
rX = (-200,2200)
rY = (-200,2200)
qty = 150

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

# print(randPoints)

tri = Delaunay(randPoints)
points = tri.points[tri.simplices]

# for p in points:
# 	print(tuple(map(tuple,p)))


def genWall(points, colors, img, rot=False): 	
	draw = ImageDraw.Draw(img)
	for c in range(len(colors)):
		colors[c] = [int(x*255) for x in colors[c]]
	for p in points:
		ch = choice(colors)
		tp = tuple(map(tuple,p))
		# print(img[tp[0]])
		# draw.polygon(tp, outline="#2c2c2c")
		draw.polygon(tp, fill=tuple(ch))

colors = []
# colors = sns.color_palette("muted")
# colors = sns.color_palette("Blues_d")
colors.extend(sns.color_palette("Purples_d"))
# colors.extend(sns.color_palette("PuRd_d"))
# colors.extend(sns.color_palette("BuPu_d"))

genWall(points, colors, img)

img.show()

# img.save("wall-{}.png".format(int(time.time())))
