from Config import BRAIN_TYPE
from Brain.WeaviateBrain import WeaviateBrain
from Brain.PineconeBrain import PineconeBrain

class BrainSelector():
    def __init__(self):
        self.brain_type = BRAIN_TYPE.lower()

    def select(self):
        if(self.brain_type == "pinecone"):
            return PineconeBrain()
        
        return WeaviateBrain()
