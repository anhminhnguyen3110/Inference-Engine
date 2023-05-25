import random
from constants import PROBABILITY_OF_HORN_QUERY_BEING_AN_EXPRESSION

def generate_propositions(num_propositions):
    available_chars = [chr(i) for i in range(ord("a"), ord("z") + 1)]
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

    single_literals = "; ".join(single_literals)

    tell = "; ".join(horn_clauses)
    tell = f"{tell};" 
    if single_literals.__len__() > 0:
        tell = f"{tell} {single_literals};"
    ask = random.choice(list(symbols))
    return f"TELL\n{tell}\nASK\n{ask}\n"