from abc import ABC, abstractmethod
class Brain(ABC):
    @abstractmethod
    def fetch_related_data(self, prompt):
        pass
    @abstractmethod
    def store_fact(self, fact):
        pass