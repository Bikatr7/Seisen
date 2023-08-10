
class csep:

    '''

    The csep class is used to represent alternative answers to a word.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_csep_id:int, incoming_csep_value:str, incoming_word_type:str) -> None:

        """
        
        Initializes a new csep object.\n

        Parameters:\n
        incoming_word_id (int) : The id of the word the csep is for.\n
        incoming_csep_id (int) : The id of the csep.\n
        incoming_csep_value (string) : The value of the csep.\n
        incoming_word_type (string) : The type of the word the csep is for.\n
        
        Returns:\n
        None.\n

        """

        self.word_id = incoming_word_id

        self.csep_id  = incoming_csep_id

        self.csep_value = incoming_csep_value

        self.word_type = incoming_word_type
