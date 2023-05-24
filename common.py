
import re
from termcolor import colored

from constants import OPERANDS, TEST_FOLDER_NAME
def get_content(sentences: str):
    regex_logical = r'\w+\d+|\w+|=>|<=>|~|\)|\(|&|\|\|'
    tokens = sentences.replace(" ", "")
    tokens = re.findall(regex_logical, tokens)
    return tokens

def infix_to_postfix(sentences: str):
    stack = []
    queue = []
    tokens = get_content(sentences)
    for t in tokens:
        if(t == "("):
            stack.append(t)
        elif(t == ")"):
            while(stack[-1] != "("):
                queue.append(stack.pop())
            stack.pop()
        elif(t in OPERANDS):
            if(stack.__len__() > 0 and stack[-1] == "~" and t == "~"):
                stack.pop()
                continue
            while(len(stack) != 0 and stack[-1] != "(" and OPERANDS[t] <= OPERANDS[stack[-1]]):
                queue.append(stack.pop())
            stack.append(t)
        else:
            queue.append(t)
    while(len(stack) != 0):
        queue.append(stack.pop())
    return queue

def postfix_to_infix(sequences):
    stack = []
    for token in sequences:
        if token not in OPERANDS:
            stack.append(token)
        elif(stack.__len__() >= 2 and token != "~"):
            right = stack.pop()
            left = stack.pop()
            stack.append(f'({left} {token} {right})')
        elif(stack.__len__() >= 1 and token == "~"):
            right = stack.pop()
            stack.append(f'~{right}')
    return stack.pop()
 
def execute_logic(operator: str, operand1: bool, operand2: bool):
    if(operator == "~"):
        return not operand1
    elif(operator == "||"):
        return operand1 or operand2
    elif(operator == "&"):
        return operand1 and operand2
    elif(operator == "=>"):
        return not operand1 or operand2
    elif(operator == "<=>"):
        return operand1 == operand2
        
def infix_to_prefix(sequences):
    while "~~" in sequences:
        sequences = sequences.replace("~~", "")
        
    if(len(sequences) == 1):
        return sequences
    
    sequences = get_content(sequences)[::-1]
    new_sequence = []
    for s in sequences:
        if(s == "("):
            new_sequence.append(")")
        elif(s == ")"):
            new_sequence.append("(")
        else:
            new_sequence.append(s)
    new_sequence = "".join(new_sequence)
    prefix = (infix_to_postfix(new_sequence))[::-1]
    return prefix
              
def construct_expression_tree(sequence):
    stack = []
    expression = infix_to_prefix(sequence)[::-1]
    if(len(expression) == 1):
        return expression
    for token in expression:
        if token == "~":
            right = stack.pop()
            node = [token, right]
            stack.append(node)
        elif token in OPERANDS:
            left = stack.pop()
            right = stack.pop()
            node = [token, left, right]
            stack.append(node)
        else:
            stack.append(token)
    return stack[0]

def postfix_to_infix(sequences):
    stack = []
    for token in sequences:
        if token not in OPERANDS:
            stack.append(token)
        else:
            if token == '~':
                right = stack.pop()
                stack.append(f'(~{right})')
            else:
                right = stack.pop()
                left = stack.pop()
                if token == '=>':
                    stack.append(f'(~{left} | {right})')
                elif token == '<=>':
                    stack.append(f'(({left} & {right}) | (~{left} & ~{right}))')
                elif token == "||":
                    stack.append(f'({left} | {right})')
                else:
                    stack.append(f'({left} {token} {right})')
    return stack.pop()
                
def fail(test, method, output1, output2, index):
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

def prefix_to_infix(expression):
    if isinstance(expression, str):
        return expression

    operator = expression[0]
    if operator == '~':
        operand = prefix_to_infix(expression[1])
        return f"~{operand}"
    elif operator == '||' or operator == '&':
        operands = [prefix_to_infix(exp) for exp in expression[1:]]
        return f"({f' {operator} '.join(operands)})"