'''
# Name: distance_measurement.py
# Task: Defining the class where the distance of the camera is measured
# Date: (Revised) 1.Feb 2021
# Src:  https://www.amphioxus.org/content/real-time-speed-estimation-cars
#       https://ieeexplore.ieee.org/document/5439423
#       https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
#       https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html
'''
import cv2 as cv2
import numpy as np
from base_ip_class import CameraFunctions

cam = CameraFunctions()

class DistanceMeasure():
    # set the HSV values for the camera stand
    lower = np.array([86, 114, 98])  # for camera stand -- set it in the lab
    upper = np.array([255, 255, 255])  # for camera stand

    def __init__(self):
        print("INFO: DistanceMeasure object created...")

    def run_dist_measure(self):
        cam.set_hsv_values(lower_val=self.lower, upper_val=self.upper)

        cap = cv2.VideoCapture(0)   # camera changes here
        print("INFO: Camera 2 ON...")

        while (True):
            ret, frame_og = cap.read()
            ret_contours, ret_hierarchy, frame = cam.get_contours(frame=frame_og)
            x, y = cam.get_centroid_point(ret_contours)

            # Draw the centroid point on the frame
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(frame, "centroid", (x - 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # calculate distance
            contour_area, contour_count = cam.show_contour_area(ret_contours, frame)
            dist = cam.get_distance(contour_count, frame)
            frame = cv2.putText(frame, str(dist), (80, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # show the scale markings on the frame
            cam.draw_scales_(frame)
            cv2.imshow("Camera Distance Window", frame)

            # Press D to stop Distance Measuring
            q = cv2.waitKey(1)
            if (q == ord('d')) or (q == ord('D')):
                print("ALERT: D key pressed. Stopping running of Distance Measure...")
                break
        # Exit procedure
        cap.release()
        cv2.destroyAllWindows()
        print("ALERT: Distance Measure stopped running. Exiting now...")
        print("INFO: Camera 2 OFF...")










