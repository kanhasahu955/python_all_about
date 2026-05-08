# # define class
# class Person:
#     pass

# # create object
# person1 = Person()
# person2= Person()
# print(person1,person2)
# print(type(person1), type(person2))

# person1.name = "Alice"
# person1.age = 30

# print(person1.name, person1.age)


# -----------------------------------------iinstance attribute----------------------------------------
# class Car:
#     def __init__(self, make, model):
#         self.make = make
#         self.model = model

# car1 = Car("Toyota", "Camry")
# print(car1.make, car1.model)

# -----------------------------------------instance method----------------------------------------
# class Car:
#     def __init__(self, make, model):
#         self.make = make
#         self.model = model
#     def display_info(self):        
#         print(f"Car Make: {self.make}, Model: {self.model}")

# car1 = Car("Toyota", "Camry")
# car1.display_info()

# -----------------------------------------class attribute----------------------------------------
# class Car:
#     wheels = 4  # class attribute
#     def __init__(self, make, model):
#         self.make = make
#         self.model = model
#         Car.wheels += 1  # This is an instance attribute
# car1 = Car("Toyota", "Camry")
# car2 = Car("Honda", "Civic")

# print(car1.wheels)  # Accessing instance attribute
# print(car2.wheels)  # Accessing instance attribute
# print(Car.wheels)   # Accessing class attribute directly from the class


# -----------------------------------------class method----------------------------------------
# class Person:
#     counter = 0  # class attribute to count instances
#     def __init__(self, name):
#         self.name = name
#         Person.counter += 1  # Increment the counter when a new instance is created 
#     @classmethod
#     def create_anonymous(cls):
#         return Person('ashok sahu')
    
# anonymous = Person.create_anonymous()
# print(anonymous.name)  # Output: Anonymous
# print(Person.counter)  # Output: 1

# -----------------------------------------static method----------------------------------------
# class TemperatureConverter:
#     @staticmethod
#     def celsius_to_fahrenheit(celsius):
#         return (celsius * 9/5) + 32

#     @staticmethod
#     def fahrenheit_to_celsius(fahrenheit):
#         return (fahrenheit - 32) * 5/9

# temp_c = TemperatureConverter.celsius_to_fahrenheit(25)
# temp_f = TemperatureConverter.fahrenheit_to_celsius(77)

# print(f"25 degrees Celsius is {temp_c} degrees Fahrenheit.")
# print(f"77 degrees Fahrenheit is {temp_f} degrees Celsius.")