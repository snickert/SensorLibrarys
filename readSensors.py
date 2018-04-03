"""
readSensors - Humidity-, Temperature-, PH-, Flow, Pressure- and Moisture-Sensor

Different Sensors are read with directly calculation
of default Electronic-Hardware for a couple automation tasks

Autor: Jan Wickert
Date: 27.03.2018
"""

import math
import time
import logging

"""Definition of RaspberryPi3 Pins"""
LIGHT_PIN = 40
WATERTEMPERATURE_IN = 37
WATERTEMPERATURE_OUT = 38
AIRCOOLER_IN = 35
AIRCOOLER_OUT = 36
HEATER_IN = 31
HEATER_OUT = 36
HUMIDITY_IN = 23
HUMIDITY_OUT = 22
DEHUMIDITY_IN = 19
DEHUMIDITY_OUT = 16
CO2_IN = 13
CO2_OUT = 10
AIRFLOW_IN = 35
AIRFLOW_OUT = 32
# AIRPRESSURE_IN = XX
# AIPRESSURE_OUT = XX
SOILMOISTURE_IN = 11
SOILMOISTURE_OUT = 8
SOILPH_IN = 15
SOILPH_OUT = 16
WATERPH_IN = 21
WATERPH_OUT = 12
FLUSHSYSTEM_IN = 29
FLUSHSYSTEM_OUT = 24

def readAD(pinAD):
    adValue = 0
    return adValue


""" Function for reading the ppm Value with a given analog Signal of Micro CO click """
def calcPPM(ppmAD):
    rl = 5000.00000000000
    # Calculation of used CO2-Sensor with 3,3V Input and 10-Bit Controller
    vrl = ppmAD * 3.3/1024
    rs = rl*(5-vrl)/vrl
    ratio = rs/rl
    # Calculation could be improved trough datasheet
    lgPPM = (math.log(ratio) * -3.7) + 0.9948
    oPPM = pow(10, lgPPM)
    time.sleep(0.01)
    return oPPM


""" Function for reading 40PH Value and calculate an improved avverage of the measurements """
def calcPH(pinPH):
    OffSETSOILPH = 0.0
    vPH = [0]*40
    i = 0
    # Read 40x the Sensors Value on pinPH
    while i < len(vPH):
        vPH[i] = readAD(pinPH)
    if vPH[0] < vPH[1]:
        min = vPH[0]
        max = vPH[1]
    else:
        min = vPH[1]
        max = vPH[0]
    i = 2
    allPH = 0
    # Calculate the Average with an improved algorithm
    while i < len(vPH):
        if vPH[i] < min:
            allPH += min
            min = vPH[i]
        else:
            if max < vPH[i]:
                allPH += max
                max = vPH[i]
            else:
                allPH = vPH[i]
    avgPH = allPH / (i-2)
    vIN = avgPH * 5.0/1024
    oPH = 3.5 * vIN + OffSETSOILPH
    return oPH

def notificationSend():
    return

def logicProofValues(proofValue, method):
    if method == 'AirCooler':
        acMin = 25
        logging.info('Value AirCooler: ' + proofValue + '\n')
        if proofValue < acMin:
            AIRCOOLER_OUT = 1
        elif acMin+10 < proofValue:
            notificationSend()
            logging.debug('AirCooler Temperature too high')
    elif method == 'Heater':
        heaterMin = 10
        logging.info('Value Heater: ' + proofValue + '\n')
        if proofValue < heaterMin:
            HEATER_OUT = 1
        elif proofValue < heaterMin-10:
            notificationSend()
            logging.debug('Heater Temperature too low')
    elif method == 'Humidity':
        acMin = 25
        logging.info('Value Humidity: ' + proofValue + '\n')
        if proofValue < acMin:
            HUMIDITY_OUT = 1
        elif proofValue < acMin-10:
            notificationSend()
            logging.debug('Humidity too low')
    elif method == 'DeHumidifier':
        acMin = 1500
        logging.info('Value DeHumidifier: ' + proofValue + '\n')
        if acMin < proofValue:
            DEHUMIDITY_OUT = 1
        elif acMin+10 < proofValue:
            notificationSend()
            logging.debug('Humidity too high')
    elif method == 'CO2':
        acMin = 50
        logging.info('Value CO2: ' + proofValue + '\n')
        if proofValue < acMin:
            CO2_OUT = 1
        elif proofValue < acMin-500 or  acMin+500 < proofValue:
            notificationSend()
            logging.debug('CO2 too low or high')
    elif method == 'AirFlow':
        acMin = 25
        logging.info('Value AirFlow: ' + proofValue + '\n')
        if acMin < proofValue:
            AIRFLOW_OUT = 1
        elif proofValue < acMin-20 or acMin+20 < proofValue:
            notificationSend()
            logging.debug('AirFlow too low or too high')
    elif method == 'SoilMoisture':
        acMin = 25
        logging.info('Value SoilMoisture: ' + proofValue + '\n')
        if proofValue < acMin:
            SOILMOISTURE_OUT = 1
        elif proofValue < acMin-20 or acMin+20 < proofValue:
            notificationSend()
            logging.debug('SoilMoisture Temperature too low')
    elif method == 'SoilPH':
        acMin = 25
        logging.info('Value SoilPH: ' + proofValue + '\n')
        if proofValue < acMin:
            SOILPH_OUT = 1
        elif proofValue < acMin-5 or acMin+5 < proofValue:
            notificationSend()
            logging.debug('SoilPH too low or too high')
    elif method == 'WaterPH':
        acMin = 25
        logging.info('Value WaterPH: ' + proofValue + '\n')
        if proofValue < acMin:
            WATERPH_OUT = 1
        elif proofValue < acMin-5 or acMin+5 < proofValue:
            notificationSend()
            logging.debug('WaterPH too low or too high')
    elif method == 'FlushSystem':
        flushProof = True
        logging.info('Value FlushSystem: ' + proofValue + '\n')
        if flushProof is True:
            FLUSHSYSTEM_OUT = 1
            time.sleep(10)


def __init__():
    logging.basicConfig(level=logging.DEBUG)
    return


startProgramm = True
while startProgramm:
    hallo = True
