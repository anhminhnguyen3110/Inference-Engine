from KnowledgeBase import KnowledgeBase
class Algorithm:
    def __init__(self, knowledge_base: KnowledgeBase, query, name):
        self.name = name
        self.knowledge_base = knowledge_base
        self.knowledge_base.add_query(query)

    def __str__(self):
        return self.name + ": " + str(self.knowledge_base)

    def CheckAllSentence():
        # return true if all sentences are true
        # return false if any sentence is false
        # return unknown if some sentences are true and some sentences are false
        return True
    def Entail():
        # return true if KB entails query
        # return false if KB does not entail query
        # return unknown if KB entails query is unknown
        return True

    

