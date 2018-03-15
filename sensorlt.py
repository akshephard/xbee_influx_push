# This script finds LT sensors associated to the gateway and retrieves data from them
# The data is wrriten to the CSV file specied in the ini file specified by CONFIG_FILE
# The data is also sent to an influxDB server specified in the CONFIG_FILE

#name of config file
CONFIG_FILE = 'server.ini'
INTERVAL = 1 * 30

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
import xbee
import configparser

class ServerData:
    def __init__(self,url_input,db_input,username_input,password_input,port_input,headers_input,method_input,params_input):
        self.url = url_input
        self.db = db_input
        self.username = username_input
        self.password = password_input
        self.port = port_input
        self.headers = headers_input
        self.method = method_input
        self.params = params_input

def influxDB_write(ServerDataInput,sensor_num,temp,time_stamp):
    #need to add space between timestamp and value though somehow it is still being picked up
    #make string to send to server
    payload = "Test_2_28,"+ "Fake_Meter_type=Meter_" + str(sensor_num) + " random_Float_value=" + str(temp)+str(int(time_stamp))
    response = test_session.request(
                    method=ServerDataInput.method,
                    url=ServerDataInput.url,
                    auth=(ServerDataInput.username, ServerDataInput.password),
                    params=ServerDataInput.params,
                    data=payload,
                    headers=ServerDataInput.headers,
                    verify=True
                    )
    return response.status_code

def get_sensors():
    # Obtain a list with the discovered XBee nodes
    print "Looking for XBee nodes...\r\n"
    node_list = xbee.getnodelist()
    sensor_count = 0
    sensor_address = []
    if node_list:
        for node in node_list:
            if (node.type == 'end'):
                sensor_address.append(node.addr_extended)
    return sensor_address
def cToF(reading):
    return reading * 1.8 + 32.0


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

#Make request data object
influx_server = ServerData(url,db_name,user,pwd,port_num,headers,method,params)


sensor_address = get_sensors()
numSensors = len(sensor_address)
sensor = [None]*numSensors
temp_array = [None]*numSensors
print len(sensor_address)
sample = [None]*numSensors



#Open file and start getting sensor values
with open(log_file_path, 'ab') as outfile:
    writer = csv.writer(outfile)

    header = ['TimeUTC']
    for i in range(numSensors):
        # Make the header row
        sensorString = "Sensor%d" % (i)
        header.append(sensorString)
    writer.writerow(header)

    interval_count = 0
    # create session and loop forever collecting data
    test_session = requests.Session()
    while(True):
        #Check all the sensors to see if they are still attached
        sensor_address = get_sensors()
        interval_count = 0
        numSensors = len(sensor_address)
        temp_array = [None] * numSensors
        sample = [None]*numSensors
        sensor = [None]*numSensors
        a=0
        #Could be an issue here if a sensor is disconnected between these steps
        #Try and except doesn't seem to be performing correct behaviour
        while a < numSensors:
            sensor[a] = libs.xbeelt.XBeeLTN(sensor_address[a])
            print sensor[a]
            try:
                sensor[a] = libs.xbeelt.XBeeLTN(sensor_address[a])
            except ValueError as noSensorError:
                sensor[a] = None
                interval_count = SENSOR_INTERVAL_CHECK
            a += 1

        timestampUTCstring = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print("Getting readings for timestamp %s ..." % (timestampUTCstring))
        dataRow = [timestampUTCstring]
        for j in range(numSensors):
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
            print influxDB_write(influx_server,j,temperature,time.time())


        writer.writerow(dataRow)
        print("DONE")
        outfile.flush();
        time.sleep(INTERVAL)
        interval_count +=1
