#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lifxlan import *
from time import sleep

# Démarrage du client
lifx = LifxLAN()

# Découverte des ampoules
devices = lifx.get_lights()

# Récupération de mon ampoule (nommée "AmpouleBureau")
for device in devices:
    if device.get_label() == "AmpouleBureau":
        monAmpoule = device

# Allumage et extinction
monAmpoule.set_power("on")
sleep(2)
monAmpoule.set_power("off")


