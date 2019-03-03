#!/usr/bin/python
###Freedom along with security for Internet - AOVPN
## OpenVPN Server with advanced security patches and features - Spiderman (2.0) Version
## Author : James PS
## Email  : jamesarems@hotmail.com
## Git    : github.com/jamesarems
###
import os,sys,subprocess
import json
import pprint
import random,string,time

##Generating pass
random = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])

## Catch Arg
userMain = sys.argv[1]
## Collecting Data
with open('../aovpn-config.json') as f:
        readC = json.load(f)

confFtp = readC['aovpn']['advance']['ftp']
confUrl = readC['os']['ip']
confPath = readC['aovpn']['config']



def aovpnFtp():
	if ( confFtp == "true" ):
		try:
			print('FTP Enabled')
			os.system('screen -S aovpn -d -m python -m pyftpdlib -d %s/client/%s -u %s -P %s -p 21' % (confPath, userMain, userMain, random))
			print ('FTP Server started. Server will stop within 2 minute . Please download with,')
			print ('Username: ' +userMain)
			print ('Password: ' +random)
			print ('Access URL: ftp://%s' % (confUrl) )
			time.sleep(120)
			os.system('screen -X -S "aovpn" quit')
			print('FTP Server Stopped')
			sys.exit(1)
		except KeyboardInterrupt:
			os.system('screen -X -S "aovpn" quit')
			print('Keboard interrupted. FTP Server stopped')
			sys.exit(1)

	elif ( confFtp == "false" ):
		print('FTP Disabled')
	else:
		sys.exit()
aovpnFtp()
