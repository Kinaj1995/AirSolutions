
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

import time
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


sensordata = []

# ------------DB Models-----------------------
db = SQLAlchemy(app)


class dbUsers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


class dbSensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorid = db.Column(db.String(10), nullable=False)
    sensorsecret = db.Column(db.String(10), nullable=False)
    lastseen = db.Column(db.String(20))


class dbSenData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorid = db.Column(db.String(10), nullable=False)
    co2 = db.Column(db.Integer)
    temp = db.Column(db.Integer)
    hum = db.Column(db.Integer)
    timestamp = db.Column(db.String(20), nullable=False)


# ------------Login---------------------------
login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return dbUsers.query.get(int(user_id))


@app.route('/login', methods=['GET','POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        username = request.form['user']
        password = request.form['password']

        user = dbUsers.query.filter_by(username=username).first()

        if(user and check_password_hash(user.password, password)):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = "Bitte überprüfe deine Logininformationen und probiere es nochmals"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


# ------------Webinterface--------------------

@app.route('/', methods=['GET'])  # Handels request for www.air-solutions.ch/
def index():
    # Opens template file and sends it to the user
    return render_template('index.html')


# Handels request for www.air-solutions.ch/sensors
@app.route('/sensors', methods=['GET'])
#@login_required
def sensors():
    return render_template('sensors.html', sensors=dbSensors.query.all())


# Handels request for www.air-solutions.ch/admin
@app.route('/admin', methods=['GET'])
#@login_required
def admin():
    return render_template('admin.html')

# ------------Sensor-API----------------------


@app.route('/sensors/api/savedata', methods=['POST'])
def api_savedata():
    data = request.json  # Gets the data from the POST request

    sen_id = data['sensor_id']  # Reads the sensor-ID from the request
    # Reads the sensor-secret from the request
    sen_secret = data['sensor_secret']

    sensorlist = dbSensors.query.all()

    for x in sensorlist:
        # When the sensor-id and the secret matches
        if(x.sensorid == sen_id and x.sensorsecret == sen_secret):

            # It greates an object wich gets sends to the DB
            sensordata = dbSenData(sensorid=data['sensor_id'], co2=data['co2'],
                                   temp=data['temp'], hum=data['hum'], timestamp=data['timestamp'])
            # Sends Obj to the DB
            db.session.add(sensordata)
            x.lastseen = time.strftime('%H:%M:%S %d.%m.%Y')
            # Saves changes to DB
            db.session.commit()

            return "<p>Values Saved</p>", 200  # This returns a http 200

    return "Error: No matching sensor or wrong secret"


@app.route('/sensors/api/all', methods=['get'])
def api_all():

    sensordata = dbSenData.query.all()
    outjson = []

    for x in sensordata:
        outjson.append(x.co2)
        
        

    return jsonify(outjson)  # Returns all sensordate, (just for debug!)

# ------------Error Handling------------------
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# --Starts the Server
if(__name__ == "__main__"):
    app.run(debug=True)
