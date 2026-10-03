'''
Problem Statement: Implement a recursive expression evaluator for integer expressions containing non-negative integers, +, -, *,
parentheses and variable references. Each variable may be defined by another expression. Detect cyclic variable dependencies and
report CYCLE. Use memoization so that repeated variable evaluations are not recomputed.
'''

v = int(input())

variables = {}

for i in range(v):
    line = input()
    name, expression = line.split("=", 1)
    variables[name.strip()] = expression.strip()

expression = input().strip()

memo = {}
visiting = set()

def evaluate_variable(name):
    if name in memo:
        return memo[name]

    if name in visiting:
        raise Exception("CYCLE")

    if name not in variables:
        raise Exception("INVALID")

    visiting.add(name)

    value = evaluate_expression(variables[name])

    visiting.remove(name)
    memo[name] = value

    return value


def evaluate_expression(expression):
    expression = expression.replace(" ", "")

    values = []
    operators = []

    i = 0

    while i < len(expression):

        if expression[i].isdigit():
            number = 0

            while i < len(expression) and expression[i].isdigit():
                number = number * 10 + int(expression[i])
                i += 1

            values.append(number)
            continue

        if expression[i].isalpha() or expression[i] == "_":
            name = ""

            while i < len(expression) and (expression[i].isalnum() or expression[i] == "_"):
                name += expression[i]
                i += 1

            values.append(evaluate_variable(name))
            continue

        if expression[i] == "(":
            operators.append(expression[i])

        elif expression[i] == ")":
            while operators and operators[-1] != "(":
                apply_operator(values, operators)

            if not operators:
                raise Exception("INVALID")

            operators.pop()

        elif expression[i] in "+-*":
            while (operators and operators[-1] != "(" and
                   precedence(operators[-1]) >= precedence(expression[i])):
                apply_operator(values, operators)

            operators.append(expression[i])

        else:
            raise Exception("INVALID")

        i += 1

    while operators:
        if operators[-1] == "(":
            raise Exception("INVALID")

        apply_operator(values, operators)

    if len(values) != 1:
        raise Exception("INVALID")

    return values[0]


def precedence(operator):
    if operator in "+-":
        return 1

    if operator == "*":
        return 2

    return 0


def apply_operator(values, operators):
    if len(values) < 2:
        raise Exception("INVALID")

    b = values.pop()
    a = values.pop()
    operator = operators.pop()

    if operator == "+":
        values.append(a + b)

    elif operator == "-":
        values.append(a - b)

    elif operator == "*":
        values.append(a * b)


try:
    answer = evaluate_expression(expression)
    print(answer)

except Exception as e:
    if str(e) == "CYCLE":
        print("CYCLE")
    else:
        print("INVALID")
