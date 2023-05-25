from CNF_Converter import to_cnf_form, to_cnf_form_prefix
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm

class DPLL(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "DPLL"

    def negate_literal(self, literal: list) -> list:
        if literal[0] == "~":
            return literal[1]
        else:
            return ["~"] + literal

    def compliments(self, model: list) -> list:
        return [self.negate_literal(literal) for literal in model]

    def all_true(self, list_clauses, model: list) -> bool:
        for clause in list_clauses:
            if clause[0] == "||":
                if not any(literal in model for literal in clause[1:]):
                    return False
        return True

    def some_false(self, list_clauses, model: list) -> bool:
        model_negated = self.compliments(model)
        for clause in list_clauses:
            if clause[0] == "||":
                if all(literal in model_negated for literal in clause[1:]):
                    return True
        return False

    def dpll(self, list_clauses, model: list):
        if self.all_true(list_clauses, model):
            return model
        if self.some_false(list_clauses, model):
            return False
        pure = self.pure_literal_assign(list_clauses, model)
        if pure:
            return self.dpll(list_clauses, model + [pure])
        unit_clauses = self.unit_clause_assign(list_clauses, model)
        if unit_clauses:
            return self.dpll(list_clauses, model + [unit_clauses])
        pick = self.pick_literal(list_clauses, model)
        if pick:
            result = self.dpll(list_clauses, model + [pick])
            if result:
                return result
            else:
                result = self.dpll(list_clauses, model + [self.negate_literal(pick)])
                if result:
                    return result
                else:
                    return False
                
    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        cnf_q = to_cnf_form_prefix(q_content)  

        list_sentence = []
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            list_sentence.append(cnf_sentence)

        list_clauses = list_sentence[1:]
        return (
            not bool(self.dpll(list_clauses + [self.negate_literal(cnf_q)], [])),
            [],
        )