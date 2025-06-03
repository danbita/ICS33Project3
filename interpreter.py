import grin
from grin.calculator import Calculator
from grin.parsing import parse, _parse_line

class Interpreter:
    def __init__(self):
        self._lexemes = []
        self._lexemes_backup = []
        self._processed_input = None
        self._grin_tokens = []
        self._grin_labels = {}
        self._variables = {}
        self._return_index = []

    def process_input(self):
        """processes the input provided and turn it into grin tokens"""
        next_line = input()
        while True:
            self._lexemes.append(next_line)
            next_line = input()
            if next_line.strip() == '.':
                self._lexemes.append(next_line)
                break
        self._processed_input = parse(self._lexemes)

    def run(self):
        """runs the program"""
        for line in self._processed_input:
            self._grin_tokens.append(line)

        # generate labels
        for grin_token in self._grin_tokens:
            if grin_token[0].kind() == grin.GrinTokenKind.IDENTIFIER:
                value = grin_token[1].location().line() - 1
                label = grin_token[0].value()
                self._grin_labels[label] = value
                grin_token = grin_token[1:]

        # iterate over commands
        i = 0
        while i < len(self._grin_tokens):
            cur_str = ''

            if self._grin_tokens[i][0] == grin.GrinTokenKind.IDENTIFIER:
                value = self._grin_tokens[i][1].location().line()
                label = self._grin_tokens[i].pop(0).value()
                self._grin_tokens.pop(0)
                self._grin_labels[label] = value

            if self._grin_tokens[i][0].kind() == grin.GrinTokenKind.GOTO:
                next = self._grin_tokens[i][1].value()
                next_line = 0

                # if going to a label
                if next in self._grin_labels:
                    next_line = int(self._grin_labels[next]) - i
                # if going to a variable
                elif next in self._variables:
                    next_line = int(self._variables[next])
                else:
                    next_line = int(next)

                # if GOTO statement has no if condition
                if len(self._grin_tokens[i]) == 2:
                    self._return_index.insert(0, i + 1)
                    i += next_line
                    continue

                # if GOTO statement has an if condition
                elif len(self._grin_tokens[i]) > 2:
                    if self._grin_tokens[i][2].kind() == grin.GrinTokenKind.IF:
                        value_1 = 0
                        value_2 = 0

                        # if both comparison values are variables
                        if self._grin_tokens[i][3].value() in self._variables and \
                                self._grin_tokens[i][5].value() in self._variables:
                            value_1 = self._variables[self._grin_tokens[i][3].value()]
                            value_2 = self._variables[self._grin_tokens[i][5].value()]
                        elif self._grin_tokens[i][3].value() in self._variables and not \
                        self._grin_tokens[i][5].value() in self._variables:
                            value_1 = self._variables[self._grin_tokens[i][3].value()]
                            value_2 = self._grin_tokens[i][5].value()
                        elif not self._grin_tokens[i][3].value() in self._variables and \
                                self._grin_tokens[i][5].value() in self._variables:
                            value_1 = self._grin_tokens[i][3].value()
                            value_2 = self._variables[self._grin_tokens[i][5].value()]
                        else:
                            value_1 = self._grin_tokens[i][3].value()
                            value_2 = self._grin_tokens[i][5].value()

                        # determine if comparison is true
                        comparator = self._grin_tokens[i][4].kind()

                        if comparator == grin.GrinTokenKind.LESS_THAN:
                            if value_1 < value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue

                        elif comparator == grin.GrinTokenKind.LESS_THAN_OR_EQUAL:
                            if value_1 <= value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue

                        elif comparator == grin.GrinTokenKind.GREATER_THAN:
                            if value_1 > value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue

                        elif comparator == grin.GrinTokenKind.GREATER_THAN_OR_EQUAL:
                            if value_1 >= value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue

                        elif comparator == grin.GrinTokenKind.EQUAL:
                            if value_1 == value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue

                        elif comparator == grin.GrinTokenKind.NOT_EQUAL:
                            if not value_1 == value_2:
                                self._return_index.insert(0, i + 1)
                                i += next_line
                            else:
                                i += 1
                            continue
            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.RETURN:
                i = self._return_index.pop(0)
                continue

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.GOSUB:
                next = self._grin_tokens[i][1].value()
                if next in self._grin_labels:
                    next_line = int(self._grin_labels[next]) - i
                else:
                    next_line = int(next)
                self._return_index.insert(0, i + 1)
                i += next_line
                continue

                # if keyword is let
            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.LET:
                variable_name = self._grin_tokens[i][1].value()
                variable_value = None

                if self._grin_tokens[i][2].kind() == grin.GrinTokenKind.LITERAL_INTEGER:
                    variable_value = int(self._grin_tokens[i][2].value())
                elif self._grin_tokens[i][2].kind() == grin.GrinTokenKind.LITERAL_STRING:
                    variable_value = self._grin_tokens[i][2].value()
                elif self._grin_tokens[i][2].kind() == grin.GrinTokenKind.LITERAL_FLOAT:
                    variable_value = float(self._grin_tokens[i][2].value())

                self._variables[variable_name] = variable_value

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.PRINT:
                if self._grin_tokens[i][1].value() in self._variables:
                    print(self._variables[self._grin_tokens[i][1].value()])
                else:
                    print(self._grin_tokens[i][1].value)

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.INNUM:
                number = input()
                for char in number:
                    if not (char.isdigit() or char == '.' or char == '-'):
                        raise ValueError('Not a valid number')
                if '.' in number:
                    number = float(number)
                else:
                    number = int(number)
                self._variables[self._grin_tokens[i][1].value()] = number

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.INSTR:
                str = input()
                self._variables[self._grin_tokens[i][1].value()] = str

                # if input is doing math
            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.ADD:
                cur_val = self._variables[self._grin_tokens[i][1].value()]
                add_val = self._grin_tokens[i][2].value()
                if add_val in self._variables:
                    add_val = self._variables[add_val]
                calc = Calculator()
                self._variables[self._grin_tokens[i][1].value()] = calc.add(cur_val,
                                                                            add_val)

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.SUB:
                cur_val = self._variables[self._grin_tokens[i][1].value()]
                sub_val = self._grin_tokens[i][2].value()
                if sub_val in self._variables:
                    sub_val = self._variables[sub_val]
                calc = Calculator()
                self._variables[self._grin_tokens[i][1].value()] = calc.subtract(cur_val,
                                                                                 sub_val)

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.MULT:
                cur_val = self._variables[self._grin_tokens[i][1].value()]
                mult_val = self._grin_tokens[i][2].value()
                if mult_val in self._variables:
                    mult_val = self._variables[mult_val]
                calc = Calculator()
                self._variables[self._grin_tokens[i][1].value()] = calc.multiply(cur_val,
                                                                                 mult_val)

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.DIV:
                cur_val = self._variables[self._grin_tokens[i][1].value()]
                div_val = self._grin_tokens[i][2].value()
                if div_val in self._variables:
                    div_val = self._variables[div_val]
                calc = Calculator()
                self._variables[self._grin_tokens[i][1].value()] = calc.divide(cur_val,
                                                                               div_val)

            elif self._grin_tokens[i][0].kind() == grin.GrinTokenKind.DOT or \
                    self._grin_tokens[i][0].kind() == grin.GrinTokenKind.END:
                return

            i += 1



