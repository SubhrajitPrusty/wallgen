from PIL import Image, ImageDraw
from random import *
import seaborn as sns

side = 2000
bg = "#2c2c2c"
bg = '#f9499e'

img = Image.new('RGB',(side,side), bg)

draw = ImageDraw.Draw(img)

boxes = 20
inc = side//boxes

x = -inc
y = -inc

colors = [0,0,0]
colors = sns.color_palette("muted")
# print(colors)

for c in range(len(colors)):
	colors[c] = [int(x*255) for x in colors[c]]

# print(colors)

for i in range(boxes+1):
	
	choiceOld = choice(colors)

	for j in range(boxes+1):
		squares = ((x,y),(x,y+inc),(x+inc,y+inc),(x+inc,y)) # squares
		rhombus = ((x,y),(x-inc,y+inc),(x,y+2*inc),(x+inc,y+inc)) #rhombus
		triangle = ((x,y),(x+inc,y),(x,y+inc)) # triangle

		points = list(rhombus)
		# print(points,end=" ")
		# shuffle(points)
		# print(points)
		choiceNew = choice(colors)

		while choiceOld == choiceNew:
			choiceNew = choice(colors)

		choiceOld = choiceNew
		
		draw.polygon((points), fill=tuple(choiceNew))
		# x+=2*inc
		x+=inc

		# rotate

		# img = img.rotate(90*randint(1,4))
		# draw = ImageDraw.Draw(img)
	
	# y+=2*inc
	y+=inc
	x=0
	# inc = inc*1.1

# img = img.transpose(Image.ROTATE_90)
img.show()
