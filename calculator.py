from __future__ import annotations
from typing import Any
import logging

log_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

try:
    logging.basicConfig(level=logging.DEBUG, filename="calculator.log", filemode="a", format=log_template)
except Exception as er:
    print("no logging")
    raise er

AnyNumber: Any[int, float]


class CalculateError(Exception):
    txt = ""

    def __init__(self):
        super().__init__(self.txt)


class NegativeBaseError(CalculateError):
    txt = "Power must be an integer if the base of exponentiation is negative"


class ZeroToThePowerOfZeroError(CalculateError):
    txt = "0^0 is undefined"


class UnIntegerError(CalculateError):
    txt = "Degree must be an integer"


class RootFromNegativeError(CalculateError):
    txt = "Root base must be non-negative"


class NegativeRootError(CalculateError):
    txt = "Root degree must be positive"


class NumberInputsError(Exception):
    def __init__(self):
        super(NumberInputsError, self).__init__("Wrong number of input elements. Must be 2 or 3")


class Calculation:

    @staticmethod
    def addition(number1: AnyNumber, number2: AnyNumber):
        logging.info(f"{number1} + {number2}")
        result_number: AnyNumber = number1 + number2
        return result_number

    @staticmethod
    def subtraction(number1: AnyNumber, number2: AnyNumber):
        logging.info(f"{number1} - {number2}")
        result_number: AnyNumber = number1 - number2
        return result_number

    @staticmethod
    def multiplying(number1: AnyNumber, number2: AnyNumber):
        logging.info(f"{number1} * {number2}")
        result_number: AnyNumber = number1 * number2
        return result_number

    @staticmethod
    def division(number1: AnyNumber, number2: AnyNumber):
        try:
            logging.info(f"{number1} / {number2}")
            result_number: AnyNumber = number1 / number2
            return result_number
        except ZeroDivisionError:
            logging.error(f"Denominator is {number2}")
            raise ZeroDivisionError("Denominator must be not zero")

    @staticmethod
    def exponentiation(base: AnyNumber, power: AnyNumber):
        if base < 0 and int(power) != power:
            logging.error(f"Power ({power}) is not an integer if the base ({base}) of exponentiation is negative")
            raise NegativeBaseError
        elif base == 0 and power == 0:
            logging.error(f"0^0 is undefined")
            raise ZeroToThePowerOfZeroError
        try:
            logging.info(f"{base} ^ {power}")
            result_number = pow(base, power)
            return result_number
        except ZeroDivisionError as error:
            logging.error(f"Zero is raised to the power of a negative number ({power})")
            raise ZeroDivisionError("Zero cannot be raised to the power of a negative number")

    @staticmethod
    def root(number: AnyNumber, degree: AnyNumber):
        if int(degree) != degree:
            logging.error(f"Root degree ({degree}) is not an integer")
            raise UnIntegerError
        if degree < 1:
            logging.error(f"Root degree ({degree}) is negative")
            raise NegativeRootError
        if number < 0:
            logging.error(f"Root base ({number}) is negative")
            raise RootFromNegativeError
        logging.info(f"{number} r {degree}")
        result_number = pow(number, pow(degree, -1))
        return result_number

    @staticmethod
    def get_percent(number: AnyNumber, percent: AnyNumber):
        logging.info(f"{number} % {percent}")
        result_number = percent * number / 100
        return result_number


class Calculator:
    OPERATORS = {"+": Calculation.addition, "-": Calculation.subtraction, "*": Calculation.multiplying,
                 "/": Calculation.division, "^": Calculation.exponentiation, "r": Calculation.root,
                 "%": Calculation.get_percent}

    def __init__(self):
        self.result = 0

    @classmethod
    def calculate(cls, number1: AnyNumber, action: str, number2: AnyNumber):
        if action not in cls.OPERATORS:
            logging.error("Undefined operator")
            raise ValueError(f"Operator must be from {cls.OPERATORS.keys()}")
        try:
            result_number = cls.OPERATORS[action](number1, number2)
            return result_number
        except CalculateError as er:
            raise er

    def input_output(self):
        input_str = input()
        input_args = input_str.split()
        if len(input_args) not in (0, 2, 3):
            logging.error("Input number is not real")
            raise NumberInputsError
        if len(input_args) != 0:
            try:
                if len(input_args) == 2:
                    self.result = self.calculate(self.result, input_args[0], float(input_args[1]))
                elif len(input_args) == 3:
                    self.result = self.calculate(float(input_args[0]), input_args[1], float(input_args[2]))
                print(self.result, end=" ")
            except (CalculateError, ValueError, ZeroDivisionError) as er:
                print(er.args[0])
                print(self.result, end=" ")

    def run(self):

        while True:
            try:
                self.input_output()
            except NumberInputsError as er:
                print(er.args[0])


calc = Calculator()
calc.run()



