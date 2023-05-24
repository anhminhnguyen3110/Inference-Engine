from sympy import *
from sympy.logic.inference import entails

from common import infix_to_postfix, postfix_to_infix

def sympyTest(input_file: str): # check if the result is entail or not
    sequences = input_file.split("\n")[1]
    query = input_file.split("\n")[3]
    
    SequenceSet = set()
    sequences = sequences.split(";")
    for sequence in sequences:
        if(sequence == " "):
            continue
        else:
            sequence = simplify(postfix_to_infix(infix_to_postfix(sequence)))
            SequenceSet.add(sequence)    
    query = simplify(postfix_to_infix(infix_to_postfix(query)))
    return entails(query, SequenceSet)
# string = "TELL\nb => r; d & r & n => b; r & d => n; b & r => d; n & d => r; n => b; r & n & d => b; b => d; \nASK\nr"
# sympyTest(string)