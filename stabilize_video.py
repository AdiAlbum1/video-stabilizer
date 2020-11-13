import numpy as np
import cv2
import time
from parameters import *

# Input Video
cap = cv2.VideoCapture(IN_VID_NAME)

# Get input video information
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Output Video
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter(OUT_VID_NAME,fourcc, fps, (2*w,h))

# Read first frame
_, first_frame = cap.read()
first_frame_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

start = time.time()

for i in range(n_frames-2):
    ret, curr_frame = cap.read()
    curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Run ECC Algorithm
    cc, warp_matrix = cv2.findTransformECC(first_frame_gray, curr_frame_gray, warp_matrix, warp_mode, criteria, inputMask=None, gaussFiltSize=1)

    curr_aligned_image = cv2.warpAffine(curr_frame_gray, warp_matrix, (w,h),
                                        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    frame_out = cv2.hconcat([curr_frame_gray, curr_aligned_image])
    frame_out = cv2.cvtColor(frame_out, cv2.COLOR_GRAY2BGR)
    out.write(frame_out)

out.release()

end = time.time()

print("FPS: ", (n_frames-2)/(end-start))

cap.release()
cv2.destroyAllWindows()