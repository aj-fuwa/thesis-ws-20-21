'''
# Name: base_ip_class
# Aim: To implement the base IP functionality common for the two Python Codes
# Date: (Revised) 31.Jan 2021
# Src:  https://opencv-python-tutroals.readthedocs.io/en/latest/index.html
#       https://docs.opencv.org/master/index.html
#       https://art-of-electronics.blogspot.com/2020/02/object-distance-calculation-using.html
#       https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
#       https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
#       https://docs.opencv.org/3.4/d4/d76/tutorial_js_morphological_ops.html
#       https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
#       http://www.learningaboutelectronics.com/Articles/How-to-find-the-x-and-y-coordinates-of-an-object-in-an-image-Python-OpenCV.php
#       https://www.youtube.com/watch?v=Dggl0fJJ81k
'''
import cv2 as cv2
import numpy as np

class CameraFunctions():
    Kernel_size = np.ones((3, 3), dtype=int)    # default Kernel
    lower_range = np.array([0, 0, 0])   # default lower range
    upper_range = np.array([255, 255, 255]) # default upper range
    font = cv2.FONT_HERSHEY_SIMPLEX
    dist = 0

    def __init__(self):
        print("INFO: CameraFunctions class called...")

    # set the HSV values. Use only Numpy arrays
    def set_hsv_values(self, lower_val, upper_val):
        self.lower_range = lower_val
        self.upper_range = upper_val
        print("INFO: HSV Lower and Upper values set successfully...")

    # returns the contours, hierarchy, and the flipped frame
    def get_contours(self, frame):
        frame = cv2.flip(frame, 1)  # flip the frame vertically around Y axis
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame from RGB to HSV format
        frame_hsv = cv2.inRange(frame_hsv, self.lower_range, self.upper_range)  # set the ranges for the objects
        post_morph = cv2.morphologyEx(frame_hsv, cv2.MORPH_OPEN, self.Kernel_size)  # removing noise from the frame
        ret_contours, ret_hierarchy = cv2.findContours(post_morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    # find the contours
        if (len(ret_contours) == 0):    # return -1 for error condition
            print("ERROR: No contours detected. Exiting the code.")
            return -1
        else:
            return ret_contours, ret_hierarchy, frame

    # returns the contour area and the contour count
    def show_contour_area(self, contours, frame):
        contour_count = contours[0]
        contour_area = cv2.contourArea(contour_count)
        #print("INFO: Contour Area calculated...")
        return contour_area, contour_count

    # returns the centroid point of a particular shape
    def get_centroid_point(self, contours):
        contour_count = contours[0]
        moments_shape = cv2.moments(contour_count)
        x_cood = int(moments_shape['m10'] / moments_shape['m00'])
        y_cood = int(moments_shape['m01'] / moments_shape['m00'])
        return x_cood, y_cood

    # calculate the distance based on the curve-fitted equation
    def get_distance(self, contour_count, frame):
        x, y, w, h = cv2.boundingRect(contour_count)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cood_x = x + (w / 2)
        self.dist = -7.438e-05 * (cood_x * cood_x) - 0.02505 * (cood_x) + 31.12  # obtained using a small Numpy code
        #frame = cv2.putText(frame, str(self.dist), (80, 30), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return self.dist


    # draw the scale markings on the frame for Camera 2, easier to see the position of the camera
    def draw_scales_(self, frame):
        # Applying markings in the video
        frame = cv2.line(frame, (30, 420), (600, 420), (0, 0, 255), 3)  # Add the base scale line in the frame
        frame = cv2.line(frame, (30, 420), (30, 400), (0, 0, 255), 3)  # Add left scale marking
        frame = cv2.line(frame, (600, 420), (600, 400), (0, 0, 255), 3)  # Add right scale marking
        frame = cv2.line(frame, (315, 420), (315, 400), (0, 0, 255), 3)  # Add mid scale marking
        # Add smaller middle-mid scale markings (from right-side)
        frame = cv2.line(frame, (101, 420), (101, 410), (0, 0, 255), 3)  # for 0.5
        frame = cv2.line(frame, (172, 420), (172, 400), (0, 0, 255), 3)  # for 1
        frame = cv2.line(frame, (243, 420), (243, 410), (0, 0, 255), 3)  # for 1.5
        frame = cv2.line(frame, (386, 420), (386, 410), (0, 0, 255), 3)  # for 2.5
        frame = cv2.line(frame, (457, 420), (457, 400), (0, 0, 255), 3)  # for 3
        frame = cv2.line(frame, (528, 420), (528, 410), (0, 0, 255), 3)  # for 3.5
        # Add the text on the frame
        frame = cv2.putText(frame, "Dist:", (10, 30), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "(in cms)", (500, 470), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "0", (590, 450), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "7.5", (430, 450), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "15", (290, 450), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "22.5", (140, 450), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "30", (20, 450), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)









