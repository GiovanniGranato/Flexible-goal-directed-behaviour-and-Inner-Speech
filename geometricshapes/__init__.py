#!/usr/bin/env python

"""A collection of geometrical objects.

Function:
math_round(x)

Classes:
Shape
Square
Rectangle
Fovea
Circle
"""


import numpy as np


def math_round(x):
    """Round to integer

    Round arithmetically to nearest integer, with ties going away from
    zero.
    """
    if abs(x) < 1:
        if x >= 0.5:
            x = 1
        else:
            x = 0
    else:
        if x % int(x) >= 0.5:
            x = int(x) + 1
        else:
            x = int(x)
    return x


class Shape(object):
    """Geometric shape.

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure (number of pixels in environment)
    - value -- value (float/int) of reward if accomplished sub-goal

    Methods:
    - move -- Move object
    """
    type_ = "Shape"

    def __init__(self, center, size, color, unit, value=1):
        self.center = np.array(center)
        self.size = size
        self.color = color
        self.unit = unit
        self.value = value

    def move(self, vector):
        """Move object by adding vector to its center position.

        Keyword arguments:
        vector -- 2D vector array (list or numpy array)
        """
        self.center += np.array(vector)


class Square(Shape):
    """Square object with inheritance from Shape class.

    Added in Square:
    - Methods draw and is_inside

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure (number of pixels in environment)
    - value -- value (float/int) of reward if accomplished sub-goal

    Methods:
    - move -- Move object
    - draw -- Draw in image array
    - is_inside -- Tell if point is inside square
    """
    type_ = "Square"

    def get_corners(self):
        """Get the coordinates of the square's corners."""
        _x_min = (self.center[0] - self.size/2)
        _x_max = (self.center[0] + self.size/2)
        _y_min = (self.center[1] - self.size/2)
        _y_max = (self.center[1] + self.size/2)
        return np.array([[_x_min, _x_max], [_y_min, _y_max]])

    def get_index_values(self):
        """Get the coodrinates of the square's corners in index values."""
        _corners = self.get_corners()*self.unit
        _corner_index_values = np.array([[math_round(_corners[0][0]),
                                          math_round(_corners[0][1])],
                                         [math_round(_corners[1][0]),
                                          math_round(_corners[1][1])] # math_round(_corners[1][1])]
                                         ], dtype=int
                                        )
        return _corner_index_values

    def draw(self, image_array):
        """Draw object in image array.

        Keyword arguments:
        image_array -- the image array to draw in.

        Get coordinates of square's corners, convert to array index
        values and update image_array by coloring the pixels within
        the square.
        """
        _corner_index_values = self.get_index_values()
        x_min = _corner_index_values[0][0]
        x_max = _corner_index_values[0][1]
        y_min = _corner_index_values[1][0]
        y_max = _corner_index_values[1][1]

        diag_points = [np.array([x_min, y_min]), np.array([x_max, y_max])]
        for idx1 in range(y_min, y_max):
            for idx2 in range(x_min, x_max):
                    single_pix = image_array[idx2, idx1]
                    image_array[idx1, idx2] = self.color



                # # if idx1  >= idx2:
                # single_pix = image_array[idx2, idx1]
                # image_array[idx1, idx2] = self.color




    def is_inside(self, point):
        """Check if point is inside square.

        Keyword arguments:
        point -- array of float coordinates of the point

        If x-coordinate of point is between x_min and x_max of square
        and y-coordinate of point is between y_min and _ymax of square,
        return True. Otherwise return False.
        """
        _corners = self.get_corners()
        if (_corners[0][0] <= point[0] <= _corners[0][1] and
                _corners[1][0] <= point[1] <= _corners[1][1]):
            return True
        else:
            return False

class Triangle(Shape):
    """Triangle object with inheritance from Shape class.

    Added in Square:
    - Methods draw and is_inside

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure (number of pixels in environment)
    - value -- value (float/int) of reward if accomplished sub-goal

    Methods:
    - move -- Move object
    - draw -- Draw in image array
    - is_inside -- Tell if point is inside square
    """
    type_ = "Triangle"

    def get_corners(self):
        """Get the coordinates of the square's corners."""
        _x_min = (self.center[0] - self.size/2)
        _x_max = (self.center[0] + self.size/2)
        _y_min = (self.center[1] - self.size/2)
        _y_max = (self.center[1] + self.size/2)
        return np.array([[_x_min, _x_max], [_y_min, _y_max]])

    def get_index_values(self):
        """Get the coodrinates of the square's corners in index values."""
        _corners = self.get_corners()*self.unit
        _corner_index_values = np.array([[math_round(_corners[0][0]),
                                          math_round(_corners[0][1])],
                                         [math_round(_corners[1][0]),
                                          math_round(_corners[1][1])] # math_round(_corners[1][1])]
                                         ], dtype=int
                                        )
        return _corner_index_values

    def draw(self, image_array):
        """Draw object in image array.

        Keyword arguments:
        image_array -- the image array to draw in.

        Get coordinates of square's corners, convert to array index
        values and update image_array by coloring the pixels within
        the square.
        """
        _corner_index_values = self.get_index_values()
        x_min = _corner_index_values[0][0]
        x_max = _corner_index_values[0][1]
        y_min = _corner_index_values[1][0]
        y_max = _corner_index_values[1][1]


        diag_points = [np.array([x_min, y_min]), np.array([x_max, y_max])]
        for idx1 in range(y_min, y_max):
            for idx2 in range(x_min, x_max):
                point_coord = np.array([idx2,idx1])

                in_p = (np.cross(point_coord - diag_points[0], diag_points[1] - diag_points[0])) > 0
                if in_p == False:
                    single_pix = image_array[idx2, idx1]
                    image_array[idx1, idx2] = self.color



                # if idx1  >= idx2:
                #     single_pix = image_array[idx2, idx1]
                #     image_array[idx1, idx2] = self.color




    def is_inside(self, point): # to change for Triangle
        """Check if point is inside Triangle.

        Keyword arguments:
        point -- array of float coordinates of the point

        If x-coordinate of point is between x_min and x_max of square
        and y-coordinate of point is between y_min and _ymax of square,
        return True. Otherwise return False.
        """
        _corners = self.get_corners()
        x_min = _corners[0,0]
        x_max = _corners[0,1]
        y_min = _corners[1,0]
        y_max = _corners[1,1]
        point_coord = [point[1], point[0]]
        diag_points = [np.array([x_min, y_min]), np.array([x_max, y_max])]
        in_p = (np.cross(point - diag_points[0], diag_points[1] - diag_points[0])) > 0
        if (_corners[0][0] <= point[0] <= _corners[0][1] and
                _corners[1][0] <= point[1] <= _corners[1][1]) and in_p == False : # maybe it is useful np.cross product...or insert a nother condition: if is under the diagonal (to consider triangle)
            return True
        else:
            return False


class Rectangle(Square):
    """Rectangle class with inheritance from Square

    Added in Rectangle:
    - Changed get_corners method
    - Added orientation

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure (number of pixels in environment)
    - orientation -- integer number (0 or 1) for horizontal/vertical
    - value -- value (float/int) of reward if accomplished sub-goal

    Methods:
    - move -- Move object
    - get_corners -- Return coordinates of the corners of the object
    - get_index_values -- Return the array index values of corners
    - draw -- Draw object in image array
    - is_inside -- Tell if point is inside square
    """
    type_ = "Rectangle"

    def __init__(self, center, size, color, unit, orientation, value=1):
        super(Rectangle, self).__init__(center, size, color, unit, value)
        self.orientation = orientation

    def get_corners(self):
        """Return corner coordinates"""
        if self.orientation == 0:
            _min_1 = (self.center[0] - self.size/3.5)
            _max_1 = (self.center[0] + self.size/3.5)
            _min_2 = (self.center[1] - self.size/1.50) #1.25
            _max_2 = (self.center[1] + self.size/1.50) #1.25
        elif self.orientation == 1:
            _min_1 = (self.center[0] - self.size/1.75)
            _max_1 = (self.center[0] + self.size/1.75)
            _min_2 = (self.center[1] - self.size/3.5)
            _max_2 = (self.center[1] + self.size/3.5)

        return np.array([[_min_1, _max_1], [_min_2, _max_2]])


class Fovea(Square):
    """Fovea class with inheritance from Square

    Added in Fovea:
    - Method get_focus_image(environment_image)

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure

    Methods:
    - move -- Move object
    - draw -- Draw in image array
    - get_focus_image -- Get the array of pixels in the fovea
    """
    type_ = "Fovea"

    def get_focus_image(self, environment):
        """Get the focus image pixel array.

        Keyword arguments:
        - environment -- the pixel array of the environment the fovea
          is in

        Calculate coordinates of fovea corners in the environment
        and return array of pixels of the fovea.
        """
        _corner_index_values = self.get_index_values()
        _fov_image = environment[
            _corner_index_values[1][0]:_corner_index_values[1][1],
            _corner_index_values[0][0]:_corner_index_values[0][1]
            ]
        return _fov_image


class Circle(Shape):
    """Circle class with inheritance from Shape.

    Added in Circle:
    - self.radius (float)
    - Methods draw and is_inside

    Variables:
    - type_ -- type of object (string)
    - center -- center coordinates (floats)
    - size -- float value of object size
    - color -- color as integer (0/1) or RGB list ([R, G, B])
    - unit -- integer unit measure (number of pixels in environment)
    - radius -- float value of circle radius

    Methods:
    - move -- Move object
    - draw -- Draw in image array
    - is_inside -- Tell if point is inside circle
    """
    type_ = "Circle"

    def __init__(self, center, size, color, unit, value=1):
        super(Circle, self).__init__(center, size, color, unit, value)
        self.radius = self.size/2

    def draw(self, image_array):
        """Draw circle object in image array.

        Keyword arguments:
        image_array -- the image array to draw in

        Takes center (float coordinates), size (float) and image_array
        (matrix array). Updates the array elements in image_array
        which are within radius distance from the center of the circle
        to the color of the circle.
        """
        _x = self.center[0]*self.unit
        _y = self.center[1]*self.unit

        _r = self.radius*self.unit

        _X, _Y = np.meshgrid(np.arange(image_array.shape[0]),
                             np.arange(image_array.shape[1])
                             )

        _d = np.sqrt((_X-_x)**2 + (_Y-_y)**2)

        image_array[np.where(_d < _r)] = self.color

    def is_inside(self, point):
        """Check if point is inside circle object.

        Keyword arguments:
        point -- array of float coordinates of the point

        Takes the center (float coordinates), radius (float) and point
        (float coordinates) and calculates the distance _d between the
        point and the center of the circle. If _d is smaller than the
        radius _r of the circle the point is inside.
        """
        _d = np.sqrt((point[0]-self.center[0])**2
                     + (point[1]-self.center[1])**2
                     )

        if _d <= self.radius:
            return True
        else:
            return False


if __name__ == '__main__':
    """Main"""
    # RUN TESTS
    import matplotlib.pyplot as plt
    unit = 256
    env = np.zeros([unit, unit, 3])
    fov = Fovea([0.35, 0.65], 0.26, [1, 1, 1], unit)

    s1 = Square([0.2, 0.2], 0.14, [1, 0, 0], unit)
    s2 = Square([0.2, 0.5], 0.14, [0, 1, 0], unit)
    s3 = Square([0.2, 0.8], 0.14, [0, 0, 1], unit)
    c1 = Circle([0.5, 0.2], 0.14, [1, 0, 0], unit)
    c2 = Circle([0.5, 0.5], 0.14, [0, 1, 0], unit)
    c3 = Circle([0.5, 0.8], 0.14, [0, 0, 1], unit)
    b1 = Rectangle([0.8, 0.2], 0.14, [1, 0, 0], unit, 0)
    b2 = Rectangle([0.8, 0.5], 0.14, [0, 1, 0], unit, 0)
    b3 = Rectangle([0.8, 0.8], 0.14, [0, 0, 1], unit, 0)

    objects = [s1, s2, s3, c1, c2, c3, b1, b2, b3]
    for obj in objects:
        obj.draw(env)

    plt.imshow(env)
    plt.show()

    centers = ([0.2, 0.2], [0.2, 0.5], [0.2, 0.8], [0.5, 0.2], [0.5, 0.5],
               [0.5, 0.8], [0.8, 0.2], [0.8, 0.5], [0.8, 0.8])

    plt.figure()

    env = np.zeros([unit, unit, 3])
    for center in centers:
        b1.center = np.array(center)
        b1.draw(env)
        plt.imshow(env)
        plt.pause(0.2)

#    import matplotlib.pyplot as plt
#    import matplotlib.patches as patches

    # ALTERNATIVE WAY OF PLOTTING: USE PATCHES
    # import matplotlib.pyplot as plt
    # import matplotlib.patches as patches

    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111, aspect='equal')
    # plt.xlim(0, 1)
    # plt.ylim(1, 0)
    # ax1.add_patch(patches.Rectangle((0.2, 0.2), 0.6, 0.6, fill=False))
    # ax1.add_patch(patches.Rectangle(center, x_size, y_size, color=color))
    # ax1.add_patch(patches.Circle(center, radius, color=color))
    # ax1.plot(point[0], point[1], 'wo')
