# class Point2D:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         return f'Point2D({self.x},{self.y})'
    
# point = Point2D(0, 0)
# print(point.__dict__)

# from pprint import pprint


# class Point2D:
#     __slots__ = ('x', 'y')

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         return f'Point2D({self.x},{self.y})'
    
# point = Point2D(0, 0)
# # print(point.__dict__)
# print(point.__slots__)
# # point.z = 0

# Point2D.color = 'black'
# pprint(Point2D.__dict__)


# class Point2D:
#     __slots__ = ('x', 'y')

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         return f'Point2D({self.x},{self.y})'


# class Point3D(Point2D):
#     def __init__(self, x, y, z):
#         super().__init__(x, y)
#         self.z = z


# if __name__ == '__main__':
#     point = Point3D(10, 20, 30)
#     print(point.__dict__)


class Shape:
    pass


class Point2D(Shape):
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    # use both slots and dict to store instance attributes
    point = Point2D(10, 10)
    print(point.__slots__)
    print(point.__dict__)

    # can add the attribute at runtime
    point.color = 'black'
    print(point.__dict__)