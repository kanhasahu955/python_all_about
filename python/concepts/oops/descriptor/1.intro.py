# class Person:
#     def __init__(self, first_name, last_name):
#         self.first_name = first_name
#         self.last_name = last_name

#     @property
#     def first_name(self):
#         return self._first_name

#     @first_name.setter
#     def first_name(self, value):
#         if not isinstance(value, str):
#             raise ValueError('The first name must a string')

#         if len(value) == 0:
#             raise ValueError('The first name cannot be empty')

#         self._first_name = value

#     @property
#     def last_name(self):
#         return self._last_name

#     @last_name.setter
#     def last_name(self, value):
#         if not isinstance(value, str):
#             raise ValueError('The last name must a string')

#         if len(value) == 0:
#             raise ValueError('The last name cannot be empty')

#         self._last_name = value



# class RequiredString:
#     def __set_name__(self, owner, name):
#         self.property_name = name


#     def __get__(self, instance, owner):
#         if instance is None:
#             return self

#         return instance.__dict__[self.property_name] or None

#     def __set__(self, instance, value):
#         if not isinstance(value, str):
#             raise ValueError(f'The {self.property_name} must be a string')

#         if len(value) == 0:
#             raise ValueError(f'The {self.property_name} cannot be empty')

#         instance.__dict__[self.property_name] = value

# class Person:
#     first_name = RequiredString()
#     last_name = RequiredString()

# try:
#     person = Person()
#     person.first_name = ''
# except ValueError as e:
#     print(e)




# Descriptor protocol 
# In Python, the descriptor protocol consists of three methods:

# __get__ gets an attribute value
# __set__ sets an attribute value
# __delete__ deletes an attribute
# Optionally, a descriptor can have the __set_name__ method that sets an attribute on an instance of a class to a new value.



class RequiredString:
    def __set_name__(self, owner, name):
        print(f'__set_name__ was called with owner={owner} and name={name}')
        self.property_name = name

    def __get__(self, instance, owner):
        print(f'__get__ was called with instance={instance} and owner={owner}')
        if instance is None:
            return self

        return instance.__dict__[self.property_name] or None

    def __set__(self, instance, value):
        print(f'__set__ was called with instance={instance} and value={value}')

        if not isinstance(value, str):
            raise ValueError(f'The {self.property_name} must a string')

        if len(value) == 0:
            raise ValueError(f'The {self.property_name} cannot be empty')

        instance.__dict__[self.property_name] = value


class Person:
    first_name = RequiredString()
    last_name = RequiredString()

first_name = RequiredString()
person = Person()
person.first_name = 'Alice'
print(person.first_name)
first_name.__set_name__(Person, 'first_name')

from pprint import pprint

pprint(Person.__dict__)