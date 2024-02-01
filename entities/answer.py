## custom modules
from entities.entity import Entity

class Answer(Entity):

    """
    
    The Answer class represents an answer to a word in Seisen.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                word_id:int,
                id:int,
                value:str) -> None:

        """
        
        Initializes a new Answer object.

        Parameters:
        word_id (int) : The ID of the Word the Answer is for.
        id (int) : The ID of the Answer.
        value (str) : The value of the Answer.

        """

        super().__init__(id)

        self.word_id:int = word_id

        self.value:str = value