
from flask import Flask
from flask import render_template
from threading import Thread
import json

app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('Tiddleton.html')

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()