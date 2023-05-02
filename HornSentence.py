from Sentence import Sentence
from common import execute_logic
from constants import OPERANDS


class HornSentence(Sentence):
    def __init__(self, raw_content = "", content = "", symbols = {}):
        self.content = content
        self.symbols = symbols
        self.raw_content = raw_content
        self.conjuncts = []
        if len(self.content) == 1:
            self.head = self.content[0]
        else:
            self.head = self.content[-2]
            for element in self.content:
                if element not in OPERANDS and element != self.head:
                    self.conjuncts.append(element)
        
    def check(self, model) -> bool:
        result = []
        stack = []
        for(token, value) in model:
            if(token in self.symbols):
                self.symbols[token] = value
        symbols_clone = self.symbols.copy()
        for token in self.content:
            if token not in OPERANDS:
                stack.append(token)
            elif(stack.__len__() >= 2 and token != "~"):
                right = stack.pop()
                left = stack.pop()
                symbols_clone[f'({left} {token} {right})'] = execute_logic(token, symbols_clone[left], symbols_clone[right])
                stack.append(f'({left} {token} {right})')
            elif(stack.__len__() >= 1 and token == "~"):
                right = stack.pop()
                symbols_clone[f'~{right}'] = execute_logic(token, symbols_clone[right], symbols_clone[right])
                stack.append(f'~{right}')
        return symbols_clone[stack.pop()]

    def __str__(self) -> str:
        return f"content {str(self.content)}, symbols {str(self.symbols)}"

    
    

