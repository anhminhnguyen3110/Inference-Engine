import os
import random
from termcolor import colored
from Engine import Engine
from SympyTest import sympyTest

from constants import DEPTH, GENERAL_METHODS, NUMBER_OF_GENERAL_CLAUSES, NUMBER_OF_SYMBOLS_FIX, OPERANDS, PROBABILITY_OF_QUERY_BEING_AN_EXPRESSION, TEST_FILE_NAME, TEST_FOLDER_NAME

def generate_propositions(num_propositions):
    available_chars = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    propositions = random.sample(available_chars, num_propositions)
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

def generate_random_query(propositions, depth = 3):
    if random.random() < PROBABILITY_OF_QUERY_BEING_AN_EXPRESSION:
        return generate_random_expression(propositions, depth)
    else:
        return random.choice(propositions)

def generate_random_tests(num_propositions, num_expression, depth):
    """Generate random tests propositions"""
    propositions = generate_propositions(num_propositions)
    
    """ Generate random knowledge base """
    knowledge_base = set()
    
    """ Generate random query """
    query = []
    query = generate_random_query(propositions, depth)
    
    while knowledge_base.__len__() < num_expression:
        knowledge_base.add(generate_random_expression(propositions, depth))
    knowledge_base = "; ".join(knowledge_base)
    test = f"TELL\n{knowledge_base}\nASK\n{query}"
    return test

def run_general_test(number_of_test = 20):
    os.makedirs(TEST_FOLDER_NAME, exist_ok=True)
    for _ in range(number_of_test):
        test = generate_random_tests(NUMBER_OF_SYMBOLS_FIX, NUMBER_OF_GENERAL_CLAUSES, DEPTH)
        with open(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}", "w") as f:
            f.write(test)
        agent = Engine()
        
        output2 = sympyTest(test)
        
        agent.knowledge_base.read_input_file(f"{TEST_FOLDER_NAME}{TEST_FILE_NAME}")
        i = 0
        for method in GENERAL_METHODS:
            method = method.lower()
            agent.set_method(method)
            output1 = agent.set_up_algorithm()[0]
            if output1 == output2:
                print(f"Test {colored(str(i+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('PASSED', 'green')}")
            else:
                fail(test, method, output1, output2, i)
    
                
def fail(test, method, output1, output2, index):
    print(f"Test {method} failed")
    print(f"Test {colored(str(index+1), 'cyan')} with method {colored(method, 'yellow')}: {colored('FAILED', 'red')}")
    failed_test = f"{TEST_FOLDER_NAME}/failed_test_{index+1}.txt"
    failed_test_out_put_my = f"{TEST_FOLDER_NAME}/failed_test_output_{index+1}_method_{method}_my.txt"
    failed_test_out_put_other = f"{TEST_FOLDER_NAME}/failed_test_output_{index+1}_method_{method}_other_program.txt"
    with open(failed_test, "w") as f:
        f.write(test)
    with open(failed_test_out_put_my, "w") as f:
        f.write(str(output1 if "YES" else "NO"))
    with open(failed_test_out_put_other, "w") as f:
        f.write(str(output2 if "YES" else "NO"))
        
run_general_test(100)