#!/usr/bin/env python3

import re
import argparse
import subprocess as sp


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
	

def check():
	"""Here we cheack if the mac has changed"""
	ifconfig = sp.check_output(['sudo','ifconfig','eth0'])
	mac_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',ifconfig)
	# print(mac_result.group(0))
	if mac_result.group(0) == mac:
		print('Mac changed')
		print('[+] '+interface+' --> '+mac)
	else:
		print('Faliour')


# now just calling all the methods
(interface, mac) = get_arguments()
change(interface, mac)
check()

