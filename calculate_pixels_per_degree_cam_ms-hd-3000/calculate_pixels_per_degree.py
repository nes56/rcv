import math

# based on 100 cm distance, base of triangle 95.5 cm, resolution of 640 x 480
X__PIXELS_PER_DEGREE_D100_640x480 = 0.0
Y_PIXELS_PER_DEGREE_D100_640x480 = 0.0

# based on 50 cm distance , base of triangle 48.5 cm, resolution of 640 x 480
X__PIXELS_PER_DEGREE_D50_640x480 = 0.0
Y__PIXELS_PER_DEGREE_D50_640x480 = 0.0


X_PIXELS_PER_DEGREE_D100_320x240 = 0.0
Y_PIXELS_PER_DEGREE_D100_320x240 = 0.0

X_PIXELS_PER_DEGREE_D50_320x240 = 0.0
Y_PIXELS_PER_DEGREE_D50_320x240 = 0.0



def calculate_axes_pixels_per_degree(triangle_base, distance, axes_resolution):
    """
    calculates the view angle of a camera, based on the triangle created
    between the camera and a wall in a given distance.

    :param triangle_base: the length of the full base in cm.
    :param distance: the distance from the wall when the picture was taken
    :param axes_resolution: the resolution in pixels per the axes (X or Y)

    :returns: the number of pixels for a degree in this axes for this resolution

    """
    triangle_base = float(triangle_base)
    distance = float(distance)
    axes_resolution = float(axes_resolution)

    base = triangle_base/2
    radians = math.atan(base/distance)
    degree = math.degrees(radians)
    pixels_per_degree = axes_resolution/(degree * 2)
    return pixels_per_degree

# the data stored here was extracted from the pictures in this directory
data = {
    'X_PIXELS_PER_DEGREE_D100_640x480': {'triangle_base': 95.5, 'distance': 100, 'axes_resolution': 640}, #(95.5, 100, 640),
    'Y_PIXELS_PER_DEGREE_D100_640x480': {'triangle_base': 70.8, 'distance': 100, 'axes_resolution': 480}, #(70.8, 100, 480),
    'X_PIXELS_PER_DEGREE_D50_640x480':  {'triangle_base': 48.5, 'distance': 50, 'axes_resolution': 640},  #(48.5, 50,  640),
    'Y_PIXELS_PER_DEGREE_D50_640x480':  {'triangle_base': 36.0, 'distance': 50, 'axes_resolution': 480},  #(36.0, 50,  480),
    'X_PIXELS_PER_DEGREE_D100_320x240': {'triangle_base': 95.5, 'distance': 100, 'axes_resolution': 320}, #(95.5, 100, 320),
    'Y_PIXELS_PER_DEGREE_D100_320x240': {'triangle_base': 70.8, 'distance': 100, 'axes_resolution': 240}, #(70.8, 100, 240),
    'X_PIXELS_PER_DEGREE_D50_320x240':  {'triangle_base': 48.5, 'distance': 50, 'axes_resolution': 320},  #(48.5, 50,  320),
    'Y_PIXELS_PER_DEGREE_D50_320x240':  {'triangle_base': 36.0, 'distance': 50, 'axes_resolution': 240}, #(36.0, 50,  240),
}


if __name__ == '__main__':
    x_sum_640_480 = 0.0
    x_items_640_480 = 0
    x_sum_320_240 = 0.0
    x_items_320_240 = 0
    y_sum_640_480 = 0.0
    y_items_640_480 = 0
    y_sum_320_240 = 0.0
    y_items_320_240 = 0
    for key in data.keys():
        tmp = eval("calculate_axes_pixels_per_degree(**(data[key]))")
        #exec("key = tmp")
        print("{} = {}".format(key, tmp))
        if key.startswith('X'):
            if data[key]['axes_resolution'] in [640,480]:
                x_sum_640_480 += tmp
                x_items_640_480 += 1
            else:
                x_sum_320_240 += tmp
                x_items_320_240 += 1
        elif key.startswith('Y'):
            if data[key]['axes_resolution'] in [640,480]:
                y_sum_640_480 += tmp
                y_items_640_480 += 1
            else:
                y_sum_320_240 += tmp
                y_items_320_240 += 1
    print("X 640x480 avarage angle = {}".format(x_sum_640_480/x_items_640_480))
    print("Y 640x480 avarage angle = {}".format(y_sum_640_480/y_items_640_480))
    print("X 640x480 avarage radians = {}".format(x_sum_640_480/x_items_640_480/180 * math.pi))
    print("Y 640x480 avarage radians = {}".format(y_sum_640_480/y_items_640_480/180 * math.pi))

    print("X 320x240 avarage angle = {}".format(x_sum_320_240/x_items_320_240))
    print("Y 320x240 avarage angle = {}".format(y_sum_320_240/y_items_320_240))
    print("X 320x240 avarage radians = {}".format(x_sum_320_240/x_items_320_240/180 * math.pi))
    print("Y 320x240 avarage aadians = {}".format(y_sum_320_240/y_items_320_240/180 * math.pi))
