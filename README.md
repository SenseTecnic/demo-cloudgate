================
CloudGate Router
================

This is a very simple script that posts data to a sensor in WoTKit using an Option Cloudgate (http://www.option.com/). Data is received as a JSON object in the serial port ```/dev/ttySP0```, and posted to ```/api/v2/sensors/{sensorname}/data```.

Dependencies
================

* Python >2.7

Setting up Script
================

Edit the wotkit_demo.py file and modify the following lines:

```
SENSOR_NAME = "your_sensor_name"
USERNAME = 'a_key_id'
PASSWORD = 'a_key_password'
```

You can generate a key and password at: http://wotkit.sensetecnic.com/wotkit/keys. You can create a sensor to receive the data at: http://wotkit.sensetecnic.com/wotkit/sensors

Running Script
================

To run the script run:

```
python wotkit_demo.py
```

In any scripts you must run python directly from its location (found using ```which python```). In the CloudGate version of OpenWRT it lives in: 

```
/rom/mnt/cust/usr/bin/python wotkit_demo.py
```

Running at boot
================

Use the provided "startwotkitdemo.sh" script to run your script. First, create a logfile, in our case we have created it at ```/root/logs```. Then, edit the ```/etc/rc.local``` file and add the following line:

```
sh /root/startwotkitdemo.sh > /root/logs/cronlog 2>&1 &
exit 0
```

NOTE: The linux version running in the CloudGate is a proprietary version of OpenWRT, adding a ```@boot ...``` line using ```sudo crontab -e``` will not work.
