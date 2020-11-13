import cv2
import numpy as np

IN_VID_NAME = 'in_vid.avi'
OUT_VID_NAME = 'out_vid.avi'

warp_mode = cv2.MOTION_EUCLIDEAN
warp_matrix = np.eye(2, 3, dtype=np.float32)
number_of_iterations = 2
termination_eps = 1e-10
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
