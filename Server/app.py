
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import uuid
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

import time
from datetime import datetime
import json
import csv


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# ------------Functions----------------------

def name_check(string):
    val = True

    if len(string) < 2:
        val = False

    if len(string) > 20:
        val = False

    if val:
        return val


def date_check(startdate, enddate):
    if(startdate > enddate):
        temp = startdate
        startdate = enddate
        enddate = temp

    return startdate, enddate


def password_check(passwd):

    SpecialSym = ['$', '@', '#', '%', '!']
    val = True

    if len(passwd) < 8:
        val = False

    if len(passwd) > 20:
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False

    if val:
        return val

# ------------Template Filters----------------


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    timestamp = date.strftime('%d.%m.%Y %H:%M')
    return timestamp


# ------------DB Models-----------------------
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'  # Testing DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://as-user:pH54eESyuQWt@localhost:5432/db-air-sol'   #PostgreSQL Server
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class dbUsers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(64))
    prename = db.Column(db.String(64))
    email = db.Column(db.String(64))


class dbSensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorid = db.Column(db.String(20), nullable=False, unique=True)
    sensorsecret = db.Column(db.String(20), nullable=False)
    sensordata = db.relationship('dbSenData', backref='sendata', lazy=True)
    lastseen = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(50))
    description = db.Column(db.String(100))


class dbSenData(db.Model):
    id = db.Column(db.String(40), default=lambda: str(uuid.uuid4()), primary_key=True)
    sensorid = db.Column(db.Integer, db.ForeignKey('db_sensors.id'), nullable=False)
    co2 = db.Column(db.Integer)
    temp = db.Column(db.Integer)
    hum = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)

    


# ------------Login---------------------------
login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return dbUsers.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Checks if User is already loged in
    if(current_user.is_authenticated):
        return redirect(url_for('index'))

    # If the method is POST it checks the Data
    if(request.method == 'POST'):
        username = request.form['user']
        password = request.form['password']

        # Searches the user in the Database
        user = dbUsers.query.filter_by(username=username).first()

        # If the user exists and the password hashes matches the user gets loged in.
        if(user and check_password_hash(user.password, password)):
            login_user(user)
            return redirect(url_for('index'))
        # If there is provided wrong data the login site gets displayd with an error message
        else:
            error = "Bitte überprüfen Sie ihre Logininformationen und probieren Sie es nochmals"
            return render_template('login.html', error=error)
    else:                                                           # If its a get request it will show the login form
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():  # Logs out the user
    logout_user()
    return redirect("/")


# ------------Webinterface--------------------

@app.route('/', methods=['GET'])    # Handels request for the mainpage
def index():                        # Opens template file and sends it to the user

    # Gets the selected sensor from the URL
    currentsensor = request.args.get('currentsensor')
    # Gets the startdate from the URL
    startdate = request.args.get('startdate')
    # Gets the enddate from the URL
    enddate = request.args.get('enddate')

    showchart = False
    error = ""

    if(currentsensor):
        sensor = dbSensors.query.filter_by(sensorid=currentsensor).first()
        dbdata = dbSenData.query.filter_by(sendata=sensor)

        try:

            if(startdate == None or enddate == None):  # Checks if the var is empty

                daten = dbdata.order_by(dbSenData.timestamp.desc()).limit(
                    1000)  # Selects just the wanted Sensordata, max 1000 entires
                # Selects just the wanted Sensordata, max 30 entires for the chart
                chartdata = dbdata.order_by(dbSenData.timestamp.desc()).limit(40)[::-1]
                showchart = True

            elif(startdate and enddate):             # Checks if the var is empty

                # Formats the startdate into an obj
                startdate = datetime.strptime(startdate, '%Y-%m-%d')
                # Formats the enddate  into an obj
                enddate = datetime.strptime(enddate, '%Y-%m-%d')

                startdate, enddate = date_check(
                    startdate, enddate)  # Data comparison

                dbdata = dbdata.filter(dbSenData.timestamp >= startdate).filter(
                    dbSenData.timestamp <= enddate)

                daten = dbdata.order_by(dbSenData.timestamp.desc())
                chartdata = dbdata.order_by(dbSenData.timestamp.asc())
                showchart = True

            else:
                daten = dbdata.limit(50)
                chartdata = dbdata.limit(50)
                error = "Es ist ein unerwarteter Fehler aufgetreten."

        except ValueError:
            daten = dbdata.limit(50)
            chartdata = dbdata.limit(50)
            error = "Es wurde ein falscher Wert mitgegeben."

    else:  # When the vars are empty
        daten = dbSenData.query.order_by(dbSenData.timestamp.desc()).limit(
            1000)  # Selects the last 1000 datapoints
        chartdata = daten

    return render_template('index.html', daten=daten, chartdata=chartdata, sensors=dbSensors.query.order_by(dbSensors.sensorid.asc()), showchart=showchart, error=error)

# Handels request for www.air-solutions.ch/sensors
@app.route('/sensors', methods=['GET'])
@login_required
def sensors():
    return render_template('sensors.html', sensors=dbSensors.query.order_by(dbSensors.sensorid.asc()))

# Handels request for www.air-solutions.ch/admin


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template('admin.html', user=dbUsers.query.order_by(dbUsers.username.asc()))

# ------------API----------------------

# To save de Data from the Sensor


@app.route('/sensors/api/savedata', methods=['POST'])
def api_savedata():
    data = request.json  # Gets the data from the POST request

    sen_id = data['sensor_id']          # Reads the sensor-ID from the request
    # Reads the sensor-secret from the request
    sen_secret = data['sensor_secret']

    sensor = dbSensors.query.filter_by(sensorid=sen_id).first()

    if(sensor and sensor.sensorsecret == sen_secret):  # When the sensor-id and the secret matches

        for d in data["data"]:
            timestamp = datetime.strptime(d['timestamp'], '%d.%m.%Y %H:%M:%S')
            # It greates an object wich gets sends to the DB
            sensordata = dbSenData(
                sendata=sensor, co2=d['co2'], temp=d['temp'], hum=d['hum'], timestamp=timestamp)

            db.session.add(sensordata)  # Sends Obj to the DB
            # Upates the last seen in the Senors DB Table
            sensor.lastseen = datetime.now()

        db.session.commit()  # Saves changes to DB

        return "<p>Values Saved</p>", 200  # This returns a http 200

    else:
        return "<p>Error: No matching sensor or wrong secret</p>", 406


# To Export the data in CSV Format
@app.route('/sensors/api/exportdata', methods=['POST'])
def api_exportdata():
    data = request.form  # Gets the data from the POST request

    sen_id = data['sensor_id']
    startdate = data['startdate']
    enddate = data['enddate']

    try:
        startdate = datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.strptime(enddate, '%Y-%m-%d')

        startdate, enddate = date_check(startdate, enddate)  # Data comparison

        sensor = dbSensors.query.filter_by(sensorid=sen_id).first()
        exportdata = dbSenData.query.filter_by(sendata=sensor).filter(dbSenData.timestamp >= startdate).filter(
            dbSenData.timestamp <= enddate).order_by(dbSenData.timestamp.desc())

        with open('./download/_daten.csv', 'w') as f:  # Creates a file or opens it
            out = csv.writer(f, delimiter=";")
            # Writes the colum names
            out.writerow(
                ['Messzeitpunkt', 'CO2', 'Luftfeuchtigkeit', 'Temperatur'])

            for item in exportdata:
                # Adds each row to the file
                out.writerow([item.timestamp, item.co2, item.hum, item.temp])

            f.close  # Closes the File

        # Sends the file to the client.
        return send_file('./download/_daten.csv', mimetype="text/csv", attachment_filename=sen_id + "_daten.csv", as_attachment=True)

    except ValueError:  # When a value was not set
        error = "Bitte wählen Sie einen Zeitraum aus!"
        return redirect(url_for("index", currentsensor=sen_id, error=error))


# To add a sensor
@app.route('/sensors/api/addsensor', methods=['POST'])
@login_required
def addSensor():
    data = request.form  # Gets the data from the POST request

    sen_id = data['sensor_id']
    sen_secret = data['sensor_secret']
    sen_location = data['location']
    sen_description = data['description']

    savetime = datetime.now()

    if(name_check(sen_id) and password_check(sen_secret)):

        try:
            sensor = dbSensors(sensorid=sen_id, sensorsecret=sen_secret,
                               lastseen=savetime, location=sen_location, description=sen_description)

            db.session.add(sensor)
            db.session.commit()

            return redirect(url_for('sensors'))

        except Exception:
            error = "Der Sensor konnte nicht erfasst werden."

    else:
        error = "Die Sensor ID Sensor Secret entspricht nicht den Richtlinien"

    return redirect(url_for('sensors', error=error))


# To delete a sensor and its data
@app.route('/sensors/api/delsensor', methods=['POST'])
@login_required
def delSensor():
    data = request.form         # Gets the data from the POST request
    # Reads the SensorID from the Post request
    sen_id = data['sensor_id_hidden']

    print(sen_id)

    sensor = dbSensors.query.filter_by(sensorid=sen_id).first()

    try:
        # Delets all data from the table where the SensorID is used
        dbSenData.query.filter_by(sendata=sensor).delete()
        # Delets the Senor from the Sensor table in the DB
        dbSensors.query.filter_by(sensorid=sen_id).delete()
        # Commits the changes to the DB
        db.session.commit()

        return redirect(url_for('sensors'))

    except Exception:

        error = "Es ist ein unerwarteter Fehler aufgetreten."
        return redirect(url_for('sensors', error))


@app.route('/users/api/adduser', methods=['POST'])
@login_required
def addUser():
    data = request.form         # Gets the data from the POST request

    username = data['username']
    password = data['password']
    password1 = data['password1']
    prename = data['prename']
    name = data['name']
    email = data['email']

    if(password == password1 and name_check(username) and password_check(password)):

        try:
            hash = generate_password_hash(password)

            user = dbUsers(username=username, password=hash, prename=prename, name=name, email=email)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('admin'))

        except Exception:

            error = "Der Benutzername ist bereits vergeben."

    else:
        error = "Passwörter stimmen nicht überein oder entspricht nicht den Richtlinien."

    return redirect(url_for('admin', error=error))


@app.route('/users/api/deluser', methods=['POST'])
@login_required
def delUser():

    data = request.form         # Gets the data from the POST request

    username = data['username_del']

    if(username == current_user.username):
        error = "Der eigene Benutzer kann nicht gelöscht werden!"

    else:
        try:
            dbUsers.query.filter_by(username=username).delete()
            db.session.commit()

            return redirect(url_for('admin'))

        except Exception:

            error = "Der Benutzer konnte nicht gelöscht werden."

    return redirect(url_for('admin', error=error))


@app.route('/users/api/changePassword', methods=['POST'])
@login_required
def changePassword():

    data = request.form         # Gets the data from the POST request

    oldPassword = data['oldPassword']
    newPassword = data['newPassword']
    newPassword1 = data['newPassword1']

    # Searches the user in the Database
    user = dbUsers.query.filter_by(username=current_user.username).first()

    # If the user exists and the password hashes matches the user gets loged in.
    if(user and check_password_hash(user.password, oldPassword)):
        if(newPassword == newPassword1 and password_check(newPassword)):

            try:
                hash = generate_password_hash(newPassword)
                user.password = hash
                db.session.commit()

                return redirect(url_for('index'))

            except Exception:

                error = "Das Passwort konnte nicht geändert werden."

        else:
            error = "Passwörter stimmen nicht überein oder entspricht nicht den Richtlinien."

    return redirect(url_for('index', error=error))


# ------------Error Handling------------------
@app.errorhandler(403)
def page_not_found(e):
    return "<h1>403</h1><p>Sie sind nicht berechtig diese Seite aufzurufen.</p>", 403


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Die gewünschte Seite wurde nicht gefunden.</p>", 404


# --Starts the Server
if(__name__ == "__main__"):
   app.run(debug=False, host="0.0.0.0")  # Server startparameter
