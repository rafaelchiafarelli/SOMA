"""this file is to push data into the devices"""

import getopt
import sys
import paramiko
import glob
import os

def main(IPAddress, OriginPath,DestinationPath):

    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=IPAddress,username="controlroom",password="controlroom")


    ftp_client=ssh_client.open_sftp()
    path = r"{}/*.png".format(OriginPath)
    files = glob.glob(path)
    for file in files:
        print(file)
        destination = os.path.basename(file)
        ftp_client.put(file,"{}/{}".format(DestinationPath,destination))
    ftp_client.close()


# Get the arguments from the command-line except the filename
argv = sys.argv[1:]


try:
	# Define the getopt parameters
	opts, args = getopt.getopt(argv, 'o:d:i:', ['origin','destination','ip'])
	
	# Check if the options' length is 2 (can be enhanced)
    
	if len(opts) == 0 or len(opts) < 3:
		print ('usage: add.py -o <origin> -d <destintion> -i <IP_destination>')
	else:
		if os.path.isdir(opts[0][1]):	
			main(opts[2][1],opts[0][1], opts[1][1])
		else:
			print("file not fount")
		
		

except getopt.GetoptError:
	# Print something useful
	print ('ERROR usage: add.py  -o <origin> -d <destintion> -i <IP_destination>')
	sys.exit(2)	