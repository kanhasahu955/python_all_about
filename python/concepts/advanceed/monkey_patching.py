def add_speech(cls):
    cls.speak = lambda self, message :print(message)
    return cls

class Robot:
    def __init__(self,name):
        self.name = name

Robot = add_speech(Robot)

robot = Robot('ashok')
robot.speak('hi')


def add_speech(cls):
    cls.speak = lambda self, message:print(message)
    return cls

@add_speech
class Robot:
    def __init__(self,name):
        self.name = name

robot = Robot('ashok')
robot.speak('hi')