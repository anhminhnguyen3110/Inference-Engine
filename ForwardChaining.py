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
            symbol = self.agenda.pop(0)
            self.path.append(symbol)
            if not self.inferred[symbol]:
                self.inferred[symbol] = True
                for sentence in self.count:
                    if symbol in sentence.premises:
                        self.count[sentence] -= 1
                        if not self.count[sentence]:
                            if sentence.conclusion == query:
                                self.path.append(sentence.conclusion)
                                return (True, self.path)
                            self.agenda.append(sentence.conclusion)
        return False, []

    def entails(self) -> tuple[bool, list]: 
        self.query = self.knowledge_base.query[0]
        q = self.query.content[0]
        for sentence in self.knowledge_base.sentences:
            if len(sentence.premises) > 0:
                self.count[sentence] = len(sentence.premises)
            else:
                if sentence.conclusion == q:
                    return (True, q)
                self.agenda.append(sentence.conclusion)
        for symbol in self.knowledge_base.symbols:
            self.inferred[symbol] = False
        return self.check_all()
        

       


       


