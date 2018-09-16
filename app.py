from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import wallgen
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form['side'] and request.form['np']:
            side = int(request.form['side'])
            np = int(request.form['np'])
            print(side, np)
            error = None
            if (side > 5000 and side >= 100) or side < 100:
                error = "WARNING: Image too large OR Image too small"
            if np < 10 or np > side*0.2:
                error = "WARNING: Too less points OR points more than 20% of side"

            if error != None:
                print(error)
                return render_template('error.html', context=error)
            else:
                fname = "wall-{}-{}.png".format(side,np)
                shift = side//10
                side += shift*2
                points = wallgen.genPoints(np, side)
                img = wallgen.genWall(points, side, shift)
                img.save('static/images/'+fname)
                imgurl = url_for('static',filename='images/'+fname)
                # return redirect(url_for('static',filename='images/wall.png'))
                return render_template("download.html", context=imgurl)
            # return redirect("/image")
    else:
        return render_template('index.html')


# @app.route("/image")
# def getImage():
#     return send_file('static/images/wall.png', mimetype="image/png", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('',port),app)
    http_server.serve_forever()