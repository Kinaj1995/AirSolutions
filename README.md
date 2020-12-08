# Semesterarbeit WS20 Air-Solution



# Sensor
Programmiert in: 	Visual Studio Code
Extension:			PlattformIO





# Server

Programmiert in: 	Visual Studio Code
Extension:			Python, REST Client

## Requirements
```.txt
flask==1.0
```

## DB
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
