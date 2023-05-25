from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm


class BackwardChaining(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "BC"
        self.fact = dict()
        self.query = HornSentence()

    def check_all(self, visited: dict(), chain: dict(), goal):
        if goal in self.fact:
            chain[goal] = True
            return True, chain

        visited[goal] = True

        for sentence in self.knowledge_base.sentences:
            if sentence.conclusion == goal:
                check = True
                for premise in sentence.premises:
                    # print("Sentence: ", goal, ", Premise: ", premise)
                    if premise in chain:
                        # print("Reach here already in chain -> True: ", premise)
                        # print()
                        continue

                    if premise in visited:
                        check = False
                        # print("Reach here already visited -> False: ", premise)
                        # print()
                        break
                    # print("Loop: ")
                    # print()
                    result, chain = self.check_all(visited, chain, premise)
                    check = check and result
                if check:
                    chain[goal] = True
                    return True, chain
        return False, chain

    def entails(self) -> tuple[bool, list]:
        self.query = self.knowledge_base.query[0]
        for sentence in self.knowledge_base.sentences:
            if len(sentence.raw_content) == 1:
                self.fact[sentence.raw_content[0]] = True
        ans = self.check_all(dict(), dict(), self.query.conclusion)
        return (ans[0], list(ans[1].keys()))
