def PL_RESOLVE(ci, cj):
    resolvents = []
    if ci.count('~') == 1 or cj.count('~') == 1:
        for literal_i in ci:
            for literal_j in cj:
                if literal_i == ['~', literal_j] or literal_j == ['~', literal_i]:
                    resolvent = [x for x in (ci + cj) if x != literal_i and x != literal_j]
                    if not resolvent:
                        resolvent = [[]]  # Empty clause represented as [[]]
                    resolvents.append(resolvent)
        return resolvents


def PL_RESOLUTION(KB, alpha):
    clauses = KB + [['~', alpha]]
    new = []

    while True:
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                resolvents = PL_RESOLVE(clauses[i], clauses[j])
                for resolvent in resolvents:
                    if resolvent == [[]]:
                        return True  # Empty clause found, α is satisfiable
                    if resolvent not in new:
                        new.append(resolvent)
        
        if all(clause in clauses for clause in new):
            return False  # New clauses are already present in the set of clauses
        
        clauses += new

KB = ['&', ['~', 'a'], ['||', 'b', 'c'], 'd', 'c']
alpha = '~a'

result = PL_RESOLUTION(KB, alpha)

print(result)
