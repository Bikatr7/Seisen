class Synonym:

    """

    The Synonym class represents an alternative answer for a Word.
        
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                incoming_word_id:int, 
                incoming_synonym_id:int, 
                incoming_synonym_value:str) -> None:

        """
        
        Initializes a new Synonym object.

        Parameters:
        incoming_word_id (int): The ID of the Word that the Synonym is associated with.
        incoming_synonym_id (int): The ID of the Synonym.
        incoming_synonym_value (str): The value of the Synonym.

        """

        self.word_id:int = incoming_word_id

        self.synonym_id:int = incoming_synonym_id

        self.synonym_value:str = incoming_synonym_value