#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports pour le BLED112 et le SensorTag
import pygatt.backends
import pysensortag

# Import pour la LIFX
from lifxlan import *

import sched
from time import time, sleep
import signal
import sys

# Variables pour la gestion de la luminosité
Lux = 0
etatLampe = 0
# Un hystérésis sera nécessaire
seuilLuminositeMin = 50
seuilLuminositeMax = 100

# Création d'un scheduler pour exécuter des opérations à cadence fixe
T0 = time()
dt = 1
i = 0
s = sched.scheduler(time, sleep)


def setup():
    global adapter, sensortag, light, monAmpoule
    
    adapter = pygatt.backends.BGAPIBackend()
    adapter.start()
        
    print("Connexion au SensorTag")
    sensortag = pysensortag.PySensorTag(adapter, 'B0:B4:48:C0:5D:00')
    
    print("Activation du luxometre")
    sensortag.ActivateLuxometerSensor()
    
    # Délai pour que l'activation se fasse
    sleep(1)
    
    # Gestion de l'ampoule
    # Démarrage du client
    lifx = LifxLAN()

    # Découverte des ampoules
    devices = lifx.get_lights()

    # Récupération de mon ampoule (nommée "AmpouleBureau")
    for device in devices:
        if device.get_label() == "AmpouleBureau":
            monAmpoule = device

    # Allumage et extinction
    print("Test de l'ampoule: allumage pendant 2 s")
    monAmpoule.set_power("on")
    sleep(2)
    monAmpoule.set_power("off")
    

 
def loop():
    global i
    i = i+1
    s.enterabs( T0 + (i * dt), 1, Automate, ())
    s.run()


def Automate():
    global sensortag, Lux, seuilLuminositeMin, seuilLuminositeMax, etatLampe, monAmpoule
    
    # Scan des périphériques Bluetooth
    devices = adapter.scan(timeout = 2, scan_interval=200, scan_window=200, active = False)
    
    # Recherche de l'adresse de l'iBeacon
    foundAddress = False
    for dev in devices:
        address = dev.get('address')
        if address == '68:9E:19:10:DA:CE':
            foundAddress = True
            print("iBeacon en vue !")
        else:
            print("iBeacon absent !")
    
    # On passe à la suite uniquement si l'iBeacon est présent
    if foundAddress:
        # Lecture de la luminosité et allumage en fonction de la
        # valeur par rapport à l'hystérésis
        Lux = sensortag.GetLuxometer()
        print "Light intensity: %.2f lx" % Lux
        if Lux < seuilLuminositeMin:
            if etatLampe==0:
                print("Luminosite suffisante: allumage lampe")
                monAmpoule.set_power("on")
                etatLampe = 1
        elif Lux > seuilLuminositeMax:
            if etatLampe==1:
                print("Luminosite insuffisante: extinction lampe")
                monAmpoule.set_power("off")
                etatLampe = 0
    else:
        if etatLampe==1:
            print("iBeacon absent: extinction lampe")
            monAmpoule.set_power("off")
            etatLampe = 0
        

    print("")

# Gestion du CTRL-C
def signal_handler(signal, frame):
    global adapter, monAmpoule
    print("You pressed Ctrl+C!")
    print("Stop")
    monAmpoule.set_power("off")
    adapter.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__=="__main__":
    setup()
    print("Setup done.")
    while True: loop()


