import os.path
import subprocess
import pwd

# Cria um utilizador com o nome e password se não existir e devolve true
# Devolve false se já existir esse utilizador
def addUser(name):
	try:
		pwd.getpwnam(name)
	except KeyError:
		subprocess.call(["useradd", name])
		subprocess.call(["passwd", name])
		return True
	else:
		return False


# Desativa SELINUX e Iptables
def disableFirewall():
	# Change SELINUX=enforcing to SELINUX=disabled in /etc/selinux/config file
	selinuxFile = open("/etc/selinux/config", "rt")
	data = selinuxFile.read()
	data = data.replace('SELINUX=enforcing', 'SELINUX=disabled')
	selinuxFile.close()
	selinuxFile = open("/etc/selinux/config", "wt")
	selinuxFile.write(data)
	selinuxFile.close()

	# turn off iptables
	subprocess.call(["chkconfig", "iptables", "off"])

	# ask to reboot system
	subprocess.call("reboot")

# Devolve true se o serviço estiver instalado no sistema e false c.c.
def isServiceInstalled(service):
	servicePath = "/etc/init.d/{service}".format(service=service)
	return os.path.isfile(servicePath)

def makeBackup(path, filename):
	command = "tar -cf /storagebackups/{filename}.tgz {path}"
	subprocess.call(command, shell=True)

def makeCriticalBackup():
	# cria o ficheiro de backup das configurações com o ficheiro da placa de rede
	subprocess.call("tar -cf /storagebackups/configurationsbackups.tgz /etc/sysconfig/network-scripts/ifcfg-eth0", shell=True)
	# adiciona ao ficheiro os ficheiros de configuração do samba
	subprocess.call("tar -rvf /storagebackups/configurationsbackups.tgz /etc/samba/smb.conf", shell=True)
	# adiciona o ficheiro de configuração do nfs ao backup das configurações
	subprocess.call("tar -rvf /storagebackups/configurationsbackups.tgz /etc/exports", shell=True)
	# adiciona o ficheiro de configuração do dns ao backup das configurações
	subprocess.call("tar -rvf /storagebackups/configurationsbackups.tgz /etc/named.conf", shell=True)
	# adiciona o ficheiro de configuração do http ao backup das configurações
	subprocess.call("tar -rvf /storagebackups/configurationsbackups.tgz /etc/httpd/conf/httpd.conf", shell=True)
	# cria o ficheiro de backup dos ficheiros das zonas configuradas no dns
	subprocess.call("tar -cf /storagebackups/hostsbackups.tgz /var/named/", shell=True)
	# cria o ficheiro de backup da pasta que contém os ficheiros dos vários domínios dos virtual hosts
	subprocess.call("tar -cf /storagebackups/domainsbackups.tgz /domains/", shell=True)
 

def createRaid(directoryPath):
	# cria um raid 1 + 1 hotspare, por definição com os discos sdb sdc e o sdd como hotspare
	subprocess.call("mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc --spare-devices=1 /dev/sdd", shell=True)
	# cria o sistema de ficheiros, por definição xfs e monta na diretoria mencionada
	subprocess.call(["mkfs.xfs", "/dev/md0"])
	if not os.path.exists(directoryPath):
		os.mkdir(directoryPath)
	subprocess.call(["mount", "/dev/md0", directoryPath])