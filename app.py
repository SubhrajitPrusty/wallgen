from flask import Flask, request, send_file, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
import wallgen
from gevent.pywsgi import WSGIServer
from PIL import Image

UPLOAD_FOLDER = os.path.join("static","upload")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def index():
	return render_template("home.html")


@app.route("/poly", methods=['GET','POST'])
def poly():
	if request.method == 'POST':
		# get data

		side = int(request.form.get('side'))
		np = int(request.form.get('np'))

		outline = request.form.get('outline')
		
		nColors = request.form.get('nColors')
		# print(nColors)

		colors = []

		for i in range(int(nColors)):
			colors.append(request.form.get('rgb'+str(i+1)))

		error = None
		
		try:
			colors = [tuple(bytes.fromhex(x[1:])) for x in colors]
		except Exception as e:
			print(e)
			error = "ERROR: Invalid color hex"
		
		if side > 5000 or side < 100:
			error = "WARNING: Image too large OR Image too small"
		if np < 10 or np > 1000:
			error = "WARNING: Too less points OR too many points"

		if error != None:
			print(error)
			return render_template('error.html', context=error)
		else:
			fname = "wall-{}.png".format(int(time.time()))
			fpath = 'static/images/'+fname
			
			shift = side//10
			nside = side + shift*2 # increase size to prevent underflow

			img = wallgen.nGradient(nside, *colors)

			if outline:
				outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
			else:
				outline = None

			pts = wallgen.genPoints(np, nside, nside)
			img = wallgen.genPoly(side, side, img, pts, shift, shift, outl=outline)

			# print(fpath)
			img.save(fpath)

			imgurl = url_for('static',filename='images/'+fname)
			return render_template("download.html", context=imgurl, home="poly")
	else:
		return render_template('poly.html')

@app.route("/shape", methods=['GET','POST'])
def shape():
	if request.method == 'POST':
		# get data
		side = int(request.form.get('side'))
		shape = request.form.get('shape')
		# print(shape)
		
		outline = request.form.get('outline')

		nColors = request.form.get('nColors')
		# print(nColors)

		colors = []

		for i in range(int(nColors)):
			colors.append(request.form.get('rgb'+str(i+1)))

		error = None
		
		try:
			colors = [tuple(bytes.fromhex(x[1:])) for x in colors]
		except Exception as e:
			print(e)
			error = "ERROR: Invalid color hex"
		
		if side > 5000 or side < 100:
			error = "WARNING: Image too large OR Image too small"

		if error != None:
			print(error)
			return render_template('error.html', context=error)
		else:
			fname = "wall-{}.png".format(int(time.time()))
			fpath = 'static/images/'+fname
			img = wallgen.nGradient(side, *colors)

			if outline:
				outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
			else:
				outline = None

			if shape == 'hexagon':
				img = wallgen.genHexagon(side, side, img, outline)
			elif shape == 'squares':
				img = wallgen.genSquares(side, side, img, outline)
			elif shape == 'diamond':
				img = wallgen.genDiamond(side, side, img, outline)
			elif shape == 'triangle':
			    img = wallgen.genTriangle(side, side, img, outline)
			elif shape == 'isometric':
			    img = wallgen.genIsometric(side, side, img, outline)
			# print(fpath)
			img.save(fpath)
			imgurl = url_for('static',filename='images/'+fname)
			return render_template("download.html", context=imgurl, home="shape")
	else:
		return render_template('shape.html')


@app.route("/pic", methods=['GET', 'POST'])
def pic():
	if request.method == 'POST':
		# print(request.files)
		# print(request.form)
		if 'image' not in request.files:
			error = "No file part"
			return render_template("error.html", context=error)
		else:
			file = request.files['image']
			# print(file.filename)
			# print(len(file.filename))
			if len(file.filename) < 1:
				error = "No file selected"
				return render_template("error.html", context=error)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				ufpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				file.save(ufpath)
				if request.form.get('np'):
					np = request.form.get('np')
					outline = request.form.get('outline')

					img = Image.open(ufpath)
					width = img.width
					height = img.height

					if outline:
						outline = tuple(bytes.fromhex("#2c2c2c"[1:]))
					else:
						outline = None

					pts = wallgen.genPoints(int(np), width, height)
					img = wallgen.genPoly(img.width, img.height, img, pts, outline, pic=True)

					fname = "wall-{}.png".format(int(time.time()))
					fpath = 'static/images/'+fname

					# print(fpath)
					img.save(fpath)
					imgurl = url_for('static',filename='images/'+fname)
					return render_template("download.html", context=imgurl, home="pic")
				else:
					error = "Invalid input, try again"
					return render_template("error.html", context=error)
			else:
				error = "filetype not allowed"
				return render_template("error.html", context=error)
	else:
		return render_template("pic.html")


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	http_server = WSGIServer(('',port),app)
	http_server.serve_forever()
