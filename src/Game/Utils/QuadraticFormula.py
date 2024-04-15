import math


class QuadraticFormula:
    @staticmethod
    def calculate(a: float, b: float, c: float) -> float:
        delta = b ** 2 - 4 * a * c
        # print(delta)
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        return (x1, x2)