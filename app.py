import os
import json
from urllib import response
from flask import Flask
from flask import render_template, request
import zoom
from dotenv import load_dotenv

load_dotenv()

ZOOM_ACCOUNT_ID = os.getenv('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')

zoom_client = zoom.Zoom(ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET)

template_dir = os.path.abspath('./')
app = Flask(__name__, template_folder=template_dir)


def zoom_chat_send(meeting_id, message):

    meeting_id = 'f787566257a44d798e05c8407f627882'

    return zoom_client.chat_send(meeting_id, message)



@app.route("/")
def index_html():
    return render_template("index.html", **locals())

@app.route("/break.html")
def break_html():
    return render_template("break.html", **locals())

@app.route("/date.html")
def date_html():
    return render_template("date.html", **locals())


@app.route("/dates.html")
def dates_html():
    return render_template("dates.html", **locals())

@app.route("/timer.html")
def timer_html():
    return render_template("timer.html", **locals())

@app.route("/zoom.html")
def zoom_html():
    return render_template("zoom.html", **locals())


@app.route("/zoom_meeting_info.html")
def zoom_meeting_info_html():
    return render_template("zoom_meeting_info.html", **locals())


@app.route("/api/chat/send", methods = ['GET','POST'])
def chat_send():

    if request.method == 'GET':
        message = request.values.get("message")
    if request.method == 'POST':
        message = request.json['message']

    zoom_response = zoom_chat_send(message)
    resp = app.response_class(
        response=json.dumps(zoom_response),
        status=200,
        mimetype='application/json'
    )
    return resp


@app.route("/api/zoom/meeting", methods = ['GET'])
def zoom_meeting():

    if request.method == 'GET':

        meeting_id = request.values.get("meeting_id")

        zoom_response = zoom_client.meeting(meeting_id)

        resp = app.response_class(
            response=json.dumps(zoom_response),
            status=200,
            mimetype='application/json'
        )

    return resp


@app.route("/api/zoom/meetings", methods = ['GET'])
def zoom_meetings():

    if request.method == 'GET':

        type = request.values.get("type")

        zoom_response = zoom_client.meeting_list(type)

        resp = app.response_class(
            response=json.dumps(zoom_response),
            status=200,
            mimetype='application/json'
        )

    return resp



if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')