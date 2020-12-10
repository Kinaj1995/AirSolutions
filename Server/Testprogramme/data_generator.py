import requests
import random
import json

url = "http://localhost:5000/sensors/api/savedata"

headers = {
    'user-agent': "vscode-restclient",
    'content-type': "application/json"
    }


data = '{"sensor_id": "TEKO_LU_5.5","sensor_secret": "PW12345","co2": "401ppm","temp": 26.937,"hum": 40,"timestamp": "27.06.2020 00:00:03"}'

data = json.loads(data)



for x in range(24):

    if(x<10):
        hour = "0" + str(x)
    else:
        hour = str(x)


    data["co2"] = str(random.randrange(500)) + "ppm"
    data["temp"] = random.randrange(5,40)
    data["hum"] = random.randrange(5,100)
    data["timestamp"] = "06.12.2020 " + hour + ":00"
    
    payload = json.dumps(data)
    print(json.dumps(data))

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)








