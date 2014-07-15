#!/usr/bin/env python
#
# Raspberry Pi Garage door controller 
# Print log cgi-script
# $Id: log.py,v 1.1 2014/06/18 16:29:22 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This script provides log output via an HTML page
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#

import shutil;
import sys;
import os;
import logging
import cgi
import time
from subprocess import call 

def write_html_header():
    print "Content-Type: text/html", "\n";
    print "<html>";
    print "<head>";
    print "<title>Garage Door Event Log</title>";
    print "<link rel='stylesheet' type='text/css' href='/garage/basic-noise.css' title='Basic Noise' media='all' />"
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";
    print "</head>";
    print "<body>";
    return;

def write_html_footer():
    print "</body>";
    print "</html>";
    return;

write_html_header();

print "<h1>Event log</h1>";

print "<button type='button' onClick=\"parent.location='/garage/garage.html'\" >Back</button>"

# Get the pid from the pidfile
try:
	pf = file('/var/run/ggpiod.pid','r')
	pid = int(pf.read().strip())
	pf.close()
except IOError:
	pid = None

if not pid:
	message = "ggpiod status: not running"
	print "<button type='button' onClick=\"parent.location='startdaemon.py'\" >Start daemon</button>"
	print "<h2>" +  message + "</h2>"
else:
	message = "ggpiod running pid " + str(pid)
	print  "<h2>" + message + "</h2>"

print "<font color='white'>"
# Only get last 100 lines
os.system("tail -100 /var/log/ggpiod.log > /tmp/door.log")
file = open("/tmp/door.log")

while 1:
	line = file.readline()
	line.strip("\n")
	print line, "<br/>"
	if not line:
		break

print "</font>"

print "<button type='button' onClick=\"parent.location='/garage/garage.html'\" >Back</button>"
print "<h3>Use browser refresh to redisplay event log</h3>";

write_html_footer();
 
# End of script

