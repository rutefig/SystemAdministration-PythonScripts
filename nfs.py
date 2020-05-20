import subprocess
import utilities

# Instala os pacotes necessários se o serviço não estiver instalado
# Devolve True se instalar os pacotes, False se não tiver instalado porque já estava instalado
def installPack():
	if utilities.isServiceInstalled("nfs"):
		return False
	subprocess.call("yum install nfs-utils -y", shell=True)
	return True
	

def makeShare(path, ip, netmaskBits, isWritten):
	installPack()
	share = "{path} {ip}/{netmaskBits}(ro,nohide)".format(path=path, ip=ip, netmaskBits=netmaskBits)
	if isWritten:
		share = "{path} {ip}/{netmaskBits}(rw,nohide,sync)".format(path=path, ip=ip, netmaskBits=netmaskBits)
	
	exportsFile = open("/etc/exports", "a+")
	exportsFile.write(share)
	exportsFile.close()
	subprocess.call("/etc/init.d/nfs restart", shell=True)
	subprocess.call(["chkconfig", "nfs", "on"])
	

def deleteShare(path, ip):
	share = "{path} {ip}".format(path=path, ip=ip)
	exportsFile = open("/etc/exports", "rt")
	line_list = exportsFile.readlines()
	data = ''''''
	for line in line_list:
		if line.find(share) == -1:
			data = data + line
	exportsFile.close()
	exportsFile = open("/etc/exports", "wt")
	exportsFile.write(data)
	exportsFile.close()

def stopShares():
	subprocess.call("/etc/init.d/nfs stop", shell=True)
	subprocess.call(["chkconfig", "nfs", "off"])