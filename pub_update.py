#!/usr/bin/python

import paho.mqtt.publish as publish
import sys

publish.single(sys.argv[1], sys.argv[2], hostname="localhost")
