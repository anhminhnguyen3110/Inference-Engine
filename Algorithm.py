""" This file contains the abstract class Algorithm. 
It is the parent class of all the algorithms. 
It contains the knowledge base and the symbols. 
It also contains the abstract method entails. """
from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase


class Algorithm(ABC):
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.name = "Algorithm"
        self.symbols = []

    def check_all(self):
        pass

    @abstractmethod
    def entails(self):
        pass
