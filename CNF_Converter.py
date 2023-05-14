from common import construct_expression_tree, infix_to_post_fix
from constants import OPERANDS
import random

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

def generate_random_propositional_logic(num_propositions, depth):
    propositions = generate_propositions(num_propositions)
    expression = generate_random_expression(propositions, depth)
    return expression

# Example usage
num_propositions = 5
depth = 3

random_logic_expression = generate_random_propositional_logic(num_propositions, depth)

def cnf_converter(expression):
    stack = []
    
    for token in expression:
        
        if token not in OPERANDS:
            stack.append(token)
        elif token == '~':
            if len(stack) >= 1:
                operand = stack.pop()
                clause = f"~{operand}"
                stack.append(clause)
            else:
                print("Stack underflow: Insufficient operands for '!' operator")
        else:
            if len(stack) >= 2:
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                if token == '&':
                    clause = f"({left_operand} & {right_operand})"
                elif token == '||':
                    clause = f"({left_operand} || {right_operand})"
                elif token == '=>':
                    clause = f"(~{left_operand} || {right_operand})"
                elif token == '<=>':
                    clause = f"(({left_operand} & {right_operand}) || (~{left_operand} & ~{right_operand}))"
                
                stack.append(clause)
            else:
                print(f"Stack underflow: Insufficient operands for '{token}' operator")

    if len(stack) != 1:
        print("Invalid expression: Unbalanced operators and operands")
    
    cnf = stack[0] if stack else ""
    return cnf
random_logic_expression = "((~e & (c <=> c)) || ((b <=> c <=> d) <=> ~b <=> (e => c)))"
print(construct_expression_tree(random_logic_expression))
# print(construct_expression_tree(random_logic_expression))
# print(cnf_converter(infix_to_post_fix(random_logic_expression)))