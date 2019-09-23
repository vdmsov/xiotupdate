#!/usr/bin/python

import paho.mqtt.publish as publish
import sys

publish.single("update", sys.argv[1], hostname="localhost")
