from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm


class BackwardChaining(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "BC"
        self.fact = dict()
        self.query = HornSentence()
        self.output = []

    def check_all(self, visited: list, goal):
        if goal in self.fact.keys() and self.fact[goal]:
            if goal not in self.output:
                self.output.append(goal)
            return True

        for sentence in self.knowledge_base.sentences:
            if sentence.conclusion == goal:
                symbolCount = 0
                for premise in sentence.premises:
                    if premise == goal:
                        break
                    if premise in visited:
                        if self.fact[premise] == False:
                            break
                    else:
                        visited.append(premise)

                    self.fact[premise] = self.check_all(visited.copy(), premise)

                    if (self.fact[premise] == False):
                        break
                    symbolCount += 1

                if symbolCount == len(sentence.premises):
                    if goal not in self.output:
                        self.output.append(goal)
                    return True
        return False

    def entails(self) -> tuple[bool, list]:
        self.query = self.knowledge_base.query[0]
        for symbol in self.knowledge_base.symbols:
            self.fact[symbol] = False

        for sentence in self.knowledge_base.sentences:
            if len(sentence.raw_content) == 1:
                self.fact[sentence.raw_content[0]] = True

        ans = self.check_all([], self.query.conclusion)
        if ans:
            output = []
            for symbol in self.output:
                if symbol != self.query.conclusion:
                    output.append(symbol)
            output.append(self.query.conclusion)
            return (ans, output)
        else:
            return (ans, [])
