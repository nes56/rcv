import cv2
import numpy as np
import sys
import os
import math
import argparse


def line_distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return math.sqrt((x1-x2)**2 + (y1 - y2)**2)


def averge_point(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return(int((x1 + x2)/2), int((y1 + y2)/2))


def show_images(image):
    cv2.imshow("image", image)
    cv2.imshow("cleaned_image", cleaned_image)
    # show image with the rectangle marked,
    # if none found will show regular image
    output = image.copy()
    if line_countour is not None:
        output = cv2.drawContours(
            output, [line_countour],
            -1, (0, 0, 255), 4
        )
        output = cv2.circle(output, points[0], 3, (255, 0, 0), -1)
        output = cv2.circle(output, points[1], 3, (255, 0, 0), -1)
    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extermum_points(contour):
    min_distance = sys.maxsize
    line_top = (0, 0)
    line_bot = (0, 0)
    for i in range(0, 2):
        dis = line_distance(contour[i], contour[i+1])
        if dis < min_distance:
            min_distance = dis
            line_top = averge_point(contour[i], contour[i + 1])
            line_bot = averge_point(contour[i + 2], contour[(i + 3) % 4])
    return (line_top, line_bot)


def find_line_contour(image):
    # every ratio of circumscribing box to contour
    # will be smaller than this number
    min_ratio = sys.maxsize
    # find the contours in the image
    _, contours, _ = cv2.findContours(
        image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # this is the contour we will return as the best contour
    cont = None
    for c in contours:
        contour_area = cv2.contourArea(c)
        # the contour we are searching for won't be smaller
        # than 600 and larger than 10000
        if not (600 <= contour_area <= 10000):
            continue
        # get a parameter for how close the approximated should be
        peri = cv2.arcLength(c, True)
        # get the approximated contour shape for our contour
        # each point of the approximated shape is closer then 2nd argument
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        # if the contour has more then 6 vertexes or less than 4 skip it
        if not(4 <= len(approx) <= 6):
            continue
        # get the circumscribing rectangle
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # get the area of circumscribing rectangle area
        box_area = cv2.contourArea(box)
        # find whether the current rectangle to contour ratio
        # is smaller than our current best
        if box_area / contour_area < min_ratio:
            cont = box
            min_ratio = box_area / contour_area
    return cont


def clean_image(image):
    # get a gray copy of image
    gray = cv2.cvtColor(
        image[0:image.shape[0], 0:image.shape[1]], cv2.COLOR_BGR2GRAY
        )
    # use threshold on image
    _, thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)
    # use open to remove white noise from image
    kernel = np.ones((5, 5), np.uint8)
    thresh_opened = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel, iterations=1
        )
    # blur the image to dull the image
    blurred = cv2.GaussianBlur(thresh_opened, (5, 5), 0)
    return blurred


def do_work(image):
    global cleaned_image
    global line_countour
    global points
    # clean the image
    cleaned_image = clean_image(image)
    # find the best contour in the cleaned image
    line_countour = find_line_contour(cleaned_image)
    if line_countour is not None:
        points = extermum_points(line_countour)
    if(show):
        show_images(image)


def main():
    global show
    # parser to get image path
    parser_description = "detects the white line in an image"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--image', type=str, required=True,
                        help='path of the image to process')
    parser.add_argument('--show', type=bool, default=False,
                        help='show images or not')
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    image_path = args.image
    show = args.show
    image = cv2.imread(image_path)
    # do work on the image
    do_work(image)


if __name__ == '__main__':
    main()
