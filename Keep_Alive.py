from flask import Flask, render_template, redirect, request, url_for
from threading import Thread
import json, requests, os

app = Flask('')
jsonPath = "opinions.json"

if not os.path.exists(jsonPath):
	with open(jsonPath , "w+") as F:
		json.dump({"null" : "null"} , F)


@app.route('/', methods=['GET', 'POST'])
def home():
	with open(jsonPath , "r") as F:
		return render_template('Tiddleton.html' , jsonFile = str(json.load(F)))

@app.route('/fuck', methods=['GET', 'POST'])
def Fuck():
	with open(jsonPath , "r") as F:
		return render_template('Fuck.html' , jsonFile = str(json.load(F)))

@app.route('/admin/<name>', methods = ['GET', 'POST'])
def hello_name(name):
    return render_template(f"admins/{name}.html")

@app.route("/handle_opinion" , methods = ["POST"])
def handle_opinion():
	with open(jsonPath , "r") as F:
		data = json.load(F)

	with open(jsonPath , "w") as F:
		name = request.form["name"]
		opinion = request.form["opinion"]
		print(f"DEBUG{request.form}")
		data[name]  = opinion
		json.dump(data , F)

	return redirect(url_for("home"))

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()