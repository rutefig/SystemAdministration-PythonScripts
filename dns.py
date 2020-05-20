import subprocess
import os.path
import utilities

# Instala os pacotes necessários
def installPack():
	if utilities.isServiceInstalled(named):
		return False
	subprocess.call("yum install bind* -y", shell=True)
	subprocess.call("yum install jwhois -y", shell=True)
	return True


def createForwZone(domain, ip):
	# Defines a string with zone to append DNS configuration file
	hostsFilePath = '/var/named/{domain}.hosts'.format(domain=domain)
	zone = '''zone "{domain}" IN {
		type master;
		file "{hostsFilePath}";
	};'''.format(domain=domain, hostsFilePath=hostsFilePath)
	dnsFile = open("/etc/named.conf", "a+")
	dnsFile.write(zone)
	dnsFile.close()

	# Creates the host file
	hostsFile = open(hostsFilePath, "w")
	data = '''
	$ttl 38400
	@	IN	SOA	server.estig.pt. mail.as.com. (
			1165190726 ;serial
			10800 ;refresh
			3600 ; retry
			604800 ; expire
			38400 ; minimum
			)
		IN	NS		dns.estig.pt.
	@	IN	A	{ip}
	www	IN	A	{ip}		
	'''.format(ip=ip)
	hostsFile.write(data)
	hostsFile.close()

	# restart DNS service
	subprocess.call("/etc/init.d/named restart", shell=True)

# Adiciona registo tipo A a um determinado dominio
def addARecord(name, domain, ip):
	hostsFilePath = '/var/named/{domain}.hosts'.format(domain=domain)
	if not os.path.isfile(hostsFilePath):
		return false
	hostsFile = open(hostsFilePath, "a+")
	record = "{name}	IN	A	{ip}".format(name=name, ip=ip)
	hostsFile.write(record)
	hostsFile.close()

# Adiciona registo tipo MX a um determinado dominio
def addMXRecord(name, priority, domain):
	hostsFilePath = '/var/named/{domain}.hosts'.format(domain=domain)
	if not os.path.isfile(hostsFilePath):
		return false
	hostsFile = open(hostsFilePath, "a+")
	record = "@	IN 	MX 	{priority}	{name}.".format(priority=priority, name=name)
	hostsFile.write(record)
	hostsFile.close()


def createReverZone(ipClass):
	


# Editar o ficheiro do DNS para que o servidor fique à escuta de todos
# /etc/named.conf
def setToListenAll():
	dnsFile = open("/etc/named.conf", "rt")
	data = dnsFile.read()
	data = data.replace('listen-on port 53 { 127.0.0.1; };', 'listen-on port 53 {127.0.0.1; any; };')
	data = data.replace('{ localhost; };', '{ localhost; any; };')
	dnsFile.close()
	dnsFile = open("/etc/named.conf", "wt")
	dnsFile.write(data)
	dnsFile.close()
