from datetime import datetime
from datetime import date
import nmap
import sys
import platform
import time
import csv
import asyncio
import discord
from discord.ext.commands import CommandNotFound
from discord.ext import commands
from discord.ext.commands import Cog,Context
from threading import Timer

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




@bot.command()
async def displayUnkownDevices(ctx):
	#will display all Uknown Devices which the discord user will name them 
	print("Nothing")

@bot.command()
async def displayKnownDevices(ctx):
	#will display connected devices and log last connections
	print("Nothing")


def fillUknownMACAddress(uknownHost):
	timeout = 30
	t = Timer(timeout,print,['[+] Time\'s up to fill the name about of this addresses'])
	print("You have {} seconds to fill the name of this MAC address".format(timeout))
	t.start()
	toName = input()
	t.cancel()
	if toName is not None:
		uknownHost[0] = toName
		writeCommonMACAddress(uknownHost)
		# now its a known host
		return uknownHost


def getCurrentTime():
	now = datetime.now()
	return now.strftime("%H:%M:%S")
	
## Needs fix
def writeCommonMACAddress(registry):
	with open('mac_addresses.csv', 'a+',newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(registry)


def replaceCommonMACAddresses(hostList):

	with open('mac_addresses.csv','r') as csvfile:
		reader = csv.reader(csvfile,skipinitialspace=True)

		for row in reader:
		
			for host in hostList:
			
				if (host[1] == row[0]):
					host[0] = row[1]
	return hostList


def scanNetwork(hostList):
	nmp.scan(hosts='192.168.1.0/24',arguments='-script smb-os-discovery.nse -T5 192.168.1.0/24')
	i = 0
	for host in nmp.all_hosts():
		try:
			name = nmp[host].get('hostnames')[0].get('name')
			mac_adress = nmp[host].get('addresses').get('mac')
			localIPv4 = nmp[host].get('addresses').get('ipv4')
			vendor = nmp[host].get('vendor').get(mac_adress)
			hostList.append([name,mac_adress,localIPv4,vendor])
			i += 1
		except:
			vendor = mac_adress = localIPv4 = 'unknown'	

	return replaceCommonMACAddresses(hostList)
	
def keepLogs(logs):
	
	if platform.system() == 'Linux' or platform.system() == 'Darwin':

		with open("./logs/"date.today().strftime("%d_%m_%y") + ".log","a+") as logfile:
			logfile.write(logs)
			logfile.close()
	else if platform.system() == 'Windows':

		with open(".\\logs\\"date.today().strftime("%d_%m_%y") + ".txt","a+") as logfile:
			logfile.write(logs)
			logfile.close()

def alert():
	print("Alert")



def main():
	hostList = []
	hostCountNew = 0
	hostCountOld = 0
	logs = ""
	while True:

		print("[+] Performing a NMAP scan ====> {}".format(getCurrentTime()))
		logs += "[+] Performing a NMAP scan ====> {}\n".format(getCurrentTime())
		hostList = scanNetwork(hostList)
		for host in hostList:
			if host[0] == "":
				replIndex = hostList.index(host)
				hostList[replIndex] = fillUknownMACAddress(host)


		print("[+] Hosts found ===> {} ".format(len(hostList)))
		logs += "[+] Hosts found ===> {} \n".format(len(hostList))

		for host in hostList:
			if (host[0] != ""):
				print("		:+: Name -> {} MAC -> {} IPv4 -> {} Vendor -> {} ".format(host[0],host[1],host[2],host[3]))
				logs += "         :+: Name -> {} MAC -> {} IPv4 -> {} Vendor -> {} \n".format(host[0],host[1],host[2],host[3])
			else:
				print("		:+: Name -> [UNKNOWN] MAC -> {} IPv4 -> {} Vendor -> {} ".format(host[0],host[1],host[2],host[3]))
				logs += "         :+: Name -> [UNKNOWN] MAC -> {} IPv4 -> {} Vendor -> {} \n".format(host[0],host[1],host[2],host[3])
		
		hostCountOld = hostCountNew
		hostCountNew = len(hostList)
		
		if (hostCountNew > hostCountOld):
			print("[ALERT] Alerting owner new host connected")
			logs += "[ALERT] Alerting owner new host connected\n"
			time.sleep(1)

		keepLogs(logs)
		time.sleep(300)
		hostList.clear()

if __name__ == '__main__':
	main()
	#bot.run(discordBotAPIKey)
