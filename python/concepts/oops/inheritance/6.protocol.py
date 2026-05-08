from typing import List, Protocol


class Item(Protocol):
    quantity: float
    price: float


class Product:
    def __init__(self, name: str, quantity: float, price: float):
        self.name = name
        self.quantity = quantity
        self.price = price


def calculate_total(items: List[Item]) -> float:
    return sum([item.quantity * item.price for item in items])


# calculate total a product list
total = calculate_total([
    Product('A', 10, 150),
    Product('B', 5, 250)
])

print(total)