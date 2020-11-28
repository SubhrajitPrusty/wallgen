import math
from random import randint
from .points import calcCenter
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = 200000000


def drawSlants(side):
    def randcolor(): return (randint(0, 255), randint(0, 255), randint(0, 255))

    img = Image.new("RGB", (side, side), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    y = 0
    min_w = int(side * 0.01)
    max_w = int(side * 0.1)
    adj = max_w * 2
    while y <= side + adj:
        w = randint(min_w, max_w)
        c = randcolor()
        draw.line([-adj, y, y, -adj], width=w, fill=c)
        draw.line([y, side + adj, side + adj, y], width=w, fill=c)
        y += w

    return img


#################
# TRIANGULATION #
#################

def genPoly(width, height, img, points, wshift, hshift, outl=None, pic=False):

    baseImg = Image.new(
        "RGB", (width + (wshift * 2), height + (hshift * 2)), "#000000")

    baseImg.paste(img, box=(wshift, hshift))
    bw = baseImg.width
    bh = baseImg.height

    if pic:
        idata = baseImg.load()  # load pixel data
    else:
        idata = img.load()  # load pixel data

    draw = ImageDraw.Draw(baseImg)

    for p in points:
        tp = tuple(map(tuple, p))  # convert each pair of points to tuples
        a, b = calcCenter(tp)
        try:
            b = bh - hshift - 5 if b >= bh - hshift else b
            b = hshift + 5 if b <= hshift else b

            a = bw - wshift - 5 if a >= bw - wshift else a
            a = wshift + 5 if a <= wshift else a

            c = idata[a, b]
        except Exception:
            # print(a,b)
            c = "#00ff00"  # i dont remember why i did this lmao

        if outl:
            draw.polygon(tp, fill=c, outline=outl)
        else:
            draw.polygon(tp, fill=c)  # draw one triangle

    img = baseImg.crop((wshift, hshift, baseImg.width - wshift,
                        baseImg.height - hshift))  # crop back to normal size

    return img


###########
# diamond #
###########

def genDiamond(width, height, img, outl=None, pic=False, per=1):

    x = y = 0
    per = per / 5  # more percentage is too small

    wboxes = int(per / 100.0 * width)
    hboxes = int(per / 100.0 * height)

    idata = img.load()  # load pixel data
    draw = ImageDraw.Draw(img)

    inc = width // wboxes  # increment size

    wboxes += 2
    hboxes += 2

    for i in range(hboxes - 1):  # one extra line
        for j in range(wboxes // 2 - 1):  # ¯\_(ツ)_/¯

            points = [(x, y), (x + inc, y + inc), (x + 2 * inc, y),
                      (x + inc, y - inc)]  # diamond

            a, b = (x + x + 2 * inc) // 2, y

            try:  # adj to not overflow
                b = height - 2 if b >= height else b
                b = 2 if b <= 0 else b

                a = width - 2 if a >= width else a
                a = 2 if a <= 0 else a

                c = idata[a, b]

            except Exception:
                # print(a,b)
                c = "#00ff00"  # backup

            if outl:
                draw.polygon((points), fill=c, outline=outl)
            else:
                draw.polygon((points), fill=c)
            x += 2 * inc

        y += inc

        if i % 2 == 0:
            x = -inc
        else:
            x = 0

    return img  # return final image


###########
# SQUARES #
###########

def genSquares(width, height, img, outl=None, pic=False, per=1):

    x = y = 0
    per = per / 5  # more percentage is too small

    wboxes = int(per / 100.0 * width)
    hboxes = int(per / 100.0 * height)

    idata = img.load()  # load pixel data
    draw = ImageDraw.Draw(img)

    inc = width // wboxes  # increment size

    wboxes += 1
    hboxes += 1

    for i in range(hboxes):
        for j in range(wboxes):
            points = [(x, y), (x, y + inc), (x + inc, y + inc),
                      (x + inc, y)]  # squares

            a, b = (x + x + inc) // 2, (y + y + inc) // 2  # to get pixel data
            try:  # adj to not overflow
                b = height - 5 if b >= height else b
                b = 5 if b <= 0 else b

                a = width - 5 if a >= width else a
                a = 5 if a <= 0 else a

                c = idata[a, b]

            except Exception:
                # print(a,b)
                c = "#00ff00"  # backup

            # draw one square

            if outl:
                draw.polygon((points), fill=c, outline=outl)
            else:
                draw.polygon((points), fill=c)

            x += inc  # shift cursor horizontally

        y += inc  # shift cursor vertically
        x = 0  # restore horizontal starting point

    return img  # return final image


###########
# HEXAGON #
###########

def genHexagon(width, height, img, outl=None, pic=False, per=1):

    per = 11 - per
    x = y = 0

    radius = int(per / 100.0 * min(height, width))

    idata = img.load()  # load pixel data
    draw = ImageDraw.Draw(img)

    ang = 2 * math.pi / 6  # angle inside a hexagon
    apothem = radius * math.cos(math.pi / 6)  # radius of inner circle
    side = 2 * apothem * math.tan(math.pi / 6)  # length of each side
    hexwidth = 2 * apothem  # horizontal width of a hexagon
    wboxes = width // int(hexwidth)  # adj
    hboxes = height // int((side + radius) * 0.75)  # adj

    xback = 0  # backup of x
    x, y = xback + apothem, -(side / 2)  # start here

    if pic:
        hboxes += 1

    for i in range(-1, hboxes + 1):
        for j in range(-1, wboxes + 2):
            points = [((x + radius * math.sin(k * ang)),
                       (y + radius * math.cos(k * ang))) for k in range(6)]

            a, b = x, y
            try:  # adj to not overflow
                b = b - side // 2 if b >= height else b
                b = b + side // 2 if b <= 0 else b

                a = a - radius if a >= width else a
                a = a + radius if a <= 0 else a

                c = idata[a, b]

            except Exception:
                # print(a,b)
                c = "#00ff00"  # backup

            if outl:
                # draw one hexagon
                draw.polygon((points), fill=c, outline=outl)
            else:
                draw.polygon((points), fill=c)  # draw one hexagon
            x += hexwidth

        y += radius + (side / 2)  # shift cursor vertically
        if i % 2 == 0:
            x = xback + apothem  # restore horizontal starting point
        else:
            x = xback  # restore horizontal starting point, for honeycombing

    return img  # return final image

#############
# ISOMETRIC #
#############


def genIsometric(width, height, img, outl=None, pic=False, per=1):

    per = 11 - per
    x = y = 0

    radius = int(per / 100.0 * min(height, width))

    idata = img.load()  # load pixel data
    draw = ImageDraw.Draw(img)

    ang = 2 * math.pi / 6  # angle inside a hexagon
    apothem = radius * math.cos(math.pi / 6)  # radius of inner circle
    side = 2 * apothem * math.tan(math.pi / 6)  # length of each side
    hexwidth = 2 * apothem  # horizontal width of a hexagon
    wboxes = width // int(hexwidth)  # adj
    hboxes = height // int((side + radius) * 0.75)  # adj

    xback = 0  # backup of x
    x, y = xback + apothem, -(side / 2)  # start here

    if pic:
        hboxes += 1

    for i in range(-1, hboxes + 1):
        for j in range(wboxes + 2):
            points = [((x + radius * math.sin(k * ang)),
                       (y + radius * math.cos(k * ang))) for k in range(6)]
            # to store the vertices of the individual equilateral triangles
            # that make up a hexagon
            triangle_points = []
            c = []  # store center colors of each equilateral triangle
            for k in range(-5, 1):
                # storing vertices of individual triangles
                triangle_points.append([(x, y), points[k], points[k + 1]])
                # calculating centre of individual triangles
                a, b = calcCenter([(x, y), points[k], points[k + 1]])
                try:  # adj to not overflow
                    b = height - 1 if b >= height else b
                    b = 1 if b <= 0 else b

                    a = width - 1 if a >= width else a
                    a = 1 if a <= 0 else a

                    c.append(idata[a, b])  # setting the color of the triangle

                except Exception:
                    # print(a,b)
                    c.append("#00ff00")  # backup

            if outl:
                for k in range(6):
                    # draw 6 triangles that form a hexagon
                    draw.polygon((triangle_points[k]), fill=c[k], outline=outl)
            else:
                for k in range(6):
                    # draw 6 triangles that form a hexagon
                    draw.polygon((triangle_points[k]), fill=c[k])
            x += hexwidth

        y += radius + (side / 2)  # shift cursor vertically
        if i % 2 == 0:
            x = xback + apothem  # restore horizontal starting point
        else:
            x = xback  # restore horizontal starting point, for honeycombing

    return img  # return final image

#############
# TRIANGLES #
#############


def genTriangle(width, height, img, outl=None, pic=False, per=1):

    x = y = 0
    per = per / 5  # more percentage is too small

    wboxes = int(per / 100.0 * width)
    hboxes = int(per / 100.0 * height)

    idata = img.load()  # load pixel data
    draw = ImageDraw.Draw(img)

    inc = width // wboxes  # increment size

    wboxes += 1
    hboxes += 1

    pair = 0
    for i in range(hboxes * 2):
        for j in range(wboxes):

            if i % 2 == 0:
                # triangle pointing down
                points = [(x, y), (x + inc * 2, y), (x + inc, y + inc)]
            else:
                # triangle pointing up
                points = [(x, y), (x + inc, y - inc), (x + inc * 2, y)]

            a, b = calcCenter(points)

            try:  # adj to not overflow
                b = height - 5 if b >= height else b
                b = 5 if b <= 0 else b

                a = width - 5 if a >= width else a
                a = 5 if a <= 0 else a

                c = idata[a, b]

            except Exception:
                # print(a,b)
                c = "#00ff00"  # backup

            # draw one triangle

            if outl:
                draw.polygon((points), fill=c, outline=outl)
            else:
                draw.polygon((points), fill=c)

            x += inc * 2  # shift cursor horizontally

        pair += 1
        if pair != 2:
            y += inc  # shift cursor vertically
        else:
            pair = 0

        if i % 2 == 0:
            x = -inc
        else:
            x = 0

    return img  # return final image
