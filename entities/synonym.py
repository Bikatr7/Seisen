class Synonym:

    """

    The Synonym class represents an alternative answer for a Word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_word_id:int, incoming_synonym_id:int, incoming_synonym_value:str, incoming_word_type:str):

        """
        
        Initializes a new Synonym object.

        Parameters:
        incoming_word_id (int): The ID of the Word that the synonym is associated with.
        incoming_synonym_id (int): The ID of the synonym.
        incoming_synonym_value (str): The value of the synonym.
        incoming_word_type (str): The type of the Word that the synonym is associated with.

        """

        self.word_id:int = incoming_word_id

        self.synonym_id:int = incoming_synonym_id

        self.synonym_value:str = incoming_synonym_value

        self.word_type:str = incoming_word_type
