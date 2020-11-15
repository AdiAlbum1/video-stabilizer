import numpy as np
import cv2
import time

from parameters import *
from vertical_line import StoreCoordinates
from vertical_line import obtain_rotation_mat

# Input Video
cap = cv2.VideoCapture(IN_VID_NAME)

# Get input video information
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

curr_state = State.SETUP
count = 0
start_time = False

for i in range(n_frames-2):
    ret, curr_frame = cap.read()

    if curr_state == State.SETUP:
        cv2.imshow("video", curr_frame)
        k = cv2.waitKey(25)

        if k == ord('a'):
            curr_state = State.SELECT_ROI

    if curr_state == State.SELECT_ROI:
        cv2.imshow("video", curr_frame)
        cv2.waitKey(25)
        roi = cv2.selectROI("video", curr_frame)

        curr_state = State.MARK_VERTICAL_POINTS

    if curr_state == State.MARK_VERTICAL_POINTS:
        base_frame = curr_frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        curr_frame = curr_frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        height = base_frame.shape[0]
        width = base_frame.shape[1]

        # Output Video
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        out = cv2.VideoWriter(OUT_VID_NAME, fourcc, fps, (2 * width, height))

        coordinates_store = StoreCoordinates()
        cv2.imshow("video", curr_frame)
        cv2.setMouseCallback('video', coordinates_store.click_event, curr_frame)
        k = cv2.waitKey(0)

        rotation_matrix = obtain_rotation_mat(base_frame, coordinates_store.points)
        ## Initial Warp Matrix
        warp_matrix = obtain_rotation_mat(base_frame, coordinates_store.points, inverse=True).astype(np.float32)
        base_frame = cv2.warpAffine(base_frame, rotation_matrix, (width, height),
                                    flags=cv2.INTER_LINEAR)
        base_frame_gray = cv2.cvtColor(base_frame, cv2.COLOR_BGR2GRAY)

        curr_state = State.STABILIZE

    if curr_state == State.STABILIZE:
        if not start_time:
            start = time.time()
            start_time = True
        count += 1
        curr_frame = curr_frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        height = curr_frame.shape[0]
        width = curr_frame.shape[1]

        # Run ECC Algorithm
        cc, warp_matrix = cv2.findTransformECC(base_frame_gray, curr_frame_gray, warp_matrix, warp_mode, criteria,
                                               inputMask=None, gaussFiltSize=1)

        curr_aligned_image = cv2.warpAffine(curr_frame_gray, warp_matrix, (width, height),
                                            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

        curr_aligned_image = cv2.cvtColor(curr_aligned_image, cv2.COLOR_GRAY2BGR)
        curr_frame_gray = cv2.cvtColor(curr_frame_gray, cv2.COLOR_GRAY2BGR)
        frame_out = cv2.hconcat([curr_frame_gray, curr_aligned_image])
        cv2.imshow("video", curr_aligned_image)
        cv2.waitKey(1)

        out.write(frame_out)

end = time.time()

fps = count / (end - start)
print("Algorithm FPS:")
print(fps)

out.release()

cap.release()
cv2.destroyAllWindows()