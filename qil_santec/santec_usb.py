# -*- coding: utf-8 -*-

"""
Python script to control Santec Instruments via USB communication
using Santec_FTDI DLL and FTDI USB Driver
Created on Mon Feb 27 18:42:37 2024

@organization: santec holdings corp.
@version: 2.1.0

The current version supports Santec's Instruments connected via USB.
"""

"""
QIL edits this class to become a communication handler parent class such that 
hopefully GPIB capability will just be a matter of changing the class to inherit from
"""

# Basic imports (or dependencies)
import os
import clr
import sys
import time

# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r".\qil_santec\DLL"  # device-class path
abs_path=os.path.abspath(os.path.join(assembly_path))
sys.path.append(abs_path)
ref = clr.AddReference(abs_path+r"\Santec_FTDI.dll")

# Importing the main method from the DLL
import Santec_FTDI as ftdi

# Calling the FTD2xx_helper class from the Santec_FTDI dll
ftdi_class = ftdi.FTD2xx_helper


def get_devices():
    # ListDevices() returns the list of all Santec instruments
    list_of_devices = ftdi_class.ListDevices()

    # List to store all the detected instruments
    device_list = {}

    # Print the Name and Serial number of each detected instrument
    if not list_of_devices:
        raise DeviceException("No instruments found")
    else:
        for index, device in enumerate(list_of_devices, start=1):
            if device:
                device_list[device.SerialNumber]=device
    return device_list

# Instrument control class
class Santec:
    """
    Santec Instrument control class
    """

    def __init__(self, instrument):
        """
        default parameter initialization
        :parameter instrument - user selected instrument instance
        """
        self.instrument = instrument

    def query(self,command):
        """
         Queries a command to the instrument inputted by the user
        """
        query = self.instrument.Query(f'{command}')
        time.sleep(0.2)
        return query
 
    def write(self,command):
        """
        Writes a command to the instrument inputted by the user
        """
        if self.instrument.Write(f'{command}'):
            return True
        return False


    def queryIdn(self):
        """
        Instrument identification query
        """
        print(self.instrument.QueryIdn())
        return True

    def closeConnection(self):
        self.instrument.CloseUsbConnection()

    def Exit(self):
        self.closeConnection()
        sys.exit()

class USB_COMMS():
    def __init__(self,serialNumber=16120001):
        device_list=get_devices()
        serialNumber=str(serialNumber)
        if serialNumber in device_list:
            instrument = ftdi.FTD2xx_helper(serialNumber)
            print(f"CONNECTION SUCCESSFUL, CONNECTED TO {instrument.QueryIdn()}")
            self.instrument=Santec(instrument)
        else:
            raise DeviceException("Device with serial number %s not found."%serialNumber)

    




class DeviceException(Exception):
    pass