# Semesterarbeit WS20 Air-Solution

Author: Janik Schilter, Pascal Rusca
Changed at: 28.02.2021




# Sensor
Programmed in: 	Visual Studio Code
Extension:			PlattformIO

## Sendata 
Endpoint:   "yoururl"/sensors/api/savedata

Method:     POST
```json
{
"sensor_id": "PARU_HOME",
"sensor_secret": "EinEmachtnoch1angekeinCordonBleu",
  "data": [
    {
      "co2": 426,
      "temp": 25,
      "hum": 40,
      "timestamp": "13.01.2021 23:00:00"
    },
    {
      "co2": 4430,
      "temp": 25,
      "hum": 41,
      "timestamp": "13.01.2021 23:01:00"
    }]
}
```




# Server

Programmed in: 	Visual Studio Code
Extension:			Python, REST Client


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
jsonpatch==1.22
jsonpointer==2.0
jsonschema==3.2.0
requests==2.22.0
SQLAlchemy==1.3.19
ufw==0.36
uuid==1.30
wadllib==1.3.3
Werkzeug==1.0.1
```

## DB



### Generate DB

```python
from app import db
db.create_all()
db.session.commit()
```

### Add first User

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

Install DB Server
``` bash
sudo apt install postgresql postgresql-contrib

```

Change to PG User and open the management programm
``` bash
sudo -i -u postgres

psql

```


Close the Management Programmes
```bash
\q
```

Create User 
```bash
createuser --interactive
```

Create DB 
```bash
createdb DBNAME
```

