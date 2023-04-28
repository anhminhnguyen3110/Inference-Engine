
from Sentence import Sentence


class KnowledgeBase:
    def __init__(self):
        self.sentences = [] # list of sentences
        self.symbols = [] # list of symbols for logic connectives
        self.query = [] # list of queries
        self.current_action = "TELL" # current action
    def __str__(self) -> str:
        return "KB: " + str(self.sentences) + "\nQuery: " + str(self.query)
    
    def add_sentence(self, str: str): # add sentence to knowledge base
        sentence = Sentence(str)
        self.sentences.append(sentence)

    def add_query(self, query:str): # add query to knowledge base
        query = Sentence(query)
        return self.query.append(query)
    
    def act(self, command):
        if(self.current_action == "TELL"):
            self.add_sentence(command)
        elif(self.current_action == "ASK"):
            self.add_query(command)

    def set_action(self, action):
        if(action == "TELL"):
            self.current_action = "TELL"
        elif(action == "ASK"):
            self.current_action = "ASK" 
