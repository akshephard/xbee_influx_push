**xbee_influx_push script**

This repository contains all of the files used in the development of the xbee_influx_push script. In order to use this script on the Digi Gateway, you must copy the files ltsensor.py as well as the two directories requests and config parser. 

Replace IP address with address of gateway as well.
scp sensorlt.py python@192.0.0.103:/userfs/WEB/python
scp -r configparser-3.5.0 python@10.0.0.191:/userfs/WEB/python

To run the script use: python sensorlt.py

**The folders contained in this repository are necessary libraries for ltsensor.py as well as a library used for developmenmt**

influxdb-python/ - is a modified version of the library that prints out the contents of the http request made by influxDBclient. This is useful for determining how to reimplement the influx API with requests library.

configparser-3.5.0/ - this library is used for parsing the server.ini file 



##
