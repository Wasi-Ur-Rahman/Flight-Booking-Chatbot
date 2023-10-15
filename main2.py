from flask import Flask, request
import json
import logging

logging.basicConfig(filename='chatbot.log', level=logging.INFO)

app = Flask(__name__)

@app.route("/", method=["POST"])
def home():
    data = request.json
    logging.info(f"Incoming request: {data}")
    json.dump(data, open("input.json", "w"), indent=4, sort_keys=True)
    return "Hi from flask"

app.run(port=8000)