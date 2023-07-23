
# Import Libraries
import cv2
import getopt
import sys

import uuid

import os.path
import os, shutil
import requests

def main(VideoFileName, DestinationPath):

	uuid_for_file = VideoFileName

	# (0) in VideoCapture is used to connect to your computer's default camera
	capture = cv2.VideoCapture(0)

	# Initializing current time and precious time for calculating the FPS
	previousTime = 0
	currentTime = 0
	recording_state = {"paused", "recording", "saved"}
	recording = "paused"
	ret, frame = capture.read()
	height = frame.shape[0]
	width = frame.shape[1]

	even_odd = False
	even_odd_count = 0
	while capture.isOpened():
		
		# capture frame by frame
		ret, frame = capture.read()
		#frame = cv2.cvtColor(frame, cv2.COLOR_2RGB)
		# resizing the frame for better view
		v_frame = cv2.resize(frame, (800, 600))
		even_odd_count+=1
		if even_odd_count >= 15:
			if even_odd == True:
				even_odd = False
			else:
				even_odd = True
			
			
			even_odd_count = 0

		# Display the resulting image
		if recording == "recording":
			if even_odd == True:
				cv2.circle(v_frame,(675,100), 50, (0,0,255), -1)
				
		elif recording == "paused":
			if even_odd == True:
				cv2.rectangle(v_frame, pt1=(600,50), pt2=(650,150), color=(0,0,0), thickness=-1)	
				cv2.rectangle(v_frame, pt1=(700,50), pt2=(750,150), color=(0,0,0), thickness=-1)	

			
		cv2.imshow("frame", v_frame)

		# Enter key 'q' to break the loop
		key = cv2.waitKey(5)
		if key & 0xFF == ord(' '):
			if recording == "recording":
				recording = "paused"
				out.release()

			elif recording == "paused":
				
				out = cv2.VideoWriter("{}/{}".format(DestinationPath,uuid_for_file), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (width, height))
								
				recording = "recording"

		if key & 0xFF == ord('q'):
			#pause record and stop
			out.release()
			break

		if recording == "recording":
			
			out.write(frame)


	# When all the process is done
	# Release the capture and destroy all windows
	capture.release()
	cv2.destroyAllWindows()
	tell_server(uuid_for_file, DestinationPath)


def tell_server(uuid_for_file, DestinationPath):
	url = 'http://localhost:5000/update_video'
	myobj = {'Folder': DestinationPath, 'FileName': str(uuid_for_file), 'cur_state':"recorded"}
	x = requests.post(url, json = myobj)
	return

# Get the arguments from the command-line except the filename
argv = sys.argv[1:]

try:
	# Define the getopt parameters
	opts, args = getopt.getopt(argv, 'f:d:', ['file','destination'])
	
	# Check if the options' length is 2 (can be enhanced)
	print(opts)
	if len(opts) == 0 or len(opts) > 3:
		print ('usage: add.py -f <file name> -d <destination>')
	else:
		if os.path.isdir(opts[1][1]):
			for filename in os.listdir(opts[1][1]):
				file_path = os.path.join(opts[1][1], filename)
				try:
					if os.path.isfile(file_path) or os.path.islink(file_path):
						os.unlink(file_path)
					elif os.path.isdir(file_path):
						shutil.rmtree(file_path)			
				except Exception as e:
					print('Failed to delete %s. Reason: %s' % (file_path, e))						
			print("will try to process file: {} to the destination:{}".format(opts[0][1], opts[1][1]))
			
			main(opts[0][1], opts[1][1])
		else:
			print("file not fount")
		
		

except getopt.GetoptError:
	# Print something useful
	print ('usage: add.py -f <file name> -d <destination>')
	sys.exit(2)	