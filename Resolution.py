from cnf_converter_2 import *

def negate_literal(literal):
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal
    
def is_inverse(literal1, literal2):
    return literal1 == negate_literal(literal2)

def PL_RESOLVE(Ci, Cj):
    resolvents = []

    for i in range(len(Ci)):
        for j in range(len(Cj)):
            if is_inverse(Ci[i], Cj[j]):
                resolvent = Ci[:i] + Ci[i+1:] + Cj[:j] + Cj[j+1:]
                resolvents.append(resolvent)

    return resolvents

def PL_RESOLUTION(KB, alpha):
    clauses = to_cnf_form(KB + " & ~(" + alpha + ")")  
    print(f"Clause: {clauses}")
    list_clauses = [clause.strip() for clause in clauses.split("&")]
    print(list_clauses)
    new = list()
    while True:
        for i in range(len(list_clauses) - 1):
            for j in range(i + 1, len(list_clauses)):
                resolvents = PL_RESOLVE([list_clauses[i]], [list_clauses[j]])

                if [] in resolvents:  # Empty clause found
                    return True
                for resolvent in resolvents:
                    if resolvent not in new:
                        new.append(resolvent)

        if all(element in list_clauses for element in new):  # No new resolvents found
            return False

        if new not in list_clauses:
            list_clauses.append(new)

# Example usage
KB =  "c & (d || e || ~c)"
alpha = "c"


result = PL_RESOLUTION(KB, alpha)
print(result)
