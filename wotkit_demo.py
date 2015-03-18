#!/rom/mnt/cust/usr/bin/python

# This is a demo script that will run at boot and send any json objects
# received to its sensor. This only works with a CloudGate device.

import httplib, urllib, base64
import urllib2
import random, time
import serial
import json
import sys
import time

import urllib
import urllib2
import base64
import httplib
import config


import threading
from Queue import Queue

serial_in_queue = Queue(maxsize=0)
serial_out_queue = Queue(maxsize=0)
num_threads = 10

try:
    import json
except ImportError:
    import simplejson as json

#TODO: ADD YOUR SENSOR NAME AND CREDENTIALS
SENSOR_NAME = 'sensetecnic.demo-cloudgate'
USERNAME = ''
PASSWORD = ''
SUBSCRIPTION_ID =''

SERIAL_PORT = '/dev/ttySP0'
HOST = "wotkit.sensetecnic.com"
URL = "/api/v1/sensors/%s/data" % SENSOR_NAME

class serialThread (threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.ser = serial.Serial(serial_port)
        self.ser.timeout = 10;

    def run(self):
        while True:
            line_in = self.ser.readline()
            if line_in:
                serial_in_queue.put(line_in)

            line_out = serial_out_queue.get()        
            if line_out:
                self.ser.write(line_out)
            serial_out_queue.task_done()

class sendEventsThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        auth = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "Authorization": "Basic %s" % auth
        }  

    def run(self):
        while True:
            line = serial_in_queue.get()
            serial_in_queue.task_done()
      
            if not line:
                continue

            data = json.loads(line)

            params = urllib.urlencode(data)
            conn = httplib.HTTPConnection(HOST);
            conn.request("POST", URL, params, self.headers)
            response = conn.getresponse()
            conn.close()

class getControlEventsThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #subscribe to control       
        auth = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
        self.headers = {'Authorization': "Basic %s" % auth} # Headers here do not require content-type
        self.params = urllib.urlencode({'@type': 'subscription'}) #CloudGate httplib requires params, using dummy ones.
        conn = httplib.HTTPConnection(HOST)
        conn.request("POST", "/api/v1/control/sub/" + SENSOR_NAME + "/", self.params, headers=self.headers)
        data = conn.getresponse().read()
        json_object = json.loads(data)
        self.subscription_id = json_object['subscription']
        conn.close()

    def run(self):
        while True:
            conn = httplib.HTTPConnection(HOST)
            conn.request("GET", "/api/v1/control/sub/" + str(self.subscription_id) + "?wait=10", headers=self.headers)
            response = conn.getresponse()
            data = response.read()
            data_str = json.dumps(data)
            serial_out_queue.put(data+'\n')
            conn.close()


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
            time.sleep(5)
        except:
            pass

    print "Sending Events to %s" % SENSOR_NAME
    sys.stdout.flush() 

    serial_thread = serialThread(SERIAL_PORT)
    serial_thread.start()

    events_thread = sendEventsThread()
    events_thread.start()

    control_thread = getControlEventsThread()
    control_thread.start()

    serial_in_queue.join()
    serial_out_queue.join()


if __name__ == "__main__":
    main()    

