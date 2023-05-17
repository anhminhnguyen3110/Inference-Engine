from cnf_converter_2 import *
from HornSentence import HornSentence
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm

class DPLL(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "DPLL"

    def negate_literal(self, literal:str) -> str:
        if literal.startswith("~"):
            return literal[1:]
        else:
            return "~" + literal
    
    def compliments(self, model: list) -> list:
        return [self.negate_literal(literal) for literal in model]

    def all_true(self, list_clauses, model: list) -> bool:
        for clause in list_clauses:
            if len([literal for literal in clause.split(" || ") if literal in model]) == 0:
                return False
        return True
        
    def some_false(self, list_clauses, model: list) -> bool: 
        model_negated = self.compliments(model)
        for clause in list_clauses:
            unsatisfied_literals = [literal for literal in clause.split(" || ") if literal not in model_negated]
            if len(unsatisfied_literals) == 0: 
                return True
        return False
        
    def pure_literal_assign(self, list_clauses, model : list): 
        model_negated = [self.negate_literal(literal) for literal in model]
        candidates = []
        for clause in list_clauses:
            literals = clause.split(" || ")
            len_list_literals = len([literal for literal in literals if literal in model])
            if len_list_literals == 0:
                candidates += literals
        candidates_negated = [self.negate_literal(literal) for literal in candidates]
        pure = [literal for literal in candidates if literal not in candidates_negated]
        for literal in pure:
            if literal not in model and literal not in model_negated:
                return literal
        return False
    
    def unit_clause_assign(self, list_clauses, model: list): 
        model_negated = self.compliments(model)
        for clause in list_clauses:
            list_remaining = [literal for literal in clause.split(" || ") if literal not in model_negated]
            if len(list_remaining) == 1:
                if list_remaining[0] not in model:
                    return list_remaining[0]
        return False

    def pick_literal(self, list_clauses, model: list):
        combined = model + self.compliments(model)
        for clause in list_clauses:
            for literal in clause.split(" || "):
                if literal not in combined and not literal.startswith("~"):
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
                    return False
    
    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        list_sentence= list()
        list_clauses = list()
        cnf_q = to_cnf_form(q_content)
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form(sentence.raw_content)
            list_sentence.append(cnf_sentence)
        for clause in list_sentence:
            split_clause = clause.split('&')
            list_clauses.extend([component.strip() for component in split_clause])
        return not bool(self.dpll(list_clauses + [self.negate_literal(cnf_q)], list())), list()   