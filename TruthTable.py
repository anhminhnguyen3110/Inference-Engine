from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm
from Sentence import Sentence


class TruthTable(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "TT"
        self.count = 0
        self.knowledge_base = knowledge_base
        self.query = Sentence()

    def check_all(self, symbols: list, model: list[tuple[str, bool]]):
        if symbols.__len__() == 0:
            result = True
            if self.knowledge_base.check(model):
                result = self.query.check(model)
                if result:
                    self.count += 1
            return result
        else:
            p = symbols[0]
            rest = symbols[1:]
            # check all combinations of p
            return self.check_all(rest, model + [(p, True)]) and self.check_all(
                rest, model + [(p, False)]
            )

    def entails(self) -> tuple[bool, int]:
        symbols = self.knowledge_base.symbols
        for symbol in self.knowledge_base.query_symbols:
            symbols[symbol] = True
        symbols = list(symbols.keys())
        self.query = self.knowledge_base.query[0]
        result = self.check_all(symbols, [])
        if not result:
            self.count = 0
        return (result, self.count)
