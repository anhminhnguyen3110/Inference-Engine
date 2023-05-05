from Sentence import Sentence
from common import execute_logic
from constants import OPERANDS

class HornSentence(Sentence):
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        super().__init__(raw_content, content, symbols)
        self.conclusion = ""
        self.premises = []
        self.set_variables()

    def set_variables(self):
        if len(self.content) == 0:
            self.conclusion = ""
        elif len(self.content) == 1:
            self.conclusion = self.content[0]
        else:
            self.conclusion = self.content[-2]
            index = self.raw_content.index("=>")
            self.left = self.raw_content[:index].strip()
            for element in self.left:
                if element not in OPERANDS:
                    self.premises.append(element)
            
    def check(self, model) -> bool:
        return super().check(model)

    def __str__(self) -> str:
        return super().__str__() + ", conclusion: " + str(self.conclusion) + ", premises: " + str(self.premises)

    
    

