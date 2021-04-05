from flask import Blueprint, json, request, render_template, jsonify
import datetime

from ..extensions import db

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
ui = Blueprint('ui', __name__)
databaseapi = Blueprint('databaseapi', __name__)

# endpoint for github to send notifications
@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        datajson = request.json
        if 'pusher' in  list(datajson.keys()):
            # it is push request
            author = datajson['pusher']['name']
            tobranch = datajson['ref'].split('/')[-1]
            print('auther:', author, 'tobranch:', tobranch, 'timestamp: ',  datetime.datetime.now())
            # save to mongodb database
            db.log.insert_one({
                'request_id': datajson['after'],
                'author': author,
                'action': "PUSH",
                'from_branch': "",
                'to_branch': tobranch,
                'timestamp': datetime.datetime.utcnow()
            })
            return {}, 200

        elif 'pull_request' in  list(datajson.keys()) and datajson['action'] == 'opened':
            db.log.insert_one({
                'request_id': datajson['number'],
                'author': datajson['pull_request']['user']['login'],
                'action': "PULL_REQUEST",
                'from_branch': datajson['pull_request']['head']['ref'],
                'to_branch': datajson['pull_request']['base']['ref'],
                'timestamp': datetime.datetime.utcnow()
            })
            return {}, 200

    return {}, 404


# route for rendering our ui page
@ui.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# api route for ui to call call every 15 seconds
@databaseapi.route('/webhook_list', methods=['GET'])
def database_list():
    alldocument = list(db.log.find())
    [document.pop('_id') for document in alldocument]
    response = {'data': alldocument}
    print(jsonify(response))
    return jsonify(response), 200
