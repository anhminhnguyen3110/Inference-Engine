from common import (
    construct_expression_tree,
    infix_to_postfix,
    postfix_to_infix,
    prefix_to_infix,
)

def biconditional_eliminating(
    expression_tree,
):
    # If the expression tree is a string, return it
    if type(expression_tree) is str:
        return expression_tree
    
    # ["<=>", "A", "B"] => ["&", ["=>", "A", "B"], ["=>", "B", "A"]]
    # A <=> B => (A => B) and (B => A)
    elif type(expression_tree) is list and expression_tree[0] == "<=>":
        return [
            "&",
            [
                "=>",
                biconditional_eliminating(expression_tree[1]),
                biconditional_eliminating(expression_tree[2]),
            ],
            [
                "=>",
                biconditional_eliminating(expression_tree[2]),
                biconditional_eliminating(expression_tree[1]),
            ],
        ]
    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(biconditional_eliminating(sub_expression_tree))
        return result

def implies_eliminating(
    expression_tree,
):
    # If the expression tree is a string, return it
    if type(expression_tree) is str:
        return expression_tree
    # ["=>", "A", "B"] => ["||", ["~", "A"], "B"]
    # A => B => (not A) or B
    elif type(expression_tree) is list and expression_tree[0] == "=>":
        return [
            "||",
            [
                "~",
                implies_eliminating(expression_tree[1]),
            ],
            implies_eliminating(expression_tree[2]),
        ]
    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(implies_eliminating(sub_expression_tree))
        return result

def negation_eliminating(
    expression_tree,
):  # Demorgan
    old_expression_tree = negation_eliminating_training(expression_tree)
    if old_expression_tree == expression_tree:  # if the training algorithm is converge
        return expression_tree
    else:  # retrain
        return negation_eliminating(old_expression_tree)  # retrain

# Demorgan
def negation_eliminating_training(
    expression_tree,
):
    # If the expression tree is a string, return it
    if type(expression_tree) is str:
        return expression_tree

    # ["~", ["&", "A", "B"]] => ["||", ["~", "A"], ["~", "B"]]
    # not (A and B) => (not A) or (not B)
    elif (
        type(expression_tree) is list
        and expression_tree[0] == "~"
        and type(expression_tree[1]) is list
        and expression_tree[1][0] == "&"
    ):
        result = ["||"]
        for sub_expression_tree in expression_tree[1][1:]:
            result.append(
                negation_eliminating(
                    [
                        "~",
                        sub_expression_tree,
                    ]
                )
            )
        return result
    
    # ["~", ["||", "A", "B"]] => ["&", ["~", "A"], ["~", "B"]]
    # (not (A or B)) => ((not A) and (not B))
    elif (
        type(expression_tree) is list
        and expression_tree[0] == "~"
        and type(expression_tree[1]) is list
        and expression_tree[1][0] == "||"
    ):
        result = ["&"]
        for sub_expression_tree in expression_tree[1][1:]:
            result.append(
                negation_eliminating(
                    [
                        "~",
                        sub_expression_tree,
                    ]
                )
            )
        return result
    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(negation_eliminating(sub_expression_tree))
        return result

def doubleNegEleminating(
    expression,
):
    # If the expression tree is a string, return it
    if type(expression) is str:
        return expression
    
    # ["~", ["~", "A"]] => "A"
    # (not (not A)) => A
    elif (
        type(expression) is list
        and expression[0] == "~"
        and type(expression[1]) is list
        and expression[1][0] == "~"
    ):
        return doubleNegEleminating(expression[1][1])
    else:
        result = [expression[0]]
        # Examine each sub-expression tree
        for sub_expression in expression[1:]:
            result.append(doubleNegEleminating(sub_expression))
        return result

# this function ensure that every sub_expression_tree is in binary form
def groupToBinaryForm(
    expression_tree,
):
    if type(expression_tree) is str:
        return expression_tree

    # ["&", "p", "q", "r", "s"] => ["&", "p", ["&", "q", ["&", "r", "s"]]]
    # p and q and r and s => p and (q and (r and s))
    elif type(expression_tree) is list and expression_tree[0] == "&" and len(expression_tree) > 3:
        result = [
            "&",
            expression_tree[1],
        ]
        for sub_expression_tree in expression_tree[2:]:
            result.append(
                groupToBinaryForm(
                    [
                        "&",
                        sub_expression_tree,
                    ]
                )
            )
        return result

    # ["||", "p", "q", "r", "s"] => ["||", "p", ["||", "q", ["||", "r", "s"]]
    # p or q or r or s => p or (q or (r or s))
    elif type(expression_tree) is list and expression_tree[0] == "||" and len(expression_tree) > 3:
        result = [
            "||",
            expression_tree[1],
        ]
        for sub_expression_tree in expression_tree[2:]:
            result.append(
                groupToBinaryForm(
                    [
                        "||",
                        sub_expression_tree,
                    ]
                )
            )
        return result

    # check another sub_expression_tree
    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(groupToBinaryForm(sub_expression_tree))
        return result


# only works on binary connectives that is ["&", "p", "q"] or (p and q)
def distribution_perform(
    expression_tree,
):  # Distributive law to convert A or (B and C) to (A or B) and (A or C)
    
    old_expression_tree = distribution_perform_training(expression_tree)
    if old_expression_tree == expression_tree:  # if the training algorithm is converge
        return expression_tree
    else:  # retrain
        return distribution_perform(old_expression_tree)


# Distributive law to convert A or (B and C) to (A or B) and (A or C) => CNF
def distribution_perform_training(
    expression_tree,
):
    if type(expression_tree) is str:
        return expression_tree

    # ["||", "A", ["&", "B", "C"]] => ["&", ["||", "A", "B"], ["||", "A", "C"]
    # A or (B and C) to (A or B) and (A or C)
    elif (
        type(expression_tree) is list
        and expression_tree[0] == "||"
        and type(expression_tree[1]) is list
        and expression_tree[1][0] == "&"
    ):
        result = ["&"]
        for sub_expression_tree in expression_tree[1][1:]:
            result.append(
                distribution_perform(
                    [
                        "||",
                        sub_expression_tree,
                        expression_tree[2],
                    ]
                )
            )
        return result

    # ["||", ["&", "B", "C"], "A"] => ["&", ["||", "B", "A"], ["||", "C", "A"]
    # (B and C) or A to (B or A) and (C or A)
    elif (
        type(expression_tree) is list
        and expression_tree[0] == "||"
        and type(expression_tree[2]) is list
        and expression_tree[2][0] == "&"
    ):
        result = ["&"]
        for sub_expression_tree in expression_tree[2][1:]:
            result.append(
                distribution_perform(
                    [
                        "||",
                        sub_expression_tree,
                        expression_tree[1],
                    ]
                )
            )
        return result

    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(distribution_perform(sub_expression_tree))
        return result

def association_perform(
    expression_tree,
    expression,
):
    old_expression_tree = association_perform_training(
        expression_tree,
        expression,
    )
    if old_expression_tree == expression_tree:  # if the training algorithm is converge
        return expression_tree
    else:  # retrain
        return association_perform(
            old_expression_tree,
            expression,
        )

def association_perform_training(
    expression_tree,
    expression,
):
    # If the expression tree is a string, then it is a variable
    if type(expression_tree) is str:
        return expression_tree
    
    # ["&", "p", ["&", "q", "r"]] => ["&", "p", "q", "r"]
    # p and (q and r) => p and q and r
    elif type(expression_tree) is list and expression_tree[0] == expression:
        result = [expression]
        for sub_expression_tree in expression_tree[1:]:
            if type(sub_expression_tree) is list and sub_expression_tree[0] == expression:
                result += sub_expression_tree[1:]
            else:
                result.append(sub_expression_tree)
        return result
    
    else:
        result = [expression_tree[0]]
        # Examine each sub-expression tree
        for sub_expression_tree in expression_tree[1:]:
            result.append(
                association_perform(
                    sub_expression_tree,
                    expression,
                )
            )
        return result


def duplication_symbols_eliminating(
    expression_tree,
):
    
    # If the expression tree is a string, then it is a variable
    if type(expression_tree) is str:
        return expression_tree
    elif type(expression_tree) is list:
        # not is not influenced by duplication        
        if expression_tree[0] == "~":
            return expression_tree
        # ["&", "b", "c", "b", "c"] => ["&", "b", "c"]
        # b and c and b and c => b and c
        elif expression_tree[0] == "&":
            result = ["&"]
            for sub_expression_tree in expression_tree[1:]:
                result.append(duplication_symbols_eliminating(sub_expression_tree))
            return result
        # ["||", "b", "c", "b", "c"] => ["||", "b", "c"]
        # b or c or b or c => b or c
        elif expression_tree[0] == "||":
            exist = []
            for sub_expression_tree in expression_tree[1:]:
                if sub_expression_tree not in exist:
                    exist.append(sub_expression_tree)
            if len(exist) == 1:
                return exist[0]
            else:
                return ["||"] + exist


def duplication_sub_expression_eliminating(
    expression_tree,
):
    # If the expression tree is a string, then it is a variable
    if type(expression_tree) is str:
        return expression_tree
    elif type(expression_tree) is list:
        # Not is not influenced by sub-expression duplication
        if expression_tree[0] == "~":
            return expression_tree
        # Or is not influenced by sub-expression duplication
        elif expression_tree[0] == "||":
            return expression_tree
        
        # ["&", ["||", "b", "c"], ["||", "b", "c"]] => ["||", "b", "c"]
        elif expression_tree[0] == "&":
            exist = []
            for sub_expression_tree in expression_tree[1:]:
                if check_duplication_of_nested_array(
                    sub_expression_tree,
                    exist,
                ):
                    exist.append(sub_expression_tree)
            if len(exist) == 1:
                return exist[0]
            else:
                return ["&"] + exist

# Recursive find every root of nested array/expression tree and compare with the exist array
def check_duplication_of_nested_array(
    expression_tree,
    exist,
) -> bool:
    for element in exist:
        if type(expression_tree) is str or type(element) is str:
            if expression_tree == element:
                return False
        # Compare the root of nested array
        elif len(expression_tree) == len(element):
            if len([i for i in expression_tree[1:] if i not in element[1:]]) == 0:
                return False
    return True


def cnf_converter(
    expression_tree,
):
    if type(expression_tree[0]) == str and len(expression_tree) == 1:
        return expression_tree[0]

    expression_tree = biconditional_eliminating(expression_tree)
    expression_tree = implies_eliminating(expression_tree)
    expression_tree = negation_eliminating(expression_tree)
    expression_tree = doubleNegEleminating(expression_tree)
    expression_tree = groupToBinaryForm(expression_tree)
    expression_tree = distribution_perform(expression_tree)
    
    # the and association perform
    expression_tree = association_perform(
        expression_tree,
        "&",
    )
    
    # the or association perform
    expression_tree = association_perform(
        expression_tree,
        "||",
    )
    expression_tree = duplication_symbols_eliminating(expression_tree)
    expression_tree = duplication_sub_expression_eliminating(expression_tree)
    return expression_tree


def to_cnf_form(
    sequence,
):
    sequence_x = infix_to_postfix(sequence)
    expression = postfix_to_infix(sequence_x).replace(
        "|",
        "||",
    )
    my_converter = prefix_to_infix(cnf_converter(construct_expression_tree(expression)))
    if my_converter[0] == "(" and my_converter[-1] == ")":
        my_converter = my_converter[1:-1]
    return my_converter


def to_cnf_form_prefix(
    sequence,
):
    sequence_x = infix_to_postfix(sequence)
    expression = postfix_to_infix(sequence_x).replace(
        "|",
        "||",
    )
    my_converter = cnf_converter(construct_expression_tree(expression))
    return my_converter