#! /bin/bash

<< credits
# Authors: Inaky Ordiales, Bryan Vargas, Emilio Garcia
# Date:    Dec 03, 2023.
# Program to mount usb on special mounting point.
credits

<< licence
GNU General Public License v3.0
licence

ACTION=$1 						
DEVBASE=$2						
DEVICE="/dev/${DEVBASE}"		


sudo mkdir /media/pi/usb-aux	
sudo mount ${DEVICE} /media/pi/usb-aux	
