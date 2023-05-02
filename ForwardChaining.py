from typing import Sequence
from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm
from Sentence import Sentence

class ForwardChaining(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "FC"
        self.count = {}
        self.inferred = {}
        self.agenda = []
        self.path = []
        self.query = HornSentence()

    def check_all(self):
        query = self.query.content[0]
        while len(self.agenda) > 0:
            p = self.agenda.pop(0)
            self.path.append(p)
            if self.inferred[p] == False:
                self.inferred[p] = True
                for c in self.count:
                    if p in c.conjuncts:
                        self.count[c] -= 1
                        if self.count[c] == 0:
                            if c.head == query:
                                self.path.append(c.head)
                                return (True, self.path)
                            self.agenda.append(c.head)
        return False

    def entails(self) -> tuple[bool, int]: 
        self.query = self.knowledge_base.query[0]
        q = self.query.content[0]
        for sentence in self.knowledge_base.horn_sentences:
            if len(sentence.conjuncts) > 0:
                self.count[sentence] = len(sentence.conjuncts)
            else:
                if sentence.head == q:
                    return (True, q)
                self.agenda.append(sentence.head)
        for symbol in self.knowledge_base.symbols:
            self.inferred[symbol] = False
        return self.check_all()
        

       


       


