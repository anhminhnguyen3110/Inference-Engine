# COS30019 - Inference Engine

## 1. Introduction
This report aims to provide a concise overview of the Inference Engine Problem, encompassing various aspects such as algorithms, test case generation, exploration of additional algorithms, and a review of the team's summary report. The report will introduce five key algorithms: Truth Table, Forward Chaining, Backward Chaining, Resolution, and Davis–Putnam–Logemann–Loveland (DPLL). These algorithms are responsible for interpreting a text file comprising a knowledge base along with a query, primarily assessing if the query is inferred from the knowledge base.

## 2. Features, Bugs, and Missing
### 2.1 Features
In this assignment, several features have been implemented to meet the fundamental requirements of the Inference Engine. These include the ability to read and parse the input using the Shunting Yard Algorithm, implementation of three logical reasoning algorithms (Truth Table, Forward Chaining, and Backward Chaining), and extended research and exploration of techniques and algorithms beyond the basic requirements.

### 2.2 Bugs
The Resolution algorithm can take a significantly longer time to run in complex test cases. This behavior arises from the nature of its implementation.

### 2.3 Missing
Test Cases and Automated Tests Generator are missing in this report.

## 3. Acknowledgments/Resources
Russell and Norvig's book, titled "Artificial Intelligence: A Modern Approach," has been instrumental in providing a comprehensive understanding of the functioning of inference engines and offering insights into their implementation.

## 4. Notes
To use the program, the syntax is `iengine [method][filename]`. The available methods are TT, FC, BC, Resolution, and DPLL which are not case-sensitive. The filename is a text file formatted as demonstrated in the assignment. To run a test for Horn clauses, the command syntax would be `python GenTest.py horn`.

## 5. Research/Additional Algorithms
### 5.1 Generic Handler For Truth Table
An implementation to handle generic clauses using a truth table has been explored. 

### 5.2 Conjunctive Normal Form Conversion
The implementation of Conjunctive Normal Form (CNF) conversion was also explored in this report. 

### 5.3 Resolution Algorithm
The implementation of the Resolution algorithm is described, which works by proofing the contradiction.

