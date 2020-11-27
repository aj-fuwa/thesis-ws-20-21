'''
# Aim: To measure the area of the laser for FLC
# Name: laser_code_v1.py
# Language: Python
# Date: 5.November 2020
# Src: https://docs.opencv.org/3.4/d3/d05/tutorial_py_table_of_contents_contours.html
'''

import numpy as np
import cv2 as cv2

# open webcam
cap = cv2.VideoCapture(1)

while(1):

    # read the captured frame
    ret, frame = cap.read()
    if (ret == False):
        print("ERROR: Return value from cap.read() not correct. Exiting the code...")

    # convert the frame from BGR to Gray
    f2gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold apply
    f_nach_canny = cv2.Canny(f2gray, 30, 200)

    # Find contours in the video frame
    contours, hierarchy = cv2.findContours(f_nach_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Store the main contour
    haupt_contour = contours[0]

    # Calculate the area of the main contour and display it
    area_haupt_contour = cv2.contourArea(haupt_contour)
    print("INFO: Area of the main contour is: ", area_haupt_contour)
    # TODO: Add categories of the area for FLC classification into Good, Bad, etc.

    # Draw the main contour on the frame and display it
    cv2.drawContours(frame, [haupt_contour], 0, (0, 255, 0), 3)
    cv2.imshow("Main Window", frame)

    # exit condition --quit
    if (cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q')):
        print("INFO: Quit key pressed. Quitting the code...")
        break

# close routine --quit
cap.release()
cv2.destroyAllWindows()
print("INFO: Program closed")
