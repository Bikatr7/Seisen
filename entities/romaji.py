

class Romaji:

    """
    
    The Romaji class represents the romaji of a Word.

    Romaji is the romanization of the Japanese language.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                incoming_word_id:int,
                incoming_romaji_id:int,
                incoming_romaji_value:str) -> None:
        
        """

        Initializes a new Romaji object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the Romaji is for.
        incoming_romaji_id (int) : The ID of the Romaji itself.
        incoming_romaji_value (str) : The value of the Romaji.

        """

        self.word_id:int = incoming_word_id

        self.romaji_id:int = incoming_romaji_id
        
        self.romaji_value:str = incoming_romaji_value