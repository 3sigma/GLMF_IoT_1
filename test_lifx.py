#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lifxlan import *
from time import sleep

# D�marrage du client
lifx = LifxLAN()

# D�couverte des ampoules
devices = lifx.get_lights()

# R�cup�ration de mon ampoule (nomm�e "AmpouleBureau")
for device in devices:
    if device.get_label() == "AmpouleBureau":
        monAmpoule = device

# Allumage et extinction
monAmpoule.set_power("on")
sleep(2)
monAmpoule.set_power("off")


