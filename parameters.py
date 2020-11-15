import cv2
import numpy as np
from enum import Enum
import argparse

parser = argparse.ArgumentParser(description='Video Stabilization Algorithm implemented using OpenCV')
parser.add_argument('-i', '--input', type=str, help='path to input video', default='in_vid.mp4')
parser.add_argument('-o', '--output', type=str, help='path to output video', default='out_vid.mp4')

args = parser.parse_args()

IN_VID_NAME = args.input
OUT_VID_NAME = args.output

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