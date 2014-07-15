#!/usr/bin/env python
#
# Raspberry Pi Garage door controller 
# Close door script
# $Id: closedoor.py,v 1.1 2014/06/18 16:29:22 bob Exp $
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
    print "<title>Close Garage Door</title>";
    print "<link rel='stylesheet' type='text/css' href='/garage/basic-noise.css' title='Basic Noise' media='all' />"
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";
    print "<META HTTP-EQUIV='refresh' CONTENT='4;URL=/garage/garage.html'>"
    print "</head>";
    print "<body>";
    return;

def write_html_footer():
    print "</body>";
    print "<head>";
    print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";
    print "</head>";
    print "</html>";
    return;

write_html_header();
print "</p></p>"
print "<h1 align='center'>Closing garage door</h1>";
print "</p></p>"
print "<p align='center'>"
print "<img border='0' src='/garage/garage_door_transit.jpg' width='265' height='197'></td>"
#print "<!--webbot bot='Include' u-include='/transit.html' tag='BODY' -->"
print "</p>"

write_html_footer();
os.system("/usr/bin/sudo /usr/lib/cgi-bin/ggpiod.py close")
time.sleep(3)
 
# End of script

