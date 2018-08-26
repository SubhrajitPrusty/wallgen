from PIL import Image, ImageDraw
import random

img = Image.new('RGB',(1000,1000), "#2c2c2c")
# img.show()

draw = ImageDraw.Draw(img)

x = 0
y = 0
# c1,c2,c3 = 255,0,0

for i in range(10):
	c1 = random.randint(100,255)
	c2 = random.randint(0,100)
	c3 = random.randint(100,255)
	for j in range(10):
		# points = ((0,0),(100,50),(100,150),(0,100))
		points = ((x,y),(x,y+100),(x+100,y+100),(x+100,y))
		draw.polygon((points), fill=(c1,c2,c3))
		x+=100
		# y+=100
		c1+=random.randint(10,15)
		c2+=random.randint(10,15)
		c3+=random.randint(10,15)
	x=0
	y+=100

img.show()