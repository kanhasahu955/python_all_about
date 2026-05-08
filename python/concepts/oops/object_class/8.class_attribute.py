class Circle:
    pi = 3.14159

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return self.pi * self.radius**2

    def circumference(self):
        return 2 * self.pi * self.radius

circle1 = Circle(5)
print(circle1.area())  # Output: 78.53975 (area of the circle with radius 5)
print(circle1.circumference())  # Output: 31.4159 (circumference of the circle with radius 5)
print(Circle.pi)  # Output: 3.14159 (accessing the class variable pi using the class name)
print(circle1.pi)  # Output: 3.14159 (accessing the class variable pi using the instance)
Circle.pi = 3.14  # Modifying the class variable pi
print(Circle.pi)  # Output: 3.14 (the class variable pi has been modified)
print(circle1.pi)  # Output: 3.14 (the instance circle1 also reflects the modified class variable pi)
circle2 = Circle(10)
print(circle2.area())  # Output: 314.159 (area of the circle with radius 10, using the modified class variable pi)
print(circle2.circumference())  # Output: 62.8 (circumference of the circle with radius 10, using the modified class variable pi)


class Product:
    default_discount = 0

    def __init__(self, price):
        self.price = price
        self.discount = Product.default_discount

    def set_discount(self, discount):
        self.discount = discount

    def net_price(self):
        return self.price * (1 - self.discount)


p1 = Product(100)
print(p1.net_price())
 # 100

p2 = Product(200)
p2.set_discount(0.05)
print(p2.net_price())
 # 190


class Circle:
    circle_list = []
    pi = 3.14159

    def __init__(self, radius):
        self.radius = radius
        # add the instance to the circle list
        self.circle_list.append(self)

    def area(self):
        return self.pi * self.radius**2

    def circumference(self):
        return 2 * self.pi * self.radius


c1 = Circle(10)
c2 = Circle(20)

print(len(Circle.circle_list))  # 2