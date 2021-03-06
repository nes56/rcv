import math
from constants import X_PIXELS_PER_DEGREE, Y_PIXELS_PER_DEGREE


def find_distance_and_angle_by_coordinates(
    x, y, image_shape, camera_height, y_leaning_angle, x_turning_angle,
    show=False
):
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
        float(dx-(x_pixels_per_degree * x_turning_angle))
        / float(x_pixels_per_degree)
        )
    # adding the y leaning angle to the angle calculated by pixels
    y_diviation_degree = float(y_leaning_angle) + (
        float(dy) / float(y_pixels_per_degree)
        )    
    # calculating distance from camera base to (x_center, y)
    d_to_x_center_y = camera_height/math.tan(math.radians(y_diviation_degree))
    # calculating distance from camera base to (x,y)
    d_to_x_y = d_to_x_center_y/math.cos(math.radians(x_diviation_degree))
    if show:
        print("***********************************")
        print("camera_height = {}".format(camera_height))
        print("x = {} , y = {}".format(x, y))
        print("x_pixels_per_degree = {}".format(x_pixels_per_degree))
        print("y_pixels_per_degree = {}".format(y_pixels_per_degree))
        print("dx = {}".format(dx))
        print("dy = {}".format(dy))
        print("x_diviation_degree = {}".format(x_diviation_degree))
        print("y_diviation_degree = {}".format(y_diviation_degree))
    return (d_to_x_y, x_diviation_degree)
