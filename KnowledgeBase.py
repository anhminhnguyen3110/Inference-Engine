class KnowledgeBase:
    def __init__(self) -> None:
        self.sentences = []
        self.query = []
        self.current_action = "TELL"
        
    def __str__(self) -> str:
        return "KB: " + str(self.sentences) + "\nQuery: " + str(self.query)
    def set_action(self, action):
        if(action == "TELL"):
            self.current_action = "TELL"
        elif(action == "ASK"):
            self.current_action = "ASK"
            
    def add_sentence(self, sentence):
        self.sentences.append(sentence)
        
    def add_query(self, query):
        self.query.append(query)
    
    def act(self, str):
        if(self.current_action == "TELL"):
            self.add_sentence(str)
        elif(self.current_action == "ASK"):
            self.add_query(str)