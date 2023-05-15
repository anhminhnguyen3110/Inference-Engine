
from HornSentence import HornSentence
from Sentence import Sentence
from common import *

class KnowledgeBase:
    def __init__(self):
        self.sentences = []
        self.symbols = dict()
        self.query = []
        self.query_symbols = dict()
        self.current_action = "TELL"
        self.method = "TT"
        
    def print_kb(self, location):
        print(f"KB at {location}")
        for sentence in self.sentences:
            print(sentence)
        print()
        for symbol in self.symbols:
            print(symbol, end=" ")
        print()
        for query in self.query:
            print(query, end=" ")
        print()
        for symbol in self.query_symbols:
            print(symbol, end=" ")
        print()
        

    def add_sentence(self, sentence:str):
        post_fix = infix_to_postfix(sentence)
        sentence_symbols = self.add_symbol(post_fix, True)
        if (self.method.lower() == "fc" or self.method.lower() == "bc"):
            self.sentences.append(HornSentence(sentence, post_fix, sentence_symbols))
        else:
            self.sentences.append(Sentence(sentence, post_fix, sentence_symbols))


    def add_query(self, query:str):
        post_fix = infix_to_postfix(query)
        sentence_symbols = self.add_symbol(post_fix, False)
        if (self.method.lower() == "fc" or self.method.lower() == "bc"):
            self.query.append(HornSentence(query, post_fix, sentence_symbols))
        else:
            self.query.append(Sentence(query, post_fix, sentence_symbols))
    
    def add_symbol(self, sequence:str, flag: bool) -> dict():
        sentence_symbols = dict()
        for symbol in sequence:
            if(symbol not in OPERANDS and symbol not in sentence_symbols):
                sentence_symbols[symbol] = True
                if(flag):
                    if(symbol not in self.symbols):
                        self.symbols[symbol] = True
                else:
                    if(symbol not in self.query_symbols):
                        self.query_symbols[symbol] = False
        return sentence_symbols
    
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
            
    def read_input(self, file_name):
        try:
            with open(file_name, "r", encoding="utf8") as file:
                lines = file.read().splitlines()
                for line in lines:
                    if(line == "TELL"):
                        self.set_action("TELL")
                    elif(line == "ASK"):
                        self.set_action("ASK")
                    else:
                        sentences = line.split(';')
                        for sequence in sentences:
                            sequence = sequence.strip().replace(" ", "")
                            if(sequence == ""):
                                continue
                            else:
                                self.act(sequence)
                file.close()    
                return self
        except IOError:
            print("File not found")
            return
    
    def check(self, model):
        for sentence in self.sentences:
            if(not sentence.check(model)):
                return False
        return True