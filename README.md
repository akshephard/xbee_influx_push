**xbee_influx_push script**

This repository contains all of the files used in the development of the xbee_influx_push script as well as a zip file that will run on a DIGI Gateway. In order to use this script on the Digi Gateway, follow the instructions below. 


**Installing script and libraries on fresh DIGI Gateway**

 Copy the zip file from the repo to your gateway. Change IP address to the actual 
 IP addresss of your gateway
 ```
 LOCAL_MACHINE $ scp xbee_influx_push.zip python@10.0.0.191:/userfs/WEB/python
 
 GATEWAY $ unzip xbee_influx_push.zip
 
 GATEWAY $ cd xbee_influx_push.zip
 
 ```
 Either modify the example to contain your credentials and rename it to server.ini or copy server.ini over with scp
 
 ```
 LOCAL_MACHINE $ scp server.ini python@192.0.0.103:/userfs/WEB/python/xbee_influx_push
 
 GATEWAY $ vi server-example.ini
 
 GATEWAY $ cp server-example.ini server.ini
 
 ```
 To run the script use:
 
 GATEWAY $ python sensorlt.py

**Libraries**

influxdb-python/ - This is a modified version of the library that prints out the contents of the http request made by influxDBclient. This is useful for determining how to reimplement the influx API with requests library.

configparser-3.5.0/ - This library is used for parsing the server.ini file

requests-1.2.3/ - This is the version of requests that must be used to maintain compatibility with the xbee library

libs/ - This is the library the enables connection to xbee lt sensors

**Python files**

influxdb_test.py - This python script along with the modified version of influxdb-python was used to get the http request information that is sent during a write to the influxdb.

influx_requests.py - This python script was used to prove that a successful http request could be made with requests using the information obtained from the modified influxdb-python library.

ltsensor.py - This is the python script that retrieves the temperature data from the xbee sensors attached to the gateway and sends the values to the influxdb server specified. It also writes this data to a csv file specified in the configuration file.

**Other Files**

server-example.ini - Example server.ini which needs to be modified with the server credentials

xbee_influx_push.zip - Archive containing everything necessary to run the ltsensor.py script.

##
