from CNF_Converter import to_cnf_form_prefix
from KnowledgeBase import KnowledgeBase
from Algorithm import Algorithm

class DPLL(Algorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "DPLL"

    def compliments(self, model: list) -> list:
        result = []
        for symbol in model:
            if type(symbol) is str:
                result.append(["~", symbol])
            else:
                result.append(symbol[1])
        # print("Compliments: ", result)
        return result
    

    def all_true(self, clauses, model):
        for clause in clauses[1:]:
            if len([var for var in clause[1:] if var in model]) == 0:
                # print("Reach here")
                return False
        return True

    def some_false(self, clauses , model: list) -> bool:
        model_negated = self.compliments(model)
        for clause in clauses[1:]:
            if len([var for var in clause[1:] if var not in model_negated]) == 0:
                # print("Reach here")
                return True
        return False
    
    def pure_literal(self, clauses, model: list):
        model_negated = self.compliments(model)
        candidates = []
        for clause in clauses[1:]:
            if len([symbol for symbol in clause[1:] if symbol in model]) == 0:
                candidates = candidates + [symbol for symbol in clause[1:]]
        candidates_negated = self.compliments(candidates)
        pure = [symbol for symbol in candidates if symbol not in candidates_negated]
        for symbol in pure:
            if symbol not in model and symbol not in model_negated:
                # print("Pure Literal: ", symbol)
                return symbol
        return False

    def unit_clause(self, clauses, model: list):
        model_negated = self.compliments(model)
        for clause in clauses[1:]:
            remaining = [symbol for symbol in clause[1:] if symbol not in model_negated]
            if len(remaining) == 1:
                if remaining[0] not in model:
                    return remaining[0]
        return False

    def pick_symbol(self, clauses, model: list):
        combined = model + self.compliments(model)
        for clause in clauses[1:]:
            for literal in clause[1:]:
                if type(literal) is str and literal not in combined:
                    # print("Picked: ", literal)
                    return literal
        return False

    def dpll(self, cnf, model):
        if self.all_true(cnf, model):
            return model
        if self.some_false(cnf, model):
            return False
        pure = self.pure_literal(cnf, model)
        if pure:
            return self.dpll(cnf, model + [pure])
        unit = self.unit_clause(cnf, model)
        if unit:
            return self.dpll(cnf, model + [unit])
        pick = self.pick_symbol(cnf, model)
        if pick:
            # try positive
            result = self.dpll(cnf, model + [pick])
            if result:
                return result
            else:
                # try negative
                result = self.dpll(cnf, model + [['~', pick]])
                if result:
                    return result
                else:
                    return False
                
    def stable(self, clause):
        if type(clause) is str: # must be a single positive literal
            return ["&", ["||", clause]]
        elif clause[0] == "~": # must be a single negative literal
            return ["&", ["||", clause]]
        elif clause[0] == "||": # a single clause
            return ["&", clause]
        else:
            result = ["&"]
            for sub_clause in clause[1:]:
                if type(sub_clause) == str:
                    result.append(["||", sub_clause])
                elif sub_clause[0] == "~":
                    result.append(["||", sub_clause])
                else:
                    result.append(sub_clause)
            return result

    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        q_content = "~(" + q_content + ")"


        cnf_q = to_cnf_form_prefix(q_content)

        list_sentence = []
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            print(sentence.raw_content, cnf_sentence)
            list_sentence.append(cnf_sentence)
        list_sentence.append(cnf_q)
        print(list_sentence)
        ans = self.dpll(self.stable(list_sentence), [])
        print (ans)
        if(ans is False):
            ans = True
        return (ans, [])
