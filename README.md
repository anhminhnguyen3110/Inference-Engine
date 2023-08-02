# Inference Engine Problem Readme

This readme provides an overview of the Inference Engine Problem, including various aspects such as algorithms, test case generation, exploration of additional algorithms, and a review of the team's summary report. It introduces five key algorithms: Truth Table, Forward Chaining, Backward Chaining, Resolution, and Davis–Putnam–Logemann–Loveland (DPLL). These algorithms are responsible for interpreting a text file comprising a knowledge base and a query, determining if the query is inferred from the knowledge base.

## Features/Bugs/Missing

### Feature

The implementation of the Inference Engine includes several features to meet the fundamental requirements. The program reads the input in the given format and parses it into postfix form using the Shunting Yard Algorithm (Rastogi et al., 2015). This allows the program to handle complex clauses nested in parentheses. The program implements three fundamental logical reasoning algorithms: "Truth Table," "Forward Chaining," and "Backward Chaining." The report extends beyond these basic requirements and explores techniques, strategies, and algorithms to handle the general form. It outlines two additional algorithms: Resolution and Davis–Putnam–Logemann–Loveland (DPLL), discussing their performance.

### Automated Tests Generator

The Inference Engine includes a test case generator that can randomly create test cases. The generator selects a random number of symbols for creating clauses. Horn form clauses are created using a specific algorithm that randomly selects fixed symbols and combines them with logical operators "AND" and "IMPLIES." The generator also adds standalone symbols as facts in the knowledge base. The program includes an automatic executor to run these tests and examine their accuracy. The "sympy" third-party library is used to compare the program's output with the standard result and identify any mismatches.

## Implementation Details Of Fundamental Algorithms

### Truth Table Algorithm

The Truth Table algorithm is a simple and accurate algorithm for logical reasoning. It checks every combination of all clauses and symbols to find a "model" or a recursive instance where the knowledge base is true. The algorithm verifies if the query is true based on the model. It continues to find the next model if the query is true and outputs "NO" if the query is false. The algorithm has soundness and completeness but has a time complexity of O(2^n) due to checking every combination of clauses and symbols.

### Forward Chaining

Forward Chaining is a "data-driven" algorithm that starts with the knowledge base and uses inference rules to determine if the query is entailed. It tracks unsatisfied premises using a dictionary and updates it when symbols are inferred. The algorithm is relatively simple to implement but may not yield desirable outcomes for large knowledge bases, as it may explore irrelevant clauses or literals.

### Backward Chaining

Backward Chaining starts from the query and utilizes a depth-first search to find known facts in the knowledge base. It recursively checks every premise of the query. If there are sufficient facts to prove the goal, it returns "YES"; otherwise, it returns "NO." Backward Chaining performs better in terms of runtime compared to Forward Chaining and the Truth Table algorithm as it focuses on the specific goal and avoids examining the entire knowledge base.

### CNF Conversion

The CNF Conversion algorithm transforms a logical expression in general form into Conjunctive Normal Form (CNF). CNF is a requirement for successful execution of the Resolution and DPLL algorithms. This algorithm performs operations such as biconditional and implication elimination, De Morgan's laws, distribution, association, and duplication elimination. It iteratively simplifies the expression until convergence is achieved.

### Resolution Algorithm

The Resolution algorithm is a complete inference algorithm used for logical assertions and queries in propositional logic. It aims to prove that a knowledge base (KB) entails a query (α) by checking the unsatisfiability of the conjunction of KB and the negation of α in CNF form. The algorithm applies the resolution rule, which resolves pairs of clauses containing complementary literals. If an empty clause is derived, it concludes that KB entails α. If no new clauses can be generated, it determines that KB does not entail α.

### DPLL Algorithm

The DPLL (Davis-Putnam-Logemann-Loveland) algorithm is a backtracking algorithm for solving the satisfiability problem of a knowledge base in CNF form. It explores different assignments of literals using recursion. The algorithm employs unit propagation and pure literal elimination to reduce the problem size. Unit propagation assigns truth values to unit clauses, which are clauses with only one unassigned literal. Pure literal elimination identifies literals that appear with the same polarity in all clauses and assigns them a truth value. By pruning the search space, the algorithm can efficiently determine the satisfiability of the CNF formula.

Please refer to the code and comments in the respective files for a detailed implementation of these algorithms.

**Note**: The Resolution and DPLL algorithms are complete, but the DPLL algorithm is not guaranteed to be optimal. Its worst-case time complexity is still exponential.

## Acknowledgments/Resources

The implementation of the Inference Engine was guided by the book "Artificial Intelligence: A Modern Approach" by Russell and Norvig. The book provided a comprehensive understanding and practical insights into inference engine operations.

## Notes

To use the program, the syntax is `iengine [method] [filename]`. The available methods are TT, FC, BC, Resolution, and DPLL (not case-sensitive). The filename should be a text file formatted as demonstrated in the assignment. To run a test for Horn clauses, the.

## Contributors
Duy Khoa Pham - 103515617
Anh Minh Nguyen - 103178955
