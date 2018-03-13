# This script along with the modified version of InfluxDBClient is useful to see
# what is being sent in the http request in order to satisfy the influxDB API
import os,sys
sys.path.append("/home/werd/lbnl/requests")
sys.path.append("/home/werd/lbnl/influxdb-python")
import requests as req
import json
import datetime


from influxdb import InfluxDBClient

# Client instance to access influxDB cloud service via URL given
# DO NOT CHANGE DATABASE FROM 'pyTestDB' FOR DEVELOPMENT PHASE
client = InfluxDBClient(host='url', port=portNum, username='user',
    password='pwd',database='dbName', ssl=True, verify_ssl=True)


# Json structure used to build an insert for data to be entered into database
json_body = [
        {
            "measurement": "Test_2_28",
            "tags": {
                "Fake_Meter_type": "Meter_1"
            },
            "time": "2018-02-28T11:00:00Z",
            "fields": {
                "random_Float_value": 0.0222
            }
        },
        {
            "measurement": "Test_2_28",
            "tags": {
                "Fake_Meter_type": "Meter_2"
            },
            "time": "2018-02-28T11:00:00Z",
            "fields": {
                "random_Float_value": 0.03333
            }
        }
    ]
print("first")
print(json_body)
print("second")
print(json.dumps(json_body))
# Will write json body to 'pyTestDB' database since it was specified in beginning client instantiation.
result = client.write_points(json_body)
