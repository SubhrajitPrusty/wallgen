from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import time
import wallgen
from gevent.pywsgi import WSGIServer
from PIL import Image

app = Flask(__name__, static_url_path="/static")

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
			
			side = side * 2

			shift = side//10
			nside = side + shift*2 # increase size to prevent underflow

			img = wallgen.nGradient(nside, *colors)

			pts = wallgen.genPoints(np, nside, nside)
			img = wallgen.genPoly(side, side, img, pts, shift, shift, outl=outline)

			img = img.resize((side//2, side//2), resample=Image.BICUBIC)

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
			side = side * 2

			fname = "wall-{}.png".format(int(time.time()))
			fpath = 'static/images/'+fname
			img = wallgen.nGradient(side, *colors)

			if shape == 'hexagon':
				img = wallgen.genHexagon(side, side, img, outline)
			elif shape == 'squares':
				img = wallgen.genSquares(side, side, img, outline)
			elif shape == 'diamond':
				img = wallgen.genDiamond(side, side, img, outline)

			img = img.resize((side//2, side//2), resample=Image.BICUBIC)
			
			# print(fpath)
			img.save(fpath)
			imgurl = url_for('static',filename='images/'+fname)
			return render_template("download.html", context=imgurl, home="shape")
	else:
		return render_template('shape.html')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	http_server = WSGIServer(('',port),app)
	http_server.serve_forever()