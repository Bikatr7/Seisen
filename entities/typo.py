
class Typo:

    """

    The Typo class is used to represent typos the user makes when guessing a word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_typo_id:int, incoming_typo_value:str, incoming_word_type:str) -> None:

        """
        
        Initializes a new Typo object.

        Parameters:
        incoming_word_id (int) : The id of the word the Typo is for.
        incoming_typo_id (int) : The id of the Typo.
        incoming_typo_value (str) : The value of the Typo.
        incoming_word_type (st) : The type of the word the Typo is for.

        """

        self.word_id:int = incoming_word_id

        self.typo_id:int = incoming_typo_id

        self.typo_value:str = incoming_typo_value

        self.word_type:str = incoming_word_type