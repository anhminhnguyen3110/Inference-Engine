import math
import random
import os
from termcolor import colored

from constants import OPERANDS

def generate_propositions(num_propositions):
    propositions = []
    for i in range(num_propositions):
        proposition = chr(ord('a') + i)
        propositions.append(proposition)
    return propositions

def generate_random_expression(propositions, depth):
    if depth == 0 or len(propositions) == 1:
        return random.choice(propositions)
    else:
        operator = random.choices(list(OPERANDS.keys()), weights=list(OPERANDS.values()))[0]
        if operator == '~':
            operand = generate_random_expression(propositions, depth - 1)
            return f"~{operand}"
        else:
            num_operands = random.randint(2, len(propositions))
            operands = random.sample(propositions, num_operands)
            subexpressions = [generate_random_expression([p for p in propositions if p != op], depth - 1) for op in operands]
            expression = f" {operator} ".join(subexpressions)
            return f"({expression})"

def generate_general_clause(num_propositions, depth, number_of_expression):
    propositions = generate_propositions(num_propositions)
    expressions = []
    for _ in range(number_of_expression):
        expression = generate_random_expression(propositions, depth)
        expressions.append(expression)
    return "; ".join(expressions)

def write_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def run_tests(num_tests, test_folder, num_propositions, depth, max_num_expressions, function1, function2):
    os.makedirs(test_folder, exist_ok=True)
    for i in range(num_tests):
        for num_expressions in range(1, max_num_expressions + math.floor(i/5)):
            program = generate_general_clause(num_propositions, depth, num_expressions)
            
            output1 = function1(program)
            output2 = function2(program)
            
            if output1 != output2:
                print(f"Test {colored(str(i+1), 'cyan')} with {num_expressions} expressions: {colored('FAILED', 'red')}")
                
                test_input_file = os.path.join(test_folder, f"test_{i+1}_expressions_{num_expressions}_input.txt")
                test_output1_file = os.path.join(test_folder, f"test_{i+1}_expressions_{num_expressions}_output1.txt")
                test_output2_file = os.path.join(test_folder, f"test_{i+1}_expressions_{num_expressions}_output2.txt")
                
                write_to_file(test_input_file, program)
                write_to_file(test_output1_file, output1)
                write_to_file(test_output2_file, output2)
            else:
                print(f"Test {colored(str(i+1), 'cyan')} with {num_expressions} expressions: {colored('PASS', 'green')}")

num_tests = 2
test_folder = "./dist"
num_propositions = 4
depth = 2
max_num_expressions = 4

def function1(program):
    return program

def function2(program):
    return program

run_tests(num_tests, test_folder, num_propositions, depth, max_num_expressions, function1, function2)
