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