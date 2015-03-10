#!/rom/mnt/cust/usr/bin/python

# This is a demo script that will run at boot and send any json objects
# received to its senso



import httplib, urllib, base64
import urllib2
import random, time
import serial
import json
import sys
import time

#TODO: ADD YOUR VALUES
SENSOR_NAME = ""
USERNAME = ''
PASSWORD = ''

SERIAL_PORT = '/dev/ttySP0'
HOST = "wotkit.sensetecnic.com"
URL = "/api/v2/sensors/%s/data" % SENSOR_NAME


def sendEvents():

    auth = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        "Authorization": "Basic %s" % auth
    }
    ser = serial.Serial(SERIAL_PORT)
    ser.timeout = 10;

    while 1:

        # read data from the serial port
        line = ser.readline()

        if not line:
            continue

        data = json.loads(line)

        params = urllib.urlencode(data)
        conn = httplib.HTTPConnection(HOST);
        conn.request("POST", URL, params, headers)
        response = conn.getresponse()
        conn.close()
        #print response.status, response.reason
        #sys.stdout.flush() 

def internet_on():
    try:
        response=urllib2.urlopen('http://%s' % HOST,timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def main():
    ison = False
    while ison is False:
        try: 
            print "Waiting for internet connection..."
            sys.stdout.flush() 
            ison = internet_on()
            time.sleep(20)
        except:
            pass

    print "Sending Events to %s" % SENSOR_NAME
    sys.stdout.flush() 
    sendEvents();


if __name__ == "__main__":
    main()    

