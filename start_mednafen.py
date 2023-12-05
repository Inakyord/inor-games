#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ## ###############################################
#
# start_mednafen.py
# Run the mednafen emulator and change to its window when ready.
#
# Authors: Inaky Ordiales, Bryan Vargas, Emilio Garcia
# Date:    Dec 03, 2023.
# 
# License: GNU General Public License v3.0
#
# ## ###############################################

import os					# Access to OS functions											
from time import sleep		# waiting time

# PATHS and flags
WINDOWS_TXT="/home/pi/inor-games/windows.txt" 
exit = False

if __name__ == '__main__':
	# wait for boot program.
	sleep(10)
	# run mednafen
	os.popen("cd /usr/games/ ; ./mednaffe")
	
	# Infinite cycle to make sure window is ready.
	while exit == False:
		# Get open windows and save them in text file
		os.popen('wmctrl -l > {}'.format(WINDOWS_TXT))
		with open("{}".format(WINDOWS_TXT), 'r') as w_txt:
			contenido = w_txt.read()
			# check if window is opened
			if contenido.find('Mednaffe') != -1:
				# change to this window in fullscreen mode
				os.popen("wmctrl -r 'Mednaffe' -b toggle,fullscreen")
				# end cycle
				exit = True
			else:
				# keep in cycle
				exit = False
