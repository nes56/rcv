import argparse
import cv2
from enum import Enum
import math
import numpy as np
import os
import sys


# GLOBALS #
# the below 2 globals were calculated using calculate_pixels_per_degree.py utility
X_PIXELS_PER_DEGREE = {640: 12.452453991885616, 320: 6.226226995942808}
Y_PIXELS_PER_DEGREE = {480: 12.216701907035985, 240: 6.108350953517992}
image_cleared = True
image_orig = None
image_copy = None


class XOrientation(Enum):
    left = -1
    center = 0
    right = 1


class YOrientation(Enum):
    up = -1
    center = 0
    down = 1


def draw_measure_box(x, y):
    global image_copy
    height, width = image_copy.shape[0:2]
    print("***********************************")
    print("camera_height = {}".format(camera_height))
    print("x = {} , y = {}".format(x, y))
    x_center = width/2
    y_center = height/2
    x_pixels_per_degree = X_PIXELS_PER_DEGREE[width]
    y_pixels_per_degree = Y_PIXELS_PER_DEGREE[height]
    print("x_pixels_per_degree = {}".format(x_pixels_per_degree))
    print("y_pixels_per_degree = {}".format(y_pixels_per_degree))
    x_orientation = XOrientation.center
    y_orientation = YOrientation.center
    if x > x_center:
        x_orientation = XOrientation.right
    elif x < x_center:
        x_orientation = XOrientation.left
    if y > y_center:
        y_orientation = YOrientation.down
    elif y < y_center:
        y_orientation = YOrientation.up
    # calculating the quadrants
    o_sum = x_orientation.value + y_orientation.value
    q = -1
    if o_sum == 2:
        q = 4
    elif o_sum == -2:
        q = 2
    elif o_sum == 0:
        if x_orientation.value > y_orientation.value:
            q = 1
        if x_orientation.value < y_orientation.value:
            q = 3
    # drawing the box
    top_left = None
    bottom_right = None
    # implemented quadrants 1 and 2
    if q == 1:
        top_left = (int(x_center), int(y))
        bottom_right = (int(x), int(y_center))
    elif q == 2:
        top_left = (int(x), int(y))
        bottom_right = (int(x_center), int(y_center))
    elif q == 3:
        top_left = (int(x), int(y_center))
        bottom_right = (int(x_center), int(y))
    elif q == 4:
        top_left = (int(x_center), int(y_center))
        bottom_right = (int(x), int(y))
    print("top_left = {}".format(top_left))
    print("bottom_right = {}".format(bottom_right))
    image_copy = cv2.rectangle(image_copy, top_left, bottom_right,
                               (0, 255, 0), 2)
    dy = y - y_center
    dx = abs(x - x_center)
    print("dx = {}".format(dx))
    print("dy = {}".format(dy))
    # adding the turning angle to the angle calculated by pixels
    x_diviation_degree = x_turning_angle + (
        float(dx) / float(x_pixels_per_degree)
        )
    # adding the y leaning angle to the angle calculated by pixels
    y_diviation_degree = float(y_leaning_angle) + (
        float(dy) / float(y_pixels_per_degree)
        )
    print("x_diviation_degree = {}".format(x_diviation_degree))
    print("y_diviation_degree = {}".format(y_diviation_degree))
    # calculating distance from camera base to (x_center, y)
    d_to_x_center_y = camera_height/math.tan(math.radians(y_diviation_degree))
    # calculating distance from camera base to (x,y)
    d_to_x_y = d_to_x_center_y / math.cos(math.radians(x_diviation_degree))
    print("distance is {}".format(d_to_x_y))


def mouse_callback(event, x, y, flags, param):
    global image_orig, image_copy, image_cleared
    global marks_updated
    if event == cv2.EVENT_LBUTTONDOWN and image_cleared:
        cv2.circle(image_copy, (x, y), 3, (0, 0, 255), 2)
        draw_measure_box(x, y)
        image_cleared = False
    if event == cv2.EVENT_RBUTTONDOWN and not image_cleared:
        image_copy = np.copy(image_orig)
        height, width = image_copy.shape[0:2]
        cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
                 (0, 0, 0), 1)
        cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
                 (0, 0, 0), 1)
        image_cleared = True


def do_work(img):
    global image_orig, image_copy
    print("img = {}".format(img))
    image_orig = cv2.imread(img)
    image_copy = np.copy(image_orig)
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)
    height, width = image_copy.shape[0:2]
    cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
             (0, 0, 0), 1)
    cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
             (0, 0, 0), 1)

    while True:
        cv2.imshow('Image', image_copy)
        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()


def main():
    global camera_height
    global y_leaning_angle
    global x_turning_angle
    parser_description = "Performs distance calculation to the x,y where the \
        left mouse was clicked"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--image', type=str, required=True,
                        help='path of the image to process')
    parser.add_argument('--camera-height', type=float, default=38.5,
                        help="the height of camera when the picture was taken")
    parser.add_argument('--y_leaning_angle', type=float, default=28,
                        help="the y angle of camera when the picture was taken"
                        )
    parser.add_argument('--x_turning_angle', type=float, default=1.9,
                        help="the difference in pixels between the center line\
                         and a straight reference line\
                         when the picture was taken\
                         positive angle is to the right"
                        )
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    camera_height = args.camera_height
    y_leaning_angle = args.y_leaning_angle
    x_turning_angle = args.x_turning_angle
    do_work(args.image)


if __name__ == '__main__':
    main()
