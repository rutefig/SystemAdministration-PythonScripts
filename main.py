import sys
import nfs

samba_menu = '''
What do you want to do in your SAMBA Configuration?
1. Install packages only
'''


nfs_menu = '''
What do you want to do in your NFS Configuration?
1. Install packages only
2. Add shared directory
3. Delete shared directory
4. Stop sharing all directories
5. Start/Restart NFS service
10. Go Back
'''
def nfs_option1():
	nfs_option1 = "Do you want to only install nfs package? Say yes or no\n"
	nfs_confirmation = raw_input(nfs_option1)
	if nfs_confirmation == "yes":
		nfs.installPack()
	elif nfs_confirmation == "no":
		break
	else:
		print("Please enter something rigth")
		continue

def nfs_option2():
	print("You want to add a new shared directory, please enter the needed information")
	path = raw_input("Directory path: ")
	ip = raw_input("Subnet IP: ")
	netmaskBits = raw_input("Subnet mask bits: ")
	isNotWritten = raw_input("Is read only? yes or no: ")
	if isNotWritten == "yes":
		nfs.makeShare(path, ip, netmaskBits, False)
	else:
		nfs.makeShare(path, ip, netmaskBits, True)

def nfs_option3():
	nfs_confirmation = raw_input("Do you really want to delete a share? yes or no: ")
	if nfs_confirmation == "yes":
		print("Please enter the path and ip from the shared you want to delete")
		path = raw_input("Directory path: ")
		ip = raw_input("Subnet IP: ")
		nfs.deleteShare(path, ip)
	elif nfs_confirmation == "no":
		break
	else:
		print("Please enter something rigth")
		continue

def nfs_option4():
	nfs_confirmation = raw_input("Do you really want to stop ALL shares? yes or no: ")
	if nfs_confirmation == "yes":
		print("Stoping all shares")
		nfs.stopShares()
		print("NFS SERVICE WAS STOPPED AND TURNED OFF!")
	elif nfs_confirmation == "no":
		break
	else:
		print("Please enter something rigth")
		continue

def nfs_option5():
	nfs_confirmation = raw_input("Do you really want to start/restart ALL shares? yes or no: ")
	if nfs_confirmation == "yes":
		nfs.stopShares()
		print("NFS SERVICE WAS RESTARTED!")
	elif nfs_confirmation == "no":
		break
	else:
		print("Please enter something rigth")
		continue

dns_menu = '''
What do you want to do in your DNS Configuration?
1. Install packages only
2. Set up this machine as a DNS Server (includes package instalation)
3. Create master forward zone
4. Add A record type to a forward zone
5. Add MX record type to a forward zone
6. Create master reverse zone 
10. Go Back
'''

def dns_option1():
	nfs_option1 = "Do you want to only install dns package? Say yes or no\n"
	nfs_confirmation = raw_input(nfs_option1)
	if nfs_confirmation == "yes":
		nfs.installPack()
	elif nfs_confirmation == "no":
		break
	else:
		print("Please enter something rigth")
		continue

http_menu = '''
What do you want to do in your HTTP Configuration?
1. Install packages only
2. Create a Virtual Host
3. Delete a Virtual Host
'''
http_option1 = "Do you want to only install http package? Say yes or no\n"

main_menu = '''
What type of service do you want to configure?
Type the number associated with the service you want and then type "Enter".
The associations are defined below:
1. NFS Server Configuration
2. DNS Server Configuration
3. HTTP Server Configuration
4. SAMBA Server Configuration
10. Exit
'''
while(True):
	user_choice = raw_input(main_menu)

	if user_choice == "1":
		nfs_choice = raw_input(nfs_menu)
		if nfs_choice == "1":
			nfs_option1()
		elif nfs_choice == "2":
			nfs_option2()
		elif nfs_choice == "3":
			nfs_option3()
		elif nfs_choice == "4":
			nfs_option4()
		elif nfs_option5 == "5":
			nfs_option5()
		else:
			print("Going BACK")
			pass
	elif user_choice == "2":
		user_choice = raw_input(dns_menu)
	elif user_choice == "3":
		user_choice = raw_input(http_menu)
	elif user_choice == "4":
		user_choice = raw_input(samba_menu)
	elif user_choice == "10":
		sys.exit()
	else:
		print("You must choose a valid number")

