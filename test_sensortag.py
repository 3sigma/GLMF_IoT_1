#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Requirement: you must have pygatt installed:
# git clone https://github.com/3sigma/pygatt.git
# cd pygatt
# sudo python setup.py install
# cd ..
import pygatt.backends

import pysensortag
from time import sleep

# Démarrage du BLED112
adapter = pygatt.backends.BGAPIBackend()
adapter.start()

# Connexion au SensorTag
sensortag = pysensortag.PySensorTag(adapter, 'B0:B4:48:C0:5D:00')

print("Activation du capteur de temperature")
sensortag.ActivateTemperatureSensor()

print("Activation du luxometre\n")
sensortag.ActivateLuxometerSensor()

# Délai laissant le temps aux activations de se réaliser
sleep(1)

# Lecture et affichage des températures
temperatures = sensortag.GetTemperature()
ambientTemp = temperatures[0]
objectTemp = temperatures[1]
print("Ambient Temp: %.2f C" % ambientTemp)
print("Object Temp: %.2f C\n" % objectTemp)

# Lecture et affichage de la luminosité
Lux = sensortag.GetLuxometer()
print("Light intensity: %.2f lx" % Lux)

# Arrêt du BLED112
adapter.stop()
