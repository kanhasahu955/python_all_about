# def currency(fn):
#     def wrapper(*args, **kwargs):
#         result = fn(*args,**kwargs)
#         return f'{result}'
#     return wrapper

# @currency
# def net_price(price,tax):
#     """ calculate the net price from price and tax
#     Arguments:
#         price: the selling price
#         tax: value added tax or sale tax
#     Return
#         the net price
#     """
#     return price*(1+ tax)


# print(net_price(100, 0.05))
# print(net_price.__name__)
# # help(net_price)

# from functools import wraps

# def currency(fn):
#     @wraps(fn)
#     def wrapper(*args,**kwargs):
#         result = fn(*args,**kwargs)
#         return f'{result}'
#     return wrapper

# @currency
# def net_price(price,tax):
#     """ calculate the net price from price and tax
#     Arguments:
#         price: the selling price
#         tax: value added tax or sale tax
#     Return
#         the net price
#     """
#     return price * (1 + tax)

# # help(net_price)
# print(net_price(100,0.05))
# print(net_price.__name__)







# from functools import wraps

# def repeat(times):
#     def decorate(fn):
#         @wraps(fn)
#         def wrapper(*args,**kwargs):
#             for _ in range(times):
#                 result = fn(*args,**kwargs)
#             return result
#         return wrapper
#     return decorate


# @repeat(3)
# def say(msg):
#     print(msg)

# say('hi')

from functools import wraps

class Star:
    def __init__(self,n):
        self.n = n
    
    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args,**kwargs):
            print(self.n * "*")
            result = fn(*args,**kwargs)
            print(result)
            print(self.n * '*')
            return result
        return wrapper
    

@Star(5)
def add(a,b):
    return a+b

add(1,2)