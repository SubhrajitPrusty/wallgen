import os
import time
from PIL import Image
from skimage import color, io
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, url_for
from wallgen import (
    NbyNGradient,
    genDiamond,
    genHexagon,
    genIsometric,
    genPoints,
    genPoly,
    genSmartPoints,
    genSquares,
    genTriangle,
    nGradient,
    random_gradient,
    swirl_image,
)

UPLOAD_FOLDER = os.path.join("static", "upload")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

app = Flask(__name__, static_url_path="/static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/poly", methods=["GET", "POST"])
def poly():
    if request.method == "POST":
        # get data
        side = int(request.form.get("side"))
        np = int(request.form.get("np"))
        outline = request.form.get("outline")
        bgtype = request.form.get("bgtype")
        swirl = request.form.get("swirl")

        error = None

        if side > 5000 or side < 100:
            error = "WARNING: Image too large OR Image too small"
        if np < 10 or np > 10001:
            error = "WARNING: Too less points OR too many points"

        fname = "wall-{}.png".format(int(time.time()))
        fpath = "static/images/" + fname

        shift = side // 10
        nside = side + shift * 2  # increase size to prevent underflow

        img = random_gradient(nside)

        if bgtype == "nbyn":
            img = NbyNGradient(nside)
        elif bgtype == "customColors":
            nColors = request.form.get("nColors")
            colors = []

            for i in range(int(nColors)):
                colors.append(request.form.get("rgb" + str(i + 1)))

            try:
                colors = [tuple(bytes.fromhex(x[1:])) for x in colors]
            except Exception as e:
                print(e)
                error = "ERROR: Invalid color hex"

            img = nGradient(nside, *colors)

        if error is not None:
            print(error)
            return render_template("error.html", context=error)

        if outline:
            outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
        else:
            outline = None

        if swirl:
            img = swirl_image(img)

        pts = genPoints(np, nside, nside)
        img = genPoly(side, side, img, pts, shift, shift, outl=outline)

        # print(fpath)
        img.save(fpath)

        imgurl = url_for("static", filename="images/" + fname)
        return render_template("download.html", context=imgurl, home="poly")
    else:
        return render_template("poly.html")


@app.route("/shape", methods=["GET", "POST"])
def shape():
    if request.method == "POST":
        side = int(request.form.get("side"))
        outline = request.form.get("outline")
        bgtype = request.form.get("bgtype")
        swirl = request.form.get("swirl")
        shape = request.form.get("shape")

        error = None

        if side > 5000 or side < 100:
            error = "WARNING: Image too large OR Image too small"

        fname = "wall-{}.png".format(int(time.time()))
        fpath = "static/images/" + fname

        img = random_gradient(side)

        if bgtype == "nbyn":
            img = NbyNGradient(side)
        elif bgtype == "customColors":
            nColors = request.form.get("nColors")
            colors = []

            for i in range(int(nColors)):
                colors.append(request.form.get("rgb" + str(i + 1)))

            try:
                colors = [tuple(bytes.fromhex(x[1:])) for x in colors]
            except Exception as e:
                print(e)
                error = "ERROR: Invalid color hex"

            img = nGradient(side, *colors)

        if error is not None:
            print(error)
            return render_template("error.html", context=error)

        if outline:
            outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
        else:
            outline = None

        if swirl:
            img = swirl_image(img)

        if shape == "hexagon":
            img = genHexagon(side, side, img, outline, per=5)
        elif shape == "squares":
            img = genSquares(side, side, img, outline, per=5)
        elif shape == "diamond":
            img = genDiamond(side, side, img, outline, per=5)
        elif shape == "triangle":
            img = genTriangle(side, side, img, outline, per=5)
        elif shape == "isometric":
            img = genIsometric(side, side, img, outline, per=5)
        # print(fpath)
        img.save(fpath)
        imgurl = url_for("static", filename="images/" + fname)
        return render_template("download.html", context=imgurl, home="shape")
    else:
        return render_template("shape.html")


@app.route("/pic", methods=["GET", "POST"])
def pic():
    if request.method == "POST":
        # print(request.files)
        # print(request.form)
        if "image" not in request.files:
            error = "No file part"
            return render_template("error.html", context=error)
        else:
            file = request.files["image"]
            # print(file.filename)
            # print(len(file.filename))
            if len(file.filename) < 1:
                error = "No file selected"
                return render_template("error.html", context=error)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ufpath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(ufpath)
                np = request.form.get("np")
                outline = request.form.get("outline")
                smart = request.form.get("smart")

                if np or smart:
                    og_img = Image.open(ufpath)
                    width = og_img.width
                    height = og_img.height

                    if min(height, width) > 1080:
                        scale = min(height, width) // 1080
                    else:
                        scale = 1
                    img = og_img.resize(
                        (width // scale, height // scale),
                        resample=Image.BICUBIC,
                    )
                    width = img.width
                    height = img.height
                    wshift = width // 100
                    hshift = height // 100

                    n_width = width + 2 * wshift
                    n_height = height + 2 * height

                    if outline:
                        outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
                    else:
                        outline = None

                    if smart:
                        ski_img = io.imread(ufpath, True)
                        gray_img = color.rgb2gray(ski_img)
                        pts = genSmartPoints(gray_img)
                    else:
                        pts = genPoints(int(np), n_width, n_height)

                    img = genPoly(
                        img.width,
                        img.height,
                        img,
                        pts,
                        wshift,
                        hshift,
                        outline,
                        pic=True,
                    )

                    fname = "wall-{}.png".format(int(time.time()))
                    fpath = "static/images/" + fname

                    # print(fpath)
                    img.save(fpath)
                    imgurl = url_for("static", filename="images/" + fname)
                    return render_template(
                        "download.html", context=imgurl, home="pic"
                    )
                else:
                    error = "Invalid input, try again"
                    return render_template("error.html", context=error)
            else:
                error = "filetype not allowed"
                return render_template("error.html", context=error)
    else:
        return render_template("pic.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    http_server = WSGIServer(("", port), app)
    print("Starting server:")
    http_server.serve_forever()
