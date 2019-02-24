import cv2
import json
from find_parameters_by_coordinates import find_distance_and_angle_by_coordinates
from find_line import do_work


def init():
    global cap
    global points_dictionary
    global last_time            
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    points_dictionary = {
        "front": True,
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0}
    }


def get_data():
    global points_dictionary
    ret, frame = cap.read()
    points = do_work(frame, False)
    print(points)
    if points[0]:
        points_dictionary["found"] = True
        d1, a1 = find_distance_and_angle_by_coordinates(
            points[1][0][0], points[1][0][1], frame.shape, 38.5, 25, 0
        )
        d2, a2 = find_distance_and_angle_by_coordinates(
            points[1][1][0], points[1][1][1], frame.shape, 38.5, 25, 0
        )
        points_dictionary["p1"]["d"] = d1
        points_dictionary["p2"]["d"] = d2
        points_dictionary["p1"]["a"] = a1
        points_dictionary["p2"]["a"] = a2
    else:
        points_dictionary = {
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0}
    }
    return json.dumps(points_dictionary).encode('utf-8')