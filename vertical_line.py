# importing the module
import cv2
from scipy.stats import linregress
import math

class StoreCoordinates:
    def __init__(self):
        self.points = []

    def click_event(self, event, x, y, flags, params):

        img = params
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(x) + ',' + str(y), (x,y),
                        font, 0.5, (255, 0, 0), 2)
            cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
            cv2.imshow('video', img)

            self.points.append((x,y))

def obtain_rotation_mat(image, points, inverse=False):
    X = [point[0] for point in points]
    y = [point[1] for point in points]
    line = linregress(X, y)
    slope = line.slope
    angle = math.atan(slope)

    if angle < 0:
        angle += math.pi

    cols = image.shape[1]
    rows = image.shape[0]

    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), math.degrees(-(math.pi/2 - angle)), 1)
    if inverse:
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), math.degrees(math.pi / 2 - angle), 1)
    return rotation_matrix
