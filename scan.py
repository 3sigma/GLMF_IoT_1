#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygatt.backends

# D�marrage du BLED112
adapter = pygatt.backends.BGAPIBackend()
adapter.start()

# Scan des p�riph�riques Bluetooth � port�e du BLED112
print("Scan...\n")
devices = adapter.scan()

# Affichage du nom, de l'adresse et de la puissance du signal de chaque p�riph�rique
for dev in devices:
    name = dev.get('name')
    address = dev.get('address')
    rssi = dev.get('rssi')
    print(name + ":  " + address + " - RSSI: " + str(rssi))

# Arr�t du BLED112
adapter.stop()

