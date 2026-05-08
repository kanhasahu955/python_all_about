# class Car:
#     def go(self):
#         print('Going')

# class Flyable:
#     def fly(self):
#         print('Flying')        


# class FlyingCar(Flyable, Car):
#     pass

# if __name__ == '__main__':
#     fc = FlyingCar()
#     fc.go()
#     fc.fly()



# Method resolution order (MRO)
# class Car:
#     def start(self):
#         print('Start the Car')

#     def go(self):
#         print('Going')


# class Flyable:
#     def start(self):
#         print('Start the Flyable object')

#     def fly(self):
#         print('Flying')


# class FlyingCar(Flyable, Car):
#     def start(self):
#         super().start()
        
# if __name__ == '__main__':
#     car = FlyingCar()
#     car.start()    
#     print(FlyingCar.__mro__)
    
   
class Car:
    def __init__(self, door, wheel):
        self.door = door
        self.wheel = wheel

    def start(self):
        print('Start the Car')

    def go(self):
        print('Going')

class Flyable:
    def __init__(self, wing):
        self.wing = wing

    def start(self):
        print('Start the Flyable object')

    def fly(self):
        print('Flying')

class FlyingCar(Flyable, Car):
    def __init__(self, door, wheel, wing):
        super().__init__(wing=wing)
        self.door = door
        self.wheel = wheel

    def start(self):
        super().start()

if __name__ == '__main__':
    car = FlyingCar('door', 'wheel', 'wing')
    car.start()    
    print(FlyingCar.__mro__)