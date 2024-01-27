## Custom Modules
from entities.entity import Entity

class Synonym(Entity):

    """

    The Synonym class represents an alternative answer for a Word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                word_id:int,
                id:int,
                value:str) -> None:

        """
        
        Initializes a new Synonym object.

        Parameters:
        word_id (int) : The ID of the Word the Synonym is for.
        id (int) : The ID of the Synonym.
        value (str) : The value of the Synonym.

        """

        super().__init__(id)

        self.word_id:int = word_id

        self.value:str = value