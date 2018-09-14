from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import wallgen
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form['side']:
            side = int(request.form['side'])
            if side > 5000:
                return "WARNING: DONOT EXCEED 5000"
            shift = side//10
            side += shift*2
            points = wallgen.genPoints(100,100,side)
            img = wallgen.genWall(points, side, shift)
            img.save('static/images/wall.png')
            return send_file('static/images/wall.png', mimetype="image/png", as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('',port),app)
    http_server.serve_forever()