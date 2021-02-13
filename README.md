# Semesterarbeit WS20 Air-Solution



# Sensor
Programmiert in: 	Visual Studio Code
Extension:			PlattformIO

## Sendata 
Endpoint:   "yoururl"/sensors/api/savedata

Method:     POST
```json
{
    "sensor_id": "TEKO_BE_2.5",
    "sensor_secret": "PW12345",
    "co2": "400ppm",
    "temp": 26.937,
    "hum": 40,
    "timestamp": "27.06.2020 00:00:03"
}
```




# Server

Programmiert in: 	Visual Studio Code

Extension:			Python, REST Client

## Testuser
Username:   admin

Password:   12345

## Requirements
Intall needed Python libarys
```bash
pip3 install -r requirements.txt
```

Requirements (contained in requirements.txt)
```requirements.txt
Flask==1.1.2
Flask-Login==0.5.0
Flask-SQLAlchemy==2.4.4
Jinja2==2.10.1
SQLAlchemy==1.3.19
Werkzeug==1.0.1
```

## DB

Master PW:  3qEL8D$ZIn&m

DB-Name:    db-air-sol

Username: as-user
PW:       pH54eESyuQWt

### Generate DB

```python
from app import db
db.create_all()
db.session.commit()
```

### Add User

```python
from app import db
from app import dbUsers
from werkzeug.security import generate_password_hash

hash = generate_password_hash('passwort')
user = dbUsers(username='username', password=hash)

db.session.add(user)
db.session.commit()
```

### Add Sensor

```python
from app import db
from app import dbSensors

sensor = dbSensors(sensorid='String 10', sensorsecret='String 10', lastseen='Erfasst: 081220')

db.session.add(sensor)
db.session.commit()
```

### Read Data

```python
from app import db
from app import dbSenData

sendata = dbSenData.query.all()

print(sendata[0].sensorid)
print(sendata[0].co2)

```


## DB Install

Installiere DB Server + Hilfsprogramme
``` bash
sudo apt install postgresql postgresql-contrib

```

Wechsel zum PG User und Öffne das Management Programm
``` bash
sudo -i -u postgres

psql

```


Beenden des Management Programmes
```bash
\q
```

User erstellen
```bash
createuser --interactive
```

DB erstellen
```bash
createdb DBNAME
```

