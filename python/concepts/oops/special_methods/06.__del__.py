class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __del__(self):
        print('__del__ was called')


person = Person('John Doe', 23)
person = None

del person
