import os
from flask import Flask
from flask import render_template

template_dir = os.path.abspath('./')
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def hello_world():
    return render_template("break.html", **locals())

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')