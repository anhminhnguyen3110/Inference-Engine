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
            return ["~"] + [literal]

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
    
    def pure_literal_assign(self, list_clauses, model: list):
        model_negated = self.compliments(model)
        candidates = []
        for clause in list_clauses:
            if clause[0] == "||":
                if not any(var in model for var in clause[1:]):
                    candidates += [var for var in clause[1:]]
        candidates_negated = self.compliments(candidates)
        pure = [var for var in candidates if var not in candidates_negated]
        for var in pure:
            if var not in model and var not in model_negated:
                return var
        return False

    def unit_clause_assign(self, list_clauses, model: list):
        model_negated = self.compliments(model)
        for clause in list_clauses:
            if clause[0] == "||":
                remaining = [var for var in clause[1:] if var not in model_negated]
                if len(remaining) == 1:
                    if remaining[0] not in model:
                        return remaining[0]
        return False

    def pick_literal(self, list_clauses, model: list):
        combined = model + self.compliments(model)
        for clause in list_clauses:
            if clause[0] == "||":
                for literal in clause[1:]:
                    if literal not in combined:
                        return literal
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
                    print("3")
                    return False
                
    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        cnf_q = to_cnf_form_prefix(q_content)  
        list_sentence = []
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            list_sentence.append(cnf_sentence)
        # if '&' is the first item in the list
        if list_sentence[0] == "&":
            list_clauses = list_sentence[1:]
        list_clauses = [list_sentence]
        return (
            not bool(self.dpll(list_clauses + [self.negate_literal(cnf_q)], [])),
            [],
        )