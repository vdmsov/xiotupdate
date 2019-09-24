#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import subprocess as sp
import paho.mqtt.client as mqttc
import paho.mqtt.publish as mqttp


def version(direct=''):

	process = sp.Popen(["""dpkg --list xiot | grep xiot | awk '{print $3}'"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0].replace('\n', '')
	process.wait()

	if direct == 'mqtt':
		mqttp.single('/xsys/version', stdout, hostname='localhost')

	return stdout


def check_install():

	process = sp.Popen(["""dpkg --list xiot | grep xiot | awk '{print $1}'"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	process.wait()

	if stdout[:2] == 'ii': return True
	else: return False


def delete():

	process = sp.Popen(["""dpkg -r xiot"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	process.wait()

	mqttp.single('/xsys/install', 'XIoT Automation packet is deleted!', hostname='localhost')

	print(stdout)


def download(url):

	path = os.getcwd()

	for file in os.listdir(path):
		if file[:8] == 'xiot.deb':
			os.remove(file)

	process = sp.Popen(["""wget """ + str(url)], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	process.wait()

	mqttp.single('/xsys/install', 'XIoT Automation packet new version is downloaded!', hostname='localhost')

	print(stdout)


# /xsysui/install https://github.com/XiotLogic/xiot-deb/raw/master/xiot.deb
def install(url):

	if check_install():
		delete()

	download(url)

	process = sp.Popen(["""dpkg -i xiot.deb"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	process.wait()

	mqttp.single('/xsys/install', 'XIoT Automation packet is installed! Version: ' + version(), hostname='localhost')

	print(stdout)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/xsysui/install", 0)
    client.subscribe("/xsysui/version", 0)


def on_message(client, userdata, msg):
	
	if msg.topic == '/xsysui/install':
		install(msg.payload)

	if msg.topic == '/xsysui/version':
		version('mqtt')


client = mqttc.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
