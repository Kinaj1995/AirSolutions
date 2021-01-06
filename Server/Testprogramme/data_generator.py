import requests
import random
import json

url = "http://localhost:5000/sensors/api/savedata"

headers = {
    'user-agent': "vscode-restclient",
    'content-type': "application/json"
    }


data = '{"sensor_id": "TEKO_LU_5.5","sensor_secret": "PW12345w!","co2": 401,"temp": 26.937,"hum": 40,"timestamp": "27.06.2020 00:00:03"}'

data = json.loads(data)

for m in range(13):
    
    if(m !=0):
        if(m<10):
            month = "0" + str(m)
        else:
            month = str(m)


        for i in range(32):

            if(i !=0):
                if(i<10):
                    day = "0" + str(i)
                else:
                    day = str(i)

                for x in range(24):

                    if(x<10):
                        hour = "0" + str(x)
                    else:
                        hour = str(x)


                    data["co2"] = random.randrange(400,1000)
                    data["temp"] = random.randrange(5,40)
                    data["hum"] = random.randrange(5,100)
                    data["timestamp"] = day + "." + month + ".2018 " + hour + ":00:00"
                    
                    payload = json.dumps(data)
                    print(json.dumps(data))

                    response = requests.request("POST", url, data=payload, headers=headers)
                    print(response.text)








