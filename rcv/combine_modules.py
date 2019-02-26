import cv2
from find_line import do_work
from find_parameters_by_coordinates import find_distance_and_angle_by_coordinates
import json
import argparse
import os
import sys

# intialize the data structre of what we return as a json
points_dictionary = {
        "front": False,
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0},
    }


def init(cap_id=0, init_cap=True):
    global cap
    # if we test on image we don't want to try to open a camera
    if init_cap:
        cap = cv2.VideoCapture(cap_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 30)


def get_data(camera_height=38.5, y_leaning_angle=25, x_turning_angle=0, frame=None, show=False):
    global points_dictionary
    # if the functions works on image then frame won't be equal None
    # if it it got None as frame it reads frame from the capture
    # that was intialized before
    if frame is None:
        ret, frame = cap.read()
        # if cap ran out of data if the video ended ret will be false and
        # the program will return false
        if not ret:
            return False
    # return the points that the program will find the distance to them
    # if get_data got show as True it will display the cleaned image
    # in black and white, the original frame and the frame with the rectangle
    # drawn on it
    points = do_work(frame, show)
    # if points is not None there were points found
    if points is not None:
        # put the calculated distances and angles into the data structre
        # we return as json
        points_dictionary["found"] = True
        d1, a1 = find_distance_and_angle_by_coordinates(
            points[0][0], points[0][1], frame.shape, camera_height, y_leaning_angle, x_turning_angle
        )
        points_dictionary["p1"]["d"] = d1
        points_dictionary["p1"]["a"] = a1
        d2, a2 = find_distance_and_angle_by_coordinates(
            points[1][0], points[1][1], frame.shape, camera_height, y_leaning_angle, x_turning_angle
        )
        points_dictionary["p2"]["d"] = d2
        points_dictionary["p2"]["a"] = a2
    # if no line was found return a unique message that will be recognized
    # as no line was found
    else:
        points_dictionary["found"] = False
        points_dictionary["p1"]["d"] = 0
        points_dictionary["p1"]["a"] = 0
        points_dictionary["p2"]["d"] = 0
        points_dictionary["p2"]["a"] = 0
    return json.dumps(points_dictionary)


def main():
    parser_description = "detects the white line in an image and shows\
                          distances to both it's edges"
    parser = argparse.ArgumentParser(description=parser_description)
    group = parser.add_mutually_exclusive_group(required=True)    
    group.add_argument('--video', type=str,
                        help='path of video process')
    group.add_argument('--image', type=str,
                        help='path of the image to process')
    parser.add_argument('--show', type=bool, default=False,
                        help='show images or not')
    args = parser.parse_args()
    if args.image is not None:
        if not os.path.isfile(args.image):
            print('Please provide a valid path to an image file')
            sys.exit(-1)
        # no cap needed to be intialized, working on an image
        init(init_cap=False)
        # read the image
        image = cv2.imread(args.image)
        # get the data about the line in the image and display it
        # if show is True
        data = get_data(image, args.show)
        if args.show:
            print(data)
            cv2.waitKey(0)
    if args.video is not None:
        if not os.path.isfile(args.video):
            print('Please provide a valid path to a video file')
            sys.exit(-1)
        # intialize cap as the video that was given
        init(args.video)
        # if the program is ran on video display the images anyway
        data = get_data(show=True)
        # if the video is over data will be false
        while data != False:
            # display the data of every frame in the video
            # wait a specific time so the video will be played in correct speed
            # if q is pressed the program will quit
            if cv2.waitKey(int(1000 / 30)) == ord('q'):
                break
            # get data for next iteration if it is false the program will quit
            data = get_data(show=True)
        # after cap was intialized and video is over release it
        cap.release()
    # destroy all opened windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
