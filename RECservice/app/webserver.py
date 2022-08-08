from flask import request, jsonify,make_response
from flask_api import FlaskAPI, status, exceptions
import update_scores as us
import sm2Like 
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/search/", methods=['GET'])
def search():
    if request.method == 'GET':
        args = request.args
        resp = us.search(searchquery=args['searchquery'],querykeyid=None)
        resp=make_response(jsonify(resp),200)
        print("webserver resp:",resp)
        return resp
    else:
        return "bad request",400

@app.route("/similardoc/", methods=['GET'])
def similardoc():
    if request.method == 'GET':
        args = request.args
        resp = us.search(searchquery=None,querykeyid=args['docid'])
        resp=make_response(jsonify(resp),200)
        print("webserver resp:",resp)
        return resp
    else:
        return "bad request",400

@app.route("/triggerupdate/", methods=['GET'])
def triggerrecomupdate():
    if request.method == 'GET':
        args = request.args
        if args['trigger']=="1":
            result=us.update_recoms()
        resp=make_response(jsonify({'result':result}),200)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        print("webserver resp:",resp)
        return resp
    else:
        return "bad request",400

@app.route("/userprofile/", methods=['GET','POST'])
def getuserprofile():
    if request.method == 'GET':
        result=us.retrieve_user_profile()
        resp=make_response(jsonify({'profile':result}),200)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        print("webserver resp:",resp)
        return resp

    if request.method == 'POST':
        # args = request.args
        result=us.update_user_profile(list(request.json['tags']))
        resp=make_response(jsonify({'result':result}),200)
        # resp.headers.add("Access-Control-Allow-Origin", "*")
        print("webserver resp:",resp)
        return resp

    else:
        return "bad request "+request.method,400

@app.route("/trigger_rediscover_updates/", methods=['GET'])
def trigger_rediscover_updates():
    if request.method == 'GET':
        args = request.args
        if args['method']=="updateStatus":
            result=sm2Like.updateStatus()
        if args['method']=="sm2likeCalc":
            result=sm2Like.calculate_sm2like([args['keyid']])
        resp=make_response(jsonify({'result':result}),200)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        print("webserver resp:",resp)
        return resp
    else:
        return "bad request",400


if __name__ == "__main__":
    # app.config['CORS_HEADERS'] = 'Content-Type'
    from waitress import serve
    serve(app, host="0.0.0.0", port=8002)
