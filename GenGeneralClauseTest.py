import random
from constants import OPERANDS, PROBABILITY_OF_QUERY_BEING_AN_EXPRESSION

# Generate random propositions
def generate_propositions(num_propositions):
    available_chars = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    propositions = random.sample(available_chars, num_propositions)
    return propositions

# Generate random expression
def generate_random_expression(propositions, depth):
    if depth == 0 or len(propositions) == 1:
        return random.choice(propositions)
    else:
        operator = random.choices(list(OPERANDS.keys()), weights=list(OPERANDS.values()))[0]
        if operator == "~":
            operand = generate_random_expression(propositions, depth - 1)
            return f"~{operand}"
        else:
            num_operands = random.randint(2, len(propositions))
            operands = random.sample(propositions, num_operands)
            subexpressions = [
                generate_random_expression([p for p in propositions if p != op], depth - 1)
                for op in operands
            ]

            # Check if any clause and its negation are present in subexpressions
            while any(f"~{op}" in subexpressions for op in operands):
                subexpressions = [
                    generate_random_expression([p for p in propositions if p != op], depth - 1)
                    for op in operands
                ]

            expression = f" {operator} ".join(subexpressions)
            return f"({expression})"


def generate_random_query(propositions, depth=3):
    # Check if query is an expression or a single proposition by probability
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
