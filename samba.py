import subprocess
import utilities

# Instala os pacotes necessários se o serviço não estiver instalado
# Devolve True se instalar os pacotes, False se não tiver instalado porque já estava instalado
def installPack():
	if utilities.isServiceInstalled("smb"):
		return False
	subprocess.call("yum install samba4* -y", shell=True)
	return True

def restartServices():
	subprocess.call("/etc/init.d/smb restart", shell=True)
	subprocess.call("/etc/init.d/nmb restart", shell=True)
	subprocess.call("/etc/init.d/winbind restart", shell=True)

def addUserSamba(name):
	utilities.addUser(name)
	subprocess.call(["smbpasswd", "-a", name])


# falta confirmar que o path existe
def makeShare(name, path, isWriteable=False, isPublic=True):
	writeableOrReadOnly = "read only = yes"
	if isWriteable:
		writeableOrReadOnly = "writeable = yes"
	share = '''
	[{name}]
		path = {path}
		browseable = yes
		public = {public}
		{writeableOrReadOnly} 
	'''
	sambaFile = open("/etc/samba/smb.conf", "a+")
	sambaFile.write(share)
	sambaFile.close()