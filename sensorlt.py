#Initial version of script to stor and push xbee sensor information to influxDB
#TODO poll for xbee sensors
#TODO put things into functions

CONFIG_FILE = 'server.ini'

import time
import csv
from datetime import datetime
import sys, os
#TODO put all of this inside of some sort of zip file
sys.path.insert(0, os.path.join(os.path.abspath('.'), '_xbee_lt_sensor.zip'))
sys.path.append("/userfs/WEB/python/requests-1.2.3")
sys.path.append("/userfs/WEB/python/configparser-3.5.0/src")

import requests
import libs.xbeelt #this import must be after requests or else an error occurs
import configparser

def cToF(reading):
    return reading * 1.8 + 32.0

class ServerData:
    def __init__(self,url_input,db_input,username_input,password_input,port_input,headers_input,method_input):
        self.url = url_input
        self.db = db_input
        self.username = username_input
        self.password = password_input
        self.port = port_input
        self.headers = headers_input
        self.method = method_input

#Read in .ini file and get all configuration settings
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
user = config['influx_server']['User']
pwd = config['influx_server']['Password']
url = config['influx_server']['URL_With_Credentials']
db_name = config['influx_server']['DB_Name']
port_num = config['DEFAULT']['Port_Number']
ssl_flag = config['DEFAULT']['SSL_Flag']
ssl_flag = config['DEFAULT']['SSL_Flag']
log_file_path=config['DEFAULT']['Log_File_Path']

params = {
    'db': db_name
}
headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'text/plain'
}
method = 'POST'
username=user
password=pwd

influx_server = ServerData(url,db_name,user,pwd,port_num,headers,method)

sensor_address = [None]*2
sensor_address[0] = "[00:13:A2:00:40:ac:05:ca]!"
sensor_address[1] = "[00:13:A2:00:40:a7:1b:15]!"
numSensors = len(sensor_address)
sensor = [None]*numSensors
temp_array = [None]*2




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
with open(log_file_path, 'ab') as outfile:
    writer = csv.writer(outfile)

    header = ['TimeUTC']
    for i in range(numSensors):
        # Make the header row
        sensorString = "Sensor%d" % (i)
        header.append(sensorString)
    writer.writerow(header)

    # loop forever
    while(True):
        #make a function to do the actual write to influxDB
        #make a function that looks for new sensors
        #add count and poll for sensor addresses every n number of iterations
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
