#!/usr/bin/env python
#
# Raspberry Pi Garage door controller 
# Get door switches state (Diagnostic only)
# $Id: doorstate.py,v 1.1 2014/06/18 16:29:22 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This script closes the garage door
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#
# Usage: doorstate.py 
#
# GPIO 18 Pin 12 - Door Relay
# GPIO 23 Pin 16 - Door closed switch
# GPIO 24 Pin 18 - Door open switch
#

import shutil;
import os;
import sys;
import logging
import RPi.GPIO as GPIO
import time
import getopt

# Set up logging, level can be INFO, WARNING, ERROR, DEBUG
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/var/log/door.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.WARNING)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

#logger.info('Door ' + sys.argv[1])
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)	 	# Door closed switch 
GPIO.setup(4, GPIO.IN)	 	# Door open switch
GPIO.setup(24, GPIO.IN)	 	# Permanent +3.3 V

door_closed = GPIO.input(22)
door_open = GPIO.input(4)
logger.debug(sys.argv[0] )
logger.debug('Door closed switch = ' + str(door_closed))
logger.debug('Door open switch = ' + str(door_open))
print "Door closed switch is " + str(door_closed)
print "Door open switch is " + str(door_open)
os.system("sudo service ggpiod status")

