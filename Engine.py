from Algorithm import Algorithm
from KnowledgeBase import KnowledgeBase
from TruthTable import TruthTable


class Engine:
    def __init__(self) -> None:
        self.method = "TT"
        self.knowledge_base = KnowledgeBase()
        self.algorithm: Algorithm = None
        
    def do_algorithm(self) -> bool:
        if(self.method == "TT"):
            self.algorithm = TruthTable(self.knowledge_base)
            print(self.algorithm.entails())
        return True
    
    def set_method(self, method: str) -> None:
        self.method = method