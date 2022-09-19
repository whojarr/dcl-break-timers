import os
from urllib import response
from flask import Flask
from flask import render_template
from pyzoom import ZoomClient


template_dir = os.path.abspath('./')
app = Flask(__name__, template_folder=template_dir)

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


def zoom_me():

    zoom_client = ZoomClient('SI6hJxlaTYeUlbUcFmwu9Q', 'QmLnnClzUZ6vRmKcmgi3Alznd7w6x8Od')
    response = zoom_client.meetings.list_meetings()
    print(response)



if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')