import cv2
import math
import numpy as np
import os
import sys

constants_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(constants_path)
from constants import X_PIXELS_PER_DEGREE, Y_PIXELS_PER_DEGREE

response_structure = {
        "front": False,
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0},
    }


class FrameHandler():
    def __init__(self, configuration):
        self._conf = configuration
        self._frame = None
        self._output_frame = None
        self._cleaned_frame = None
        self._line_contour = None
        self._points = None
        self._line_contour = None
        self._response = None
        self._is_front = self._conf.getboolean('rcv_server', 'is_front')
        response_structure['front'] = self._is_front
        self._camera_height=float(self._conf.get('rcv_server', 'camera_height'))
        self._y_leaning_angle=float(self._conf.get('rcv_server', 'y_leaning_angle'))
        self._x_turning_angle=float(self._conf.get('rcv_server', 'x_turning_angle'))
        self._show = self._conf.getboolean('rcv_server', 'show')
        self._frame_threshold= int(self._conf.get('rcv_server', 'frame_threshold'))
        focus_image_path = self._conf.get('rcv_server', 'focus_image')
        if os.path.exists(focus_image_path) and os.path.isfile(focus_image_path):
            self._focus_image = cv2.imread(focus_image_path)
            self._focus_image_gray = cv2.imread(focus_image_path, cv2.IMREAD_GRAYSCALE)
        else:
            raise FileNotFoundError("File {} was not found")
        print("#### Initialized FrameHandler .......")

    def init_frame_analysis(self):
        self._frame = None
        self._cleaned_frame = None
        self._line_contour = None
        self._output_frame = None
        self._points = None
        self._response = response_structure.copy()

    def line_distance(self, p1, p2):
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

    def averge_point(self, p1, p2):
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        return(int((x1 + x2)/2), int((y1 + y2)/2))

    def prep_output_image(self):
        # prepare image with the rectangle marked,
        # if none found will show regular image
        output = self._frame.copy()
        output = cv2.bitwise_and(output, self._focus_image)
        if self._line_contour is not None:
            output = cv2.drawContours(
                output, [self._line_contour],
                -1, (0, 0, 255), 4)
            output = cv2.circle(output, self._points[0], 3, (255, 0, 0), -1)
            output = cv2.circle(output, self._points[1], 3, (0, 255, 0), -1)
        self._output_frame = output

    def show_images(self):
        self.prep_output_image()
        cv2.imshow("output", self._output_frame)
        cv2.waitKey(1)

    def extermum_points(self, contour):
        min_distance = sys.maxsize
        line_top = (0, 0)
        line_bot = (0, 0)
        for i in range(0, 2):
            dis = self.line_distance(contour[i], contour[i+1])
            if dis < min_distance:
                min_distance = dis
                line_top = self.averge_point(contour[i], contour[i + 1])
                line_bot = self.averge_point(contour[i + 2], contour[(i + 3) % 4])
        if line_top[1] > line_bot[1]:
            line_top, line_bot = line_bot, line_top
        return (line_bot, line_top)

    def find_line_contour(self):
        # every center of mass will be closer to what we need then this one
        fitting_mass_center = (0, -sys.maxsize-1)
        # find the contours in the frame
        _, contours, _ = cv2.findContours(
            self._cleaned_frame, cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        # this is the contour we will return as the best contour
        cont = None
        for c in contours:
            contour_area = cv2.contourArea(c)
            # the contour we are searching for won't be smaller
            # than 340 by our calculations of pix to degree and trigonometric
            # and larger than 2950
            if not (340 <= contour_area <= 2950):
                continue
            # get a parameter for how close the approximated should be
            peri = cv2.arcLength(c, True)
            # get the approximated contour shape for our contour
            # each point of the approximated shape is closer then 2nd argument
            # 0.02 is there because it works better on our videos
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if the contour has more then 6 vertexes or less than 4 skip it
            if not(4 <= len(approx) <= 6):
                continue
            # get the circumscribing rectangle
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # get the area of circumscribing rectangle area
            box_area = cv2.contourArea(box)
            # get the moments which will help us find the center of mass
            # of the contour
            M = cv2.moments(approx)
            # calculate x,y coordinate of center
            if M["m00"] != 0:
                cY = int(M["m01"] / M["m00"])
                cX = int(M["m10"] / M["m00"])
            else:
                cY = 0
                cX = 0
            half_x = self._frame.shape[1] / 2
            # if the y of the center of mass of the new contour is bigger
            # it means the contour is closer to us and is probably what we
            # are looking for
            if cY > fitting_mass_center[1]:
                # if the current contour is closer in y and x to the bottom center
                # it is out best fitting contour
                if abs(half_x - cX) < abs(half_x - fitting_mass_center[0]):
                    cont = box
                    fitting_mass_center = (cX, cY)
                # if the current contour has bigger y then the last one
                # by an amount that matters it is probably what we are
                # looking for
                elif cY - fitting_mass_center[1] > 20:
                    cont = box
                    fitting_mass_center = (cX, cY)
            # if the contour is closer in x to the center but doesn't have bigger Y
            elif abs(half_x - cX) < abs(half_x - fitting_mass_center[0]):
                # then we check if the difference in Y matters and if it does
                # it is probably what are looking for
                if cY - fitting_mass_center[1] > -20:
                    cont = box
                    fitting_mass_center = (cX, cY)
        return cont

    def clean_frame(self):
        # get a gray copy of frame
        gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        focused_image = cv2.bitwise_and(gray, self._focus_image_gray)
        # use threshold on frame
        _, thresh = cv2.threshold(focused_image, self._frame_threshold, 255, cv2.THRESH_BINARY)
        # use open to remove white noise from frame
        kernel = np.ones((5, 5), np.uint8)
        thresh_opened = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        # blur the frame to dull the image
        blurred = cv2.GaussianBlur(thresh_opened, (5, 5), 0)
        return blurred

    def find_track(self):
        # clean the image
        self._cleaned_frame = self.clean_frame()
        # find the best contour in the cleaned image
        self._line_contour = self.find_line_contour()
        if self._line_contour is not None:
            self._points = self.extermum_points(self._line_contour)
        if self._show:
            self.show_images()
        return self._points

    def find_distance_and_angle_by_coordinates(self, x, y, image_shape):
        height, width = image_shape[0:2]
        x_pixels_per_degree = X_PIXELS_PER_DEGREE[width]
        y_pixels_per_degree = Y_PIXELS_PER_DEGREE[height]
        x_center = width/2
        y_center = height/2
        dy = y - y_center
        dx = x - x_center
        x_diviation_degree = (
            # adding the turning angle to the angle calculated by pixels
            # x_turning angle is negative if the camera is turned to the right
            # and positive if to the left
            float(dx-(x_pixels_per_degree * self._x_turning_angle))
            / float(x_pixels_per_degree))
        # adding the y leaning angle to the angle calculated by pixels
        y_diviation_degree = float(self._y_leaning_angle) + (
            float(dy) / float(y_pixels_per_degree))
        # calculating distance from camera base to (x_center, y)
        d_to_x_center_y = self._camera_height/math.tan(math.radians(y_diviation_degree))
        # calculating distance from camera base to (x,y)
        d_to_x_y = d_to_x_center_y/math.cos(math.radians(x_diviation_degree))
        return (d_to_x_y, x_diviation_degree)

    def handle_frame(self, frame):
        self.init_frame_analysis()
        self._frame = frame
        # return the points that the program will find the distance to them
        # if get_data got show as True it will display the cleaned image
        # in black and white, the original frame and the frame with the rectangle
        # drawn on it
        points = self.find_track()
        # if points is not None there were points found
        if points is not None:
            # put the calculated distances and angles into the data structre
            # we return as json
            self._response["found"] = True
            d1, a1 = self.find_distance_and_angle_by_coordinates(points[0][0],
                                                                 points[0][1],
                                                                 frame.shape)
            self._response["p1"]["d"] = d1
            self._response["p1"]["a"] = a1
            d2, a2 = self.find_distance_and_angle_by_coordinates(points[1][0],
                                                                 points[1][1],
                                                                 frame.shape)
            self._response["p2"]["d"] = d2
            self._response["p2"]["a"] = a2
        # if no line was found return a unique message that will be recognized
        # as no line was found
        else:
            self._response["found"] = False
            self._response["p1"]["d"] = 0
            self._response["p1"]["a"] = 0
            self._response["p2"]["d"] = 0
            self._response["p2"]["a"] = 0
        return self._response
