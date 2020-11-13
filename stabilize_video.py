import numpy as np
import cv2
import time

# Parameters
IN_VID_NAME = 'in_vid.mp4'
OUT_VID_NAME = 'out_vid.avi'

warp_mode = cv2.MOTION_EUCLIDEAN
warp_matrix = np.eye(2, 3, dtype=np.float32)
number_of_iterations = 2
termination_eps = 1e-10
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

# Input Video
cap = cv2.VideoCapture(IN_VID_NAME)

# Get input video information
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

print("width = ", w)
print("height = ", h)

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