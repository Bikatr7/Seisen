class Typo:

    """

    The Typo class represents typos the user makes when guessing a Word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                incoming_word_id:int, 
                incoming_typo_id:int, 
                incoming_typo_value:str) -> None:

        """
        
        Initializes a new Typo object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the Typo is for.
        incoming_typo_id (int) : The ID of the Typo.
        incoming_typo_value (str) : The value of the Typo.

        """

        self.word_id:int = incoming_word_id

        self.typo_id:int = incoming_typo_id

        self.typo_value:str = incoming_typo_value