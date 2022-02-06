"""
Main wallgen entry point
"""

import os
import sys
import time
import tempfile
from random import choice, randint

import click
import numpy as np
from loguru import logger
from skimage import color

from tools.wallpaper import setwallpaper
from tools.points import genPoints, genSmartPoints
from tools.gradient import (
    Image,
    NbyNGradient,
    nGradient,
    random_gradient,
    swirl_image,
    randcolor,
)
from tools.shapes import (
    drawSlants,
    genDiamond,
    genHexagon,
    genIsometric,
    genPoly,
    genSquares,
    genTriangle,
)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
TMP_DIR = os.path.join(tempfile.gettempdir(), "wallgen")
os.makedirs(TMP_DIR, exist_ok=True)

logger.remove()
logger.add(
    os.path.join(TMP_DIR, "wallgen.log"),
    rotation="5 MB",
    backtrace=True,
    diagnose=True,
    enqueue=True,
    catch=True,
    level="WARNING",
)

MAX_POINTS = 20000
MIN_POINTS = 3


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """CLI entry point group"""
    return None


@cli.command()
@click.argument("side", type=click.INT, metavar="PIXELS")
@click.option(
    "--colors",
    "-c",
    multiple=True,
    type=click.STRING,
    metavar="#HEXCODE",
    help="Use many colors in a custom gradient",
)
@click.option(
    "--points",
    "-p",
    default=100,
    metavar="no-of-points",
    help="Number of points to use, default = 100",
)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option(
    "--outline",
    "-o",
    default=None,
    metavar="#HEXCODE",
    help="Outline the triangles",
)
@click.option(
    "--name",
    "-n",
    metavar="/path/to/output_file",
    help="Rename the output file",
)
@click.option(
    "--only-color", "-oc", is_flag=True, help="Generate just a gradient image"
)
@click.option(
    "--use-nn", "-un", is_flag=True, help="Use NbyNGradient function"
)
@click.option(
    "--swirl",
    "-sw",
    type=click.INT,
    metavar="STRENGTH",
    help="Swirl the gradient. [1-10]",
)
@click.option(
    "--scale",
    "-sc",
    default=2,
    help="""Scale image to do anti-aliasing. Default=2. scale=1 means
               no antialiasing. [WARNING: Very memory expensive]""",
)
@click.option(
    "--set-wall",
    "-w",
    is_flag=True,
    help="Set the generated image as your Desktop wallpaper",
)
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
    set_wall,
):
    """Generates a HQ low poly image using a gradient"""

    error = ""
    if side < 50:
        error = "Image too small. Minimum size 50"
    elif points < MIN_POINTS:
        error = f"Too less points. Minimum points {MIN_POINTS}"
    elif points > MAX_POINTS:
        error = f"Too many points. Maximum points {MAX_POINTS}"
    elif scale < 1:
        error = "Invalid scale value"

    if error:
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    side = side * scale  # increase size to anti alias

    shift = side // 10
    nside = side + shift * 2  # increase size to prevent underflow

    if colors:
        if len(colors) < 2:
            error = "One color gradient not possible."
            logger.error(error)
            click.secho(error, fg="red", err=True)
            sys.exit(1)
        try:
            cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
        except Exception as e:
            logger.error(e)
            click.secho("Invalid color hex", fg="red", err=True)
            sys.exit(1)
        img = nGradient(nside, *cs)
    else:
        if use_nn:
            points = 1000 if points < 1000 else points
            img = NbyNGradient(nside)
        else:
            img = random_gradient(nside)

    if swirl:
        if only_color:
            img = img.resize(
                (side // scale, side // scale), resample=Image.BICUBIC
            )
        img = swirl_image(img, swirl)

    if not only_color:
        if outline:
            if isinstance(outline, tuple):
                pass
            else:
                try:
                    outline = tuple(bytes.fromhex(outline[1:]))
                except Exception as e:
                    logger.error(e)
                    click.secho("Invalid color hex", fg="red", err=True)
                    sys.exit(1)

        print("Preparing image", end="")
        pts = genPoints(points, nside, nside)

        print("\r", end="")
        print("Generated points", end="")
        img = genPoly(side, side, img, pts, shift, shift, outl=outline)

        print("\r", end="")
        print("Making final tweaks", end="")
        img = img.resize(
            (side // scale, side // scale), resample=Image.BICUBIC
        )

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = f"{name}.png"
        img.save(file_name)
    else:
        file_name = f"wall-{int(time.time())}.png"
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")

    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            logger.error(msg)
            click.secho(msg, fg="red")


@cli.command()
@click.argument("side", type=click.INT, metavar="PIXELS")
@click.option(
    "--type",
    "-t",
    "choice_of_shape",
    metavar="[sq/hex/dia/tri/iso]",
    type=click.Choice(["sq", "hex", "dia", "tri", "iso"]),
    help="""
              Choose which shape to use.
              [Square/Hexagons/Diamonds/Triangles/Isometric]
              """,
)
@click.option(
    "--colors",
    "-c",
    multiple=True,
    type=click.STRING,
    metavar="#HEXCODE",
    help="Use many colors in a custom gradient",
)
@click.option(
    "--percent",
    "-p",
    type=click.INT,
    metavar="1-10",
    default=1,
    help="Use this percentage to determine number of polygons. [1-10]\
              ",
)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option(
    "--outline",
    "-o",
    default=None,
    metavar="#HEXCODE",
    help="Outline the shapes",
)
@click.option(
    "--name",
    "-n",
    metavar="/path/to/output_file",
    help="Rename the output file",
)
@click.option(
    "--use-nn", "-un", is_flag=True, help="Use NbyNGradient function"
)
@click.option(
    "--swirl",
    "-sw",
    type=click.INT,
    metavar="STRENGTH",
    help="Swirl the gradient. [1-10]",
)
@click.option(
    "--scale",
    "-sc",
    default=2,
    help="""Scale image to do anti-aliasing. Default=2. scale=1 means
               no antialiasing. [WARNING: Very memory expensive]""",
)
@click.option(
    "--set-wall",
    "-w",
    is_flag=True,
    help="Set the generated image as your Desktop wallpaper",
)
def shape(
    side,
    choice_of_shape,
    colors,
    show,
    outline,
    name,
    percent,
    use_nn,
    swirl,
    scale,
    set_wall,
):
    """Generates a HQ image of a beautiful shapes"""

    error = ""
    if side < 50:
        error = "Image too small. Minimum size 50"
    if percent is not None:
        if percent < 1 or percent > 10:
            error = f"Error {percent} : Percent range 1-10"

    if error:
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    side = side * scale  # increase size to anti alias

    if colors:
        if len(colors) < 2:
            error = "One color gradient not possible."
            logger.error(error)
            click.secho(error, fg="red", err=True)
            sys.exit(1)
        try:
            cs = [tuple(bytes.fromhex(c[1:])) for c in colors]
        except Exception as e:
            logger.error(e)
            click.secho("Invalid color hex", fg="red", err=True)
            sys.exit(1)
        img = nGradient(side, *cs)
    else:
        if use_nn:
            img = NbyNGradient(side)
        else:
            img = random_gradient(side)

    if swirl:
        img = swirl_image(img, swirl)

    if outline:
        if isinstance(outline, tuple):
            pass
        else:
            try:
                outline = tuple(bytes.fromhex(outline[1:]))
            except Exception as e:
                logger.error(e)
                click.secho("Invalid color hex", fg="red", err=True)
                sys.exit(1)

    print("Preparing image", end="")

    if choice_of_shape == "hex":
        percent = percent if percent else 5
        img = genHexagon(side, side, img, outline, per=(percent or 1))
    elif choice_of_shape == "sq":
        img = genSquares(side, side, img, outline, per=(percent or 1))
    elif choice_of_shape == "dia":
        img = genDiamond(side, side, img, outline, per=(percent or 1))
    elif choice_of_shape == "tri":
        img = genTriangle(side, side, img, outline, per=(percent or 1))
    elif choice_of_shape == "iso":
        img = genIsometric(side, side, img, outline, per=(percent or 1))
    else:
        error = """
        No shape given. To see list of shapes \"wallgen shape --help\"
        """
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    print("\r", end="")
    print("Making final tweaks", end="")

    img = img.resize((side // scale, side // scale), resample=Image.BICUBIC)

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = f"{name}.png"
        img.save(file_name)
    else:
        file_name = f"wall-{int(time.time())}.png"
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            logger.error(msg)
            click.secho(msg, fg="red")


@cli.command()
@click.argument("side", type=click.INT, metavar="PIXELS")
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option("--name", "-n", help="Rename the output")
@click.option(
    "--swirl",
    "-sw",
    type=click.INT,
    metavar="STRENGTH",
    help="Swirl the gradient. [1-10]",
)
@click.option(
    "--set-wall",
    "-w",
    is_flag=True,
    help="Set the generated image as your Desktop wallpaper",
)
@click.option("--gradient", "-g", is_flag=True, help="Make a gradient")
@click.option("--invert", "-i", is_flag=True, help="Invert the bottom part")
def slants(side, show, name, swirl, set_wall, gradient, invert):
    """Generates slanting lines of various colors"""

    error = ""
    if side < 50:
        error = "Image too small. Minimum size 50"

    if error:
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    scale = 2
    side = side * scale  # increase size to anti alias
    print("Preparing image", end="")

    img = drawSlants(side, gradient, invert)

    print("\r", end="")
    print("Making final tweaks", end="")
    img = img.resize((side // scale, side // scale), resample=Image.BICUBIC)

    if swirl:
        img = swirl_image(img, swirl)

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = f"{name}.png"
        img.save(file_name)
    else:
        file_name = f"wall-{int(time.time())}.png"
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            logger.error(msg)
            click.secho(msg, fg="red")


@cli.group()
def pic():
    """Use a picture instead of a gradient"""


@pic.command(name="poly")
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--points",
    "-p",
    default=1000,
    metavar="no-of-points",
    help="Number of points to use, default = 1000",
)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option(
    "--outline",
    "-o",
    default=None,
    metavar="#HEXCODE",
    help="Outline the triangles",
)
@click.option(
    "--name",
    "-n",
    metavar="/path/to/output_file",
    help="Rename the output file",
)
@click.option("--smart", "-sm", is_flag=True, help="Use smart points")
@click.option(
    "--set-wall",
    "-w",
    is_flag=True,
    help="Set the generated image as your Desktop wallpaper",
)
def pic_poly(image, points, show, outline, name, smart, set_wall):
    """Generates a HQ low poly image"""

    if points < MIN_POINTS:
        error = f"Too less points. Minimum points {MIN_POINTS}"
    elif points > MAX_POINTS:
        error = f"Too many points. Maximum points {MAX_POINTS}"
    else:
        error = None

    if error:
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    # wshift = img.width//10
    # hshift = img.height//10
    # width += wshift*1
    # height += hshift*2

    if outline:
        if isinstance(outline,  tuple):
            pass
        else:
            try:
                outline = tuple(bytes.fromhex(outline[1:]))
            except Exception as e:
                logger.error(e)
                click.secho("Invalid color hex", fg="red", err=True)
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

    final_img = genPoly(
        img.width, img.height, img, pts, wshift, hshift, outline, pic=True
    )

    print("\r", end="")
    print("Making final tweaks", end="")

    if show:
        final_img.show()

    file_name = ""

    if name:
        file_name = f"{name}.png"
        final_img.save(file_name)
    else:
        file_name = f"wall-{int(time.time())}.png"
        final_img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")

    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            logger.error(msg)
            click.secho(msg, fg="red")


@pic.command(name="shape")
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--type",
    "-t",
    "shape",
    type=click.Choice(["sq", "hex", "dia", "tri", "iso"]),
    metavar="[sq/hex/dia/tri/iso]",
    help="""
              Choose which shape to use.
              [Square/Hexagons/Diamonds/Triangles/Isometric]
              """,
)
@click.option(
    "--percent",
    "-p",
    type=click.INT,
    metavar="1-10",
    help="""
              Use this percentage to determine number of polygons. [1-10]
              """,
)
@click.option("--show", "-s", is_flag=True, help="Open the image")
@click.option(
    "--outline",
    "-o",
    default=None,
    metavar="#HEXCODE",
    help="Outline the shapes",
)
@click.option(
    "--name", "-n", metavar="/path/to/output_file", help="Rename the output"
)
@click.option(
    "--set-wall",
    "-w",
    is_flag=True,
    help="Set the generated image as your Desktop wallpaper",
)
def pic_shape(image, shape, show, outline, name, percent, set_wall):
    """Generate a HQ image of a beautiful shapes"""
    error = None
    if percent:
        if percent < 1 or percent > 10:
            error = "Percent range 1-10"

    if error:
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    img = Image.open(image)

    width = img.width
    height = img.height

    if outline:
        if isinstance(outline, tuple):
            pass
        else:
            try:
                outline = tuple(bytes.fromhex(outline[1:]))
            except Exception as e:
                logger.error(type(e).__name__)
                logger.error(e)
                click.secho("Invalid color hex", fg="red", err=True)
                sys.exit(1)

    print("Preparing image", end="")

    if shape == "hex":
        percent = percent if percent else 5
        img = genHexagon(width, height, img, outline, pic=True, per=percent)
    elif shape == "sq":
        img = genSquares(width, height, img, outline, pic=True, per=percent)
    elif shape == "dia":
        img = genDiamond(width, height, img, outline, pic=True, per=percent)
    elif shape == "tri":
        img = genTriangle(width, height, img, outline, pic=True, per=percent)
    elif shape == "iso":
        img = genIsometric(width, height, img, outline, pic=True, per=percent)
    else:
        error = """
        No shape given. To see list of shapes \"wallgen pic shape --help\"
        """
        logger.error(error)
        click.secho(error, fg="red", err=True)
        sys.exit(1)

    print("\r", end="")
    print("Making final tweaks", end="")

    if show:
        img.show()

    file_name = ""

    if name:
        file_name = f"{name}.png"
        img.save(file_name)
    else:
        file_name = f"wall-{int(time.time())}.png"
        img.save(file_name)

    print("\r", end="")
    print(f"Image is stored at {file_name}")
    if set_wall:
        msg, ret = setwallpaper(file_name)
        if ret:
            click.secho(msg, fg="green")
        else:
            logger.error(msg)
            click.secho(msg, fg="red")


@cli.command(name="random")
@click.argument("side", type=click.INT, metavar="PIXELS")
@click.option(
    "--name",
    "-n",
    metavar="/path/to/output_file",
    help="Rename the output file",
)
@click.pass_context
def randomize(ctx, side, name):
    """Generate a random config
    """
    choice_of_pattern = ["poly", "shape", "slants"]
    pattern = choice(choice_of_pattern)
    click.secho(f"Random choice of pattern: {pattern}")

    points = randint(3, 5000)
    outline = randcolor()
    outline_hex = "#" + "".join((hex(x)[2:] for x in randcolor()))
    use_nn = choice([True, False])
    swirl = choice(list(range(0, 11)))

    if pattern == "poly":
        click.secho(
            f"Random config: \
            \npoints = {points}\
            \noutline = {outline} | {outline_hex}\
            \nuse_nn = {use_nn}\
            \nswirl = {swirl}"
        )

        ctx.invoke(
            poly,
            side=side,
            points=points,
            outline=outline,
            use_nn=use_nn,
            swirl=swirl,
            name=name,
            colors=False,
        )

    elif pattern == "shape":
        choice_of_shape = choice(["sq", "hex", "dia", "tri", "iso"])
        percent = choice(list(range(1, 11)))
        click.secho(
            f"Random config: \
            \nchoice_of_shape = {choice_of_shape}\
            \npercent = {percent}\
            \npoints = {points}\
            \noutline = {outline} | {outline_hex}\
            \nuse_nn = {use_nn}\
            \nswirl = {swirl}"
        )

        ctx.invoke(
            shape,
            side=side,
            percent=percent,
            outline=outline,
            use_nn=use_nn,
            swirl=swirl,
            name=name,
            choice_of_shape=choice_of_shape,
            colors=False,
        )

    elif pattern == "slants":
        gradient = choice([True, False])
        invert = choice([True, False])
        click.secho(
            f"Random config: \
            \ngradient = {gradient}\
            \ninvert = {invert}\
            \nswirl = {swirl}"
        )

        ctx.invoke(
            slants,
            side=side,
            swirl=swirl,
            gradient=gradient,
            invert=invert,
            name=name,
        )

    print()


if __name__ == "__main__":
    cli()
