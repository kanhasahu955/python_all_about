# By definition, an enumeration is a set of members that have associated unique constant values. Enumeration is often called enum.

# Python provides you with the enum module that contains the Enum type for defining new enumerations. And you define a new enumeration type by subclassing the Enum class.


# from enum import Enum


# class Color(Enum):
#     RED = 1
#     GREEN = 2
#     BLUE = 3

# print(type(Color.RED))
# print(isinstance(Color.RED, Color))

# print(Color.RED.name)
# print(Color.RED.value)


from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    
# print(type(Color.RED))    
# print(isinstance(Color.RED, Color))

# print(Color.RED.name)
# print(Color.RED.value)

# if Color.RED in Color:
#     print('Yes')

# if Color.RED is Color.BLUE:
#     print('red is blue')
# else:
#     print('red is not blue')

# if Color.RED == 1:
#     print('Color.RED == 1')
# else:
#     print('Color.RED != 1')


# rgb = {
#     Color.RED: '#ff0000',
#     Color.GREEN: '#00ff00',
#     Color.BLUE: '#0000ff'
# }
# # print(Color['RED'])
# # print(Color.RED)
# # print(Color(1))
# # print(Color['RED'] == Color(1))

# for color in Color:
#     print(color) 

# print(list(Color))

# Color['YELLOW'] = 4 #'EnumType' object does not support item assignment


# class Color(Enum):
#     pass


# class RGB(Color):
#     RED = 1
#     GREEN = 2
#     BLUE = 3

# class ResponseStatus(Enum):
#     PENDING = 'pending'
#     FULFILLED = 'fulfilled'
#     REJECTED = 'rejected'

# response = '''{
#     "status":"fulfilled"
# }'''



# import json

# data = json.loads(response)
# status = data['status']
# print(status)

# print(ResponseStatus(status))

# from enum import Enum
# import json


# class ResponseStatus(Enum):
#     PENDING = 'pending'
#     FULFILLED = 'fulfilled'
#     REJECTED = 'rejected'


# response = '''{
#     "status":"fulfilled"
# }'''

# data = json.loads(response)
# status = data['status']

# print(ResponseStatus(status))



from enum import Enum
import json


class ResponseStatus(Enum):
    PENDING = 'pending'
    FULFILLED = 'fulfilled'
    REJECTED = 'rejected'


response = '''{
    "status":"ok"
}'''

data = json.loads(response)
status = data['status']

try:
    if ResponseStatus(status) is ResponseStatus.FULFILLED:
        print('The request completed successfully')
except ValueError as error:
    print(error)