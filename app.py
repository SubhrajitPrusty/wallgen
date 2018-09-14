from flask import Flask, jsonify, request, send_file
import os
import wallgen

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        if request.args['side']:
            print("HERE")
            side = int(request.args['side'])
            shift = side//10
            side += shift*2
            points = wallgen.genPoints(200,100,side)
            img = wallgen.genWall(points, side, shift)
            img.save('wall.png')
            return send_file(os.path.abspath('wall.png'), mimetype="image/png")
        else:
            print("no, HERE")
            return "403"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



