import warnings
import numpy as np
from scipy.spatial import Delaunay
from skimage.filters import sobel
from skimage import color, img_as_ubyte
from PIL import Image, ImageDraw, ImageFilter


def distance(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2

	d = int((y2-y1)**2 + (x2-x1)**2)**0.5
	return d

def populate(a, b, n, width, height, ret):
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

	ret.extend(points)

def genPoints(qty, width, height):
	side = max(width, height)
	randPoints = np.random.choice(side, size=(qty, 2))

	og = side
	
	tri = Delaunay(randPoints) # calculate D triangulation of points
	points = tri.points[tri.simplices] # find all groups of points

	return points


def calcCenter(ps):
	""" calculate incenter of a triangle given all vertices"""
	mid1 = ((ps[0][0]+ps[1][0])/2, (ps[0][1]+ps[1][1])/2)
	mid = ((mid1[0]+ps[2][0])/2, (mid1[1]+ps[2][1])/2)
	return mid

def genSmartPoints(image):
	width = image.shape[1]
	height = image.shape[0]

	edges = sobel(image)

	# convert to RGB compatible image
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		rgb_img = img_as_ubyte(color.gray2rgb(edges))

	# convert to PIL image
	pimg = Image.fromarray(rgb_img)
	idata = pimg.load()

	edges_data = []

	# get image pixel data and pass through a filter to get only prominent edges

	for x in range(pimg.width):
		for y in range(pimg.height):
			if sum(idata[x,y])/3 > 10:
				edges_data.append((x,y))

	# print(len(edges_data))
	
	# sometimes edges detected wont pass ^ this required case
	if len(edges_data) < 1:
		raise Exception("EdgeDetectionError")
		sys.exit(1)

	# get a n/5 number of points rather than all of the points
	sample = np.random.choice(len(edges_data), len(edges_data)//5 if len(edges_data)/5 < 50000 else 50000)
	edges_data = [edges_data[x] for x in sample]

	# print(len(edges_data))

	points = []
	radius = int(0.1 * (width+height)/2)

	# print(radius)
		
	points = edges_data

	ws = width//50
	hs = height//50

	for x in range(0, width+ws, ws):
		points.append((x,0))
		points.append((x,height))

	for y in range(0, height+hs, hs):
		points.append((0,y))
		points.append((width,y))

	tri = Delaunay(points) # calculate D triangulation of points
	delaunay_points = tri.points[tri.simplices] # find all groups of points

	return delaunay_points


