# from enum import Enum


# class PaymentStatus(Enum):
#     PENDING = 1
#     COMPLETED = 2
#     REFUNDED = 3

#     def __str__(self):
#         return f'{self.name.lower()}({self.value})'

#     def __eq__(self, other):
#         if isinstance(other, int):
#             return self.value == other

#         if isinstance(other, PaymentStatus):
#             return self is other

#         return False


# if PaymentStatus.PENDING == 1:
#     print('The payment is pending.')


# from enum import Enum
# from functools import total_ordering


# @total_ordering
# class PaymentStatus(Enum):
#     PENDING = 1
#     COMPLETED = 2
#     REFUNDED = 3

#     def __str__(self):
#         return f'{self.name.lower()}({self.value})'

#     def __eq__(self, other):
#         if isinstance(other, int):
#             return self.value == other

#         if isinstance(other, PaymentStatus):
#             return self is other

#         return False

#     def __lt__(self, other):
#         if isinstance(other, int):
#             return self.value < other

#         if isinstance(other, PaymentStatus):
#             return self.value < other.value

#         return False


# # compare with an integer
# status = 1
# if status < PaymentStatus.COMPLETED:
#     print('The payment has not completed')

# # compare with another member
# status = PaymentStatus.PENDING
# if status >= PaymentStatus.COMPLETED:
#     print('The payment is not pending')


# from enum import Enum
# from functools import total_ordering


# @total_ordering
# class PaymentStatus(Enum):
#     PENDING = 1
#     COMPLETED = 2
#     REFUNDED = 3

#     def __str__(self):
#         return f'{self.name.lower()}({self.value})'

#     def __eq__(self, other):
#         if isinstance(other, int):
#             return self.value == other

#         if isinstance(other, PaymentStatus):
#             return self is other

#         return False

#     def __lt__(self, other):
#         if isinstance(other, int):
#             return self.value < other

#         if isinstance(other, PaymentStatus):
#             return self.value < other.value

#         return False

#     def __bool__(self):
#         if self is self.COMPLETED:
#             return True

#         return False


# for member in PaymentStatus:
#     print(member, bool(member))


from enum import Enum
from functools import total_ordering


@total_ordering
class OrderedEnum(Enum):
    def __lt__(self, other):
        if isinstance(other, OrderedEnum):
            return self.value < other.value
        return NotImplemented


class ApprovalStatus(OrderedEnum):
    PENDING = 1
    IN_PROGRESS = 2
    APPROVED = 3


status = ApprovalStatus(2)
if status < ApprovalStatus.APPROVED:
    print('The request has not been approved.')