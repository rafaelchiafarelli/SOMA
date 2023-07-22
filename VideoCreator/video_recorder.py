
# Import Libraries
import cv2
import time

import uuid

uuid_for_file = uuid.uuid4()

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

out = cv2.VideoWriter("./{}{}.avi".format(uuid_for_file,"_video"), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (width, height))
print("./{}{}.avi".format(uuid_for_file,"_video"))
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
			uuid_for_file = uuid.uuid4()
			out = cv2.VideoWriter("./{}{}.avi".format(uuid_for_file,"_video"), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (width, height))
			print("./{}{}.avi".format(uuid_for_file,"_video"))
		elif recording == "paused":
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
