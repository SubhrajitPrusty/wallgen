import sys
import time
import click
import numpy as np
from skimage import color
from tools.wallpaper import setwallpaper
from tools.points import (
    genPoints,
    genSmartPoints)
from tools.gradient import (
    Image,
    NbyNGradient,
    nGradient,
    random_gradient,
    swirl_image)
from tools.shapes import (
    drawSlants,
    genDiamond,
    genHexagon,
    genIsometric,
    genPoly,
    genSquares,
    genTriangle)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--colors", "-c", multiple=True, type=click.STRING,
              metavar="#HEXCODE", help="Use many colors in a custom gradient")
@click.option("--points", "-p", default=100, metavar="no-of-points",
              help="Number of points to use, default = 100")
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--outline", "-o", default=None,
              metavar="#HEXCODE", help="Outline the triangles")
@click.option("--name", "-n", metavar="/path/to/output_file",
              help="Rename the output file")
@click.option("--only-color", "-oc", is_flag=True,
              help="Generate just a gradient image")
@click.option("--use-nn", "-un", is_flag=True,
              help="Use NbyNGradient function")
@click.option("--swirl", "-sw", is_flag=True, help="Swirl the gradient")
@click.option("--scale", "-sc", default=2,
              help="""Scale image to do anti-aliasing. Default=2. scale=1 means
               no antialiasing. [WARNING: Very memory expensive]""")
@click.option("--set-wall", "-w", is_flag=True,
              help="Set the generated image as your Desktop wallpaper")
def poly(
        side,
        points,
        show,
        colors,
        outline,
        name,
        only_color,
        use_nn,
        swirl,
        scale,
        set_wall):
    """ Generates a HQ low poly image using a gradient """

    error = ""
    if side < 50:
        error = "Image too small. Minimum size 50"
    elif points < 3:
        error = "Too less points. Minimum points 3"
    elif points > 200000:
        error = "Too many points. Maximum points 200000"
    elif scale < 1:
        error = "Invalid scale value"

    if error:
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    side = side * scale  # increase size to anti alias

    shift = side // 10
    nside = side + shift * 2  # increase size to prevent underflow

    if colors:
        if len(colors) < 2:
            click.secho("One color gradient not possible.", fg="red", err=True)
            sys.exit(1)
        cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
        img = nGradient(nside, *cs)
    else:
        if use_nn:
            points = 1000 if points < 1000 else points
            img = NbyNGradient(nside)
        else:
            img = random_gradient(nside)

    if swirl:
        img = swirl_image(img)

    if not only_color:
        if outline:
            try:
                outline = tuple(bytes.fromhex(outline[1:]))
            except Exception:
                click.secho("Invalid color hex", fg='red', err=True)
                sys.exit(1)

        print("Preparing image", end="")
        pts = genPoints(points, nside, nside)

        print("\r", end="")
        print("Generated points", end="")
        img = genPoly(side, side, img, pts, shift, shift, outl=outline)

        print("\r", end="")
        print("Making final tweaks", end="")
        img = img.resize((side // scale, side // scale),
                         resample=Image.BICUBIC)

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = "{}.png".format(name)
        img.save(file_name)
    else:
        file_name = "wall-{}.png".format(int(time.time()))
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")

    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            click.secho(msg, fg="red")


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--type",
              "-t",
              "shape",
              metavar="[sq/hex/dia/tri/iso]",
              type=click.Choice(['sq',
                                 'hex',
                                 'dia',
                                 'tri',
                                 'iso']),
              help="""
              Choose which shape to use.
              [Square/Hexagons/Diamonds/Triangles/Isometric]
              """)
@click.option("--colors", "-c", multiple=True, type=click.STRING,
              metavar="#HEXCODE", help="Use many colors in a custom gradient")
@click.option("--percent", "-p", type=click.INT, metavar="1-10", default=1,
              help="Use this percentage to determine number of polygons. [1-10]\
              ")
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--outline", "-o", default=None,
              metavar="#HEXCODE", help="Outline the shapes")
@click.option("--name", "-n", metavar="/path/to/output_file",
              help="Rename the output file")
@click.option("--use-nn", "-un", is_flag=True,
              help="Use NbyNGradient function")
@click.option("--swirl", "-sw", is_flag=True, help="Swirl the gradient")
@click.option("--scale", "-sc", default=2,
              help="""Scale image to do anti-aliasing. Default=2. scale=1 means
               no antialiasing. [WARNING: Very memory expensive]""")
@click.option("--set-wall", "-w", is_flag=True,
              help="Set the generated image as your Desktop wallpaper")
def shape(
        side,
        shape,
        colors,
        show,
        outline,
        name,
        percent,
        use_nn,
        swirl,
        scale,
        set_wall):
    """ Generates a HQ image of a beautiful shapes """

    error = ""
    if side < 50:
        error = "Image too small. Minimum size 50"
    if percent is not None:
        if percent < 1 or percent > 10:
            error = "Error {} : Percent range 1-10".format(percent)

    if error:
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    side = side * scale  # increase size to anti alias

    if colors:
        if len(colors) < 2:
            click.secho("One color gradient not possible.", fg="red", err=True)
            sys.exit(1)
        cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
        img = nGradient(side, *cs)
    else:
        if use_nn:
            img = NbyNGradient(side)
        else:
            img = random_gradient(side)

    if swirl:
        img = swirl_image(img)

    if outline:
        try:
            outline = tuple(bytes.fromhex(outline[1:]))
        except Exception:
            click.secho("Invalid color hex", fg='red', err=True)
            sys.exit(1)

    print("Preparing image", end="")

    if shape == 'hex':
        percent = percent if percent else 5
        img = genHexagon(side, side, img, outline, per=(percent or 1))
    elif shape == 'sq':
        img = genSquares(side, side, img, outline, per=(percent or 1))
    elif shape == 'dia':
        img = genDiamond(side, side, img, outline, per=(percent or 1))
    elif shape == 'tri':
        img = genTriangle(side, side, img, outline, per=(percent or 1))
    elif shape == 'iso':
        img = genIsometric(side, side, img, outline, per=(percent or 1))
    else:
        error = """
        No shape given. To see list of shapes \"wallgen shape --help\"
        """
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    print("\r", end="")
    print("Making final tweaks", end="")

    img = img.resize((side // scale, side // scale), resample=Image.BICUBIC)

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = "{}.png".format(name)
        img.save(file_name)
    else:
        file_name = "wall-{}.png".format(int(time.time()))
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            click.secho(msg, fg="red")


@cli.command()
@click.argument("side", type=click.INT)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--name", "-n", help="Rename the output")
@click.option("--swirl", "-sw", is_flag=True, help="Swirl the image")
@click.option("--set-wall", "-w", is_flag=True,
              help="Set the generated image as your Desktop wallpaper")
def slants(side, show, name, swirl, set_wall):
    """ Generates slanting lines of various colors """

    scale = 2
    side = side * scale  # increase size to anti alias
    print("Preparing image", end="")

    img = drawSlants(side)

    print("\r", end="")
    print("Making final tweaks", end="")
    img = img.resize((side // scale, side // scale), resample=Image.BICUBIC)

    if swirl:
        img = swirl_image(img)

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = "{}.png".format(name)
        img.save(file_name)
    else:
        file_name = "wall-{}.png".format(int(time.time()))
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            click.secho(msg, fg="red")


@cli.group()
def pic():
    """ Use a picture instead of a gradient """


@pic.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option("--points", "-p", default=1000, metavar="no-of-points",
              help="Number of points to use, default = 1000")
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--outline", "-o", default=None,
              metavar="#HEXCODE", help="Outline the triangles")
@click.option("--name", "-n", metavar="/path/to/output_file",
              help="Rename the output file")
@click.option("--smart", "-sm", is_flag=True, help="Use smart points")
@click.option("--set-wall", "-w", is_flag=True,
              help="Set the generated image as your Desktop wallpaper")
def poly(image, points, show, outline, name, smart, set_wall):  # noqa: F811
    """ Generates a HQ low poly image """

    if points < 3:
        error = "Too less points. Minimum points 3"
    elif points > 200000:
        error = "Too many points. Maximum points {}".format(200000)
    else:
        error = None

    if error:
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    # wshift = img.width//10
    # hshift = img.height//10
    # width += wshift*1
    # height += hshift*2

    if outline:
        try:
            outline = tuple(bytes.fromhex(outline[1:]))
        except Exception:
            click.secho("Invalid color hex", fg='red', err=True)
            sys.exit(1)

    print("Preparing image", end="")

    img = Image.open(image)
    width = img.width
    height = img.height
    wshift = width // 100
    hshift = height // 100

    n_width = width + 2 * wshift
    n_height = height + 2 * hshift

    if smart:
        # Sobel Edge
        ski_img = np.array(img)
        gray_img = color.rgb2gray(ski_img)
        pts = genSmartPoints(gray_img)
    else:
        pts = genPoints(points, n_width, n_height)

    print("\r", end="")
    print("Generated points", end="")

    final_img = genPoly(img.width, img.height, img, pts,
                        wshift, hshift, outline, pic=True)

    print("\r", end="")
    print("Making final tweaks", end="")

    if show:
        final_img.show()

    file_name = ""

    if name:
        file_name = "{}.png".format(name)
        final_img.save(file_name)
    else:
        file_name = "wall-{}.png".format(int(time.time()))
        final_img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")

    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            click.secho(msg, fg="red")


@pic.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option("--type",
              "-t",
              "shape",
              type=click.Choice(['sq',
                                 'hex',
                                 'dia',
                                 'tri',
                                 'iso']),
              metavar="[sq/hex/dia/tri/iso]",
              help="""
              Choose which shape to use.
              [Square/Hexagons/Diamonds/Triangles/Isometric]
              """)
@click.option("--percent", "-p", type=click.INT, metavar="1-10",
              help="""
              Use this percentage to determine number of polygons. [1-10]
              """)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--outline", "-o", default=None,
              metavar="#HEXCODE", help="Outline the shapes")
@click.option("--name",
              "-n",
              metavar="/path/to/output_file",
              help="Rename the output")
@click.option("--set-wall", "-w", is_flag=True,
              help="Set the generated image as your Desktop wallpaper")
def shape(image, shape, show, outline, name, percent, set_wall):  # noqa: F811
    """ Generate a HQ image of a beautiful shapes """
    error = None
    if percent:
        if percent < 1 or percent > 10:
            error = "Percent range 1-10"

    if error:
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    img = Image.open(image)

    width = img.width
    height = img.height

    if outline:
        try:
            outline = tuple(bytes.fromhex(outline[1:]))
        except Exception:
            click.secho("Invalid color hex", fg='red', err=True)
            sys.exit(1)

    print("Preparing image", end="")

    if shape == 'hex':
        percent = percent if percent else 5
        img = genHexagon(width, height, img, outline, pic=True, per=percent)
    elif shape == 'sq':
        img = genSquares(width, height, img, outline, pic=True, per=percent)
    elif shape == 'dia':
        img = genDiamond(width, height, img, outline, pic=True, per=percent)
    elif shape == 'tri':
        img = genTriangle(width, height, img, outline, pic=True, per=percent)
    elif shape == 'iso':
        img = genIsometric(width, height, img, outline, pic=True, per=percent)
    else:
        error = """
        No shape given. To see list of shapes \"wallgen pic shape --help\"
        """
        click.secho(error, fg='red', err=True)
        sys.exit(1)

    print("\r", end="")
    print("Making final tweaks", end="")

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = "{}.png".format(name)
        img.save(file_name)
    else:
        file_name = "wall-{}.png".format(int(time.time()))
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            click.secho(msg, fg="red")


if __name__ == "__main__":
    cli()
