import os
from flask import Flask
from flask import render_template

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

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')