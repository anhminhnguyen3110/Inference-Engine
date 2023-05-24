import os
import random
import subprocess
import sys
from sympy import parse_expr, to_cnf
from termcolor import colored
from CNF_Converter import cnf_converter
from Engine import Engine
from GenGeneralClauseTest import generate_random_tests
from GenHornClauseTest import generate_horn_clause
from SympyTest import sympyTest
from common import (
    construct_expression_tree,
    fail,
    infix_to_postfix,
    postfix_to_infix,
    prefix_to_infix,
)
from constants import (
    DEPTH,
    GENERAL_METHODS,
    HORN_METHODS,
    NUM_SYMBOLS_HIGH,
    NUM_SYMBOLS_LOW,
    NUMBER_OF_GENERAL_CLAUSES,
    NUMBER_OF_HORN_CLAUSES,
    NUMBER_OF_SYMBOLS_FIX,
    PROGRAM_PATH_1,
    PROGRAM_PATH_2,
    TEST_FILE_NAME,
    TEST_FOLDER_NAME,
)


def run_general_test(number_of_test=20):
    os.makedirs(TEST_FOLDER_NAME, exist_ok=True)
    for i in range(number_of_test):
        test = generate_random_tests(NUMBER_OF_SYMBOLS_FIX, NUMBER_OF_GENERAL_CLAUSES, DEPTH)
        with open(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}", "w") as f:
            f.write(test)
        agent = Engine()

        output2 = sympyTest(test)

        agent.knowledge_base.read_input_file(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}")
        for method in GENERAL_METHODS:
            method = method.lower()
            agent.set_method(method)
            result = agent.set_up_algorithm()
            if result[1] == 0:
                print(f"Test {colored(str(i+1), 'cyan')}: Invalid knowledge base")
                break
            output1 = result[0]
            if output1 == output2:
                print(
                    f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASSED', 'green')}"
                )
            else:
                fail(test, method, output1, output2, i)


def run_horn_tests_compared_between_two_programs(
    num_tests, num_symbols_low=10, num_symbols_high=20, number_of_horn_clauses=10, horn_clause=True
):
    for i in range(num_tests):
        if horn_clause:
            test = generate_horn_clause(
                num_symbols=random.randint(num_symbols_low, num_symbols_high),
                number_of_horn_clauses=number_of_horn_clauses,
            )
        for method in HORN_METHODS:
            input_test = "./dist/input.txt"
            with open(input_test, "w") as f:
                f.write(test)

            result1 = subprocess.run([PROGRAM_PATH_1, method, input_test], capture_output=True)
            output1 = result1.stdout.decode().strip()

            result2 = subprocess.run([PROGRAM_PATH_2, method, input_test], capture_output=True)
            output2 = result2.stdout.decode().strip()

            if output1 == output2:
                print(
                    f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASS', 'green')}"
                )
            else:
                fail(test, method, output1, output2, i)


def run_horn_tests(num_tests):
    os.makedirs(TEST_FOLDER_NAME, exist_ok=True)
    for i in range(num_tests):
        test = generate_horn_clause(
            num_symbols=random.randint(NUM_SYMBOLS_LOW, NUM_SYMBOLS_HIGH),
            number_of_horn_clauses=NUMBER_OF_HORN_CLAUSES,
        )
        with open(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}", "w") as f:
            f.write(test)
        agent = Engine()

        output2 = sympyTest(test)
        for method in HORN_METHODS:
            method = method.lower()
            agent.set_method(method)
            agent.knowledge_base.read_input_file(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}")
            result = agent.set_up_algorithm()
            output1 = result[0]
            if output1 == output2:
                print(
                    f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASSED', 'green')}"
                )
            else:
                fail(test, method, output1, output2, i)
    pass


def print_test(exp):
    if exp:
        print("Test " + colored("PASSES", "green"))
        pass
    else:
        print("Test " + colored("FAILS", "red"))
        pass


def testCNF(sequences):
    sequences = sequences.split("; ")
    for sequence in sequences:
        if sequence == " ":
            continue
        sequence_x = infix_to_postfix(sequence)
        expression = postfix_to_infix(sequence_x)
        sym_converter = to_cnf(expression)
        my_converter = prefix_to_infix(
            cnf_converter(construct_expression_tree(expression.replace("|", "||")))
        )
        result = sym_converter.equals(
            parse_expr(my_converter.replace("||", "|").replace("=>", ">>"))
        )
        print_test(result)


def gentest():
    if len(sys.argv) <= 1:
        print("Invalid input")
        return
    else:
        test = sys.argv[1]
        test = test.lower()
        if test == "cnf":
            for _ in range(100000):
                input_file = generate_random_tests(
                    NUMBER_OF_SYMBOLS_FIX, NUMBER_OF_GENERAL_CLAUSES, DEPTH
                ).split("; ")[1]
                testCNF(input_file)
        elif test == "horn":
            run_horn_tests(1000)
        elif test == "general":
            run_general_test(1000)
        elif test == "other_program":
            run_horn_tests_compared_between_two_programs(
                1000, NUM_SYMBOLS_LOW, NUM_SYMBOLS_HIGH, NUMBER_OF_HORN_CLAUSES
            )
        else:
            print("Invalid input")
            return
    return


gentest()
