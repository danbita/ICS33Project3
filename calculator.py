class Calculator:
    def __init__(self):
        pass

    def add(self, a, b):
        """method for adding two numbers"""
        if type(a) is int and type(b) is int:
            return int(a + b)
        elif type(a) is float and type(b) is float:
            return float(a + b)
        elif type(a) is int and type(b) is float:
            return float(a) + b
        elif type(a) is float and type(b) is int:
            return a + float(b)
        elif type(a) is str and type(b) is str:
            return a + b
        else:
            raise ValueError('Invalid inputs for addition')

    def subtract(self, a, b):
        """method for subtracting one number from another"""
        if type(a) is int and type(b) is int:
            return int(a - b)
        elif type(a) is float and type(b) is float:
            return float(a - b)
        elif type(a) is int and type(b) is float:
            return float(a) - b
        elif type(a) is float and type(b) is int:
            return a - float(b)
        else:
            raise ValueError('Invalid inputs for subtraction')

    def multiply(self, a, b):
        """method for multiplying two numbers"""
        if type(a) is int and type(b) is int:
            return int(a * b)
        elif type(a) is float and type(b) is float:
            return float(a * b)
        elif type(a) is int and type(b) is float:
            return float(a) * b
        elif type(a) is float and type(b) is int:
            return a * float(b)
        elif type(a) is str and type(b) is int:
            return a * b
        elif type(a) is int and type(b) is str:
            return a * b
        else:
            raise ValueError('Invalid inputs for multiplication')

    def divide(self, a, b):
        """method for dividing one number from another"""
        if type(a) is int and type(b) is int:
            return int(a / b)
        elif type(a) is float and type(b) is float:
            return float(a / b)
        elif type(a) is int and type(b) is float:
            return float(a) / b
        elif type(a) is float and type(b) is int:
            return a / float(b)
        else:
            raise ValueError('Invalid inputs for division')