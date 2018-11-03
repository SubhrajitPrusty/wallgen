from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import time
import wallgen
from gevent.pywsgi import WSGIServer

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
		
		rgb1 = request.form.get('rgb1')[1:]
		rgb2 = request.form.get('rgb2')[1:]

		outline = request.form.get('outline')

		error = None
		
		try:
			rgb1 = tuple(bytes.fromhex(rgb1))
			rgb2 = tuple(bytes.fromhex(rgb2))
		except Exception as e:
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
			side += shift*2

			points = wallgen.genPoints(np, side)
			img = wallgen.nGradient(side, rgb1, rgb2)
			img = wallgen.genPoly(img, points, side, shift, outline)

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

		rgb1 = request.form.get('rgb1')[1:]
		rgb2 = request.form.get('rgb2')[1:]

		error = None
		
		try:
			rgb1 = tuple(bytes.fromhex(rgb1))
			rgb2 = tuple(bytes.fromhex(rgb2))
		except Exception as e:
			error = "ERROR: Invalid color hex"
		
		if side > 5000 or side < 100:
			error = "WARNING: Image too large OR Image too small"

		if error != None:
			print(error)
			return render_template('error.html', context=error)
		else:
			fname = "wall-{}.png".format(int(time.time()))
			fpath = 'static/images/'+fname
			img = wallgen.nGradient(side, rgb1, rgb2)
			boxes = side // 100 + 2 # this config looks good

			if shape == "squares":
				img = wallgen.genSquares(side, img, outline)
			elif shape == "hexagon":
				img = wallgen.genHexagon(side, side//20, img, outline)
			elif shape == "diamond":
				img = wallgen.genDiamond(side, img, outline)

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