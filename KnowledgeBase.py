# import necessary libraries

class KnowledgeBase:
    def __init__(self):
        self.sentences = [] # list of sentences
        self.symbols = [] # list of symbols for logic connectives
        self.query = [] # list of queries
        self.current_action = "TELL" # current action
    def __str__(self) -> str:
        return "KB: " + str(self.sentences) + "\nQuery: " + str(self.query)
    
    def add_sentence(self, sentence): # add sentence to knowledge base
        self.sentences.append(sentence)
        for symbol in sentence.symbols:
            if symbol not in self.symbols:
                self.symbols.append(symbol)

    def add_query(self, query): # add query to knowledge base
        return self.query.append(query)
    
    def act(self, sentence):
        if(self.current_action == "TELL"):
            self.add_sentence(sentence)
        elif(self.current_action == "ASK"):
            self.add_query(sentence)
