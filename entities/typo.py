## Custom Modules
from entities.entity import Entity

class Typo(Entity):

    """

    The Typo class represents typos the user makes when guessing a Word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                word_id:int, 
                id:int, 
                value:str) -> None:

        """
        
        Initializes a new Typo object.

        Parameters:
        word_id (int) : The ID of the Word the Typo is for.
        id (int) : The ID of the Typo.
        value (str) : The value of the Typo.

        """

        super().__init__(id)

        self.word_id:int = word_id

        self.value:str = value