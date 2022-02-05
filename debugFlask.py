#this is a very basic flask setup to test the website

from flask import Flask , render_template

app = Flask(__name__ , template_folder = "templates2" , static_folder="stylesheets")

@app.route("/")
def home():
    return render_template("mainPage.html")

app.run(debug = True)