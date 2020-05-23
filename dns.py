import subprocess
import os
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

def deleteForwZone(domain):
	hostsFilePath = '/var/named/{domain}.hosts'.format(domain=domain)
	zone = '''zone "{domain}" IN {
		type master;
		file "{hostsFilePath}";
	};'''.format(domain=domain, hostsFilePath=hostsFilePath)
	# Apaga o ficheiro dos hosts
	os.remove(hostsFilePath)
	# Retira a zona do ficheiro de configuração de DNS
	dnsFile = open("/etc/named.conf", "rt")
	data = dnsFile.read()
	data.replace(zone, "")
	dnsFile.close()
	dnsFile = open("/etc/named.conf", "wt")
	dnsFile.write(data)
	dnsFile.close()



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


def createReverZone(ip, name):
	ipBitsList = ip.split('.')
	reverseIPClass = "{}.{}.{}.".format(ipBitsList[2], ipBitsList[1], ipBitsList[0])

	# Defines a string with zone to append DNS configuration file
	hostsFilePath = '/var/named/{reverseIPClass}in-addr.arpa.hosts'.format(reverseIPClass=reverseIPClass)
	# se o ficheiro já existir significa que já existe a zona criada
	# fazer possível atualização
	if os.path.isfile(hostsFilePath):
		return False

	zone = '''zone "{reverseIPClass}in-addr.arpa" IN {
		type master;
		file "{hostsFilePath}";
	};'''.format(reverseIPClass=reverseIPClass, hostsFilePath=hostsFilePath)
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
	{lastBits}	IN	PTR	{name}.		
	'''.format(lastBits=reverseIPClass[3], name=name)
	hostsFile.write(data)
	hostsFile.close()

	# restart DNS service
	subprocess.call("/etc/init.d/named restart", shell=True)

def deleteReverZone(ip, name):
	ipBitsList = ip.split('.')
	reverseIPClass = "{}.{}.{}.".format(ipBitsList[2], ipBitsList[1], ipBitsList[0])

	hostsFilePath = '/var/named/{reverseIPClass}in-addr.arpa.hosts'.format(reverseIPClass=reverseIPClass)
	zone = '''zone "{reverseIPClass}in-addr.arpa" IN {
		type master;
		file "{hostsFilePath}";
	};'''.format(reverseIPClass=reverseIPClass, hostsFilePath=hostsFilePath)
	# Apaga o ficheiro dos hosts
	os.remove(hostsFilePath)
	# Retira a zona do ficheiro de configuração de DNS
	dnsFile = open("/etc/named.conf", "rt")
	data = dnsFile.read()
	data.replace(zone, "")
	dnsFile.close()
	dnsFile = open("/etc/named.conf", "wt")
	dnsFile.write(data)
	dnsFile.close()


