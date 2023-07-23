
# Import Libraries
import cv2
import time
import mediapipe as mp
import numpy as np

import getopt
import sys

import uuid


import os.path
def main(VideoFileName, DestinationPath):



	# (0) in VideoCapture is used to connect to your computer's default camera
	capture = cv2.VideoCapture(VideoFileName)

	# Initializing current time and precious time for calculating the FPS
	previousTime = 0
	currentTime = 0

	while capture.isOpened():
		# capture frame by frame
		ret, frame = capture.read()
		if ret == False:
			break
		# resizing the frame for better view
		frame = cv2.resize(frame, (800, 600))

		rgba = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

		cv2.imwrite("{}/{}.png".format(DestinationPath,uuid.uuid4()), rgba)
		
		cv2.imshow("iamge", rgba)
		
		# Enter key 'q' to break the loop
		if cv2.waitKey(5) & 0xFF == ord('q'):
			break


	# When all the process is done
	# Release the capture and destroy all windows
	capture.release()
	cv2.destroyAllWindows()


# Get the arguments from the command-line except the filename
argv = sys.argv[1:]


try:
	# Define the getopt parameters
	opts, args = getopt.getopt(argv, 'f:d:', ['file','destination'])
	
	# Check if the options' length is 2 (can be enhanced)
	if len(opts) == 0 or len(opts) > 3:
		print ('usage: add.py -f <file name>')
	else:
		if os.path.isfile("{}/{}".format(opts[1][1],opts[0][1])) and os.path.isdir(opts[1][1]):
			print("will try to process file: {} to the destination:{}".format(opts[0][1], opts[1][1]))
			
			main("{}/{}".format(opts[1][1],opts[0][1]), opts[1][1])
		else:
			print("file not fount")
		
		

except getopt.GetoptError:
	# Print something useful
	print ('usage: add.py -a <first_operand> -b <second_operand>')
	sys.exit(2)	