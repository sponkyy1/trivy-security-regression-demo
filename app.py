from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Insecure Flask App Running!"

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    r = requests.get(url)
    return r.text
