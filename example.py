#!/usr/bin/python3
# -*- coding: utf-8 -*-
# license removed for brevity

import HiwonderServoController as a
import time


a.setConfig('/dev/ttyAMA0', timeout=5)
while True:
	a.moveServo(1, 0, 100)
	print(a.ServoPosRead(1))
	time.sleep(1.1)
	a.moveServo(1, 1000, 2000)
	print(a.ServoPosRead(1))
	time.sleep(2.1)
	print(a.getBatteryVoltage())

