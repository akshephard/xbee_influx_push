import requests
import json
import calendar, datetime, time
from datetime import datetime


#Timestamp is a datetime object in UTC time
def UTC_time_to_epoch(timestamp):
  epoch = calendar.timegm(timestamp.utctimetuple())
  return epoch
url = url_with_credentials
json_body = [
        {
            "measurement": "testing",
            "tags": {
                "Sensor1": "new_value",
                "Sensor3": "new_value"
            },
            "time": "2009-11-10T23:00:00Z"
        }
    ]
date_str = "2008-11-10 17:53:59"
dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print repr(dt_obj)
time.time()
print repr(dt_obj)
method = 'POST'
data = json.dumps(json_body)
print("After the json dump")
print(data)
username=user
password=pwd
params=None
params = {
    'db': 'pyTestDB'
}
headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'text/plain'
}
points = data
test_data = {'points':points}
print(method)
print(url)
print(params)
print(headers)
print(test_data)
print(data)
payload = 'testing,Sensor1=159635643,Sensor3=1999999 Float_value=9.99 ' + str(int(time.time()))
print(payload)
test_session = requests.Session()
response = test_session.request(
    method=method,
    url=url,
    auth=(username, password),
    params=params,
    data=payload,
    headers=headers,
    verify=True
    )
print(response.text)
print(response.status_code)
