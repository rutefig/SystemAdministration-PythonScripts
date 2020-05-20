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
	share = "{path} {ip}/{netmaskBits}(ro,nohide)".format(path=path, ip=ip, netmaskBits=netmaskBits)
	if isWritten:
		share = "{path} {ip}/{netmaskBits}(rw,nohide,sync)".format(path=path, ip=ip, netmaskBits=netmaskBits)
	
	exportsFile = open("/etc/exports", a+)
	exportsFile.write(share)
	exportsFile.close()

def deleteShare(path, ip):
