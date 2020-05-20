import subprocess
import os, sys
import os.path
import dns

# Instala os pacotes necessários
def installPack():
	subprocess.call("yum install httpd -y", shell=True)

def makeVirtualHost(domain, ip, port):
	# Verifica a existencia do ficheiro dos hosts da zona forward e se não existir cria essa zona
	hostsFilePath = '/var/named/{domain}.hosts'.format(domain=domain)
	if not os.path.isfile(hostsFilePath):
		dns.createForwZone(domain, ip)

	# Acrescentar no ficheiro de configuração do Apache a configuração do Virtual Host
	httpFilePath = '/etc/httpd/conf/httpd.conf'
	httpFile = open(httpFilePath, "a+")
	directoryPath = '/domains/{domain}'.format(domain=domain)
	data = '''
	NameVirtualHost {ip}:{port}
	<VirtualHost {ip}:{port}>
	DocumentRoot "{directoryPath}/"
	ServerName www.{domain}
	ServerAlias {domain}
	<Directory "{directoryPath}">
		Options Indexes FollowSymLinks
		AllowOverride All
		Order allow,deny
		Allow from all
	</Directory>
	</VirtualHost>		
	'''.format(ip=ip, port=port, directoryPath=directoryPath, domain=domain)
	httpFile.write(data)
	httpFile.close()

	# Cria os directorios
	os.mkdir('/domains', 0755)
	os.mkdir(directoryPath, 0755)

	# Cria o ficheiro "index.html"
	index = open("{directoryPath}/index.html".format(directoryPath=directoryPath, "w")
	indexData = '''
	<h1>Bem Vindo</h1>
	<h2>{domain}</h2>
	'''.format(domain=domain)
	index.write(indexData)
	index.close()
