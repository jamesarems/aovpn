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
with open('aovpn-config.json') as f:
        readC = json.load(f)

confFtp = readC['aovpn']['advance']['ftp']
confEnc = readC['aovpn']['advance']['encrypt']
confUrl = readC['os']['ip']
confPath = readC['aovpn']['config']
aBlink    = '\33[5m'
aEnd = '\033[0m'

def aovpnFtp():
	if ( confFtp == "true" ):
		try:	
			print('\x1b[6;30;42m' +'FTP ACCESS MODE------>'+ '\x1b[0m')
			os.system('iptables -A INPUT -p tcp --dport 6000:7000 -m state --state NEW -s 0.0.0.0/0 -j ACCEPT')	
			os.system('screen -S aovpn -d -m python -m pyftpdlib -d %s/client/%s -u %s -P %s -p 21 -r 6000-7000' % (confPath, userMain, userMain, random))
			print ('FTP Server started. Server will stop within 2 minute . Please download with,')
			print ('Username: ' +userMain)
			print ('Password: ' +random)
			print ('Access URL: ftp://%s' % (confUrl) )
			time.sleep(120)
			os.system('screen -X -S "aovpn" quit')
			os.system('iptables -D INPUT -p tcp --dport 6000:7000 -m state --state NEW -s 0.0.0.0/0 -j ACCEPT')
			print('FTP Server Stopped')
			#sys.exit(1)
		except KeyboardInterrupt:
			os.system('screen -X -S "aovpn" quit')
			os.system('iptables -D INPUT -p tcp --dport 6000:7000 -m state --state NEW -s 0.0.0.0/0 -j ACCEPT')
			print('Keboard interrupted. FTP Server stopped')
			

	elif ( confFtp == "false" ):
		print('\x1b[6;37;44m' +'[SKIPPING]FTP ACCESS MODE------>'+ '\x1b[0m')
		sys.exit()
	else:
		sys.exit()

def aovpnEnc():
	if ( confEnc == "true" ):
	 	print('\x1b[6;30;42m' +'ENCRYPTING ARCHIVE------>'+ '\x1b[0m')	
		os.system('rm -rf /etc/aovpn/client/%s/%s.tgz' % (userMain, userMain))
		os.system('cd /etc/aovpn/client/ ; zip -P %s %s.zip %s' % (random, userMain, userMain,))
		aovpnFtp()
	else:
		print('\x1b[6;37;44m' +'[SKIPPING]ENCRYPTING ARCHIVE------>'+ '\x1b[0m')
		aovpnFtp()

if ( confFtp == "false" and confEnc == "false"):
	print('Seems like advanced option is enabled and all other ' +aBlink+'sub options are disabled'+aEnd+'. What is this? Please look aovpn-config.json file.')
else:
	aovpnEnc()
