
from sympy import *

from GenTestAutomatically import generate_random_propositional_logic
from common import infix_to_postfix
from constants import OPERANDS

num_propositions = 5
depth = 2
random_logic_expression = generate_random_propositional_logic(num_propositions, depth)

def get_symbols_list(sequences):
    symbols_list = set()
    for literals in sequences:
        if literals not in OPERANDS:
            symbols_list.add(literals)
    return symbols_list

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


def to_cnf_form(sequences):
    sequences = infix_to_postfix(sequences)
    symbol_list = symbols(list(get_symbols_list(sequences)))  
    expression = postfix_to_infix(sequences)

    postfix = str(to_cnf(expression))
    postfix = postfix.replace("|", "||")			
    return postfix