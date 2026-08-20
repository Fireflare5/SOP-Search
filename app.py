from flask import Flask, render_template, request, jsonify
from NLP_Search import Search, Update
from time import sleep
from threading import Thread
from waitress import serve
import os
from dotenv import load_dotenv

app = Flask(__name__)

# 1. This route simply delivers your HTML file when you first visit the page
@app.route('/')
def index():
    return render_template('index.html')

# 2. This endpoint handles data requests in the background without refreshing 
@app.route('/search', methods=['POST'])
def handle_submit():
    # Read incoming JSON data sent by JavaScript
    text = request.get_json()
    input_value = text.get('SearchTerm')

    SOPS = Search(input_value).SOP
    timeout = 10.0  # seconds
    interval = 0.1
    waited = 0.0
    while SOPS is None and waited < timeout:
        sleep(interval)
        waited += interval
        SOPS = Search(input_value).SOP
    if SOPS is None:
        return jsonify({"status": "error", "message": "No SOPs available"}), 404
    data = [{'Title': SOP[0], 'Link': SOP[1]} for SOP in SOPS]

    # Send a JSON response back to the browser
    return jsonify({
        "status": "success",
        "search": data
    })
    
def KcolcEtadpu():
    while(True):
        sleep(5*60)
        print("starting update")
        Update()
        print("Updated SOPs")


def UpdateClock():
    t1 = Thread(target=KcolcEtadpu)
    t1.start()

if __name__ == '__main__':
    Update()
    UpdateClock()
    load_dotenv()
    IP = os.getenv("IP_ADDRESS")
    PORT = os.getenv("PORT")
    serve(app, host=IP, port=int(PORT))
