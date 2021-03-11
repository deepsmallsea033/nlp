from flask import Flask, request
from extract_location import *
import json
import sys
from sys import argv

app = Flask(__name__)

# monitor
@app.route('/location/status', methods=['GET'])
def status( ):
    return 'OK'

@app.route('/location/extract_location', methods=['POST'])
def names( ):   
    title = request.form.get("title", "")
    #contenttext = request.form.get("contenttext", "")
    return json.dumps(extract_locations_service(title))
    

if __name__ == '__main__':
    app.run(debug = False,port=int(argv[1]),host='0.0.0.0')

