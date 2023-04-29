from typing import Sequence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm
class TruthTable(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "TT"
        self.count = 0
        
    def check_all(self, knowledge_base: KnowledgeBase, aList, symbols, model):
        if(symbols.__len__() == 0):
            result = True
            if(knowledge_base.check(model)):
                print(model)
                for sequence in aList:
                    result = result and sequence.check(model)
                if(result):
                    self.count += 1
            return result
        else:
            p = symbols[0]
            rest = symbols[1:]
            return self.check_all(knowledge_base, aList, rest, model + [(p, True)]) and self.check_all(knowledge_base, aList, rest, model + [(p, False)])            
    
    def entails(self) -> tuple[bool, int]:
        symbols = self.knowledge_base.symbols
        for symbol in self.knowledge_base.query_symbols:
            symbols[symbol] = True
        symbols = list(symbols.keys())
        a = self.knowledge_base.query
        result = self.check_all(self.knowledge_base, a, symbols, [])
        if(not result):
            self.count = 0
        return (result, self.count)