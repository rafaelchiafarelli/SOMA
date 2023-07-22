
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

	# Grabbing the Holistic Model from Mediapipe and
	# Initializing the Model
	mp_holistic = mp.solutions.holistic
	holistic_model = mp_holistic.Holistic(
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5
	)

	# Initializing the drawing utils for drawing the facial landmarks on image
	mp_drawing = mp.solutions.drawing_utils

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

		# Converting the from BGR to RGB
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# Making predictions using holistic model
		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		results = holistic_model.process(image)
		image.flags.writeable = True

		# Converting back the RGB image to BGR
		d_image =  np.zeros((800,600,3),dtype=np.uint8) #cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		# Drawing the Facial Landmarks
		mp_drawing.draw_landmarks(
			d_image,
			results.face_landmarks,
			mp_holistic.FACEMESH_TESSELATION,
		0,
			mp_drawing.DrawingSpec(
				color=(255,0,0),
				thickness=1,
				circle_radius=0
			)
		)
		mp_drawing.draw_landmarks(
			d_image,
			results.face_landmarks,
			mp_holistic.FACEMESH_LEFT_IRIS,
		0,
			mp_drawing.DrawingSpec(
				color=(255,0,0),
				thickness=1,
				circle_radius=0
			)
		)
		mp_drawing.draw_landmarks(
			d_image,
			results.face_landmarks,
			mp_holistic.FACEMESH_RIGHT_IRIS,
		0,
			mp_drawing.DrawingSpec(
				color=(255,0,0),
				thickness=1,
				circle_radius=0
			)
		)	
		# Drawing Right hand Land Marks
		mp_drawing.draw_landmarks(
		d_image,
		results.right_hand_landmarks,
		mp_holistic.HAND_CONNECTIONS
		)

		# Drawing Left hand Land Marks
		mp_drawing.draw_landmarks(
		d_image,
		results.left_hand_landmarks,
		mp_holistic.HAND_CONNECTIONS
		)
		
		# Calculating the FPS
		currentTime = time.time()
		fps = 1 / (currentTime-previousTime)
		previousTime = currentTime
		
		# Displaying FPS on the image
		#cv2.putText(image, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

		# Display the resulting image
		
		rgba = cv2.cvtColor(d_image, cv2.COLOR_RGB2RGBA)


		# Color to make transparent
		col = (0, 0, 0)

		# Color tolerance
		tol = (1, 1, 1)

		# Temporary array (subtract color)
		temp = np.subtract(d_image, col)

		# Tolerance mask
		mask = (np.abs(temp) <= tol)
		mask = (mask[:, :, 0] & mask[:, :, 1] & mask[:, :, 2])

		# Generate alpha channel
		temp[temp < 0] = 0                                            # Remove negative values
		alpha = (temp[:, :, 0] + temp[:, :, 1] + temp[:, :, 2]) / 3   # Generate mean gradient over all channels
		alpha[mask] = alpha[mask] / np.max(alpha[mask]) * 255         # Gradual transparency within tolerance mask
		alpha[~mask] = 255                                            # No transparency outside tolerance mask

		# Set alpha channel in output
		rgba[:, :, 3] = alpha


		cv2.imwrite("{}/{}.png".format(DestinationPath,uuid.uuid4()), rgba)
		
		cv2.imshow("Facial and Hand Landmarks", rgba)
		
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
		if os.path.isfile(opts[0][1]) and os.path.isdir(opts[1][1]):
			print("will try to process file: {} to the destination:{}".format(opts[0][1], opts[1][1]))
			
			main(opts[0][1], opts[1][1])
		else:
			print("file not fount")
		
		

except getopt.GetoptError:
	# Print something useful
	print ('usage: add.py -a <first_operand> -b <second_operand>')
	sys.exit(2)	