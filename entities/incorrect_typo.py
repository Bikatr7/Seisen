## Custom Modules
from entities.entity import Entity

class IncorrectTypo(Entity):

    """

    The IncorrectTypo class represents typos the user makes but are not actually typos when guessing a Word.
        
    """

##--------------------start-of-IncorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, 
                word_id:int, 
                typo_id:int, 
                value:str) -> None:

        """
        
        Initializes a new IncorrectTypo object.

        Parameters:
        word_id (int) : The ID of the Word the IncorrectTypo is for.
        typo_id (int) : The ID of the IncorrectTypo.
        value (str) : The value of the IncorrectTypo.

        """

        super().__init__(typo_id)

        self.word_id:int = word_id

        self.value:str = value