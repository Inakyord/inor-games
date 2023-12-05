#! /bin/bash

<< credits
# Authors: Inaky Ordiales, Bryan Vargas, Emilio Garcia
# Date:    Dec 03, 2023.
# Program to get the running window id from the running rom.
credits

<< licence
GNU General Public License v3.0
licence

# Positional parameters $0-$9, $0 is reserved for the script name. Example hola.sh inaky --> hola, inaky
# echo "hola, $1"

# xdotool search --name ${NOMBRE_ROM} allows to search a window by name and get the windows id.
# devuelve el X window identifier, window ids.



NOMBRE_ROM=$1 		#Se asigna el parámetro recibido a una variable

xdotool search --name ${NOMBRE_ROM} > /home/pi/inor-games/pid.txt #Se ejecuta un comando para buscar una ventana de acuerdo al
																#identificador de proceso de la misma.
