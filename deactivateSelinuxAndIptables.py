import subprocess

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