import argparse
import cv2
import numpy as np
import os
import sys
import math
from find_parameters_by_coordinates import find_distance_and_angle_by_coordinates


image_cleared = True
image_orig = None
image_copy = None


def draw_measure_box(x, y):
    global image_copy
    height, width = image_copy.shape[0:2]
    x_center = int(width/2)
    y_center = int(height/2)
    image_copy = cv2.rectangle(image_copy, (x, y), (x_center, y_center),
                               (0, 255, 0), 2)
    distance, x_turn_angle = find_distance_and_angle_by_coordinates(
        x, y, image_copy.shape, camera_height, y_leaning_angle, x_turning_angle, show=True
        )
    print("distance is {}".format(distance))
    print("x_turn_angle is {}".format(x_turn_angle))


def mouse_callback(event, x, y, flags, param):
    global image_orig, image_copy, image_cleared
    global marks_updated
    if should_do_work:
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


def do_work(img, from_cap=False):
    global image_orig, image_copy
    global y_leaning_angle
    global x_turning_angle
    if not from_cap:
        print("img = {}".format(img))
        image_orig = cv2.imread(img)
    else:
        image_orig = img
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
            on_exit()
        elif k == 32:
            break
        elif k == ord('x'):
            x_turning_angle = float(input("x angle = "))
        elif k == ord('y'):
            y_leaning_angle = float(input("y angle = "))
        elif k == ord('c'):
            center_distance = float(input("center distance = "))
            y_leaning_angle = math.degrees(math.atan(camera_height / center_distance))
            print("y_leaning_angle = " + str(y_leaning_angle))


def on_exit():
    print("final x_turning_angle = " + str(x_turning_angle))
    print("final y_leaning_angle = " + str(y_leaning_angle))
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    sys.exit(-1)


def main():
    global camera_height
    global y_leaning_angle
    global x_turning_angle
    global image_cleared
    global should_do_work
    global cap
    parser_description = "Performs distance calculation to the x,y where the \
        left mouse was clicked"
    parser = argparse.ArgumentParser(description=parser_description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--video', action='store_true',
                    help='path of video process'    
                    )
    group.add_argument('--image', type=str,
                        help='path of the image to process')
    parser.add_argument('--camera-height', type=float, required=True,
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
    if (args.image is not None) and (not os.path.isfile(args.image)):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    camera_height = args.camera_height
    y_leaning_angle = args.y_leaning_angle
    x_turning_angle = args.x_turning_angle
    if args.image is not None:
        do_work(args.image)
    elif args.video:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Image', frame)
            k = cv2.waitKey(1)
            if k == 32:
                should_do_work = True
                do_work(frame, from_cap=True)
                image_cleared = True
                should_do_work = False
            elif k == 27:
                on_exit()
            elif k == ord('x'):
                x_turning_angle = float(input("x angle = "))
            elif k == ord('y'):
                y_leaning_angle = float(input("y angle = "))
            elif k == ord('c'):
                center_distance = float(input("center distance = "))
                y_leaning_angle = math.degrees(math.atan(camera_height / center_distance))
                print("y_leaning_angle = " + str(y_leaning_angle))


if __name__ == '__main__':
    main()
