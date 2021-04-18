__author__ = 'Peter LeBlanc'

''' This is the circle class
This is a development toolkit tutorial from pycon

Circuitous, LLC -
An Advanced Circle Analytics Company

'''
#External Libraries
import math


class Circle(object):
    'An advanced circle analytic toolkit'

    # flyweight design pattern suppresses
    # the instance dictionary

    #__slots__ = ['diameter']   # This should only me used for scaling, functionality lost


    version = '0.1'     # class variable

    def __init__(self, radius):
            self.radius = radius  #instance variable

    def area(self):
        'Perform quadrature on a shape of uniform radius'
        return math.pi * self.radius ** 2.0

    def perimeter(self):    #new function added for customer
        return 2.0 * math.pi * self.radius

    @property       #convert dotted access to method calls
    def radius(self):
        'Radius of a circle'
        return self.diameter / 2.0

    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.0


    @staticmethod       # Attach function to classes
    def angle_to_grade(angle):      #new function added for customer
        'Converts angle in degree to a percentage grade'
        return math.tan(math.radians(angle)) * 100.0

    @classmethod        # alternative constructor added for a customer
    def from_bbd(cls, bbd):
        'Construct a circle from a bounding box diagonal'
        radius = bbd / 2.0 / math.sqrt(2.0)
        return cls(radius)


'''
    # Tutorial
    print 'Circuituous version', Circle.version
    c = Circle(10)
    print 'A circle of radious', c.radius
    print 'has an area of', c.area()
'''
