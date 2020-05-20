



nfs_menu = '''
What do you want to do in your NFS Configuration?
1. Install packages only
2. Add shared directory
3. Delete shared directory
10. Go Back
'''

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

http_menu = '''
What do you want to do in your HTTP Configuration?
'''

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

user_choice = raw_input(main_menu)

if user_choice == "1":
	print("You chose NFS Server Configuration")
elif user_choice == "2":
	print("You chose DNS Server Configuration")
elif user_choice == "3":
	print("You chose HTTP Server Configuration")
elif user_choice == "4":
	print("You chose SAMBA Server Configuration")
else:
	print("You must choose a valid number")
