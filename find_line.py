import cv2
import numpy as np
import sys
import os
import argparse


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
            cont = approx
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
    cv2.imshow("blurred", blurred)
    return blurred


def do_work(image_path):
    # read the image into image
    image = cv2.imread(image_path)
    cv2.imshow("image", image)
    # clean the image
    cleaned_image = clean_image(image)
    # find the best contour in the cleaned image
    line_countour = find_line_contour(cleaned_image)
    # show image with the rectangle marked,
    # if none found will show regular image
    output = image.copy()
    if line_countour is not None:
        output = cv2.drawContours(
            output, [line_countour],
            -1, (0, 0, 255), 4
        )
    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # parser to get image path
    parser_description = "detects the white line in an image"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--image', type=str, required=True,
                        help='path of the image to process')
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    image_path = args.image
    # do work on the image path
    do_work(image_path)


if __name__ == '__main__':
    main()
