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

##Read Configuration File
with open('aovpn-config.json') as f:
	readC = json.load(f)

##Read by section

confDir = readC['aovpn']['config']
confV = readC['aovpn']['version']
confR = readC['aovpn']['release']
confAdv = readC['aovpn']['advance']['enable']
confProto = readC['vpn']['proto']
confPort = readC['vpn']['port']
confIf = readC['vpn']['interface']
confIp = readC['vpn']['tunnel']
confServerIp = readC['os']['ip']

## Dep info collection
uid = os.popen('id -u').read(1)
ipf = os.popen('more /proc/sys/net/ipv4/ip_forward').read(1)
ovpn = os.popen('rpm -q openvpn').read(7)
osvr = os.popen('rpm -qf /etc/redhat-release').read(16)
########################
try:
    inputd = sys.argv[1]
except IndexError:
    inputd = 'null'
########################


def checkRoot(artW):
	if ( uid == "0" ):
		osCheck(artW)
	else:
		print('\x1b[0;37;41m' +'You are not root user' + '\x1b[0m')
		sys.exit(1)


def depCheck():
	print('\x1b[6;30;42m' +'CHECKING DEPS----->'+ '\x1b[0m')
	os.system('yum install epel-release -y > /tmp/server.log')
	os.system('yum install -y openvpn python-pip screen easy-rsa iptables zip iptables-services wget yum-cron net-tools bind-utils nc mtr > /tmp/server.log')
	os.system('mkdir /etc/openvpn/ccd > /tmp/server.log ; pip install pyftpdlib > /tmp/server.log')
	os.system('mkdir -p %s/client > /tmp/server.log' % (confDir))
	print('Deps saved')
	createCerts()

def createCerts():
	os.system('/usr/share/easy-rsa/3/easyrsa init-pki')
	print('\x1b[2;30;44m' +'Now input a name for your server Eg: VPN'+ '\x1b[0m')
	os.system('/usr/share/easy-rsa/3/easyrsa build-ca nopass')
	os.system('/usr/share/easy-rsa/3/easyrsa gen-dh')
	os.system('/usr/share/easy-rsa/3/easyrsa build-server-full server nopass')
	#os.system('/usr/share/easy-rsa/3/easyrsa build-client-full client nopass')
	os.system('/usr/share/easy-rsa/3/easyrsa gen-crl')
	os.system('openvpn --genkey --secret pki/ta.key')
	copyConf()

def copyConf():
	print('\x1b[6;30;42m' +'COPYING CONFIGURATIONS AND CERTS----->'+ '\x1b[0m')
	os.system('cp server.conf.smpl server.conf')
	os.system("sed -i 's/APROTO/%s/g' server.conf " % (confProto))
	os.system("sed -i 's/APORT/%s/g' server.conf " % (confPort))
	os.system("sed -i 's/ATUNNEL/%s/g' server.conf " % (confIp))
	os.system('cp pki/ca.crt /etc/openvpn/ca.crt; cp iptables.sh.smpl iptables.sh; cp pki/dh.pem /etc/openvpn/dh.pem; cp pki/issued/server.crt /etc/openvpn/server.crt; cp pki/private/server.key /etc/openvpn/server.key; cp pki/ta.key /etc/openvpn/ta.key; cp pki/crl.pem /etc/openvpn/crl.pem; mv server.conf /etc/openvpn/server.conf ')
	if ( ipf == "1"):
		print('Done')
		fireWall()
	else:
		print('IP Forwarding is not enabled..Enabling now.')
		os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
		fireWall()
def srvConf():
	print('\x1b[6;30;42m' +'STARTING SERVICES------>'+ '\x1b[0m')
	os.system('systemctl -f enable openvpn@server.service')
	os.system('systemctl restart openvpn@server.service')
	os.system('iptables-save > /tmp/server.log')

def fireWall():
	print('\x1b[6;30;42m' +'CONFIGURING FIREWALL----->'+ '\x1b[0m')
	aeth = os.popen('ip link show').read()
	#print('\x1b[0;35;40m' +aeth+ '\x1b[0m')
	ethernet = confIf
	os.system("sed -i 's/eth0/%s/g' iptables.sh " % (ethernet))
	os.system("sed -i 's/VPNPORT/%s/g' iptables.sh " % (confPort))
	os.system('iptables -F')
	os.system('systemctl enable iptables > /tmp/server.log')
	os.system('systemctl restart iptables')
	os.system('/usr/bin/bash iptables.sh; mv iptables.sh %s' % (confDir))
	print('Done')
	srvConf()

def artWork():
       	if ( confAdv == "true"):
		artW =   """
                   		 ___  __ 
                   		|__| |  | |  | |__] |\ | 
                   		|  | |__|  \/  |    | \| Advanced
                	 """
        	os.system('clear')
        	print('\033[1;32;40m' +artW+ '\033[0m 1;32;40m')
        	print('Released on: ' +confR+ ' Verion: ' +confV)
        	checkRoot(artW)
	else:

		artW =   """
			          ___  __ 
               			 |__| |  | |  | |__] |\ | 
               			 |  | |__|  \/  |    | \| 
                 	 """
		os.system('clear')
		print('\033[1;33;40m' +artW+ '\033[0m')
		print('Released on: ' +confR+ ' Verion: ' +confV)
		checkRoot(artW)

def cleanAll():
	print('\x1b[6;30;42m' +'CHECKING EXISTING INSTALLATION------>'+ '\x1b[0m')	
	if ( ovpn == "openvpn" ):
		opt1 = raw_input('\x1b[1;31;40m' + 'Existing server found, shall I clean and reinstall? (y/n)' + '\x1b[0m')
		if ( opt1 == "y"):
			cleanAllMain()
		elif (opt1 == "n" ):
			print('You declined it, I cant process with existing installation, exiting')
			sys.exit(1)
		else:
			print('May be you put worng key, please use ' '\x1b[1;33;40m' +'y'+ '\x1b[0m' ' for yes ' 'and ''\x1b[2;32;40m' +  'n' + '\x1b[0m' ' for no')
			sys.exit(1)
	else:
		print('Fresh Installation Started')
		cleanAllMain()

def osCheck(artW):
	if ( osvr == "centos-release-7" ):
		inputCheck(artW)
	else:
		print('Your Operating system is not supported')
		sys.exit(1)	

def cleanAllMain():
	print('\x1b[1;33;41m' +'CLEANING EXISTING SERVICES AND FILES----->'+ '\x1b[0m')
	os.system('systemctl stop openvpn@server > /tmp/server.log ; systemctl disable openvpn@server > /tmp/server.log')
	os.system('yum remove -y openvpn easy-rsa iptables iptables-services wget yum-cron net-tools bind-utils nc mtr > /tmp/server.log; rm -rf /etc/openvpn ;rm -rf firewall.sh; rm -rf pki ; rm -rf /tmp/server.log')
	os.system('rm -rf %s' % (confDir))
	print('Done')
	depCheck()

def inputCheck(artW):
	if ( inputd == "client"):
		clientConf(artW)
	elif ( inputd == "server" ):
		cleanAll()
	else:	
		os.system('clear')
		print('\033[1;33;40m' +artW+ '\033[0m')
		print('Released on:' +confR+ ' Verion: ' +confV)
		print('2018-19 Developed by James PS. ')
		print('Options --> server, client.  Please check aovpn-config.json')
		sys.exit(1)

def clientConf(artW):
	mainPki = os.popen('ls -lR pki | grep ^d | wc -l').read(1)
	os.system('clear')
	print('\033[1;33;40m' +artW+ '\033[0m')
        print('Released on: ' +confR+ ' Verion: ' +confV)
	if ( mainPki == "4"):
		print('...')
	else:
		print('Server not found. Please install and configure server')
		sys.exit(1)
	print('\x1b[6;30;42m' +'CREATING CLIENT CERTIFICATES------>'+ '\x1b[0m')
	try:
		clientName = raw_input('Input user/client name: ')
		serverIp = confServerIp
		if not clientName:
			print('ERROR : YOU MUST PUT USER/CLIENT NAME..!')
			sys.exit(1)
		elif not serverIp:
			print('ERROR : YOU MUST PUT SERVER IP..!')
                	sys.exit(1)
		else:
			os.system('cd /etc/aovpn/client/ ; rm -rf %s' % (clientName) )
			os.system('rm -rf pki/issued/%s.crt;rm -rf pki/private/%s.key; rm -rf pki/reqs/%s.req;sed -i "/%s/d" pki/index.txt ' % (clientName, clientName, clientName, clientName) )
			os.system('/usr/share/easy-rsa/3/easyrsa build-client-full %s nopass' % (clientName) )
			os.system('mkdir %s/client/%s' % (confDir, clientName) )
			os.system('cp pki/ca.crt %s/client/%s/ca.crt' % (confDir, clientName) )
			os.system('cp pki/issued/%s.crt %s/client/%s/client.crt' % (clientName, confDir, clientName) )
			os.system('cp pki/private/%s.key %s/client/%s/client.key' % (clientName, confDir, clientName) )
			os.system('cp pki/ta.key %s/client/%s/ta.key' % (confDir, clientName) )
			os.system('cp client.ovpn.smpl %s/client/%s/client.ovpn ; sh /etc/aovpn/iptables.sh' % (confDir, clientName) )
			os.system("sed -i 's/serverip/%s/g' %s/client/%s/client.ovpn " % (serverIp, confDir, clientName))
			os.system("sed -i 's/serverport/%s/g' %s/client/%s/client.ovpn " % (confPort, confDir, clientName))
			os.system('cd /etc/aovpn/client/ ; tar cfz %s/%s.tgz %s ' % (clientName, clientName, clientName))
			print('YOUR CLIENT FILE IS READY AS %s.tgz' % (clientName))
			clientAdv(clientName)
	except KeyboardInterrupt:
		print('You canceled it. Please try again')
		sys.exit()
def clientAdv(clientName):
	if ( confAdv == "true"):
		print('\x1b[1;30;46m' +'ADVANCED MODE(ON CLIENT)------>'+ '\x1b[0m')
		os.system('utils/plus.py %s' % (clientName))
	else:
		sys.exit(1)

artWork()
#checkRoot()
