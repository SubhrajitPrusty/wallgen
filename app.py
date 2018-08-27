from PIL import Image, ImageDraw
from random import randint,random,choice
import seaborn as sns
import time

side = 2000
bg = "#2c2c2c"
# bg = '#f9499e'

img = Image.new('RGB',(side,side), bg)

def genWall(x,y, boxes, colors, img, rot=False): 	
	draw = ImageDraw.Draw(img)
	inc = side//boxes
	xback = x
	for c in range(len(colors)):
		colors[c] = [int(x*255) for x in colors[c]]
	for i in range(boxes+1):    		
		choiceOld = choice(colors)
		for j in range(boxes+1):
			squares = [(x,y),(x,y+inc),(x+inc,y+inc),(x+inc,y)] # squares
			rhombus = [(x,y),(x-inc,y+inc),(x,y+2*inc),(x+inc,y+inc)] #rhombus
			triangle = [(x,y),(x+inc,y),(x,y+inc)] # triangle

			points = list(rhombus)
			choiceNew = choice(colors)

			while choiceOld == choiceNew:
				choiceNew = choice(colors)

			choiceOld = choiceNew
			
			draw.polygon((points), fill=tuple(choiceNew))
			x+=2*inc
			# x+=inc

			if rot == True:
				img = img.rotate(90*randint(1,4))
				draw = ImageDraw.Draw(img)
		
		y+=2*inc
		# y+=inc
		x=xback
		# inc = inc*1.1

colors = []
# colors = sns.color_palette("muted")
# colors = sns.color_palette("Blues_d")
colors.extend(sns.color_palette("Purples_d"))
# colors.extend(sns.color_palette("PuRd_d"))
# colors.extend(sns.color_palette("BuPu_d"))

a = b = 0
boxs = 20

genWall(a,b,boxs,colors,img)
colors = sns.color_palette("Blues_d")

a = b = side//boxs
genWall(-a,-b,boxs,colors,img)


# img = img.transpose(Image.ROTATE_90)
img.show()

img.save("wall-{}.png".format(int(time.time())))
