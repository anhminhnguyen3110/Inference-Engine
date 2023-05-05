from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm

class BackwardChaining(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "BC"
        self.count = dict()
        self.inferred = dict()
        self.agenda = dict()
        self.query = HornSentence()

    def check_all(self, removed:dict(), chain: dict(), goal):
        if(goal in self.agenda):
            chain[goal] = True
            return True,chain
        
        removed[goal] = True
        
        for sentence in self.knowledge_base.sentences:
            if sentence.conclusion == goal:
                for premise in sentence.premises:
                    check = True
                    print("Sentence: ", goal, ", Premise: ", premise)
                    if(premise in chain):
                        print("Reach here already in chain -> True: ", premise)
                        print()
                        continue
                    
                    if(premise in removed):
                        check = False
                        print("Reach here already removed -> False: ", premise)
                        print()
                        break
                    print("Loop: ")
                    print()
                    result, chain = self.check_all(removed, chain, premise)
                    check = check and result
                if check:
                    chain[goal] = True
                    return True, chain
        return False,chain
    
    
    def entails(self) -> tuple[bool, int]: 
        self.query = self.knowledge_base.query[0]
        q = self.query.content[0]
        for sentence in self.knowledge_base.sentences:
            if len(sentence.premises) > 0:
                self.count[sentence] = len(sentence.premises)
            else:
                if sentence.conclusion == q:
                    return (True, q)
                self.agenda[sentence.conclusion] = True
        for symbol in self.knowledge_base.symbols:
            self.inferred[symbol] = False
        
        ans = self.check_all(dict(), dict(),self.query.conclusion)
        return (ans[0], list(ans[1].keys()))