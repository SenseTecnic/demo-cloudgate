#!/bin/sh

sleep 60 #Lets wait for network to be up
cd /root
/rom/mnt/cust/usr/bin/python wotkit_demo.py
cd /
