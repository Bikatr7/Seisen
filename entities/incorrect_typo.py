class IncorrectTypo:

    """

    The IncorrectTypo class represents typos the user makes but are not actually typos when guessing a Word.
        
    """

##--------------------start-of-IncorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, 
                incoming_word_id:int, 
                incoming_incorrect_typo_id:int, 
                incoming_incorrect_typo_value:str) -> None:

        """
        
        Initializes a new IncorrectTypo object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the IncorrectTypo is for.
        incoming_incorrect_typo_id (int) : The ID of the IncorrectTypo.
        incoming_incorrect_typo_value (str) : The value of the IncorrectTypo.

        """

        self.word_id:int = incoming_word_id

        self.incorrect_typo_id:int  = incoming_incorrect_typo_id

        self.incorrect_typo_value:str = incoming_incorrect_typo_value