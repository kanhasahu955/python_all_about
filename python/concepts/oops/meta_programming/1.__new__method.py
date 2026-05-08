# class Person:
#     # def __new__(cls, name):
#     #     print(f'Creating a new {cls.__name__} object...')
#     #     obj = object.__new__(cls)
#     #     return obj

#     # def __init__(self, name):
#     #     print(f'Initializing the person object...')
#     #     self.name = name


#     def __init__(self, name):
#         print(f'Initializing the person object...')
#         self.name = name

#     def __new__(cls, name):
#         print(f'Creating a new {cls.__name__} object...')
#         obj = object.__new__(cls)
#         return obj



# person = Person('John')


# class SquareNumber(int):
#     def __new__(cls, value):
#         return super().__new__(cls, value ** 2)


# class SquareNumber(int):
#     def __init__(self, value):
#         super().__init__(value ** 2) #object.__init__() takes exactly one argument (the instance to initialize)


# x = SquareNumber(3)
# print(x)  # 9
# print(isinstance(x, int)) # True


class Person:
    def __new__(cls, first_name, last_name):
        # create a new object
        obj = super().__new__(cls)

        # initialize attributes
        obj.first_name = first_name
        obj.last_name = last_name

        # inject new attribute
        obj.full_name = f'{first_name} {last_name}'
        return obj


person = Person('John', 'Doe')
print(person.full_name)

print(person.__dict__)