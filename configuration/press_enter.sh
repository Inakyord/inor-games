#! /bin/bash

<< credits
# Authors: Inaky Ordiales, Bryan Vargas, Emilio Garcia
# Date:    Dec 03, 2023.
# Program to press Enter key on a specific window.
credits

<< licence
GNU General Public License v3.0
licence

ID_VENTANA=$1

# key allows to simulate keyboard key press
# --window indicates a specific window id to send the key pulse.
# reurn is the enter key.

xdotool key --window ${ID_VENTANA} Return
