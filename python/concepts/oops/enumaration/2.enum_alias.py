# from enum import Enum


# class Color(Enum):
#     RED = 1
#     CRIMSON = 1
#     SALMON = 1
#     GREEN = 2
#     BLUE = 3

# # print(Color.RED is Color.CRIMSON)
# # print(Color.RED is Color.SALMON)

# # print(Color(1))

# for color in Color:
#     print(color)


# from enum import Enum
# from pprint import pprint


# class Color(Enum):
#     RED = 1
#     CRIMSON = 1
#     SALMON = 1
#     GREEN = 2
#     BLUE = 3


# pprint(Color.__members__)


# from enum import Enum


# class ResponseStatus(Enum):
#     # in progress
#     IN_PROGRESS = 1
#     REQUESTING = 1
#     PENDING = 1

#     # success
#     SUCCESS = 2
#     OK = 2
#     FULFILLED = 2

#     # error
#     ERROR = 3
#     NOT_OK = 3
#     REJECTED = 3

# code = 'OK'
# if ResponseStatus[code] is ResponseStatus.SUCCESS:
#     print('The request completed successfully')


from enum import Enum


# class Day(Enum):
#     MON = 'Monday'
#     TUE = 'Tuesday'
#     WED = 'Wednesday'
#     THU = 'Thursday'
#     FRI = 'Friday'
#     SAT = 'Saturday'
#     SUN = 'Sunday'

class Day(Enum):
    MON = 'Monday'
    TUE = 'Monday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'
    SAT = 'Saturday'
    SUN = 'Sunday'


# import enum

# from enum import Enum


# @enum.unique #duplicate values found in <enum 'Day'>: TUE -> MON
# class Day(Enum):
#     MON = 'Monday'
#     TUE = 'Monday'
#     WED = 'Wednesday'
#     THU = 'Thursday'
#     FRI = 'Friday'
#     SAT = 'Saturday'
#     SUN = 'Sunday'