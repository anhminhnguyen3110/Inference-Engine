from CNF_Converter import to_cnf_form
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm


class Resolution(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "Resolution"

    def negate_literal(self, literal: str) -> str:
        if literal.startswith("~"):
            return literal[1:]
        else:
            return "~" + literal

    def is_inverse(self, literal1: str, literal2: str) -> bool:
        return self.negate_literal(literal1) == literal2

    def PL_RESOLVE(self, Ci: list[str], Cj: list[str]) -> list[list[str]]:
        resolvents = []
        for i in range(len(Ci)):
            for j in range(len(Cj)):
                if self.is_inverse(Ci[i], Cj[j]):
                    resolvent = [x for x in Ci if x != Ci[i]] + [x for x in Cj if x != Cj[j]]
                    if resolvent not in resolvents:
                        resolvents.append(resolvent)
        return resolvents

    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        list_sentence = list()
        list_clauses = list()
        cnf_q = to_cnf_form(self.negate_literal(q_content))
        list_sentence.append(cnf_q)

        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form(sentence.raw_content)
            list_sentence.append(cnf_sentence)

        for clause in list_sentence:
            clause = clause.replace(" ", "").replace("(", "").replace(")", "")
            split_clause = clause.split("&")
            list_clauses.extend([c.split("||") for c in split_clause])

        while True:
            new = list()
            for i in range(len(list_clauses) - 1):
                for j in range(i + 1, len(list_clauses)):
                    resolvents = self.PL_RESOLVE(list_clauses[i], list_clauses[j])
                    if [] in resolvents:
                        return True, []
                    new.extend(resolvent for resolvent in resolvents if resolvent not in new)

            if len(new) == 0:
                break

            if all(c in list_clauses for c in new):
                break

            list_clauses.extend(clause for clause in new if clause not in list_clauses)

        return False, []
