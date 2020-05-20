import subprocess

# Instala os pacotes necessários
def installPack():
	subprocess.call("yum install nfs-utils -y", shell=True)
	

def makeShare(path, ):
