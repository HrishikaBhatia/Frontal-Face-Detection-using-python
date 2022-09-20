#importing OpenCV library
import cv2 , time

import pandas as pd

#importing datetime library
from datetime import datetime

#triggering the video
video = cv2.VideoCapture(0 , cv2.CAP_DSHOW)

first_frame = None
status_list = [None,None] #To record the status after each frame
times = [] #To record the time of enter and exit of the obj

df = pd.DataFrame(columns = ["Enter Time" , "Exit Time "])

while True:
	
	check , frame = video.read() #Storing the boolean value of the frame and the array in two separate variables
	gray_img = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY) #Converting the colored frame into the gray one
	gray_img = cv2.GaussianBlur(gray_img , (21,21) , 0) #Converting the gray frame into a gaussian blurr image

	status = 0

	if first_frame is None:
		first_frame = gray_img
		continue

	delta_frame = cv2.absdiff(first_frame , gray_img) #Creating a delta frame from the static first frame and the current frame

	thresh_frame = cv2.threshold(delta_frame , 30 , 255 , cv2.THRESH_BINARY)[1] #Creating a threshold frame and taking its second value 
	thresh_frame = cv2.dilate(thresh_frame , None , iterations = 2) #Dilating the threshold frame
	(cnts,_) = cv2.findContours(thresh_frame.copy() , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finding the contours from the threshold frame and storing in a tuple

	for contour in cnts:
		if cv2.contourArea(contour) < 1000: 
			continue
		else:
			status = 1
			(x,y,w,h) = cv2.boundingRect(contour) #Storing the coordinates of the contour
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255) ,3) #Drawing a rectangle around that contour

	status_list.append(status)
	if status_list[-1]==1 and status_list[-2]==0:
		times.append(datetime.now())
	if status_list[-1]==0 and status_list[-2]==1:
		times.append(datetime.now())

	cv2.imshow("Capturing image" , gray_img)
	cv2.imshow("delta_frame" , delta_frame)
	cv2.imshow("thresh_frame" , thresh_frame)
	cv2.imshow("color_frame" , frame)

	key = cv2.waitKey(1)
	if key == ord('q'):
		if status==1:
			times.append(datetime.now())
		break

print(status_list)
print(times)

for i in range(0,len(times),2):
	df.append({"Enter Time":times[i] , "Exit Time" : times[i+1]} , ignore_index = True)

df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()