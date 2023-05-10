
import re

from constants import OPERANDS
def get_content(sentences: str):
    regex_logical = r'\w+\d+|\w+|=>|<=>|~|\)|\(|&|\|\|'
    tokens = sentences.replace(" ", "")
    tokens = re.findall(regex_logical, tokens)
    return tokens
#"(a <=> (c => ~d)) & b & (b => a)" => "a c d => <=> b & b a => &"
def infix_to_post_fix(sentences: str):
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
        