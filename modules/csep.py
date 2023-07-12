
class csep:

    '''

    The csep class is used to represent alternative answers to a word.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_csep_id:int, incoming_csep_value:str, incoming_word_type:str):

        """
        
        Initializes a new typo object.\n

        Parameters:\n
        self (object - typo) : The typo object to be initialized.\n
        incoming_word_id (int) : The id of the word the typo is for.\n
        incoming_csep_id (int) : The id of the typo.\n
        incoming_csep_value (string) : The value of the typo.\n
        incoming_word_type (string) : The type of the word the typo is for.\n
        Returns:\n
        None.\n

        """

        self.word_id = incoming_word_id

        self.csep_id  = incoming_csep_id

        self.csep_value = incoming_csep_value

        self.word_type = incoming_word_type
