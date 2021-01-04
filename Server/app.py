
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
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
    


def password_check(passwd): 
      
    SpecialSym =['$', '@', '#', '%', '!'] 
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


# ------------DB Models-----------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'    #Testing DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'   #PostgreSQL Server
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

    #Checks if User is already loged in
    if(current_user.is_authenticated):
        return redirect(url_for('index'))

    #If the method is POST it checks the Data 
    if(request.method == 'POST'):
        username = request.form['user']
        password = request.form['password']

        user = dbUsers.query.filter_by(username=username).first()   # Searches the user in the Database

        if(user and check_password_hash(user.password, password)):  # If the user exists and the password hashes matches the user gets loged in.
            login_user(user)
            return redirect(url_for('index'))
        else:                                                       # If there is provided wrong data the login site gets displayd with an error message
            error = "Bitte überprüfen Sie ihre Logininformationen und probieren Sie es nochmals"
            return render_template('login.html', error=error)
    else:                                                           # If its a get request it will show the login form
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout(): # Logs out the user
    logout_user()
    return redirect("/")


# ------------Webinterface--------------------

@app.route('/', methods=['GET'])    # Handels request for the mainpage
def index():                        # Opens template file and sends it to the user

    currentsensor = request.args.get('currentsensor')   # Gets the selected sensor from the URL
    startdate = request.args.get('startdate')           # Gets the startdate from the URL
    enddate = request.args.get('enddate')               # Gets the enddate from the URL


    if(currentsensor and (startdate == None or enddate == None)):  # Checks if the var is empty
        daten = dbSenData.query.filter_by(sensorid=currentsensor).order_by(dbSenData.timestamp.desc()) # Selects just the wanted Sensordata
        chartdata = daten.limit(30)
        showchart = True

    elif(currentsensor and startdate  and enddate ):                # Checks if the var is empty
        startdate = datetime.strptime(startdate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M') # Formats the startdate
        enddate = datetime.strptime(enddate, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M')     # Formats the enddate
      
        daten = dbSenData.query.filter_by(sensorid = currentsensor).filter(dbSenData.timestamp >= startdate).filter(dbSenData.timestamp <= enddate).order_by(dbSenData.timestamp.desc())
        chartdata = dbSenData.query.filter_by(sensorid = currentsensor).filter(dbSenData.timestamp >= startdate).filter(dbSenData.timestamp <= enddate)
        showchart = True

    else:   #When the vars are empty
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
    return render_template('admin.html', user=dbUsers.query.all())

# ------------API----------------------

# To save de Data from the Sensor
@app.route('/sensors/api/savedata', methods=['POST'])
def api_savedata():
    data = request.json  # Gets the data from the POST request

    sen_id = data['sensor_id']          # Reads the sensor-ID from the request
    sen_secret = data['sensor_secret']  # Reads the sensor-secret from the request

    sensor = dbSensors.query.filter_by(sensorid=sen_id).first()

    if(sensor and sensor.sensorsecret == sen_secret): # When the sensor-id and the secret matches

        # It greates an object wich gets sends to the DB
        sensordata = dbSenData(sensorid=data['sensor_id'], co2=data['co2'],temp=data['temp'], hum=data['hum'], timestamp=data['timestamp'])
        
        db.session.add(sensordata)# Sends Obj to the DB
        sensor.lastseen = time.strftime('%H:%M:%S %d.%m.%Y') # Upates the last seen in the Senors DB Table
        db.session.commit()# Saves changes to DB

        return "<p>Values Saved</p>", 200  # This returns a http 200
    
    else:
        return "<p>Error: No matching sensor or wrong secret</p>", 406
      

    
# To Export the data in CSV Format
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

        with open('./download/_daten.csv', 'w') as f: # Creates a file or opens it
            out = csv.writer(f, delimiter=";")
            out.writerow(['Messzeitpunkt', 'CO2', 'Luftfeuchtigkeit', 'Temperatur']) # Writes the colum names

            for item in exportdata:
                out.writerow([item.timestamp, item.co2, item.hum, item.temp]) # Adds each row to the file

            f.close #Closes the File
        
        return send_file('./download/_daten.csv', mimetype="text/csv", attachment_filename= sen_id + "_daten.csv", as_attachment=True) # Sends the file to the client.

    except ValueError: # When a value was not set
        error = "Bitte wählen Sie einen Zeitraum aus!"
        return redirect(url_for("index", currentsensor=sen_id, error=error))


# To add a sensor
@app.route('/sensors/api/addsensor', methods=['POST'])
@login_required
def addSensor():
    data = request.form # Gets the data from the POST request


    sen_id = data['sensor_id']
    sen_secret = data['sensor_secret']
    sen_location = data['location']
    sen_description = data['description']

    savetime = "Erfasst: " + time.strftime('%H:%M %d.%m.%Y')

    if(name_check(sen_id) and password_check(sen_secret)):

        try:
            sensor = dbSensors(sensorid=sen_id, sensorsecret=sen_secret, lastseen=savetime, location=sen_location, description=sen_description)

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
    sen_id = data['sensor_id_hidden']  # Reads the SensorID from the Post request

    print(sen_id)

    dbSenData.query.filter_by(sensorid=sen_id).delete() # Delets all data from the table where the SensorID is used 
    dbSensors.query.filter_by(sensorid=sen_id).delete() # Delets the Senor from the Sensor table in the DB
    db.session.commit()                                 # Commits the changes to the DB

    return redirect(url_for('sensors'))


@app.route('/users/api/adduser', methods=['POST'])
@login_required
def addUser():
    data = request.form         # Gets the data from the POST request

    username = data['username']
    password = data['password']
    password1 = data['password1']

    if(password == password1 and name_check(username) and password_check(password)):

        try:
            hash = generate_password_hash(password)

            user = dbUsers(username=username, password=hash)

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
    




# ------------Error Handling------------------
@app.errorhandler(403)
def page_not_found(e):
    return "<h1>403</h1><p>Sie sind nicht berechtig diese Seite aufzurufen.</p>", 403

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Die gewünschte Seite wurde nicht gefunden.</p>", 404

# --Starts the Server
if(__name__ == "__main__"):
    app.run(debug=True) # Server startparameter
