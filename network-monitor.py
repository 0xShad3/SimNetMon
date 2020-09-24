from datetime import datetime
import os
import nmap
import sys
import time
import csv
import asyncio
import discord
from discord.ext.commands import CommandNotFound
from discord.ext import commands
from discord.ext.commands import Cog,Context

discordBotAPIKey = "REDACTED"

bot = commands.Bot(command_prefix='!')

try:
	nmp = nmap.PortScanner()
except nmap.PortScannerError:
	print("There was an PortScannerError aka nmap not found please fix it :) ")
	sys.exit(0)
except:
	print("An error occured")
	sys.exit(0)


hostList = []

@bot.command()
async def displayUnkownDevices(ctx):
	#will display all Uknown Devices which the discord user will name them 

@bot.command()
async def displayKnownDevices(ctx):
	#will display connected devices and log last connections

def getCurrentTime():
	now = datetime.now()
	return now.strftime("%H:%M:%S")
	
## Needs fix
def writeCommonMACAddresses():
	with open('mac_addresses.csv', 'w+',newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(hostList)
		csvfile.close()

def scanNetwork():
	nmp.scan(hosts='192.168.1.0/24',arguments='-script smb-os-discovery.nse -T5 192.168.1.0/24')
	i = 0
	for host in nmp.all_hosts():
		try:
			name = nmp[host].get('hostnames')[0].get('name')
			mac_adress = nmp[host].get('addresses').get('mac')
			localIPv4 = nmp[host].get('addresses').get('ipv4')
			vendor = nmp[host].get('vendor').get(mac_adress)

			hostList.insert(i,[name,mac_adress,localIPv4,vendor])
			i += 1
		except:
			vendor = mac_adress = localIPv4 = 'unknown'	

	
def alert():
	print("Alert")



def main():
	hostCountNew = 0
	hostCountOld = 0
	while True:

		print("[+] Performing a NMAP scan ====> {}".format(getCurrentTime()))
		scanNetwork()
		print("[+] Hosts found ===> {} ".format(len(hostList)))

		for host in hostList:
			print("(*) Name -> {} MAC -> {} IPv4 -> {} Vendor -> {} ".format(host[0],host[1],host[2],host[3]))
		
		hostCountOld = hostCountNew
		hostCountNew = len(hostList)
		
		if (hostCountNew > hostCountOld):
			print("[A] Alerting owner new host connected".format(hostList[0]))
			time.sleep(10)
		time.sleep(300)


if __name__ == '__main__':
	main()
	bot.run(discordBotAPIKey)