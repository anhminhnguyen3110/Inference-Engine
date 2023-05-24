import os
import random
import subprocess
from termcolor import colored
from Engine import Engine
from SympyTest import sympyTest
from common import fail
from constants import HORN_METHODS, NUM_SYMBOLS_HIGH, NUM_SYMBOLS_LOW, NUMBER_OF_HORN_CLAUSES, NUMBER_OF_SYMBOLS_FIX, PROBABILITY_OF_HORN_QUERY_BEING_AN_EXPRESSION, PROGRAM_PATH_1, PROGRAM_PATH_2, TEST_FILE_NAME, TEST_FOLDER_NAME


def generate_propositions(num_propositions):
    available_chars = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    propositions = random.sample(available_chars, num_propositions)
    return propositions

def generate_horn_clause(num_symbols, number_of_horn_clauses=10):
    symbols = generate_propositions(num_symbols)
    horn_clauses = set()
    single_literals = set()

    while len(horn_clauses) + len(single_literals) < number_of_horn_clauses:
        if random.random() <= PROBABILITY_OF_HORN_QUERY_BEING_AN_EXPRESSION:
            consequent = random.choice(symbols)
            antecedents = random.sample(symbols, random.randint(1, num_symbols - 1))
            antecedents = [a for a in antecedents if a != consequent]
            if len(antecedents) == 0:
                continue
            clause = f"{' & '.join(antecedents)} => {consequent}"
            horn_clauses.add(clause)
        else:
            consequent = random.choice(symbols)
            clause = f"{consequent}"
            single_literals.add(consequent)

    single_literals = '; '.join(single_literals)

    tell = '; '.join(horn_clauses)
    tell = f"{tell}; {single_literals}"
    ask = random.choice(list(symbols))
    return f'TELL\n{tell}\nASK\n{ask}\n'

def run_horn_tests_compared_between_two_programs(num_tests, num_symbols_low=10, num_symbols_high=20, number_of_horn_clauses=10, horn_clause = True):
    for i in range(num_tests):
        if(horn_clause):
            test = generate_horn_clause(num_symbols=random.randint(num_symbols_low, num_symbols_high), number_of_horn_clauses=number_of_horn_clauses)
        for method in HORN_METHODS:
            input_test = "./dist/input.txt"
            with open(input_test, "w") as f:
                f.write(test)
                
            result1 = subprocess.run([PROGRAM_PATH_1, method, input_test], capture_output=True)
            output1 = result1.stdout.decode().strip()
            
            result2 = subprocess.run([PROGRAM_PATH_2, method, input_test], capture_output=True)
            output2 = result2.stdout.decode().strip()
                
            if output1 == output2:
                print(f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASS', 'green')}")
            else:
                fail(test, method, output1, output2, i)
                    
# run_horn_tests_compared_between_two_programs(1000, NUM_SYMBOLS_LOW, NUM_SYMBOLS_HIGH, NUMBER_OF_HORN_CLAUSES)

def run_horn_tests(num_tests):
    os.makedirs(TEST_FOLDER_NAME, exist_ok=True)
    for i in range(num_tests):    
        test = generate_horn_clause(num_symbols=random.randint(NUM_SYMBOLS_LOW, NUM_SYMBOLS_HIGH), number_of_horn_clauses = NUMBER_OF_HORN_CLAUSES)
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
                print(f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASSED', 'green')}")
            else:
                fail(test, method, output1, output2, i)
    pass

run_horn_tests(1000)