from Sentence import Sentence
from common import execute_logic
from constants import OPERANDS

class HornSentence(Sentence):
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        super().__init__(raw_content, content, symbols)
        self.conjuncts = []
        if len(self.content) == 0:
            self.head = ""
        elif len(self.content) == 1:
            self.head = self.content[0]
        else:
            self.head = self.content[-2]
            for element in self.content:
                if element not in OPERANDS and element != self.head:
                    self.conjuncts.append(element)
        
    def check(self, model) -> bool:
        super().check(model)
        

    def __str__(self) -> str:
        super().__str__()

    
    

