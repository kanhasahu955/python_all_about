# class Employee:
#     def __init__(self, name, base_pay, bonus):
#         self.name = name
#         self.base_pay = base_pay
#         self.bonus = bonus

#     def get_pay(self):
#         return self.base_pay + self.bonus


# class SalesEmployee(Employee):
#     def __init__(self, name, base_pay, bonus, sales_incentive):
#         super().__init__(name, base_pay, bonus)
#         self.sales_incentive = sales_incentive

#     def get_pay(self):
#         return super().get_pay() + self.sales_incentive


# if __name__ == '__main__':
#     sales_employee = SalesEmployee('John', 5000, 1000, 2000)
#     print(sales_employee.get_pay())  # 8000



class Employee:
    def __init__(self, name, base_pay, bonus):
        self.name = name
        self.base_pay = base_pay
        self.bonus = bonus

    def get_pay(self):
        return self.base_pay + self.bonus


class SalesEmployee(Employee):
    def __init__(self, name, base_pay, bonus, sales_incentive):
        super().__init__(name, base_pay, bonus)
        self.sales_incentive = sales_incentive

    def get_pay(self):
        return super().get_pay() + self.sales_incentive


if __name__ == '__main__':
    sales_employee = SalesEmployee('John', 5000, 1000, 2000)
    print(sales_employee.get_pay())  # 8000