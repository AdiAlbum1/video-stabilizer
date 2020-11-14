import cv2
import numpy as np
from enum import Enum

IN_VID_NAME = 'in_vid.mp4'
OUT_VID_NAME = 'out_vid.avi'

warp_mode = cv2.MOTION_EUCLIDEAN
warp_matrix = np.eye(2, 3, dtype=np.float32)
number_of_iterations = 8               # Determines upper bound on FPS
termination_eps = -1                # Determines accuracy of stabilization. small --> accurate
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

class State(Enum):
    SETUP = 1
    SELECT_ROI = 2
    MARK_VERTICAL_POINTS = 3
    STABILIZE = 4
    END = 5