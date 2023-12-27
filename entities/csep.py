
class csep:

    """

    The csep class is used to represent alternative answers to a word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_csep_id:int, incoming_csep_value:str, incoming_word_type:str) -> None:

        """
        
        Initializes a new csep object.

        Parameters:
        incoming_word_id (int) : The id of the word the csep is for.
        incoming_csep_id (int) : The id of the csep.
        incoming_csep_value (str) : The value of the csep.
        incoming_word_type (str) : The type of the word the csep is for.
    
        """

        self.word_id:int = incoming_word_id

        self.csep_id:int = incoming_csep_id

        self.csep_value:str = incoming_csep_value

        self.word_type:str = incoming_word_type
