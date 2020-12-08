
from flask import Flask, render_template, request, jsonify


import time
import json


app = Flask(__name__)

sensorlist = [
    {'id': 0,
     'sensor-id': '12345',
     'sensor-secret': 'PW12345',
     'last-seen': ''
     },
    {'id': 1,
     'sensor-id': 'TEKO_LU_5.5',
     'sensor-secret': 'PW12345',
     'last-seen': ''
     },
    {'id': 2,
     'sensor-id': 'TEKO_BE_2.5',
     'sensor-secret': 'PW12345',
     'last-seen': ''
     },
]

sensordata = []

# ------------Webinterface--------------------


@app.route('/', methods=['GET']) #Handels request for www.air-solutions.ch/
def index():
    return render_template('index.html') #Opens template file and sends it to the user


@app.route('/sensors', methods=['GET']) #Handels request for www.air-solutions.ch/sensors
def sensors():
    return render_template('sensors.html')


@app.route('/admin', methods=['GET']) #Handels request for www.air-solutions.ch/admin
def admin():
    return render_template('admin.html')

# ------------Sensor-API----------------------


@app.route('/sensors/api/getsendata', methods=['GET'])
def api_sensor_data():

    if('id' in request.args):           # Checks if a ID parameter is provided
        id = request.args['id']
    else:                               # If no ID is given, it returns an Error
        return "Error: No id was found. Please specify an id."

    sendata = []                        # Empty array for the result data

    for sen in sensorlist:              # Searches thru the sensor list
        if(sen['sensor-id']==id):
            sendata.append(sen)

    return jsonify(sendata)


@app.route('/sensors/api/savedata', methods=['POST'])
def api_savedata():
    data = request.json                 #Gets the data from the POST request

    sen_id = data['sensor_id']          #Reads the sensor-ID from the request
    sen_secret = data['sensor_secret']  #Reads the sensor-secret from the request

    for sen in sensorlist:
        if(sen['sensor-id']==sen_id and sen['sensor-secret']==sen_secret): #When the sensor-id and the secret matches
            sensordata.append(data)                                        #It stores the values in the DB
            sen['last-seen'] = time.strftime("%H:%M:%S %d.%m.%Y")          #And updates the last-seen value in the playerlist
            return "<p>Values Saved</p>", 200                              #This returns a http 200 
        else:
            return "Error: No matching sensor or wrong secret"

    

@app.route('/sensors/api/all', methods=['get'])
def api_all():
    return jsonify(sensordata) # Returns all sensordate, (just for debug!)

# ------------Error Handling------------------

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# --Starts the Server
if(__name__ == "__main__"):
    app.run(debug=True)
