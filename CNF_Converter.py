import copy
                                  
def association_perform(expression_tree): #  ['&', ['&', 'a', 'b'], ['&', 'c', 'd']] => ['&', 'a', 'b', 'c', 'd']  
    if(expression_tree[0] == "&"):
        temp_expression_tree = copy.deepcopy(expression_tree) # deep copy because dont want to change tmp_expression_tree
        del expression_tree[:]
        for literal in temp_expression_tree:
            if literal == "&":
                expression_tree.append(literal)
            else:
                if literal[0] != "&":
                    expression_tree.append(literal)
                else:
                    for sub_literal in literal:
                        if sub_literal == "&":
                            continue
                        else:
                            expression_tree.append(sub_literal)
                            
    if(expression_tree[0] == "||"):
        temp_expression_tree = copy.deepcopy(expression_tree) # deep copy because dont want to change tmp_expression_tree
        del expression_tree[:]
        for literal in temp_expression_tree:
            if literal == "||":
                expression_tree.append(literal)
            else:
                if literal[0] != "||":
                    expression_tree.append(literal)
                else:
                    for sub_literal in literal:
                        if sub_literal == "||":
                            continue
                        else:
                            expression_tree.append(sub_literal)
                            
    for element in expression_tree:
        if len(element) > 1:
            association_perform(element)

def distribution_perform(expression_tree): #Distributive law to convert A or (B and C) to (A or B) and (A or C) => CNF
    if(expression_tree[0] == "||"):
        # expression_tree[0] will be ||, expression_tree[1] will be a single proposition, expression_tree[2] will be a list of propositions 
        if(len(expression_tree[2]) > 1 and expression_tree[2][0] == "&"): # (A or (B and C)) = (A or B) and (A or C)
            left = expression_tree[1]
            right = expression_tree[2]
            del expression_tree[:]
            expression_tree.append("&")
            for temp_right in right: # (A or B) and (A or C)
                if (temp_right == "&"): # the first element is "&"
                    continue
                expression_tree.append(["||", left, temp_right]) # append [A, (B or C)]
        # expression_tree[0] will be ||, expression_tree[1] will be a list of propositions, expression_tree[2] will be a single proposition
        elif(len(expression_tree[1]) > 1 and expression_tree[1][0] == "&"): # ((A and B) or C) = (A or C) and (B or C)
            left = expression_tree[1]
            right = expression_tree[2]
            del expression_tree[:]
            expression_tree.append("&")
            for temp_left in left: # (A or B) and (A or C)
                if (temp_left == "&"): # the first element is "&"
                    continue
                expression_tree.append(["||", temp_left, right]) # append [(A or B), C]
        
    for element in expression_tree: # recursion
        if len(element) > 1:
            distribution_perform(element)

def negation_eliminating(expression_tree): #Demorgan
    if(expression_tree[0] == "~"):
        literal = expression_tree[1]
        
        if literal[0] == "~":  # double negation: ~~A = A
            del expression_tree[:]
            if(len(literal) == 1):                
                expression_tree.append(literal[1])
            else:
                for s in literal[1]:
                    expression_tree.append(s)
                    
                if(len(expression_tree) > 1):
                    negation_eliminating(expression_tree)
        
        elif literal[0] == "||": # DeMorgan: ~(A or B) = ~A and ~B
            del expression_tree[:]
            expression_tree.append("&")
            for s in literal:                
                if s == "||": # the first element is "||"
                    continue
                else:
                    expression_tree.append(["~", s])
        
        elif literal[0] == "&": # DeMorgan: ~(A and B) = ~A or ~B
            del expression_tree[:]
            expression_tree.append("||")
            for s in literal:
                if s == "&":  # the first element is "&"
                    continue
                else:
                    expression_tree.append(["~", s])
                
    for element in expression_tree: # recursion
        if(len(element) > 1):
            negation_eliminating(element)

def implies_eliminating(expression_tree):
    if(expression_tree[0] == "=>"):
        left = expression_tree[1]
        expression_tree[0] = "||"
        expression_tree[1] = ["~", left]
    for element in expression_tree:
        if(len(element) > 1):
            implies_eliminating(element)

def bidirectional_eliminating(expression_tree):
    if(expression_tree[0] == "<=>"):
        left = expression_tree[1]
        right = expression_tree[2]
        expression_tree[0] = "&"
        expression_tree[1] = ["=>", left, right]
        expression_tree[2] = ["=>", right, left]
    
    for element in expression_tree:
        if(len(element) > 1):
            bidirectional_eliminating(element)

def square_parentheses_eliminating(expression_tree):
    for ind, sub_expression_tree in enumerate(expression_tree):
        if(len(sub_expression_tree) == 1 and type(sub_expression_tree) == list): # if the sub_expression_tree is a single proposition
            expression_tree[ind] = sub_expression_tree[0]
        elif(len(sub_expression_tree) > 1):
            square_parentheses_eliminating(sub_expression_tree)

def duplication_eliminating(expression_tree):
    delete_sub_tree = []
    if(expression_tree[0] == "&" or expression_tree[0] == "||"):
        for x in range(0, len(expression_tree)):
            for y in range(x+1, len(expression_tree)):
                sub_tree_1 = copy.deepcopy(expression_tree[x])
                sub_tree_2 = copy.deepcopy(expression_tree[y])
                if(sub_tree_1 == sub_tree_2):
                    delete_sub_tree.append(expression_tree[y])
    if(len(delete_sub_tree) >= 1):
        temp_expression_tree = []
        checked = []
        for sub_tree in expression_tree:
            if(sub_tree in delete_sub_tree and sub_tree not in checked):
                checked.append(sub_tree)
                continue
            else:
                temp_expression_tree.append(sub_tree)
        del expression_tree[:]
        for sub_tree in temp_expression_tree:
            expression_tree.append(sub_tree)
        
    for element in expression_tree:
        if(len(element) > 1):
            duplication_eliminating(element)                
            
from sympy import *
from common import infix_to_postfix
from constants import OPERANDS

def cnf_converter(expression_tree):
    bidirectional_eliminating(expression_tree)
    implies_eliminating(expression_tree) 
    negation_eliminating(expression_tree)
    distribution_perform(expression_tree)
    association_perform(expression_tree)
    
    square_parentheses_eliminating(expression_tree)
    
    sort_prefix_logic(expression_tree)
    duplication_eliminating(expression_tree)
    remove_stand_alone_sub_trees(expression_tree)
    check_if_tree_contain_multilayer(expression_tree)
    square_parentheses_eliminating(expression_tree)
    
    old = None
    while(old != expression_tree):
        old = copy.deepcopy(expression_tree)
        distribution_perform(expression_tree)
        association_perform(expression_tree)            
        sort_prefix_logic(expression_tree)
        duplication_eliminating(expression_tree)
        remove_stand_alone_sub_trees(expression_tree)
        check_if_tree_contain_multilayer(expression_tree)
        square_parentheses_eliminating(expression_tree)
    return expression_tree    
    
def sort_prefix_logic(expression):
    if isinstance(expression, list):
        expression[1:] = sorted(expression[1:], key=lambda x: (isinstance(x, list), str(x)))
        for i in range(1, len(expression)):
            sort_prefix_logic(expression[i])
    return expression

def remove_stand_alone_sub_trees(expression_tree): # remove stand alone sub_trees (e.g. [["&", "a", "b"], 'a'] -> ["&", "a", "b"])
    if(len(expression_tree)==2 and expression_tree[0]!="~"): 
        del expression_tree[0]

    for sub_tree in expression_tree:
        if(len(sub_tree)>1 and isinstance(sub_tree, list)):
            remove_stand_alone_sub_trees(sub_tree)

def check_if_tree_contain_multilayer(expression_tree):
    if(len(expression_tree)==1 and len(expression_tree[0])>1):
        sub_tree=expression_tree[0]
        del expression_tree[:]
        for tree in sub_tree:
            expression_tree.append(tree)

    for sub_tree in expression_tree:
        if(len(sub_tree)>1):
            check_if_tree_contain_multilayer(sub_tree)

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
    expression = postfix_to_infix(sequences)

    postfix = str(to_cnf(expression))
    postfix = postfix.replace("|", "||")			
    return postfix