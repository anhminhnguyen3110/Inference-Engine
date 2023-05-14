
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
    sequences = reversed(sequences)
    new_sequence = []
    for s in sequences:
        if(s == "("):
            new_sequence.append(")")
        elif(s == ")"):
            new_sequence.append("(")
        else:
            new_sequence.append(s)
    new_sequence = "".join(new_sequence)
    prefix = (infix_to_post_fix(new_sequence))[::-1]
    return prefix

def reversed(text):
    ret = []
    i = 0
    while (i < len(text)):
        if(text[i] == "<" and text[i + 1] == "=" and text[i + 2] == ">"):
            ret.insert(0, "@")
            i += 3
        elif(text[i] == "=" and text[i + 1] == ">"):
            ret.insert(0, "#")
            i += 2
        else:
            ret.insert(0, text[i])
            i += 1
    for s in ret:
        if(s == "@"):
            ret[ret.index(s)] = "<=>"
        elif(s == "#"):
            ret[ret.index(s)] = "=>"
    return "".join(ret)
              
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