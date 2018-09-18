from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import time
import wallgen
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        if request.form['side'] and request.form['np'] and (request.form['rgb1'] and request.form['rgb2']):
            side = int(request.form['side'])
            np = int(request.form['np'])
            
            rgb1 = request.form['rgb1'][1:]
            rgb2 = request.form['rgb2'][1:]

            error = None
            
            try:
                rgb1 = tuple(bytes.fromhex(rgb1))
                rgb2 = tuple(bytes.fromhex(rgb2))
            except Exception as e:
                error = "ERROR: Invalid color hex"
            
            print(side, np, rgb1, rgb2)
            
            if (side > 4000 and side >= 100) or side < 100:
                error = "WARNING: Image too large OR Image too small"
            if np < 10 or np > 300:
                error = "WARNING: Too less points OR too many points"

            if len(rgb1) != 6 or len(rgb2) != 6:
                error = "ERROR: Invalid color hex"

            if error != None:
                print(error)
                return render_template('error.html', context=error)
            else:
                fname = "wall-{}.png".format(int(time.time()))
                fpath = 'static/images/'+fname
                shift = side//10
                side += shift*2
                points = wallgen.genPoints(np, side)
                img = wallgen.gradient(side, rgb1, rgb2)
                img = wallgen.genWall(img, points, side, shift)
                print(fpath)
                img.save(fpath)
                imgurl = url_for('static',filename='images/'+fname)
                return render_template("download.html", context=imgurl)
        else:
            error = "Invalid input, try again"
            return render_template("error.html", context=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('',port),app)
    http_server.serve_forever()