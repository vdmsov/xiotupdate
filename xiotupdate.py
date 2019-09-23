#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import subprocess as sp
import paho.mqtt.client as mqtt


def check_install():

	process = sp.Popen(["""dpkg --list xiot | grep xiot | awk '{print $1}'"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]

	if stdout[:2] == 'ii': return True
	else: return False


def delete():

	process = sp.Popen(["""dpkg -r xiot"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	print(stdout)


def download(url):

	path = os.getcwd()

	for file in os.listdir(path):
		if file[:8] == 'xiot.deb':
			os.remove(file)

	process = sp.Popen(["""wget """ + str(url)], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	print(stdout)


def install(url='https://github.com/XiotLogic/xiot-deb/raw/master/xiot.deb'):

	if check_install():
		delete()

	download(url)

	process = sp.Popen(["""dpkg -i xiot.deb"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0]
	print(stdout)


def version():

	process = sp.Popen(["""dpkg --list xiot | grep xiot | awk '{print $3}'"""], \
		stdout=sp.PIPE, shell = True)
	stdout = process.communicate()[0].replace('\n', '')
	return stdout


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("update", 0)


def on_message(client, userdata, msg):
	
	if msg.payload == 'install':
		install()
		print('XIoT Automation packet is installed! Version: ' + version())

	if msg.payload == 'version':
		print(version())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
