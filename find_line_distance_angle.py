import cv2
import numpy as np
import sys
import argparse
import math
# the modules we need for finding the distance and angle to the line


PixToDegree = 12.2
# calculated the vision angle of the camera 53.3 degrees
# 640 / 53.3 = 12.2 pixels to degree
height = 42.8
# the height where the picture was taken from


def most_rectengular_contour(image):
    _, contours, _ = cv2.findContours(
        image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # finds the contours in the image after open was used on it
    # searching only for external contours
    cont = None
    # save the contour that will be returned after the function is used
    # the best fitting rectangle
    minDiffer = sys.maxsize
    # every difference in the area of the minAreaRect
    # will be smaller then sys.maxsize
    # saves it also to decide which is the best fitting rectangle
    bestBox = None
    # saves the rectangle that circumscribes the most fitting line shape
    found_box = False
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        # find the straight rectangle that circumscribes the contour
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # finds the tilted minArea circumscribing rectangle
        if cv2.contourArea(box) <= 200:
            # if the box is too small it can't be the line
            continue
        if cv2.contourArea(box) / cv2.contourArea(contour) < minDiffer:
            # the contour its shape is closest to be a rectangle
            # is the one that the ratio of the area of the rectangle
            # circumscribing to it is the smallest can't be smaller than one
            # because in every case it will be bigger then the contour inside
            minDiffer = cv2.contourArea(box) / cv2.contourArea(contour)
            # updates to be the smaller ratio
            cont = contour
            bestBox = box
            # saves the things we will need to use next
        found_box = True
        # if it got to this point
        # it means we have at least one suspect
        # of being the line we are searching for
    if not found_box:
        return
        # if we didn't find any box matching our criteria
        # we don't need to check for the distance to the rectangle
    max_box_y = 0
    second_max_box_y = 0
    # we need to have the two lower points of the rectangle which have bigger Y
    # to calculate their average to know what distance they are
    for _, y in bestBox:
        if y > second_max_box_y:
            if y >= max_box_y:
                max_box_y, second_max_box_y = y, max_box_y
            else:
                second_max_box_y = y
        # finds the max Y value and the second max Y in the box lowest because
        # y starts from the top
        # then the max value is the lowest corner of the rectangle
    average_lowest_frame_y = (max_box_y + second_max_box_y) / 2
    # contains the y of the middle of the shorter side of the line closer to us
    line_latitude_angle_to_camera = average_lowest_frame_y / PixToDegree
    # the line latitude angle is the y of its middle
    # divided by the pixels to degree ratio
    # because the camera center is parallel to the floor
    # it is the same angle as the line middle y of the center
    # to the camera
    line_latitude_angle_to_camera = math.radians(line_latitude_angle_to_camera)
    # the tangens function in python
    # returns value as if the angle was in radians
    # so we need to convert it to radians to get valid results
    height_to_distance_ratio = math.tan(line_latitude_angle_to_camera)
    # this is the ratio between the height to the distance to the line
    distance = height / height_to_distance_ratio
    # the distance equals the height
    # divided to the ratio of the height to distance
    print(distance)
    # show the distance calculated
    return [cont]
    # return the points that are in the contour


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='An image white line will be detected in'
            )
    # we need a parser
    # to run the program from command line and select one of the photos we took

    parser.add_argument(
            'image',
            help='the path of the image'
        )
    # we need an image path argument to know on what to apply the program

    args = parser.parse_args()
    # convert the arguments into something we can use

    image_path = args.image
    # reads the args image paramater into image_path

    image = cv2.imread(image_path)
    # read the image from the path we are given

    cv2.imshow("base image", image)
    # show the image before any proccesing

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # convert image to grayscale for future processing

    cv2.imshow("grayscale image", image)
    # show how the grayscale image looks

    image_half_y = int(image.shape[0] / 2)
    # see what the middle of the picture is

    roi = image[image_half_y:image.shape[0], 0:image.shape[1]]
    # our new roi is the lower half of the picture
    ret, roi = cv2.threshold(roi, 210, 255, cv2.THRESH_BINARY)
    # use threshold to eleminate the darker parts in the image
    # that we are not looking for
    cv2.imshow("lower half after threshold", roi)
    # show how the image looks like after threshold

    kernel = np.ones((5, 5), np.uint8)
    roi_morphed = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel, iterations=1)
    # use open on threshold picture
    # to reduce white noise caused by brighter spots in the picture
    cv2.imshow("lower half after threshold and open", roi_morphed)
    # show what the picture looks like after open

    best_fitting_rectangle = most_rectengular_contour(roi_morphed)
    # return the points of the contour the looks most like rectangle

    img_color = cv2.cvtColor(roi_morphed, cv2.COLOR_GRAY2BGR)
    # turn the roi into color to mark the contour in red

    output = cv2.drawContours(
        img_color, best_fitting_rectangle,
        -1, (0, 0, 255), 4
    )
    # draws the contour on the lower half of the image

    cv2.imshow("output", output)
    # show the marked best fitting rectangle if there is one

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # wait for key press then destroy all windows
