#!/bin/python
###Freedom along with security for Cyber
## Opennebula Server (Hardening - Version)
## Author : James PS
## Email  : jamesarems@hotmail.com
## Git    : github.com/jamesarems
###

import os,sys,subprocess
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


def checkRoot():
	os.system('clear')
	if ( uid == "0" ):
		osCheck()
		#print('Ok aanutto')
	else:
		print('\x1b[0;37;41m' +'You are not root user' + '\x1b[0m')
		sys.exit(1)


def depCheck():
	print('\x1b[6;30;42m' +'CHECKING DEPS----->'+ '\x1b[0m')
	os.system('yum install epel-release -y > /tmp/server.log')
	os.system('yum install -y openvpn easy-rsa iptables iptables-services wget yum-cron net-tools bind-utils nc mtr')
	os.system('mkdir /etc/openvpn/ccd > /tmp/server.log')
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
	os.system('cp pki/ca.crt /etc/openvpn/ca.crt; cp iptables.sh firewall.sh; cp pki/dh.pem /etc/openvpn/dh.pem; cp pki/issued/server.crt /etc/openvpn/server.crt; cp pki/private/server.key /etc/openvpn/server.key; cp pki/ta.key /etc/openvpn/ta.key; cp pki/crl.pem /etc/openvpn/crl.pem; cp server-sample.conf /etc/openvpn/server.conf ')
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
	os.system('systemctl start openvpn@server.service iptables')
	os.system('systemctl enable iptables')
	os.system('iptables-save')

def fireWall():
	print('\x1b[6;30;42m' +'CONFIGURING FIREWALL----->'+ '\x1b[0m')
	aeth = os.popen('ip link show').read()
	print('\x1b[0;35;40m' +aeth+ '\x1b[0m')
	ethernet = raw_input('Your ethernet inetrface name? Eg: eth0 : ')
	os.system("sed -i 's/eth0/%s/g' firewall.sh " % (ethernet))
	os.system('iptables -F')
	os.system('/usr/bin/bash iptables.sh')
	srvConf()

def cleanAll():
	print('\x1b[6;30;42m' +'CHECKING EXISTING INSTALLATION------>'+ '\x1b[0m')	
	if ( ovpn == "openvpn" ):
		opt1 = raw_input('\x1b[1;31;40m' + 'Existing server found, shall i clean and reinstall? (y/n)' + '\x1b[0m')
		if ( opt1 == "y"):
			os.system('clear')
			cleanAllMain()
		elif (opt1 == "n" ):
			print('You declined it, we cant process with existing installation, exiting')
			sys.exit(1)
		else:
			print('May be you put worng key, please use ' '\x1b[1;33;40m' +'y'+ '\x1b[0m' ' for yes ' 'and ''\x1b[2;32;40m' +  'n' + '\x1b[0m' ' for no')
			sys.exit(1)
	else:
		cleanAllMain()

def osCheck():
	if ( osvr == "centos-release-7" ):
		inputCheck()
	else:
		print('Your Operating system is not supported')
		sys.exit(1)	

def cleanAllMain():
	print('\x1b[1;33;41m' +'CLEANING EXISTING SERVICES AND FILES----->'+ '\x1b[0m')
	os.system('yum remove -y openvpn easy-rsa iptables iptables-services wget yum-cron net-tools bind-utils nc mtr; rm -rf /etc/openvpn ;rm -rf firewall.sh; rm -rf pki ; rm -rf /tmp/server.log')
	depCheck()

def inputCheck():
	if ( inputd == "client"):
		clientConf()
	elif ( inputd == "server" ):
		cleanAll()
	else:	
		os.system('clear')
		print('\x1b[0;37;44m' +'OpenVPN.py'+ '\x1b[0m' ', 2018 Developed by James PS. ')
		print('Options ------> help , server, client, advance-server, advance-client')
		sys.exit(1)

def clientConf():
	print('\x1b[6;30;42m' +'CREATING CLIENT CERTIFICATES------>'+ '\x1b[0m')
	clientName = raw_input('Input user/client name: ')
	serverIp = raw_input('Input VPN Server IP: ')
	if not clientName:
		print('ERROR : YOU MUST PUT USER/CLIENT NAME..!')
		sys.exit(1)
	elif not serverIp:
		print('ERROR : YOU MUST PUT SERVER IP..!')
                sys.exit(1)
	else:
		os.system('rm -rf %s; rm -rf %s.tar' % (clientName, clientName) )
		os.system('rm -rf pki/issued/%s.crt;rm -rf pki/private/%s.key; rm -rf pki/reqs/%s.req;sed -i "/%s/d" pki/index.txt ' % (clientName, clientName, clientName, clientName) )
		os.system('/usr/share/easy-rsa/3/easyrsa build-client-full %s nopass' % (clientName) )
		os.system('mkdir %s' % (clientName) )
		os.system('cp pki/ca.crt %s/ca.crt' % (clientName) )
		os.system('cp pki/issued/%s.crt %s/client.crt' % (clientName, clientName) )
		os.system('cp pki/private/%s.key %s/client.key' % (clientName, clientName) )
		os.system('cp pki/ta.key %s/ta.key' % (clientName) )
		os.system('cp client-sample.ovpn %s/client.ovpn' % (clientName) )
		os.system("sed -i 's/serverip/%s/g' %s/client.ovpn " % (serverIp, clientName))
		os.system('tar cfz %s.tgz %s ' % (clientName, clientName))
		print('YOUR CLIENT FILE IS READY AS %s' % (clientName))
		sys.exit(1)


checkRoot()
