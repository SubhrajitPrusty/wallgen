from flask import Flask, request, send_file
import os
import wallgen
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        if request.args['side']:
            side = int(request.args['side'])
            shift = side//10
            side += shift*2
            points = wallgen.genPoints(100,100,side)
            img = wallgen.genWall(points, side, shift)
            img.save('static/wall.png')
            return send_file(os.path.abspath('wall.png'), mimetype="image/png")
        else:
            return "403"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('',port),app)
    http_server.serve_forever()