""""Read input for me a file has format like this: 
TELL
p2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p1=>d; p1&p3 => c; a; b; p2;
ASK
d
"""
    
import re
from KnowledgeBase import KnowledgeBase
#"(a <=> (c => ~d)) & b & (b => a)" => "a c d => <=> b & b a => &"
def infix_to_post_fix(sentences: str):
    operands = {'~': 4, '&': 3, '||': 3, '=>': 1, '<=>': 1}
    regex_logical = r'\w+\d+|\w+|=>|<=>|~|\)|\(|&|\|\|'
    sentences = sentences.split(';')
    result = []
    for tokens in sentences:
        if(tokens == ""):
            continue
        stack = []
        queue = []
        tokens = tokens.replace(" ", "")
        tokens = re.findall(regex_logical, tokens)
        for t in tokens:
            if(t == "("):
                stack.append(t)
            elif(t == ")"):
                while(stack[-1] != "("):
                    queue.append(stack.pop())
                stack.pop()
            elif(t in operands):
                while(len(stack) != 0 and stack[-1] != "(" and operands[t] <= operands[stack[-1]]):
                    queue.append(stack.pop())
                stack.append(t)
            else:
                queue.append(t)
        while(len(stack) != 0):
            queue.append(stack.pop())
        result.append(queue)
    postfix_to_infix(result)
    return result

def postfix_to_infix(sequences: list):
    operands = {'~': 4, '&': 3, '||': 3, '=>': 1, '<=>': 1}
    result = []
    for sequence in sequences:
        stack = []
        for token in sequence:
            if token not in operands:
                stack.append(token)
            elif(stack.__len__() >= 2 and token != "~"):
                right = stack.pop()
                left = stack.pop()
                stack.append(f'({left} {token} {right})')
            elif(stack.__len__() >= 1 and token == "~"):
                right = stack.pop()
                stack.append(f'~{right}')
                
        result.append(stack.pop())
    print(result)
    pass    

def read_input(file_name):
    kb = KnowledgeBase()
    # print(file_name)
    try:
        with open(file_name, "r", encoding="utf8") as file:
            lines = file.read().splitlines()
            for line in lines:
                if(line == "TELL"):
                    kb.set_action("TELL")
                elif(line == "ASK"):
                    kb.set_action("ASK")
                else:
                    kb.act(infix_to_post_fix(line))
            file.close()    
            return kb
    except IOError:
        print("File not found")
        return
        
        