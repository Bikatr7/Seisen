##--------------------start-of-IncorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class IncorrectTypo:

    '''

    The IncorrectTypo class is used to represent typos the user makes but are not actually typos.
        
    '''

##--------------------start-of-IncorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_word_id:int, incoming_incorrect_typo_id:int, incoming_incorrect_typo_value:str, incoming_word_type:str) -> None:

        """
        
        Initializes a new IncorrectTypo object.

        Parameters:
        incoming_word_id (int) : The id of the word the IncorrectTypo is for.
        incoming_incorrect_typo_id (int) : The id of the IncorrectTypo.
        incoming_incorrect_typo_value (str) : The value of the IncorrectTypo.
        incoming_word_type (str) : The type of the word the IncorrectTypo is for.

        """

        self.word_id:int = incoming_word_id

        self.incorrect_typo_id:int  = incoming_incorrect_typo_id

        self.incorrect_typo_value:str = incoming_incorrect_typo_value

        self.word_type:str = incoming_word_type