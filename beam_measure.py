'''
# Name: beam_measure.py
# Task: Measuring the beam width and sending the data to the FLC
# Date: (Revised) 31.Jan 2021
# Src:  https://en.wikipedia.org/wiki/Beam_diameter#:~:text=The%20width%20of%20laser%20beams,using%20a%20laser%20beam%20profiler.
        https://docs.opencv.org/3.4/d3/d05/tutorial_py_table_of_contents_contours.html
        https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
        https://stackoverflow.com/questions/52761354/calculate-multiple-areas-with-opencv/52762658#52762658
'''
import cv2 as cv2
import numpy as np
from base_ip_class import CameraFunctions

cam = CameraFunctions()

class BeamMeasure():
    # set the HSV values for the laser beam
    lower = np.array([86, 114, 98])  # for laser beam -- set it in the lab
    upper = np.array([255, 255, 255])  # for laser beam

    def __init__(self):
        print("INFO: BeamMeasure class called...")

    def run_beam_measure(self):
        cam.set_hsv_values(lower_val=self.lower, upper_val=self.upper)

        cap = cv2.VideoCapture(0)
        print("INFO: Camera 1 ON...")

        while(True):
            ret, frame_og = cap.read()
            ret_contours, ret_hierarchy, frame = cam.get_contours(frame=frame_og)
            contour_area, contour_count = cam.show_contour_area(ret_contours, frame)

            # Draw a rectangle around the Beam Width and display Beam Area
            x, y, w, h = cv2.boundingRect(contour_count)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Box Area=' + str(contour_area), (60, 90), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            # Display the frame
            cv2.imshow("Beam Width Window", frame)

            # Press B to stop Beam Measuring
            q = cv2.waitKey(1)
            if (q == ord ('b')) or (q == ord ('B')):
                print("ALERT: B key pressed. Stopping running of Beam Measure...")
                break
        # Exit procedure
        cap.release()
        cv2.destroyAllWindows()
        print("ALERT: Beam Measure stopped running. Exiting now...")
        print("INFO: Camera 1 OFF...")




