import json


with open('test.json') as json_file:
    data = json.load(json_file)
    for d in data["data"]:
        print(d["co2"])
        print(d["sensor_id"])