from cnf_converter_2 import *
from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm

class Resolution(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "Resolution"

    def negate_literal(self, literal):
        if literal.startswith("~"):
            return literal[1:]
        else:
            return "~" + literal
        
    def is_inverse(self, literal1, literal2):
        return self.negate_literal(literal1) == literal2

    def PL_RESOLVE(self, Ci, Cj):
        resolvents = []
        for i in range(len(Ci)):
            for j in range(len(Cj)):
                if self.is_inverse(Ci[i], Cj[j]):
                    resolvent = Ci[:i] + Ci[i+1:] + Cj[:j] + Cj[j+1:]
                    resolvents.append(resolvent)
        return resolvents
    
    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        list_sentence= list()
        list_clauses = list()
        cnf_q = to_cnf_form("~(" + q_content + ")")
        list_sentence.append(cnf_q)

        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form(sentence.raw_content)
            list_sentence.append(cnf_sentence)

        for clause in list_sentence:
            split_clause = clause.split('&')
            list_clauses.extend([component.strip() for component in split_clause])
        
        while True:
            new = list()
            for i in range(len(list_clauses) - 1):
                for j in range(i + 1, len(list_clauses)):
                    resolvents = self.PL_RESOLVE([list_clauses[i]], [list_clauses[j]])

                    if [] in resolvents:
                        return True, []
                    
            for resolvent in resolvents:
                if resolvent not in new:
                    new.append(resolvent)

            if all(element in list_clauses for element in new):
                return False, []
            
            if new not in list_clauses:
                list_clauses.append(new)
