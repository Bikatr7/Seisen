
class typo:

    '''

    The typo class is used to represent typos the user makes.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_typo_id:int, incoming_typo_value:str, incoming_word_type:str):

        """
        
        Initializes a new typo object.\n

        Parameters:\n
        self (object - typo) : The typo object to be initialized.\n
        incoming_word_id (int) : The id of the word the typo is for.\n
        incoming_typo_id (int) : The id of the typo.\n
        incoming_typo_value (string) : The value of the typo.\n
        incoming_word_type (string) : The type of the word the typo is for.\n

        Returns:\n
        None.\n

        """

        self.word_id = incoming_word_id

        self.typo_id  = incoming_typo_id

        self.typo_value = incoming_typo_value

        self.word_type = incoming_word_type

##--------------------start-of-incorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class incorrectTypo:

    '''

    The incorrectTypo class is used to represent typos the user makes but are not actually typos.\n
        
    '''

##--------------------start-of-incorrectTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_word_id:int, incoming_incorrect_typo_id:int, incoming_incorrect_typo_value:str, incoming_word_type:str):

        """
        
        Initializes a new incorrectTypo object.\n

        Parameters:\n
        self (object - incorrectTypo) : The incorrectTypo object to be initialized.\n
        incoming_word_id (int) : The id of the word the incorrectTypo is for.\n
        incoming_incorrect_typo_id (int) : The id of the incorrectTypo.\n
        incoming_incorrect_typo_value (string) : The value of the incorrectTypo.\n
        incoming_word_type (string) : The type of the word the incorrectTypo is for.\n

        Returns:\n
        None.\n

        """

        self.word_id = incoming_word_id

        self.incorrect_typo_id  = incoming_incorrect_typo_id

        self.incorrect_typo_value = incoming_incorrect_typo_value

        self.word_type = incoming_word_type