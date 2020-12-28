
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

import time
from datetime import datetime
import json
import csv



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# ------------Global Var----------------------


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
    location = db.Column(db.String(50))
    description = db.Column(db.Text)


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
@login_required
def logout():
    logout_user()
    return redirect("/")


# ------------Webinterface--------------------

@app.route('/', methods=['GET'])  # Handels request for www.air-solutions.ch/
def index():
    # Opens template file and sends it to the user

    currentsensor = request.args.get('currentsensor') # Gets the selected sensor from the URL
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')

    print(enddate)




   

    if(currentsensor and (enddate == None or startdate == None)):  # Checks if the var is empty
        daten = dbSenData.query.filter_by(sensorid=currentsensor).order_by(dbSenData.timestamp.desc()) # Selects just the wanted Sensordata
        chartdata = daten.limit(30)
        showchart = True

    elif(currentsensor and startdate  and enddate ):
        startdate = datetime.strptime(startdate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M')
        enddate = datetime.strptime(enddate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M')
        """ For Debug
        print(currentsensor)
        print("Startdate: " + startdate)
        print("Enddate: " + enddate)
        """
        
        daten = dbSenData.query.filter_by(sensorid = currentsensor).filter(dbSenData.timestamp >= startdate).filter(dbSenData.timestamp <= enddate).order_by(dbSenData.timestamp.desc())
        chartdata = dbSenData.query.filter_by(sensorid = currentsensor).filter(dbSenData.timestamp >= startdate).filter(dbSenData.timestamp <= enddate)
        showchart = True

    else:   #When the var is empty
        daten = dbSenData.query.order_by(dbSenData.timestamp.desc()).limit(50)# Selects the last 50 datapoints
        chartdata = daten
        showchart = False

    error=""
    return render_template('index.html', daten=daten, chartdata=chartdata, sensors=dbSensors.query.all(), showchart=showchart, error=error)



    


# Handels request for www.air-solutions.ch/sensors
@app.route('/sensors', methods=['GET'])
@login_required
def sensors():
    return render_template('sensors.html', sensors=dbSensors.query.all())


# Handels request for www.air-solutions.ch/admin
@app.route('/admin', methods=['GET'])
@login_required
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

@app.route('/sensors/api/exportdata', methods=['POST'])
def api_exportdata():
    data = request.form # Gets the data from the POST request

    sen_id = data['sensor_id']
    startdate = data['startdate']
    enddate = data['enddate']

    try:
        startdate = datetime.strptime(startdate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M')
        enddate = datetime.strptime(enddate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M')

        print(sen_id)
        print("Startdate: " + startdate)
        print("Enddate: " + enddate)

        exportdata = dbSenData.query.filter_by(sensorid = sen_id).filter(dbSenData.timestamp >= startdate).filter(dbSenData.timestamp <= enddate)

        with open('./download/_daten.csv', 'w') as f:
            out = csv.writer(f, delimiter=";")
            out.writerow(['Messzeitpunkt', 'CO2', 'hum', 'temp'])

            for item in exportdata:
                out.writerow([item.timestamp, item.co2, item.hum, item.temp])

            f.close
        
        return send_file('./download/_daten.csv', mimetype="text/csv", attachment_filename= sen_id + "_daten.csv", as_attachment=True)

    except ValueError:
        print("No Values given")
        error = "Bitte wählen Sie einen Sensor und eine Zeitraum aus!"
        flash(u'Invalid password provided', 'error')
        return redirect(url_for("index", currentsensor=sen_id))
    

   



@app.route('/sensors/api/addsensor', methods=['POST'])
@login_required
def addSensor():
    data = request.form # Gets the data from the POST request


    sen_id = data['sensor_id']
    sen_secret = data['sensor_secret']
    sen_location = data['location']
    sen_description = data['description']

    savetime = "Erfasst: " + time.strftime('%H:%M %d.%m.%Y')

    sensor = dbSensors(sensorid=sen_id, sensorsecret=sen_secret, lastseen=savetime, location=sen_location, description=sen_description)

    db.session.add(sensor)
    db.session.commit()

    return redirect(url_for('sensors'))


@app.route('/sensors/api/delsensor', methods=['POST'])
@login_required
def delSensor():
    data = request.form         # Gets the data from the POST request
    sen_id = data['sensor_id_hidden']  # Reads the SensorID from the Post request

    print(sen_id)

    dbSenData.query.filter_by(sensorid=sen_id).delete() # Delets all data from the table where the SensorID is used 
    dbSensors.query.filter_by(sensorid=sen_id).delete() # Delets the Senor from the Sensor table in the DB
    db.session.commit()                                 # Commits the changes to the DB

    return redirect(url_for('sensors'))





# ------------Error Handling------------------
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# --Starts the Server
if(__name__ == "__main__"):
    app.run(debug=True)
