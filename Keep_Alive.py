
from flask import Flask
from flask import render_template , request
from threading import Thread
import json , requests , os

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

@app.route('/neo', methods = ['GET', 'POST'])
def NEO():
  return render_template("NEO.html")

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

	return render_template("NEO.html")
#use tabs

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()