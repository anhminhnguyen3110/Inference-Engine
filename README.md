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

## Acknowledgments/Resources

The implementation of the Inference Engine was guided by the book "Artificial Intelligence: A Modern Approach" by Russell and Norvig. The book provided a comprehensive understanding and practical insights into inference engine operations.

## Notes

To use the program, the syntax is `iengine [method] [filename]`. The available methods are TT, FC, BC, Resolution, and DPLL (not case-sensitive). The filename should be a text file formatted as demonstrated in the assignment. To run a test for Horn clauses, the.
