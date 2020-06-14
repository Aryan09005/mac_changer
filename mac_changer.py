#!/usr/bin/env python3

import re
import argparse
import subprocess as sp
from random import choice

parser = argparse.ArgumentParser()

def get_arguments():
	"""Parsing the command line arguments"""
	parser.add_argument('-i', '--interface', help='interface to affect')
	parser.add_argument('-m','--mac', help='mac to allocate')

	args = parser.parse_args()
	interface = args.interface
	mac = args.mac
	return (interface, mac)

# this is more secure b/c python understads that this
# list has one part of the same command in each element
# this removes command line injection
def change(interface, mac):
	"""Changing mac"""
	sp.call(['sudo', 'ifconfig', interface, 'down'])
	sp.call(['sudo', 'ifconfig', interface,'hw', 'ether', mac])
	sp.call(['sudo', 'ifconfig', interface, 'up'])
	# sp.call(['sudo', 'ifconfig'])
	

def check(interface, mac):
	
	"""Here we cheack if the mac has changed"""
	ifconfig = sp.check_output(['sudo','ifconfig',interface]).decode()
	regexMax = re.compile(r'(\w\w:){5}\w\w')
	# if mac in str(ifconfig):
	# 	print('Mac changed')
	# 	print('[+] '+interface+' --> '+mac)
	# else:
	result = regexMax.search(ifconfig)
	if not result == None and result.group() == mac:
		print('Mac changed')
		print('[+] '+interface+' --> '+mac)
	else:
		print('[[[[!]]]] Faliour',result.group())
		# print('Error ')
		# print()	


def random():
	mac = ''
	for _ in range(0,6):
		hex_stuff = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
		mac += str(choice(hex_stuff))
		mac += str(choice(hex_stuff))
		mac += ':'
	print('Random : ',mac[:-1])	
	return mac[:-1]

# now just calling all the methods
(interface, mac) = get_arguments()

if mac == None:
	mac = random()

change(interface, mac)
check(interface, mac)
