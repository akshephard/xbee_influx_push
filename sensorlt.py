#Initial version of script to stor and push xbee sensor information to influxDB
#TODO parse configuration file for user credentials
#TODO poll for xbee sensors
#TODO put things into functions
import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('.'), '_xbee_lt_sensor.zip'))
sys.path.append("/userfs/WEB/python/requests-1.2.3")
import requests
import libs.xbeelt
import time
from datetime import datetime
import csv
logFilePath='/userfs/WEB/python/logs/sensor_log_test.csv'
url = url_with_credentials
params = {
    'db': 'pyTestDB'
}
headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'text/plain'
}
method = 'POST'
username=user
password=pwd

sensor_address = [None]*2
sensor_address[0] = "[00:13:A2:00:40:ac:05:ca]!"
sensor_address[1] = "[00:13:A2:00:40:a7:1b:15]!"
numSensors = len(sensor_address)
sensor = [None]*numSensors
temp_array = [None]*2

def cToF(reading):
    return reading * 1.8 + 32.0



a=0;
test_session = requests.Session()
while a < numSensors:
    try:
        sensor[a] = libs.xbeelt.XBeeLTN(sensor_address[a])
    except ValueError as noSensorError:
        sensor[a] = None
    a += 1

sample = [None]*numSensors
# Time interval between readings in seconds
INTERVAL = 1 * 30
#Open file and start getting sensor values
with open(logFilePath, 'ab') as outfile:
    writer = csv.writer(outfile)

    header = ['TimeUTC']
    for i in range(numSensors):
        # Make the header row
        sensorString = "Sensor%d" % (i)
        header.append(sensorString)
    writer.writerow(header)

    # loop forever
    while(True):
        timestampUTCstring = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print("Getting readings for timestamp %s ..." % (timestampUTCstring))
        dataRow = [timestampUTCstring]
        for j in range(numSensors):
            payload = "Test_2_28,"
            # Get readings from all sensors at some point in time
            temperature = 0.0
            if (sensor[j] is None):
                dataRow.append(temperature)
            else:
                #get sensor sample
                reading = sensor[j].sample()
                temperature = cToF(reading['temperature'])
                temperature = round(temperature,2)
                temp_array[j] = temperature
                print(temperature)
                dataRow.append(temperature)
                #need to add space between timestamp and value though somehow it is still being picked up
                #make string to send to server
                payload = payload + "Fake_Meter_type=Meter_" + str(j) + " random_Float_value=" + str(temperature)+str(int(time.time()))
                response = test_session.request(
                    method=method,
                    url=url,
                    auth=(username, password),
                    params=params,
                    data=payload,
                    headers=headers,
                    verify=True
                    )
                print(payload)
                print(response.text)
                print(response.status_code)


        writer.writerow(dataRow)
        print("DONE")
        outfile.flush();
        time.sleep(INTERVAL)
