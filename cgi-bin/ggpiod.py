#!/usr/bin/env python
#
# Raspberry Pi Garage door controller 
# Main controller software 
# $Id: ggpiod.py,v 1.2 2014/06/18 17:07:36 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This interprets and executes garage door commands
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#

import os
import RPi.GPIO as GPIO
import logging
import signal
import subprocess
import sys
import time
import shutil
from ggpiod_daemon import Daemon

VERSION = "1.1"
TIMEOUT = 18
RELAYTIME = 2

# Door position definitions
OPEN = 0
CLOSED = 1
TRANSIT = 2
ERROR=3


CloseRelay = False
OpenDoor  = False
CloseDoor = False

class MyDaemon(Daemon):

	def run(self):
		global OPEN
		global CLOSED
		global TRANSIT

		global OpenDoor
		global CloseDoor
		global CloseRelay
		OpenDoor = False
		CloseDoor = False
		CloseRelay = False
		last_position = -1

            	logmsg('ggpiod running pid ' + str(os.getpid()), logging.INFO)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)	# Door relay
		GPIO.setup(22, GPIO.IN)         # Door closed switch 
		GPIO.setup(4, GPIO.IN)          # Door open switch
		GPIO.setup(24, GPIO.IN)         # Permanent +3.3V 

		signal.signal(signal.SIGUSR1, receive_signal)
		signal.signal(signal.SIGUSR2, receive_signal)
		signal.signal(signal.SIGHUP, receive_signal)

		# Main loop check door switches and waits for open/close door signals
	    	while True:
			# Get door position
			door_closed = GPIO.input(22)
			door_open = GPIO.input(4)

			if door_closed:
				position = CLOSED
			elif door_open:
				position = OPEN
			elif not door_open and not door_closed:
				position = TRANSIT

			if position != last_position:
				if position == OPEN:
					logmsg('Door open switch ' + str(door_open), logging.INFO)
				elif position == CLOSED:
					logmsg('Door closed switch ' + str(door_closed), logging.INFO)
				elif position == TRANSIT:
					logmsg('Door in transit ', logging.INFO)
				setup_photo(position)
				last_position = position

			if OpenDoor and position != OPEN:
				CloseRelay = True

			if CloseDoor and position != CLOSED:
				CloseRelay = True

			if CloseRelay:
				GPIO.output(18, True)
		        	logmsg('Operate door relay', logging.INFO)
    				time.sleep(RELAYTIME)
    				GPIO.output(18, False)

			OpenDoor = False
			CloseDoor = False
			CloseRelay = False

    			time.sleep(1)

	def status(self):
                # Get the pid from the pidfile
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None

                if not pid:
			message = "ggpiod status: not running"
            		logmsg(message, logging.INFO)
			print message 
		else:
			message = "ggpiod running pid " + str(pid)
            		logmsg(message, logging.INFO)
			print message 
		return

	def open(self):
            	logmsg('Open door', logging.INFO)
		os.system("/usr/bin/sudo kill -SIGUSR1 `cat /var/run/ggpiod.pid`")
		return

	def close(self):
            	logmsg('Close door', logging.INFO)
		os.system("/usr/bin/sudo kill -SIGUSR2 `cat /var/run/ggpiod.pid`")
		return

	def relay(self):
            	logmsg('Operate relay', logging.INFO)
		os.system("/usr/bin/sudo kill -SIGHUP `cat /var/run/ggpiod.pid`")
		return

	def version(self):
		msg = 'Version ' + VERSION
            	logmsg(msg, logging.INFO)
		print msg
		return

# End of class overrides

# Signal routines
def receive_signal(signum, stack):
	global OpenDoor
	global CloseDoor
	global CloseRelay
	logmsg('Received signal ' + str(signum), logging.DEBUG)
	if signum == signal.SIGUSR1:
		logmsg('Open door command received ' + str(signum), logging.INFO)
        	OpenDoor = True;
	if signum == signal.SIGUSR2:
		logmsg('Close door command received ' + str(signum), logging.INFO)
        	CloseDoor = True;
	if signum == signal.SIGHUP:
		logmsg('Close relay command received ' + str(signum), logging.INFO)
        	CloseRelay = True;
        return

# Logging routine
def logmsg(message, level):
      	# Set up logging, level can be INFO, WARNING, ERROR, DEBUG
        logger = logging.getLogger('gipiod')
        hdlr = logging.FileHandler('/var/log/ggpiod.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(level)
	if level == logging.INFO:
        	logger.info(message)
	if level == logging.WARNING:
        	logger.warning(message)
	if level == logging.DEBUG:
        	logger.debug(message)
	if level == logging.ERROR:
        	logger.error(message)
        logger.removeHandler(hdlr)
        hdlr.close()
	return

# Setup the new door position
def setup_photo(position):
	global OPEN
	global CLOSED
	global TRANSIT

       	logmsg('position ' + str(position), logging.DEBUG)
	WWW="/var/www/garage";
	DOOR_OPEN_IMG = WWW + "/" + "garage_door_open.jpg";
	DOOR_CLOSED_IMG = WWW + "/" + "garage_door_closed.jpg";
	DOOR_TRANSIT_IMG = WWW + "/" + "garage_door_transit.jpg";
	DOOR_POSITION_IMG = WWW + "/" + "garage_door_position.jpg";

	if position == OPEN:
		shutil.copyfile (DOOR_OPEN_IMG, DOOR_POSITION_IMG)
	elif position == CLOSED:
		shutil.copyfile (DOOR_CLOSED_IMG, DOOR_POSITION_IMG)
	elif position == TRANSIT:
		shutil.copyfile (DOOR_TRANSIT_IMG, DOOR_POSITION_IMG)
	return

### Main routine ###
if __name__ == "__main__":
	daemon = MyDaemon('/var/run/ggpiod.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		elif 'open' == sys.argv[1]:
			daemon.open()
		elif 'close' == sys.argv[1]:
			daemon.close()
		elif 'relay' == sys.argv[1]:
			daemon.relay()
		elif 'version' == sys.argv[1]:
			daemon.version()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|status|open|close|relay" % sys.argv[0]
		sys.exit(2)

