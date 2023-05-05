from Algorithm import Algorithm
from KnowledgeBase import KnowledgeBase
from TruthTable import TruthTable
from ForwardChaining import ForwardChaining

class Engine:
    def __init__(self) -> None:
        self.method = "TT"
        self.knowledge_base = KnowledgeBase()
        self.algorithm: Algorithm = None
        
    def do_algorithm(self) -> bool:
        ans = None
        if(self.method == "TT"):
            self.algorithm = TruthTable(self.knowledge_base)
            ans = self.algorithm.entails()
        if(self.method == "FC"):
            self.algorithm = ForwardChaining(self.knowledge_base)
            ans = self.algorithm.entails()
            
        print(self.method, ":", ans)
        print()
        return True
    
    def set_method(self, method: str) -> None:
        self.method = method