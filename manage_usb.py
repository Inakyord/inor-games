#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ## ###############################################
#
# manage_usb.py
# Detect the presence of USB devices, obtain information about currently open windows, 
# identify the window in which a game is running, collect an inventory of ROMs in a specific 
# directory, temporarily pause emulator execution, generate a graphical interface for viewing 
# the contents of the USB stick, and monitor and manage events associated with USB devices,
#
# Authors: Inaky Ordiales, Bryan Vargas, Emilio Garcia
# Date:    Dec 03, 2023.
# 
# License: GNU General Public License v3.0
#
# ## ###############################################

import os
import pyudev
import threading
from time import sleep
import subprocess as sp
import tkinter
from tkinter import *
from shutil import copytree

# Global variables
f_lock = threading.Lock()
usb_active = 0

# System routes
WINDOW_ELEMENTS = "/home/pi/inor-games/windows.txt"
MEDNAFFE_ROUTE = "/usr/games/mednaffe"
PID_FILE = "/home/pi/inor-games/pid.txt"
ROMS_FILE = "/home/pi/inor-games/roms.txt"
USB_FILE = "/home/pi/inor-games/usb_roms.txt"
ROMS_PATH = "/home/pi/inor-games/ROMS"
USB_PATH = "/home/pi/inor-games/manage_usb"
MEDIA_PATH = "/media/pi/usb-aux"

# Function to retrieve ROMs available in a specific directory
def retrieve_rom_names():
    new_list = list()
    os.popen('ls {} > {}'.format(ROMS_PATH, ROMS_FILE))
    sleep(0.05)
    with open('{}'.format(ROMS_FILE), 'r') as rom_txt:
        content = rom_txt.readlines()
        for x in content:
            nonl_noext_string = os.path.splitext("{}".format(x))[0]
            new_list.append(nonl_noext_string)
    return new_list

# Function to retrieve a list of currently open windows
def retrieve_windows():
    content = ""
    os.popen('wmctrl -l > {}'.format(WINDOW_ELEMENTS))
    sleep(0.05)
    with open("{}".format(WINDOW_ELEMENTS), 'r') as w_txt:
        content = w_txt.read()
    return content

# Function to find the currently open game by matching the ROM name with the window name
def match_rom_window_get_name():
    rom_list = retrieve_rom_names()
    sleep(0.05)
    window_string = retrieve_windows()
    for x in rom_list:
        if window_string.find(x) != -1:
            return x
            break

# Function to extract the first element of a string after splitting by space
def terminal_xdotool_string(string):
    x = string.split(" ")
    return x[0]

# Function to process USB ROMs
def process_usb_roms():
    if os.path.exists("/home/pi/TMP_ROMS/"):
        if os.listdir():
            return

    shutil.copytree(MEDIA_PATH, "/home/pi/TMP_ROMS/")
    lst_usb_roms = retrieve_usb_roms_list()
    copy_roms_to_permanent_directory(lst_usb_roms)
    clean_up_temporary_directory()

    display_usb_roms_gui(lst_usb_roms)

# Function to retrieve a list of USB ROMs
def retrieve_usb_roms_list():
    os.popen('ls /home/pi/TMP_ROMS > /home/pi/inor-games/usb.txt')
    sleep(0.05)

    lst_usb_roms = []
    with open('{}'.format(USB_FILE), 'r') as USB_FILE:
        content = USB_FILE.readlines()
        for x in content:
            nonl_noext_string = os.path.splitext("{}".format(x))[0]
            lst_usb_roms.append(nonl_noext_string)

    return lst_usb_roms

# Function to copy ROMs to a permanent directory
def copy_roms_to_permanent_directory(roms_list):
    os.popen("cp -r /home/pi/TMP_ROMS/* /home/pi/inor-games/ROMS")
    sleep(0.05)

# Function to clean up the temporary directory
def clean_up_temporary_directory():
    os.popen("rm -r /home/pi/TMP_ROMS")

# Function to display a GUI with the list of USB ROMs
def display_usb_roms_gui(roms_list):
    rootwindow = tkinter.Tk()
    rootwindow.title("List of ROMs obtained via USB")
    rootwindow.geometry("600x400")
    rootwindow.config(bd=20, bg="Cyan")

    roms = Text(rootwindow, font=("Arial", 15))
    for x in roms_list:
        roms.insert(END, x + '\n')
    roms.pack()

    rootwindow.eval('tk::PlaceWindow . center')
    rootwindow.mainloop()

# Main function
def main():
    global f_lock, usb_active

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="block", device_type="partition")

    usb_inserted = False
    double = 0

    while True:
        action, device = monitor.receive_device()

        if action == "remove" and usb_active != 0:
            usb_active = 0
            continue

        if action != "add":
            continue
        else:
            double += 1

        print_dev_info(device)
        auto_mount("/dev/" + device.sys_name)
        mp = get_mount_point("/dev/" + device.sys_name)
        print("Mount point: {}".format(mp))
        print_dev_stats(mp)
        usb_active = 1

        if double > 1:
            rom_name = terminal_xdotool_string(match_rom_window_get_name())
            print(rom_name)

            subprocess.call(['bash', '/home/pi/inor-games/configuration/escribirIDW.sh', rom_name])
            sleep(1)

            with open("{}".format(PID_FILE), 'r') as w_txt:
                content = w_txt.read().split("\n")
                print(content)
                print(content[0])
                prueba = list(content[0])
                print(prueba)
                sleep(1)

            subprocess.call(['bash', '/home/pi/inor-games/configuration/presionar_enter.sh', content[0]])
            sleep(2)

            process_usb_roms()
            usb_inserted = False
            double = 0


if __name__ == "__main__":
    main()