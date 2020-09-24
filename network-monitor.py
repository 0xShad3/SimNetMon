from datetime import datetime
import os
import nmap
import sys
import time
import csv


try:
	nmp = nmap.PortScanner()
except nmap.PortScannerError:
	print("There was an PortScannerError aka nmap not found please fix it :) ")
	sys.exit(0)
except:
	print("An error occured")
	sys.exit(0)


hostList = [[]]

## Needs fix
def writeCommonMACAddresses():
	with open('mac_addresses.csv', 'w+',newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(hostList)
		csvfile.close()

def scan():
	nmp.scan(hosts='192.168.1.0/24',arguments='-script smb-os-discovery.nse -T5 192.168.1.0/24')

	for host in nmp.all_hosts():
		try:
			name = nmp[host].get('hostnames')[0].get('name')
			mac_adress = nmp[host].get('addresses').get('mac')
			localIPv4 = nmp[host].get('addresses').get('ipv4')
			vendor = nmp[host].get('vendor').get(mac_adress)

			hostList.append([name,mac_adress,localIPv4,vendor])

		except:
			vendor = mac_adress = localIPv4 = 'unknown'	

	
	
	for i in hostList:
		print (i)

def alert():
	print("Alert")




def main():

	hostCountNew = 1
	hostCountOld = 0
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("[+] Performing a NMAP scan ====> {}".format(current_time))
	scan()
	print("[+] Hosts found ===> {} ".format(len(hostList)))

	for i in hostList:
		print("[host] => {}".format(i))
	
	if (hostCountNew > hostCountOld):
		print("[A] Alerting owner new host connected".format(hostList[0]))
		time.sleep(10)


if __name__ == '__main__':
	main()